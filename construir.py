"""Construye index.html (la web del test) a partir de plantilla.html y las posturas en datos/pos_*.json.

Uso:  python construir.py
Comprueba que cada pregunta tiene los 11 partidos y que cada postura es válida antes de escribir nada.
"""
import glob
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

# Enlace público del test (el del Artifact en claude.ai). Vacío = se ocultan los botones de compartir.
SHARE_URL = "https://claude.ai/artifact/HLiqBkfStM8brRdw4PWttb"

PARTIES = [
    # Orden alfabético para no dar preferencia a nadie en la portada.
    {"id": "bng", "short": "BNG", "name": "Bloque Nacionalista Galego", "where": ["galicia"], "scope": "Solo en Galicia"},
    {"id": "bildu", "short": "EH Bildu", "name": "", "where": ["euskadi", "navarra"], "scope": "País Vasco y Navarra"},
    {"id": "erc", "short": "ERC", "name": "Esquerra Republicana de Catalunya", "where": ["cataluna"], "scope": "Solo en Cataluña"},
    {"id": "fa", "short": "Frente Amplio", "name": "Sumar, IU, Más Madrid y Comuns", "where": "all", "scope": ""},
    {"id": "junts", "short": "Junts", "name": "Junts per Catalunya", "where": ["cataluna"], "scope": "Solo en Cataluña"},
    {"id": "pnv", "short": "PNV", "name": "Partido Nacionalista Vasco", "where": ["euskadi"], "scope": "Solo en País Vasco"},
    {"id": "podemos", "short": "Podemos", "name": "", "where": "all", "scope": ""},
    {"id": "pp", "short": "PP", "name": "Partido Popular", "where": "all", "scope": ""},
    {"id": "psoe", "short": "PSOE", "name": "Partido Socialista Obrero Español", "where": "all", "scope": ""},
    {"id": "salf", "short": "SALF", "name": "Se Acabó La Fiesta", "where": "all", "scope": ""},
    {"id": "vox", "short": "Vox", "name": "", "where": "all", "scope": ""},
]

V, E, T, I, A, D, SA, C, X = (
    "Vivienda", "Impuestos", "Trabajo y pensiones", "Inmigración", "Modelo de Estado",
    "Derechos y sociedad", "Sanidad", "Energía, clima y campo", "Exterior y defensa",
)

