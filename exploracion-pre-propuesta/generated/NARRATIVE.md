# Resultados de la noche (2 sep 2026)

Corrido en la Mac M4 (MPS), sin GPU externa. Todo local, reproducible con `scripts/overnight_gen.sh` y `scripts/overnight_train.sh`.

**Qué se corrió.** 13 condiciones, 80k partidas de entrenamiento cada una (≈1.6M estados) y 3k partidas de test de los mismos
expertos con otra semilla (≈60k estados). Imitador de 6.3M parámetros (8 capas, 256 d), juego "a ciegas" sobre la secuencia
de jugadas, 1600 pasos × batch 512 (≈10 epochs). Recompensa exacta del solver de Pons en cada estado y jugada. Evaluación
desde logits, sin muestreo, en τ ∈ {0.001 … 1.5}, más 150 partidas contra el bot experto por temperatura. Tres semillas por
condición (las dos adicionales entrenadas en una RTX 4090 de RunPod, 2 sep por la tarde), más un estudio de escala de una semilla.

## Hallazgos

**1. El denoising funciona y escala con la diversidad de errores (H1, H3).** A tasa de error fija, la ganancia a τ→0 sobre el
experto cae monótonamente con la fracción compartida π: en E[r], +0.040 (π=0), +0.027 (0.25), +0.017 (0.5), +0.004 (0.75),
−0.017 (1.0). El signo cambia donde la teoría lo predice y la caída es casi lineal en π, como predice la fórmula ρ(1−π) salvo por el factor de escala. Las magnitudes son ~¼ del techo teórico porque el imitador nunca
llega al argmax de la mezcla en estados no vistos: su accuracy a τ=1 está *por debajo* del experto en todas las condiciones,
o sea que la distribución aprendida es una copia más plana de los datos. Bajar τ saca el ruido de los expertos y también la
entropía residual del modelo.

**2. Un error compartido aprendible se reproduce exacto y no se puede denoisear (H2).** En la condición `rule` (todos los
expertos juegan la columna legal más a la izquierda en las jugadas múltiplo de 3) la accuracy del modelo en esas jugadas
coincide con la del experto a tres decimales en cada fase del juego, y en cada checkpoint desde el paso 200. El modelo aprende
la regla de inmediato y la mantiene. Lo mismo en el control de ceguera de apertura: P(centro | tablero vacío) = 0.0001 a τ=1
y 0 a τ→0. **No hay discovery**, como predicen el Teorema 2 y la taxonomía.

**3. Un error compartido pero no aprendible sí se denoisea en estados no vistos.** Es el hallazgo que no estaba en la
teoría. En π=1 el sesgo se define por un hash de la posición, imposible de representar. En apertura (estados vistos) la
accuracy en estados sesgados a τ→0 es 0.007: Teorema 2 exacto. En mediojuego y final (estados nuevos) sube a 0.41 y 0.56:
el modelo generaliza el comportamiento mayoritario, que es el óptimo. Por eso el modelo π=1 le gana al experto cabeza a
cabeza (0.61) aunque no transciende en la distribución de estados del experto. La noción relevante de "compartido" para un
imitador finito es *compartido entre expertos y representable como función del estado*.

**4. Skill selection tiene umbral donde se predijo.** Con errores totalmente compartidos fuera de la expertise y fuerza de
ruteo α, la ganancia a τ→0 sobre el mejor experto es −0.104 (α=0), −0.043 (0.2), +0.126 (0.45), +0.170 (0.7), +0.169 (1.0).
El cambio de signo está entre 0.2 y 0.45, consistente con α* = 1/3. Debajo del umbral bajar la temperatura **empeora**: el
modelo se compromete con el error compartido. La transición no es escalón sino suave: la accuracy en estados con jugada
equivocada disponible es 0.22, 0.60, 0.76, 0.93 para α = 0.2, 0.45, 0.7, 1.0, siguiendo el margen de la mezcla. Un dato
lateral: a τ=1 la mezcla ruteada ya supera al mejor experto para todo α>0. Selection no necesita temperatura baja;
denoising sí.

**5. Expertos complementarios (Teorema 4).** Cuatro expertos óptimos en su región y aleatorios afuera: +0.077 sobre el
mejor experto a τ→0. Mismo régimen que π=0, ganancia mayor porque los expertos individuales son mucho peores mientras el
argmax de la mezcla sigue siendo óptimo en todo el espacio.

## Actualización de la tarde (RunPod): semillas y estudio de escala

**Semillas.** Los desvíos entre 3 semillas son de 0.001 a 0.005 en E[r], muy por debajo de las diferencias entre condiciones.
Todo lo de arriba se sostiene, incluida la posición del umbral de selection (sí/sí/sí en α ≥ 0.45, no/no/no en α ≤ 0.2).

**Escala (π=0, una semilla).** 80k vs 320k partidas × 1600 / 6400 / 25600 pasos:

