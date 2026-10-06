"""Construye index.html (la web del test) a partir de plantilla.html y las posturas en datos/pos_*.json.

Uso:  python construir.py
Comprueba que cada afirmación tiene los 11 partidos y que cada postura es válida antes de escribir nada.
"""
import glob
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

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
    "Derechos y sociedad", "Sanidad", "Energía, clima y campo", "Política exterior y defensa",
)

STATEMENTS = [
    {"id": "v1", "topic": V, "text": "El Estado debería poder poner un tope al precio del alquiler en las zonas donde la vivienda está más cara.",
     "context": "Hoy la ley de vivienda permite limitar alquileres, pero solo en las zonas que la comunidad autónoma declare tensionadas."},
    {"id": "v2", "topic": V, "text": "Habría que limitar por ley la compra de viviendas que no vayan a ser la residencia habitual del comprador (por ejemplo, para invertir o especular).",
     "context": ""},
    {"id": "v3", "topic": V, "text": "Los ayuntamientos deberían poder prohibir nuevos pisos turísticos y reducir los que ya existen para que vuelvan al alquiler normal.",
     "context": ""},
    {"id": "v4", "topic": V, "text": "La policía debería poder desalojar en 24 o 48 horas a quien ocupe una vivienda sin permiso, sin esperar a un juicio.",
     "context": "Hoy, salvo que se le sorprenda entrando, el desalojo necesita la decisión de un juez."},
    {"id": "v5", "topic": V, "text": "Para abaratar la vivienda hay que liberar suelo y reducir trámites para construir más, en lugar de intervenir en los precios.",
     "context": ""},
    {"id": "e1", "topic": E, "text": "Hay que bajar los impuestos en general aunque eso obligue a recortar gasto público.", "context": ""},
    {"id": "e2", "topic": E, "text": "Debe mantenerse un impuesto especial a las grandes fortunas.",
     "context": "Es un impuesto estatal sobre patrimonios de más de 3 millones de euros, creado en 2022."},
    {"id": "e3", "topic": E, "text": "Los bancos y las grandes energéticas deberían pagar un impuesto extra sobre sus beneficios extraordinarios.", "context": ""},
    {"id": "e4", "topic": E, "text": "El impuesto de sucesiones y donaciones debería suprimirse en toda España.",
     "context": "Lo gestionan las comunidades autónomas y cada una aplica rebajas distintas."},
    {"id": "t1", "topic": T, "text": "La jornada laboral máxima debería bajar de 40 a 37,5 horas semanales sin reducción de sueldo.", "context": ""},
    {"id": "t2", "topic": T, "text": "Despedir sin causa justificada debería costar más a las empresas que ahora (mayor indemnización).",
     "context": "Hoy un despido improcedente se paga con 33 días de sueldo por año trabajado, con un máximo de 24 mensualidades."},
    {"id": "t3", "topic": T, "text": "Quien cobra el salario mínimo no debería pagar IRPF.", "context": ""},
    {"id": "t4", "topic": T, "text": "Para pagar las pensiones, las empresas y los sueldos más altos deberían cotizar más a la Seguridad Social.", "context": ""},
    {"id": "i1", "topic": I, "text": "Debería regularizarse a los inmigrantes sin papeles que ya viven y trabajan en España.", "context": ""},
    {"id": "i2", "topic": I, "text": "Los españoles deberían tener prioridad sobre los extranjeros que viven legalmente aquí para recibir ayudas públicas y vivienda social.", "context": ""},
    {"id": "i3", "topic": I, "text": "Habría que expulsar a los inmigrantes que entraron de forma irregular, aunque lleven años viviendo en España.", "context": ""},
    {"id": "i4", "topic": I, "text": "Los menores migrantes que llegan solos deberían repartirse de forma obligatoria entre todas las comunidades autónomas.", "context": ""},
    {"id": "a1", "topic": A, "text": "Cataluña (y otras comunidades que lo pidan) debería recaudar y gestionar todos sus impuestos, como hacen el País Vasco y Navarra.",
     "context": "El País Vasco y Navarra recaudan sus impuestos y pagan al Estado una cantidad por los servicios comunes."},
    {"id": "a2", "topic": A, "text": "Debería poder celebrarse un referéndum de independencia pactado si un parlamento autonómico lo pide por mayoría.", "context": ""},
    {"id": "a3", "topic": A, "text": "La amnistía a los encausados por el proceso independentista catalán fue una buena decisión.",
     "context": "Ley aprobada en 2024 para los delitos ligados al proceso independentista entre 2011 y 2023."},
    {"id": "a4", "topic": A, "text": "El Estado debería recuperar competencias que hoy tienen las comunidades autónomas, como la educación o la sanidad.", "context": ""},
    {"id": "a5", "topic": A, "text": "Las familias deberían poder elegir que sus hijos estudien en castellano en toda España, también en comunidades con otra lengua oficial.", "context": ""},
    {"id": "a6", "topic": A, "text": "Debería celebrarse un referéndum para elegir entre monarquía y república.", "context": ""},
    {"id": "a7", "topic": A, "text": "Los propios jueces, y no el Congreso y el Senado, deberían elegir a la mayoría del órgano de gobierno de los jueces (CGPJ).",
     "context": "El CGPJ nombra, entre otros, a los magistrados del Tribunal Supremo. Hoy sus vocales los eligen el Congreso y el Senado."},
    {"id": "s1", "topic": D, "text": "El derecho al aborto debería incluirse en la Constitución.",
     "context": "Hoy el aborto es legal a petición de la mujer hasta la semana 14 por ley, pero no figura en la Constitución."},
    {"id": "s2", "topic": D, "text": "Debería derogarse la ley de eutanasia.", "context": "La ley, de 2021, permite pedir ayuda para morir en casos de enfermedad grave e incurable."},
    {"id": "s3", "topic": D, "text": "La ley de violencia de género debería sustituirse por una ley de violencia intrafamiliar que no distinga si la víctima es hombre o mujer.",
     "context": "La ley actual, de 2004, protege específicamente a las mujeres frente a la violencia de sus parejas o exparejas."},
    {"id": "s4", "topic": D, "text": "Debería derogarse la Ley de Memoria Democrática.",
     "context": "Ley de 2022 sobre las víctimas de la Guerra Civil y la dictadura: exhumaciones, retirada de símbolos franquistas, etc."},
    {"id": "s5", "topic": D, "text": "Las corridas de toros deberían dejar de recibir protección y ayudas públicas como patrimonio cultural.", "context": ""},
    {"id": "p1", "topic": SA, "text": "La sanidad pública debería reducir los conciertos con clínicas y hospitales privados.", "context": ""},
    {"id": "c1", "topic": C, "text": "Las centrales nucleares deberían seguir funcionando más allá de las fechas de cierre previstas.",
     "context": "El calendario actual prevé cerrarlas todas entre 2027 y 2035."},
    {"id": "c2", "topic": C, "text": "España debería apoyar el acuerdo comercial entre la Unión Europea y los países de Mercosur (Brasil, Argentina, Uruguay y Paraguay).",
     "context": "Facilita exportar coches, maquinaria o vino a Sudamérica y abre el mercado europeo a más carne y productos agrícolas de allí."},
    {"id": "c3", "topic": C, "text": "Hay que cumplir los objetivos climáticos de la UE aunque encarezcan algunas actividades, como el transporte o el campo.", "context": ""},
    {"id": "x1", "topic": X, "text": "España debería subir el gasto en defensa hasta el nivel que pide la OTAN.",
     "context": "En 2025 la OTAN fijó llegar al 5 % del PIB en 2035. España se desmarcó y se compromete con alrededor del 2,1 %."},
    {"id": "x2", "topic": X, "text": "España debería mantener o endurecer el embargo de armas y las sanciones contra Israel.", "context": ""},
    {"id": "x3", "topic": X, "text": "España debería seguir enviando ayuda militar a Ucrania.", "context": ""},
]

