# Test de afinidad 29-N (elecciones generales 29/11/2026)

## Qué es
Web de una sola página: 36 afirmaciones sin decir de quién son; al final, % de coincidencia con 11 partidos y, por cada afirmación, dónde está cada partido, el motivo y la fuente.

## Cómo está hecho
- `plantilla.html`: la web (diseño y lógica). Lleva la marca `/*DATA*/null` donde se meten los datos.
- `construir.py`: lista de partidos, afirmaciones, notas y método. Lee `datos/pos_*.json`, comprueba que no falte nada y escribe `index.html`.
- `datos/pos_*.json`: posturas por bloque de temas (escala -2 a +2, o null si no consta), con motivo, fuente y fiabilidad.
- `index.html`: lo que se publica como Artifact en claude.ai.

Para regenerar: `python construir.py` y volver a publicar `index.html` con la misma URL.

## Estado
- 06/10/2026: primera versión. Posturas investigadas con fuentes públicas hasta el 06/10/2026 (programas del 29-N aún sin publicar).

## Pendiente
- Cuando los partidos publiquen sus programas del 29-N (previsiblemente en noviembre), revisar las posturas.
- Si Podemos entra en Frente Amplio (plazo de coaliciones: 16/10/2026), decidir si se fusionan o se dejan separados.
