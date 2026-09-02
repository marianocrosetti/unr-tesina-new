# Resultados de la noche (2 sep 2026)

Corrido en la Mac M4 (MPS), sin GPU externa. Todo local, reproducible con `scripts/overnight_gen.sh` y `scripts/overnight_train.sh`.

**Qué se corrió.** 13 condiciones, 80k partidas de entrenamiento cada una (≈1.6M estados) y 3k partidas de test de los mismos
expertos con otra semilla (≈60k estados). Imitador de 6.3M parámetros (8 capas, 256 d), juego "a ciegas" sobre la secuencia
de jugadas, 1600 pasos × batch 512 (≈10 epochs). Recompensa exacta del solver de Pons en cada estado y jugada. Evaluación
desde logits, sin muestreo, en τ ∈ {0.001 … 1.5}, más 150 partidas contra el bot experto por temperatura. Una semilla por
condición; segundas semillas de las condiciones centrales corriendo a la mañana (se agregan solas a las tablas).

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

# Results

All numbers are on held-out states generated by the same experts (fresh seed).
`acc` = probability mass the imitator puts on an optimal move (exact, from logits). `E[r]` = expected reward (win 1, draw 0.5, loss 0, illegal 0).
`best expert` = the best single expert's expected reward on the same states. **Transcendence** = imitator E[r] > best expert.
Match score = (wins + 0.5 draws)/games of the imitator against an expert bot, alternating colours, 5 retries on illegal output.

## H1–H3, H5: error correlation π at fixed error rate ρ (denoising)

Prediction: acc(τ→0) ≈ 1 − shared-error rate; gain over the expert ≈ realized random-error rate; on bias states acc(τ→0) ≈ 0.

| π | seeds | expert acc | acc τ=1 | acc τ→0 | **theory acc τ→0** | E[r] τ→0 − best expert | acc τ→0 bias states | bias states by phase (open/mid/late) | acc τ→0 non-bias | match τ→0 | match τ=1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | 2 | 84.5 ± 0.0 | 76.2 ± 0.1 | 89.3 ± 0.2 | 100.0 ± 0.0 | 4.1 ± 0.1 | – | –/–/– | 89.3 ± 0.2 | 71.3 ± 1.3 | 23.3 ± 4.7 |
| 0.25 | 1 | 84.6 | 76.4 | 87.8 | 96.2 | 2.7 | 40.3 | 13.9/62.6/60.3 | 89.7 | 65.7 | 24.7 |
| 0.5 | 1 | 85.7 | 77.9 | 87.6 | 93.5 | 1.7 | 43.0 | 12.3/63.2/58.6 | 90.7 | 72.0 | 27.3 |
| 0.75 | 1 | 86.6 | 79.5 | 86.9 | 90.5 | 0.4 | 39.0 | 7.4/53.3/59.1 | 91.9 | 56.7 | 26.0 |
| 1.0 | 1 | 86.7 | 80.6 | 84.5 | 86.7 | -1.7 | 28.4 | 0.7/40.9/56.3 | 93.2 | 61.3 | 26.7 |

## Skill selection: routing strength α with fully shared errors outside expertise

Prediction: τ→0 transcends the best expert iff α > α* = 0.333. Mixture mass on optimal = α + (1−α)/K.

| α | predicted | seeds | best expert acc | mixture acc | acc τ=1 | acc τ→0 | E[r] τ→0 − best expert | transcends? | match τ→0 | match τ=1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | no | 1 | 48.5 | 45.2 | 47.5 | 36.6 | -10.4 | no | 19.7 | 48.0 |
| 0.2 | no | 1 | 54.9 | 61.4 | 59.7 | 50.1 | -4.3 | no | 52.7 | 56.0 |
| 0.45 | yes | 1 | 62.0 | 77.3 | 71.4 | 77.8 | 12.6 | yes | 86.0 | 62.3 |
| 0.7 | yes | 1 | 67.5 | 89.2 | 80.4 | 88.4 | 17.0 | yes | 86.7 | 67.7 |
| 1.0 | yes | 1 | 78.1 | 100.0 | 94.4 | 97.6 | 16.9 | yes | 84.0 | 62.0 |

## Other conditions

| condition | seeds | best expert acc | mixture acc | acc τ=1 | acc τ→0 | E[r] τ→0 − best expert | acc τ→0 bias states (expert acc on same states) | bias by phase (open/mid/late) | match τ→0 |
|---|---|---|---|---|---|---|---|---|---|
| blind_p4_rho0.0 | 1 | 96.3 | 96.3 | 87.5 | 91.7 | -3.8 | 74.4 (74.4) | 74.4/–/– | 28.3 |
| comp_k4 | 1 | 75.7 | 72.5 | 66.8 | 85.1 | 7.7 | – (–) | –/–/– | 78.0 |
| iid_rho0.3_pi0.0_steps800 | 1 | 84.5 | 84.5 | 74.5 | 86.9 | 2.1 | – (–) | –/–/– | 66.7 |
| rule_mod3_left_rho0.3 | 1 | 72.9 | 72.9 | 67.2 | 75.0 | 1.9 | 51.1 (51.1) | 24.8/63.2/72.8 | 53.3 |

## Sanity checks

| condition | states evaluated | mass on non-move tokens (τ=1) | mass on illegal columns (τ=1) | favor: frac states with abs ΔE[r] < 0.01 | favor: frac > +0.1 | favor: frac < −0.1 |
|---|---|---|---|---|---|---|
| blind_p4_rho0.0 | 83919 | 0.8 | 0.1 | 68.8 | 13.3 | 7.4 |
| comp_k4 | 60477 | 1.4 | 0.1 | 42.8 | 41.0 | 11.7 |
| iid_rho0.3_pi0.0 | 61419 | 1.3 | 0.1 | 47.9 | 39.4 | 8.4 |
| iid_rho0.3_pi0.0_steps800 | 61419 | 1.7 | 0.2 | 47.3 | 37.4 | 9.9 |
| iid_rho0.3_pi0.25 | 62827 | 1.6 | 0.1 | 49.1 | 38.0 | 8.2 |
| iid_rho0.3_pi0.5 | 61744 | 1.5 | 0.1 | 50.2 | 33.4 | 7.8 |
| iid_rho0.3_pi0.75 | 61486 | 1.5 | 0.1 | 51.8 | 18.5 | 7.5 |
| iid_rho0.3_pi1.0 | 61667 | 1.5 | 0.1 | 75.0 | 13.4 | 7.2 |
| rule_mod3_left_rho0.3 | 71470 | 1.7 | 0.1 | 65.4 | 25.4 | 6.7 |
| sel_k4_a0.0 | 69598 | 1.5 | 0.1 | 26.8 | 9.5 | 58.5 |
| sel_k4_a0.2 | 64541 | 1.5 | 0.1 | 35.6 | 14.1 | 46.6 |
| sel_k4_a0.45 | 63205 | 1.3 | 0.1 | 44.7 | 32.2 | 19.5 |
| sel_k4_a0.7 | 62547 | 1.6 | 0.1 | 51.6 | 34.4 | 9.3 |
| sel_k4_a1.0 | 56578 | 0.7 | 0.1 | 81.7 | 10.9 | 2.2 |

## Figures

![reward vs tau](results/figs/fig1_reward_vs_tau.png)
![gain vs pi](results/figs/fig2_gain_vs_pi.png)
![selection](results/figs/fig6_selection_alpha.png)
![bias vs nonbias](results/figs/fig3_bias_vs_nonbias.png)
![favor](results/figs/fig4_favor.png)
![training](results/figs/fig5_training.png)