| Datos | Pasos | Epochs | acc τ=1 | acc τ→0 | val loss final (mínima) |
|---|---|---|---|---|---|
| 80k | 1600 | 10 | 0.763 | 0.891 | 1.76 (1.76) |
| 80k | 6400 | 42 | 0.786 | 0.837 | 2.73 (1.74 @2400) |
| 80k | 25600 | 167 | 0.790 | 0.835 | 6.63 (1.74 @2400) |
| 320k | 1600 | 2.6 | 0.758 | 0.888 | 1.76 (1.76) |
| 320k | 6400 | 10 | 0.789 | **0.914** | 1.69 (1.69 @6000) |
| 320k | 25600 | 42 | 0.807 | 0.865 | 2.18 (1.69 @8400) |

- Más entrenamiento sobre los mismos datos destruye la transcendencia: el modelo memoriza las partidas concretas, con sus
  errores aleatorios, y el argmax deja de ser el voto de la mayoría. Es la dinámica de memorización de etiquetas ruidosas de
  Arpit et al. 2017; el paper de ajedrez (una pasada sobre 10⁹ partidas) nunca entra en ese régimen. En π=1 el mismo
  sobreajuste tiene el síntoma opuesto: el modelo aprende trozos del sesgo por hash y deja de generalizarlo (acc en estados
  sesgados del final 0.67 → 0.50). En la regla, el sobreajuste no cambia nada en las jugadas de regla (0.248/0.632/0.728
  en todas las celdas) y solo degrada el resto. Una causa, tres síntomas.
- Más datos aumentan la ganancia: 320k y 10 epochs da la mejor celda, +0.062 sobre el experto (0.915 en el checkpoint de
  mejor val loss). El techo teórico (1.0) sigue lejos.
- La accuracy a τ=1 sube con datos (0.763 → 0.789 → 0.807) pero no alcanza al experto (0.845). Tendencia de límite de
  datos, no evidencia de un efecto estructural.
- Limitación del pipeline: evalúa el checkpoint final, no el de mejor val loss. Para cualquier uso serio de la fase B hay
  que cambiar eso.

## Veredicto (2 sep, noche)

Las dos teorías se cumplen en signo en todas las celdas. Los desvíos son de magnitud (el imitador captura ~¼ del techo) y de
régimen (sobreajuste, representabilidad, entropía residual), y cada uno es lo que un practicante habría predicho. No hay
paper acá más allá de una nota de workshop; el activo es el testbed. La única extensión con resultado genuinamente incierto
que encontramos en la literatura es la composición de habilidades entre demostradores con soporte disjunto (la brecha que
Zhang et al. nombran explícitamente): expertos A óptimos hasta la jugada N con partidas truncadas, expertos B con apertura
de calidad q y final óptimo, medir la calidad del final del imitador en sus propias trayectorias en función de q.

## Día 2 (2-3 sep): descomposición, composición con soporte disjunto, ley de datos

### Dónde ocurre la transcendencia: solo en estados vistos, hasta que hay datos de sobra

Descomposición de la ganancia a τ→0 de π=0 según si la posición aparece en el entrenamiento (3 semillas por fila salvo 320k):

| Datos | epochs | ganancia total | en estados vistos | en estados no vistos | fracción vista | techo teórico (argmax de la mezcla) |
|---|---|---|---|---|---|---|
| 20k | 10 | −0.031 | +0.060 | **−0.093** | 0.41 | +0.055 |
| 80k | 10 | +0.040 | +0.092 | −0.006 | 0.47 | +0.055 |
| 320k | 2.6 | +0.035 | +0.070 | −0.004 | 0.53 | +0.055 |
| 320k | 10 | +0.062 | +0.090 | **+0.030** | 0.53 | +0.055 |

En estados vistos el voto por mayoría llega al techo desde 20k partidas. En estados no vistos el imitador pasa de ser peor
que el experto (20k) a igualarlo (80k) a superarlo (320k). La ganancia total es la mezcla ponderada de las dos. Es la forma
cuantitativa de "el imitador captura ¼ del techo": el techo se alcanza donde hay votos y la generalización recién empieza
a aportar con 4× datos. La misma descomposición en π=1 muestra que el partido cabeza a cabeza (0.59) no se explica por
ventaja por jugada en las propias trayectorias (−0.013): resultado de partida y recompensa por estado son objetos distintos.

### Composición de habilidades entre demostradores con soporte disjunto (la brecha que nombra Zhang et al.)

Familia A: apertura óptima, transcripción truncada en la jugada N (nunca muestra finales). Familia B: apertura de calidad q
o de estilo restringido (sin columnas centrales; solo columnas de borde), final óptimo. Ningún transcript muestra un final
después de una apertura óptima. Métrica: P(jugada óptima) a τ→0 en finales alcanzados desde aperturas óptimas (soporte no
visto), y juego propio del imitador contra un oponente perfecto. 3 semillas por celda, desvíos ≤ 0.005.