# Preguntas cortas de sí o no. Los ids enlazan con las posturas de datos/pos_*.json.
# t3 (IRPF del salario mínimo) se retiró: desde 2025 ya no tributa y casi todos los partidos lo apoyaban.
STATEMENTS = [
    {"id": "v1", "topic": V, "text": "¿Poner un tope al precio del alquiler en las zonas donde está más caro?",
     "context": "Hoy la ley solo lo permite en las zonas que cada comunidad autónoma declare tensionadas."},
    {"id": "v2", "topic": V, "text": "¿Limitar por ley la compra de viviendas para invertir o especular, y no para vivir en ellas?", "context": ""},
    {"id": "v3", "topic": V, "text": "¿Que los ayuntamientos puedan prohibir pisos turísticos nuevos y reducir los que ya hay?", "context": ""},
    {"id": "v4", "topic": V, "text": "¿Desalojar en 24 o 48 horas a quien ocupe una vivienda sin permiso, sin esperar a un juicio completo?",
     "context": "Hoy el desalojo lo ordena un juez y el proceso puede alargarse meses."},
    {"id": "v5", "topic": V, "text": "Para abaratar la vivienda, ¿es mejor construir más con menos trámites que limitar los precios?", "context": ""},
    {"id": "e1", "topic": E, "text": "¿Bajar los impuestos aunque haya que recortar gasto público?", "context": ""},
    {"id": "e2", "topic": E, "text": "¿Mantener el impuesto a las grandes fortunas?",
     "context": "Impuesto estatal sobre patrimonios de más de 3 millones de euros, creado en 2022."},
    {"id": "e3", "topic": E, "text": "¿Un impuesto extra a los bancos y a las grandes energéticas por sus beneficios?", "context": ""},
    {"id": "e4", "topic": E, "text": "¿Eliminar el impuesto de sucesiones (herencias) en toda España?",
     "context": "Lo cobran las comunidades autónomas y cada una aplica rebajas distintas."},
    {"id": "t1", "topic": T, "text": "¿Bajar la jornada laboral máxima a 37,5 horas semanales sin bajar el sueldo?",
     "context": "Hoy el máximo son 40 horas semanales."},
    {"id": "t2", "topic": T, "text": "¿Que despedir sin causa justificada les cueste más a las empresas?",
     "context": "Hoy se paga con 33 días de sueldo por año trabajado, con un máximo de 24 mensualidades."},
    {"id": "t4", "topic": T, "text": "¿Que las empresas y los sueldos más altos coticen más para pagar las pensiones?", "context": ""},
    {"id": "i1", "topic": I, "text": "¿Hacer una regularización extraordinaria de los inmigrantes sin papeles que ya viven y trabajan aquí?", "context": ""},
    {"id": "i2", "topic": I, "text": "¿Que los españoles tengan prioridad sobre los extranjeros residentes en ayudas y vivienda social?", "context": ""},
    {"id": "i3", "topic": I, "text": "¿Expulsar a los inmigrantes que entraron de forma irregular, aunque lleven años aquí?", "context": ""},
    {"id": "i4", "topic": I, "text": "¿Repartir de forma obligatoria entre todas las comunidades a los menores migrantes que llegan solos?", "context": ""},
    {"id": "a1", "topic": A, "text": "¿Que las comunidades que lo pidan recauden todos sus impuestos, como el País Vasco y Navarra?",
     "context": "Cataluña lo reclama. El País Vasco y Navarra recaudan sus impuestos y pagan al Estado una cantidad por los servicios comunes."},
    {"id": "a2", "topic": A, "text": "¿Permitir un referéndum de independencia pactado con el Estado si una comunidad lo pide?", "context": ""},
    {"id": "a3", "topic": A, "text": "¿Fue acertada la amnistía del procés catalán?",
     "context": "Ley de 2024 para los delitos ligados al proceso independentista catalán de 2011 a 2023."},
    {"id": "a4", "topic": A, "text": "¿Que el Estado recupere competencias de las comunidades, como la educación o la sanidad?", "context": ""},
    {"id": "a5", "topic": A, "text": "¿Que las familias puedan elegir el castellano como lengua principal en el colegio, en toda España?",
     "context": "También en Galicia, Cataluña, el País Vasco y demás comunidades con otra lengua oficial."},
    {"id": "a6", "topic": A, "text": "¿Un referéndum para elegir entre monarquía y república?", "context": ""},
    {"id": "a7", "topic": A, "text": "¿Que los propios jueces elijan a los vocales jueces del CGPJ, en vez del Congreso y el Senado?",
     "context": "El CGPJ gobierna a los jueces y nombra a los del Tribunal Supremo. 12 de sus 20 vocales son jueces."},
    {"id": "s1", "topic": D, "text": "¿Incluir el derecho al aborto en la Constitución?",
     "context": "Hoy es legal a petición de la mujer hasta la semana 14, por ley."},
    {"id": "s2", "topic": D, "text": "¿Derogar la ley de eutanasia?",
     "context": "Ley de 2021 que permite pedir ayuda para morir con una enfermedad grave e incurable."},
    {"id": "s3", "topic": D, "text": "¿Cambiar la ley de violencia de género por una de violencia intrafamiliar, sin distinguir entre hombres y mujeres?",
     "context": "La ley actual, de 2004, protege específicamente a las mujeres frente a sus parejas o exparejas."},
    {"id": "s4", "topic": D, "text": "¿Derogar la Ley de Memoria Democrática?",
     "context": "Ley de 2022 sobre las víctimas de la Guerra Civil y el franquismo: exhumaciones, retirada de símbolos, etc."},
    {"id": "s5", "topic": D, "text": "¿Quitar a los toros la protección y las ayudas públicas como patrimonio cultural?", "context": ""},
    {"id": "p1", "topic": SA, "text": "¿Reducir los conciertos de la sanidad pública con empresas privadas?",
     "context": "Son pagos a clínicas privadas para que atiendan a pacientes de la pública, por ejemplo para bajar listas de espera."},
    {"id": "c1", "topic": C, "text": "¿Alargar la vida de las centrales nucleares?",
     "context": "El plan vigente es cerrarlas todas en 2035. En agosto de 2026 se prorrogó Almaraz hasta 2030."},
    {"id": "c2", "topic": C, "text": "¿Apoyar el acuerdo comercial de la UE con Mercosur (Brasil, Argentina, Uruguay y Paraguay)?",
     "context": "Se firmó en enero de 2026 y falta ratificarlo. Facilita vender allí coches, maquinaria o vino, y abre Europa a más carne y productos agrícolas sudamericanos."},
    {"id": "c3", "topic": C, "text": "¿Cumplir los objetivos climáticos de la UE aunque encarezcan el transporte o el campo?", "context": ""},
    {"id": "x1", "topic": X, "text": "¿Subir el gasto en defensa hasta lo que pide la OTAN?",
     "context": "La OTAN pide llegar al 5 % del PIB en 2035. España se desmarcó y se queda en torno al 2,1 %."},
    {"id": "x2", "topic": X, "text": "¿Mantener o endurecer el embargo de armas y las sanciones a Israel?", "context": ""},
    {"id": "x3", "topic": X, "text": "¿Seguir enviando ayuda militar a Ucrania?", "context": ""},
]

