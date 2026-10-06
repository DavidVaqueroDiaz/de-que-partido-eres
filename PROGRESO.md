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
- 06/10/2026: publicado en https://claude.ai/artifact/HLiqBkfStM8brRdw4PWttb (privado hasta compartirlo desde su menú).
  - 35 preguntas Sí/Depende/No (t3, IRPF del SMI, retirada por no distinguir entre partidos). 28 de 385 celdas sin postura (23 de SALF).
  - Portada: hemiciclo real 2023 (350 escaños, colores de Wikipedia). Durante el test, el hemiciclo es la barra de progreso, en arcoíris neutro.
  - Un partido solo puede salir primero si se le compara en al menos el 60 % de tus respuestas (SALF siempre queda al final con un aviso).
  - Comprobado: quien responde como un partido lo saca primero (>90 %), salvo el BNG, que empata casi con EH Bildu y Podemos (97-98 %).
  - Cambios de datos a mano: e2/SALF a null (su fuente daba 404).

## Pendiente
- Cuando los partidos publiquen sus programas del 29-N (previsiblemente en noviembre), revisar las posturas.
- Si Podemos entra en Frente Amplio (plazo de coaliciones: 16/10/2026), decidir si se fusionan o se dejan separados.