| Condición (N=8, 50 % A) | acc final tras aperturas ÓPTIMAS, medio / tardío | Δ vs control | juego propio: acc apertura / medio / tardío | score vs perfecto |
|---|---|---|---|---|
| control q=1 | 0.950 / 0.926 | — | 0.999 / 0.958 / 0.918 | 0.402 |
| B apertura aleatoria | 0.940 / 0.924 | −0.010 / −0.002 | 0.995 / 0.946 / 0.943 | 0.371 |
| B sin centro | 0.926 / 0.920 | −0.024 / −0.006 | 0.997 / 0.936 / 0.951 | 0.349 |
| B solo bordes | 0.925 / 0.916 | −0.025 / −0.010 | 0.999 / 0.953 / 0.958 | 0.342 |
| **solo A** (sin ningún final) | 0.868 / 0.680 | −0.082 / −0.246 | 0.997 / 0.835 / 0.779 | 0.193 |
| **solo B** (bordes, sin A) | 0.919 / 0.924 | −0.031 / −0.002 | 0.873 / 0.983 / 0.971 | 0.000 |
| bordes, N=14 | 0.945 / 0.910 (control 0.961 / 0.923) | −0.016 / −0.013 | 0.999 / 0.971 / 0.891 | 0.407 |
| bordes, modelo 0.1M | 0.918 / 0.904 (control 0.927 / 0.891) | −0.009 / +0.013 | 0.988 / 0.946 / 0.944 | 0.236 |
| bordes, modelo 0.8M | 0.924 / 0.905 (control 0.941 / 0.917) | −0.017 / −0.012 | 0.995 / 0.924 / 0.933 | 0.282 |
| bordes, 20k partidas | 0.890 / 0.855 (control 0.904 / 0.850) | −0.014 / +0.005 | 0.996 / 0.904 / 0.907 | 0.204 |

Lectura:
- **Transfiere, con un costo chico y graduado** (≤ 0.03 en el mediojuego) que crece con la severidad del desplazamiento y
  no depende de la capacidad del modelo, del tamaño de datos ni de N. No hay acantilado en ninguna celda. Gana el bando
  optimista (Mészáros et al.) contra el pesimista (two-hop de la taxonomía, stitching en Decision Transformers).
- **Solo B ya transfiere igual** (0.919 vs 0.925): los datos de A no aportan nada al final. Lo que A aporta es la apertura:
  solo-B juega aperturas de borde (acc 0.87) y pierde todas las partidas contra el oponente perfecto; solo-A no sabe jugar
  finales (0.68 tardío). **A+B gana ~70 % de sus partidas como primer jugador contra un oponente perfecto**, algo que ninguna
  de las dos poblaciones de demostradores puede hacer. Eso es composición de habilidades en el juego propio, medida exacta.
- Curiosidad: solo-A, sin haber visto jamás una jugada más allá de la 8, acierta 0.87 en el mediojuego. Extrapola la
  estructura de la apertura óptima bastante más allá de su soporte antes de colapsar en el final.

### Veredicto del día 2

La pregunta abierta que quedaba (¿compone habilidades de demostradores con soporte disjunto?) tiene respuesta clara en este
dominio: sí, con penalidad pequeña, graduada e insensible a capacidad y datos. Es un resultado limpio a favor de la lectura
"la política aprendida es función local del tablero", pero en Connect 4 la conclusión era la que un optimista esperaba, así
que vale como el contenido empírico que le faltaba al modo *skill generalization*, no como sorpresa. La descomposición
visto/no visto es el hallazgo más útil para leer el paper original: la transcendencia por voto vive en los estados
repetidos y la generalización recién la extiende con datos abundantes.

## Lo que esto dice de los dos papers

- El mecanismo de Zhang et al. se reproduce en un dominio secuencial con recompensa exacta, y la condición de diversidad que
  ellos solo correlacionaron con entropía acá se manipula y da la curva monótona esperada.
- El umbral de selection es una predicción cuantitativa que la taxonomía no tiene y que se cumple en signo. La suavidad de
  la transición es lo que agrega un modelo finito a la teoría.
- El hallazgo 3 es una forma de transcendencia que ninguno de los dos marcos captura: no es voto por estado (Teorema 2 dice
  que el argmax es el error) sino generalización entre estados. Es barata de verificar y separa dos cosas que los papers
  juntan bajo "errores correlacionados": correlación entre expertos y estructura en el espacio de estados.

## Cautelas

- Una semilla por celda en la mayoría de las condiciones. Efectos de ±0.02 en E[r] están en el borde de lo que una semilla
  sostiene; el patrón de signos entre condiciones es lo robusto. Las segundas semillas se están agregando.
- El modelo está subentrenado respecto del supuesto teórico (τ=1 por debajo de la mezcla). Con más datos o pasos la ganancia
  de π=0 debería acercarse al techo; medir cuánto es en sí informativo.
- ρ se aplica solo a los estados donde existe una jugada peor (~52 %), así que las tasas de error realizadas (~0.15) son la
  mitad de las nominales. Las predicciones usan las tasas realizadas.
- En el partido cabeza a cabeza el modelo pierde algunas partidas por jugada ilegal tras 5 reintentos (0 a 15 de 150 según
  la condición), igual que en el protocolo del paper.

Las tablas completas, generadas automáticamente, siguen abajo. Log cronológico con decisiones en `overnight/notes.md`.

---
