# Encargo común para todos los investigadores

Contexto: elecciones generales en España el 29/11/2026 (convocadas el 05/10/2026 tras caer en el Congreso los decretos de vivienda con votos de PP, Vox, Junts y UPN). Hoy es 06/10/2026. Los programas electorales del 29N TODAVÍA NO están publicados.

Estamos construyendo un test de afinidad de voto (tipo "Wahl-O-Mat"). Para cada afirmación de tu bloque y cada uno de los 11 partidos, determina la posición del partido sobre la afirmación.

## Partidos (usa estos ids exactos)
- pp: Partido Popular (Feijóo)
- psoe: PSOE (Sánchez)
- vox: Vox (Abascal)
- fa: Frente Amplio = la coalición Sumar + IU + Más Madrid + Comuns (en 2023 se presentaron como "Sumar"; en el Congreso, Grupo Plurinacional Sumar). Usa sus posiciones como Sumar/Movimiento Sumar/IU.
- podemos: Podemos (Ione Belarra / Irene Montero). Separado de Sumar desde dic. 2023, está en el Grupo Mixto.
- salf: Se Acabó La Fiesta (Alvise Pérez). Tiene eurodiputados; sin diputados en el Congreso. Puede haber poca información: usa null cuando no conste.
- bng: Bloque Nacionalista Galego
- erc: Esquerra Republicana de Catalunya
- junts: Junts per Catalunya
- pnv: PNV / EAJ
- bildu: EH Bildu

## Escala de posición (pos)
- 2 = lo defiende o propone activamente (programa, votación a favor, declaraciones claras)
- 1 = a favor con matices o condiciones
- 0 = posición ambigua, dividida o expresamente neutral (abstención sin postura clara)
- -1 = en contra con matices
- -2 = rechazo frontal
- null = no hay información fiable. MEJOR null que inventar.

## Fuentes, por orden de preferencia
1. Votaciones en el Congreso 2023-2026 (una sola votación nominal suele dar la postura de muchos partidos a la vez: aprovéchala).
2. Programas electorales de las generales de 2023 y documentos oficiales del partido.
3. Declaraciones y propuestas recientes (2025-2026) de sus dirigentes en medios reconocidos.
Si la postura ha cambiado con el tiempo, manda la más reciente y dilo en "why".

## Reglas
- No inventes URLs: pon en "src" solo una URL que hayas visto de verdad en una búsqueda o al abrir una página. Si no tienes, "src": null.
- "why": una frase neutral en español de España, de 25 palabras como mucho, que diga el hecho (p. ej. "Votó a favor del tope en la Ley de Vivienda de 2023 y lo mantiene en su programa."). Sin adjetivos valorativos y sin citas largas copiadas.
- "conf": "alta" (votación o programa explícito), "media" (declaraciones o deducción directa), "baja" (indicio indirecto).
- No sesgues: el mismo listón de pruebas para todos los partidos.
- Si la afirmación tal como está redactada te parece ambigua o te obliga a forzar posiciones, dilo en el campo "nota_redaccion" de esa afirmación y propón una redacción mejor. NO cambies tú los ids.

## Formato de salida
Escribe un archivo JSON (UTF-8) en la ruta que te indique el encargo, con esta forma exacta:
{
  "v1": {
    "nota_redaccion": null,
    "pp":     {"pos": -2, "why": "...", "src": "https://...", "conf": "alta"},
    "psoe":   {...},
    ... (los 11 partidos, siempre los 11)
  },
  "v2": {...}
}
Después, en tu respuesta final, devuelve solo: la ruta del archivo, cuántas celdas quedaron en null y las 3 posiciones de las que estés menos seguro (con el motivo).