NOTES = [
    "Los programas electorales del 29-N aún no están publicados. Las posturas salen de votaciones en el Congreso desde 2023, de los programas de 2023 y de declaraciones públicas recogidas hasta el 6 de octubre de 2026. Cuando salgan los programas conviene actualizar el test.",
    "Frente Amplio es la candidatura que preparan Sumar, IU, Más Madrid y Comuns; se usan las posturas de Sumar. Podemos negocia todavía si se une (el plazo para formar coaliciones acaba el 16 de octubre), así que aquí aparecen por separado.",
    "SALF no tiene diputados en el Congreso, así que de él hay menos datos y su porcentaje se calcula con menos afirmaciones.",
    "Faltan partidos más pequeños o de una sola provincia o comunidad, como Coalición Canaria o UPN.",
    "Unas pocas decenas de afirmaciones no recogen un programa entero. Úsalo como punto de partida para informarte, no como recomendación de voto.",
    "Es un test independiente y no oficial: no lo ha hecho ni encargado ningún partido ni institución. Las posturas las ha recopilado y resumido una inteligencia artificial (Claude) a partir de las fuentes públicas que se enlazan en cada una, y pueden contener errores.",
]

METHOD = [
    "Cada respuesta tuya se compara con la postura del partido en la misma escala de cinco puntos, de «muy de acuerdo» a «muy en desacuerdo».",
    "Coincidir del todo suma 100 %. Cada punto de distancia resta 25 %, así que estar en extremos opuestos suma 0 %.",
    "Los temas que marcas como importantes cuentan doble. Las afirmaciones que saltas no cuentan.",
    "Si de un partido no consta postura sobre una afirmación, esa afirmación no cuenta para ese partido.",
]

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
            errores.append(f"Falta la afirmación {sid}")
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
            "notes": NOTES, "method": METHOD, "footer": FOOTER}
    with open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8") as fh:
        html = fh.read()
    marca = "/*DATA*/null"
    assert html.count(marca) == 1, "La plantilla debe tener exactamente una marca de datos"
    # </ dentro del JSON cerraría la etiqueta <script>: se escapa.
    html = html.replace(marca, json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    with open(os.path.join(AQUI, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(html)

    nulos = sum(1 for sid in limpio for pid in limpio[sid] if limpio[sid][pid]["pos"] is None)
    print(f"OK: index.html con {len(STATEMENTS)} afirmaciones x {len(PARTIES)} partidos; {nulos} celdas sin postura.")


if __name__ == "__main__":
    main()