NOTES = [
    "Los programas electorales del 29-N aún no están publicados. Las posturas salen de votaciones en el Congreso desde 2023, de los programas de 2023 y de declaraciones públicas recogidas hasta el 6 de octubre de 2026. Cuando salgan los programas conviene actualizar el test.",
    "Frente Amplio es la candidatura que preparan Sumar, IU, Más Madrid y Comuns; se usan las posturas de Sumar. Podemos negocia todavía si se une (el plazo para formar coaliciones acaba el 16 de octubre), así que aquí aparecen por separado.",
    "SALF no tiene diputados en el Congreso, así que de él hay menos datos y su porcentaje se calcula con menos preguntas.",
    "Faltan partidos más pequeños o de una sola provincia o comunidad, como Coalición Canaria o UPN.",
    "Unas decenas de preguntas no recogen un programa entero. Úsalo como punto de partida para informarte, no como recomendación de voto.",
    "Es un test independiente y no oficial: no lo ha hecho ni encargado ningún partido ni institución. Las posturas las ha recopilado y resumido una inteligencia artificial (Claude) a partir de las fuentes públicas que se enlazan en cada una, y pueden contener errores.",
]

METHOD = [
    "Las posturas de los partidos se clasifican en cinco niveles: a favor, a favor con matices, ambiguo, en contra con matices y en contra. Tu «Sí» equivale a «a favor», tu «No» a «en contra» y tu «Depende» al punto medio.",
    "Coincidir del todo suma 100 %. Cada nivel de distancia resta 25 %: un «Sí» frente a un partido «a favor con matices» suma 75 %, y un «Sí» frente a uno «en contra» suma 0 %.",
    "Las preguntas que marcas con «Me importa mucho» cuentan doble. Las que saltas no cuentan.",
    "Si de un partido no consta postura sobre una pregunta, esa pregunta no cuenta para ese partido.",
]

# Congreso que salió de las generales de 2023 (escaños comprobados en es.wikipedia.org, suman 350).
# Orden aproximado de izquierda a derecha, como en los gráficos habituales. Colores de Wikipedia salvo
# PSOE, Sumar y Junts, con su color de marca habitual.
CHAMBER = {
    "title": "Así quedó el Congreso en las elecciones de 2023",
    "blocks": [
        {"short": "Sumar", "seats": 31, "color": "#E51C55"},
        {"short": "ERC", "seats": 7, "color": "#FFB232"},
        {"short": "EH Bildu", "seats": 6, "color": "#B5CF18"},
        {"short": "BNG", "seats": 1, "color": "#ADCFEF"},
        {"short": "PSOE", "seats": 121, "color": "#EF1C27"},
        {"short": "PNV", "seats": 5, "color": "#4AAE4A"},
        {"short": "CC", "seats": 1, "color": "#FFD700"},
        {"short": "Junts", "seats": 7, "color": "#20C0B2"},
        {"short": "UPN", "seats": 1, "color": "#00599B"},
        {"short": "PP", "seats": 137, "color": "#1D84CE"},
        {"short": "Vox", "seats": 33, "color": "#63BE21"},
    ],
}
assert sum(b["seats"] for b in CHAMBER["blocks"]) == 350

FOOTER = "Posturas recogidas el 6 de octubre de 2026 · Test independiente, sin relación con ningún partido ni institución."


def main():
    positions = {}
    for f in sorted(glob.glob(os.path.join(AQUI, "datos", "pos_*.json"))):
        with open(f, encoding="utf-8") as fh:
            positions.update(json.load(fh))

    errores = []
    pids = [p["id"] for p in PARTIES]
    limpio = {}
    for s in STATEMENTS:
        sid = s["id"]
        if sid not in positions:
            errores.append(f"Falta la pregunta {sid}")
            continue
        limpio[sid] = {}
        for pid in pids:
            c = positions[sid].get(pid)
            if c is None:
                errores.append(f"{sid}: falta el partido {pid}")
                continue
            if c.get("pos") not in (-2, -1, 0, 1, 2, None):
                errores.append(f"{sid}/{pid}: postura no válida {c.get('pos')!r}")
            src = c.get("src")
            if src and not str(src).startswith("http"):
                errores.append(f"{sid}/{pid}: fuente no es un enlace: {src!r}")
            limpio[sid][pid] = {k: c.get(k) for k in ("pos", "why", "src", "conf")}
    if errores:
        print("NO se ha construido. Problemas:")
        print("\n".join(errores))
        sys.exit(1)

    data = {"parties": PARTIES, "statements": STATEMENTS, "positions": limpio,
            "notes": NOTES, "method": METHOD, "footer": FOOTER, "shareUrl": SHARE_URL, "chamber": CHAMBER}
    with open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8") as fh:
        html = fh.read()
    marca = "/*DATA*/null"
    assert html.count(marca) == 1, "La plantilla debe tener exactamente una marca de datos"
    # </ dentro del JSON cerraría la etiqueta <script>: se escapa.
    html = html.replace(marca, json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)

    nulos = sum(1 for sid in limpio for pid in limpio[sid] if limpio[sid][pid]["pos"] is None)
    print(f"OK: index.html con {len(STATEMENTS)} preguntas x {len(PARTIES)} partidos; {nulos} celdas sin postura.")


if __name__ == "__main__":
    main()
