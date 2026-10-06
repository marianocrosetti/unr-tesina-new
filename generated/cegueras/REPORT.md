# Expertos ciegos para Connect 4: ¿sirven como fuentes para experimentos de trascendencia?

<AI-CONTENT-NOT-CURATED>

Noche del 30/9 al 1/10/2026. Pregunta: si construimos expertos que juegan óptimo en una variante de Connect 4
donde no cuentan algunos tipos de línea ("ceguera"), ¿son fuentes útiles para los experimentos de la tesina,
o son demasiado óptimos / demasiado tontos / generan partidas colapsadas?

Respuesta corta: **sí sirven, con tres decisiones de diseño** que este reporte fija y justifica con números.
Las secciones 1 a 3 son la construcción; la 4 los resultados; la 5 las objeciones que anticipo de Dante y Pablo.

(Las tablas detalladas están en `REPORT_v1_mix5*.md` y `REPORT_v2_mix4h_*.md`; los datos en `data/`.)

---

## 1. Construcción

**Variante G_S.** Connect 4 estándar (7x6) donde solo cuentan como victoria las líneas de los tipos en
S ⊆ {V, H, D1, D2} (D1 = diagonal `\`, D2 = diagonal `/`). El solver exacto de Pons se recompila por variante
tocando una sola función (`compute_winning_position`, un `#if` por dirección). Hay 15 variantes; G_{VHD1D2} es
el juego real y reproduce exactamente al solver original (verificado).

**Experto ciego E_S.** En cada estado consulta el solver de G_S (modo débil: gana/empata/pierde) y elige entre
las jugadas óptimas *de la variante*. Las partidas se juegan con las reglas reales: si el rival alinea 4 en
diagonal, el ciego a diagonales pierde aunque "no lo vea". Nombres: `sin_D1` = E_{VHD2}, etc.

**Tres perillas, cada una con un rol distinto:**

| perilla | qué controla | valores |
|---|---|---|
| conjunto ciego S | *dónde* en el espacio de estados erra el experto, y qué comparte con otros | sin_D1, sin_D2, sin_H, sin_V, sin_D1D2, ... |
| desempate entre óptimas de la variante | si el error es votable dentro del mismo experto y si se correlaciona por la regla de desempate | `uniform` (azar por visita), `perm` (preferencia fija de columnas por experto), `center` (misma regla para todos), `hash` |
| p (prob. de "no ver" en cada visita) | la tasa de error, linealmente: tasa(p) = p · tasa(1) | 0..1 |

**Apertura.** k jugadas uniformemente al azar, k ~ U[6, 8] (v2) o U[8, 12] (v1), y después juegan los expertos.
Es lo que hace viable el costo (sección 2) y lo que da diversidad de posiciones.

## 2. Viabilidad computacional

Sin libro de aperturas, el solver de cada variante tarda (en frío, modo débil, análisis de las 7 jugadas):

| profundidad | variantes con 3 direcciones (sin_X) | sin diagonales (VH) | una sola dirección |
|---|---|---|---|
| tablero vacío | > 10 min (abortado) | > 10 min | > 10 min |
| ply 8 | 0.5 – 6 s | 0.5 – 6 s | 1 – 20 s |
| ply 10 | 0 – 2 s | 0 – 2 s | hasta > 40 s |
| ply 12 | 0.01 – 0.5 s | 0.1 – 2.5 s | 0.6 – 8 s |

Costo de generación medido (10 núcleos, 6 procesos en paralelo, tabla de transposición caliente y caché en disco):

| apertura k | s / partida por proceso |
|---|---|
| U[8, 12] | 1.5 – 3 |
| U[6, 8] | 7 – 12 |
| U[4, 6] | ~90 (inviable para masa) |

Para un dataset de entrenamiento de 100k partidas con k ~ U[6,8]: unas 30 horas con 10 procesos; con k ~ U[8,12],
unas 6. Las variantes con una sola dirección quedan descartadas por costo y porque son casi aleatorias.

## 3. Qué se midió

Sobre ~2200 estados **decidibles** (hay al menos dos clases de resultado entre las jugadas legales) visitados
por los expertos en partidas de la población mixta:

- **A. Tasa de error estructural** por experto y fase: P(jugada no óptima en el juego real).
- **B. Correlación de errores** entre pares: Pearson de los indicadores de error por estado, y Jaccard de las
  jugadas erróneas cuando ambos erran.
- **C. Techo del voto** (Prop. 2 de Zhang): acierto del argmax de la mezcla equiponderada vs. mejor experto.
  Y **estados de composición**: donde *todos* los expertos del conjunto erran con seguridad.
- **D. Diversidad**: partidas únicas, entropía de la acción por estado (Fig. 5 de Zhang).
- **E. Fuerza**: round robin y *tasa de conservación* contra el óptimo (P de obtener el valor teórico de la
  posición tras la apertura, que es lo máximo alcanzable contra un rival perfecto).
- **Chequeo semántico**: un ciego al tipo L no puede errar si no queda ninguna ventana de 4 de tipo L sin fichas
  de ambos colores (la variante y el juego real coinciden desde ahí). Debe dar error exactamente 0.

## 4. Resultados

Datos principales: v2 = 1500 partidas de la población {sin_D1, sin_D2, sin_H, sin_V}, apertura k ~ U[6,8],
desempate `hash`; 21.480 estados visitados por expertos, 2301 decidibles analizados (también con la política de
sin_D1D2 en cada uno). Las partidas duran 21.3 jugadas en promedio, de las cuales 14.3 son de expertos; 1.5% tablas;
gana el primer jugador el 56%. v1 = lo mismo con k ~ U[8,12] y población con sin_D1D2 (2238 estados); coincide en todo.

### 4.1 Los expertos no son óptimos ni aleatorios

Tasa de error estructural (prob. de jugar no óptimo en un estado decidible), desempate hash, v2:

| experto | tasa total | pérdida media de recompensa | jugadas 8-14 | 15-21 | 22-28 | 29+ |
|---|---|---|---|---|---|---|
| sin_D1 | 0.26 | 0.21 | 0.25 | 0.28 | 0.27 | 0.15 |
| sin_D2 | 0.26 | 0.21 | 0.28 | 0.25 | 0.24 | 0.15 |
| sin_H | 0.36 | 0.29 | 0.44 | 0.30 | 0.25 | 0.25 |
| sin_V | 0.19 | 0.16 | 0.20 | 0.24 | 0.16 | 0.06 |
| sin_D1D2 | 0.35 | 0.28 | 0.37 | 0.36 | 0.32 | 0.23 |

Están en la banda que la propuesta pedía (ρ ≈ 0.3, menor que 0.5 para que el voto pueda funcionar). Erran en
todas las fases, incluida la apertura: la ceguera **no** es un fenómeno solo de finales. sin_H erra más temprano
(amenazas horizontales en las filas bajas), sin_V casi nada en el final (ya no quedan columnas con 4 lugares).

Fuerza (expertos deterministas, k ~ U[6,8], 80 partidas por par, mismas aperturas, ambos colores):

| experto | vs óptimo (W-D-L) | vs azar (W-D-L) | conserva posición ganada vs óptimo (n≈36) |
|---|---|---|---|
| sin_D1 | 27-0-53 | 70-0-10 | 0.72 |
| sin_D2 | 31-0-49 | 71-0-9 | 0.83 |
| sin_H | 16-0-64 | 69-0-11 | 0.41 |
| sin_V | 19-1-60 | 65-0-15 | 0.54 |
| sin_D1D2 | 16-0-64 | 68-0-12 | 0.42 |
| azar | 9-0-91 (v1) | 50-0-50 | 0.16 (v1) |
| óptimo | 48-4-48 | 91-0-9 | 1.00 |

"Conserva" = contra el rival perfecto obtiene exactamente el valor teórico de la posición tras la apertura (lo
máximo posible). Es la métrica de fuerza que no depende de que la apertura aleatoria ya esté decidida (lo está en
~45% de los casos en contra del experto). Los ciegos a una diagonal conservan 72–83%; los ciegos a H o a ambas
diagonales, ~40%. Hay un gradiente de fuerza claro y ninguno es trivial.

### 4.2 La correlación de errores se controla por el solapamiento de cegueras

Pearson entre indicadores de error por estado (hash, v2) y Jaccard de las jugadas erróneas cuando ambos erran:

| par | Pearson | P(ambos erran) | si fueran indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.09 | 0.09 | 0.08 | 0.25 |
| sin_D1 / sin_H | 0.10 | 0.12 | 0.10 | 0.26 |
| sin_H / sin_V | −0.04 | 0.06 | 0.07 | 0.18 |
| sin_D2 / sin_V | 0.05 | 0.06 | 0.05 | 0.23 |
| **sin_D1 / sin_D1D2** | **0.30** | 0.16 | 0.10 | 0.28 |
| **sin_D2 / sin_D1D2** | **0.31** | 0.16 | 0.09 | 0.28 |

Cegueras disjuntas: errores casi independientes (Pearson 0.0–0.1). Cegueras solapadas (sin_D1 ⊂ sin_D1D2):
0.30. Esta es la variable ρ de Pablo, manipulada por construcción y con interpretación ("no saben lo mismo").

**El desempate es una perilla de correlación por sí mismo.** Con desempate `center` (la misma regla para todos),
Pearson sube a 0.16–0.26 entre cegueras disjuntas y el Jaccard de jugadas erróneas a 0.70–0.84: cuando dos
expertos erran, erran *igual* porque comparten la preferencia. Con `perm` (una preferencia fija de columnas por
experto) pasa lo mismo entre los pares cuyas preferencias empiezan igual (Jaccard 0.58–0.64). Con `hash`
(preferencia idiosincrática por estado y experto), 0.18–0.30. Conclusión: para que el solapamiento de cegueras sea
la *única* fuente de correlación, el desempate tiene que ser idiosincrático (hash) o diseñado ortogonal.

### 4.3 El voto tiene techo positivo, y existen estados de composición

Techo de la Proposición 2 de Zhang: acierto del argmax de la mezcla equiponderada vs. el mejor experto (hash, v2):

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia | estados donde **todos** erran |
|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.73 | 0.73 | 0.73 | −0.01 | **9.3% (n=215)** |
| sin_D1 + sin_H | 0.68 | 0.68 | 0.72 | −0.04 | 12.3% (n=283) |
| sin_D1 + sin_D2 + sin_H | 0.70 | 0.76 | 0.73 | +0.03 | 5.1% (n=117) |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.72 | 0.86 | 0.81 | **+0.05** | 1.8% (n=41) |
| los 5 | 0.71 | 0.86 | 0.81 | +0.06 | 1.6% (n=36) |

Lectura:
- Con 2 expertos deterministas el voto no decide (empatan cuando discrepan): ganancia ≈ 0. Esto es exactamente lo
  que hace que el par sin_D1 + sin_D2 sea el banco de pruebas de **composición**, no de voto: en el 9.3% de los
  estados decidibles **ambos erran** (n=215 en esta muestra; guardados en `data/composition_states_D1D2_hash.jsonl`).
  La teoría de Zhang predice acierto 0 del imitador ahí a temperatura baja; si acierta, compuso.
- Con K ≥ 3 el voto gana: +0.05 a +0.06 con 4–5 expertos, sobre un mejor experto de 0.81. Es el eje K.
- Los estados de composición se concentran en la apertura y el medio juego (10.7% / 10.5% / 5.9% / 1.8% por fase).

**Desempate blando vs duro.** Con desempate `uniform` (el experto reparte su masa entre todas las óptimas de la
variante) el techo del voto es mucho mayor (+0.13 con 2 expertos, +0.15 con 4: la mezcla concentra masa en la
intersección de los conjuntos), pero los estados de composición **desaparecen** (0.5%, n=12): la ceguera se
manifiesta como *indiferencia* entre jugadas, no como una jugada confiadamente errónea. Decisión: experto
**determinista** (hash) si se quiere estudiar composición; `uniform` si solo se quiere denoising. Son dos
poblaciones legítimas en el marco de Zhang y la comparación entre ambas es en sí un resultado.

### 4.4 Las partidas no colapsan

- Partidas únicas: 100% (1500/1500) en todas las poblaciones, incluidas las de autojuego de un solo experto
  (medidas con desempate `uniform`; con desempate determinista la apertura aleatoria garantiza lo mismo). La apertura aleatoria garantiza cobertura de posiciones; en 1500 partidas ningún estado posterior a
  la apertura se visita 3 veces, así que la "diversidad por estado" de Zhang (Fig. 5) no se puede medir por conteo.
- La medida equivalente, analítica: entropía normalizada de la **mezcla** por estado (hash): 0.26 con 2 expertos,
  0.40 con 3, 0.47 con 4, 0.52 con 5. La mezcla es unánime en el 31% de los estados con 2 expertos y en el 5% con 4.
  Crece con K, como debe.
- Resultado de las partidas: 1.5% tablas, 56% gana el primero. Hay señal de resultado para el token final.

### 4.5 Chequeo semántico: los errores están donde la ceguera dice

Un ciego al tipo L no puede errar si no queda ninguna ventana de 4 de tipo L sin fichas de ambos colores
(desde ahí la variante y el juego real son el mismo juego). Medido (hash, v2):

| experto | 0 ventanas vivas | 1-2 | 3-5 | 6-10 | 11+ |
|---|---|---|---|---|---|
| sin_D1 | **0.000** (n=36) | 0.17 | 0.21 | 0.27 | 0.29 |
| sin_D2 | **0.000** (n=46) | 0.13 | 0.21 | 0.27 | 0.29 |
| sin_H | **0.000** (n=12) | 0.15 | 0.21 | 0.26 | 0.40 |
| sin_V | **0.000** (n=5) | 0.00 | 0.05 | 0.12 | 0.23 |
| sin_D1D2 | **0.000** (n=12) | 0.13 | 0.27 | 0.32 | 0.36 |

Cero exacto donde debe, y tasa creciente con la cantidad de ventanas vivas. (Este chequeo detectó que en el
código de Pons "diagonal 1" es `\` y no `/`; fue solo un problema de nombres, ya corregido.)

### 4.6 La perilla p (no corrida, analítica)

Con probabilidad p el experto usa la política ciega y con 1−p la óptima real. La tasa de error es p·tasa(1), y
en cada estado hay exactamente dos candidatas (la ciega es determinista): la mezcla de *un* experto tiene argmax
correcto si y solo si p < 0.5. Un barrido en p da una predicción de escalón en 0.5 para la trascendencia a baja
temperatura, análoga al umbral α* de la propuesta. Con p < 1 desaparecen los estados de composición (la jugada
correcta aparece en los datos), así que p es la perilla de los experimentos de voto, no del de composición.

## 5. Objeciones que anticipo y qué contestar

- **"El experto es casi óptimo."** No: erra en 19–36% de los estados decidibles, pierde 60–80% contra el óptimo
  y conserva solo 41–83% de las posiciones ganadas. El azar conserva 16%.
- **"El experto es casi aleatorio."** No: gana 65–71% al azar (el óptimo, 91%) y su error es exactamente 0 donde la
  ceguera no aplica (4.5). Es un jugador perfecto con un déficit conceptual acotado.
- **"Combinar expertos tontos de distinta manera no tiene sentido / colapsa."** Los errores de cegueras distintas
  son casi independientes (Pearson ≤ 0.1), el voto con K=4 gana +0.05 sobre el mejor experto, y la mezcla tiene
  entropía 0.47 por estado. No hay colapso de posiciones (100% de partidas únicas) ni de acciones.
- **"La apertura aleatoria es artificial."** Es necesaria por costo (el tablero vacío no se resuelve sin libro) y es
  la práctica estándar para evaluar motores con aperturas forzadas. Costo: ~45% de las aperturas ya están decididas
  contra uno de los dos. Mitigación: evaluar al imitador desde las mismas aperturas y medir conservación del valor
  teórico, no victorias crudas. k ~ U[6,8] es el mínimo viable (7–12 s/partida); k ~ U[4,6] cuesta ~90 s/partida.
- **"El desempate hash es arbitrario."** Es la forma más limpia de "preferencia idiosincrática entre jugadas que el
  experto considera equivalentes", que es exactamente el error idiosincrático de Zhang. Las alternativas con regla
  compartida introducen correlación espuria (4.2). Si se quiere que el imitador pueda aprender la preferencia, usar
  `perm` con órdenes diseñados para no compartir el inicio.
- **"Casi no hay tablas."** 1.5%. Es Connect 4 con aperturas aleatorias; la recompensa sigue siendo informativa
  porque ~55% de los estados visitados son decidibles.
- **"Esto ya lo hace Zhang con Stockfish."** Zhang mide la tasa de error; acá se *controla* su estructura: dónde
  (conjunto ciego), qué comparten (solapamiento), si es votable (desempate), cuánto (p). Con humanos ninguna de las
  cuatro es manipulable.

## 6. Qué habilita, concretamente

1. **Composición** (lo que ni [1] ni [2] tienen en un juego): población {sin_D1, sin_D2} determinista; test set =
   estados donde ambos erran (9% de los decidibles; ya hay 215 guardados, se pueden generar miles). Predicción de
   Zhang: acierto ≈ 0 a τ→0. Control: estados donde solo uno erra (voto empatado). Separar visto / no visto.
2. **Denoising y eje K**: {sin_D1, sin_D2, sin_H, sin_V}, K = 2, 3, 4; techo medido +0.00 / +0.03 / +0.05.
3. **Correlación**: {sin_D1, sin_D2} (ρ ≈ 0.09) vs {sin_D1, sin_D1D2} (ρ ≈ 0.30) con tasas parecidas; o la
   misma población con desempate hash vs center (correlación por preferencia compartida).
4. **Barrido en p** para el escalón en 0.5.

## 7. Lo que no se hizo

- No se entrenó ningún imitador: todo es sobre los expertos y sus mezclas (techos teóricos).
- La perilla p está justificada analíticamente, no corrida.
- No se probó la variante "fuerte" del solver (preferir la victoria más rápida), que daría expertos más decididos
  sin hash; cuesta más tiempo de cómputo.
- Los conjuntos de un solo tipo de línea (p. ej. "solo V") se descartaron por costo y por ser casi aleatorios.
