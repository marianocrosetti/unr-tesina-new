# Resultados de la noche (2 sep 2026)

Corrido en la Mac M4 (MPS), sin GPU externa. Todo local, reproducible con `scripts/overnight_gen.sh` y `scripts/overnight_train.sh`.

**Qué se corrió.** 13 condiciones, 80k partidas de entrenamiento cada una (≈1.6M estados) y 3k partidas de test de los mismos
expertos con otra semilla (≈60k estados). Imitador de 6.3M parámetros (8 capas, 256 d), juego "a ciegas" sobre la secuencia
de jugadas, 1600 pasos × batch 512 (≈10 epochs). Recompensa exacta del solver de Pons en cada estado y jugada. Evaluación
desde logits, sin muestreo, en τ ∈ {0.001 … 1.5}, más 150 partidas contra el bot experto por temperatura. Una semilla por
condición; segundas semillas de las condiciones centrales corriendo a la mañana (se agregan solas a las tablas).

## Hallazgos

**1. El denoising funciona y escala con la diversidad de errores (H1, H3).** A tasa de error fija, la ganancia a τ→0 sobre el
experto cae monótonamente con la fracción compartida π: en E[r], +0.040 (π=0), +0.027 (0.25), +0.017 (0.5), {PI075} (0.75),
−0.017 (1.0). El signo cambia donde la teoría lo predice. Las magnitudes son ~¼ del techo teórico porque el imitador nunca
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
