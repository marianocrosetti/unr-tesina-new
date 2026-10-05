## Resumen de [1]

## 1. Idea en una frase

Un modelo generativo entrenado sólo para **imitar** (cross-entropy / next-token) a jugadores humanos de ajedrez de rating termina jugando a rating , **mejor que cualquier jugador que produjo sus datos**. A eso lo llaman *trascendencia*. La explicación: el modelo aprende la mezcla de las políticas de muchos jugadores, y al muestrear a **baja temperatura** hace implícitamente un **voto por mayoría** entre ellos. Los errores idiosincráticos de cada jugador se cancelan ("wisdom of the crowd"). Condición práctica necesaria: **diversidad** en los datos.

## 2. Formalización (Sección 2)

- $\mathcal{X}$: espacio de entradas (posiciones / prefijos de partida), $\mathcal{Y}$: espacio finito de salidas (jugadas).
- $\mathcal{F}$: funciones $f: \mathcal{X} \to \mathcal{P}(\mathcal{Y})$, o sea políticas estocásticas $f(y \mid x)$.
- Hay $k$ **expertos** $f_1, \dots, f_k \in \mathcal{F}$ (en el paper, cada jugador humano es un experto).
- Distribución de entradas $p$ sobre $\mathcal{X}$ con soporte total ($p(x) > 0\ \forall x$).
- Proceso generador de datos: se muestrea $x \sim p$ y luego se elige un experto **uniformemente al azar** para etiquetar. Esto induce la distribución conjunta $D(x,y) = p(x)\, f(y \mid x)$ donde $f$ es la **mezcla de expertos**:

$$
f(y \mid x) = \frac{1}{k} \sum_{i=1}^{k} f_i(y \mid x) \tag{1}
$$

- **Recompensa** $r: \mathcal{X} \times \mathcal{Y} \to \mathbb{R}$, no constante en $y$ para cada $x$. Recompensa esperada de una política $f$ bajo una distribución de test $p_{\text{test}}$:

$$
R_{p_{\text{test}}}(f) = \mathbb{E}_{x \sim p_{\text{test}}}\big[r_x(f)\big], \qquad r_x(f) = \mathbb{E}_{y \sim f(\cdot \mid x)}\big[r(x,y)\big] \tag{2}
$$

- **El learner** tiene acceso a $D$ (datos infinitos, cualquier función de $\mathcal{F}$, sin restricción de arquitectura) y minimiza cross-entropy:

$$
\hat f = \arg\min_{f \in \mathcal{F}} \mathbb{E}_{x \sim p}\, H(f, \cdot)
$$

Por propiedades de la cross-entropy, el mínimo es exactamente la mezcla: $\hat f = f$.

- **Definición 1 (trascendencia).** Un setting $(f_1, \dots, f_k, p)$ exhibe trascendencia si

$$
R_{p_{\text{test}}}(\hat f) > \max_{i \in [k]} R_{p_{\text{test}}}(f_i) \tag{3}
$$

Es decir: el predictor aprendido supera al **mejor experto individual**.

Supuestos simplificadores (Remark 1): todos los expertos comparten la misma $p$, soporte total, expertos elegidos uniformemente. Lo dejan como trabajo futuro relajarlos.

## 3. Condiciones para la trascendencia (Sección 3)

### 3.1 A temperatura 1 es imposible (Prop. 1)

Como $\hat f = f$ (la mezcla) y la recompensa es **lineal** en la distribución:

$$
R_{p_{\text{test}}}(\hat f) = \frac{1}{k}\sum_{i=1}^k R_{p_{\text{test}}}(f_i) \le \max_i R_{p_{\text{test}}}(f_i)
$$

Un promedio nunca supera al máximo. **Proposición 1:** para toda elección de expertos y $p_{\text{test}}$, existe $f_i$ con $R(f_i) \ge R(\hat f)$. Imitación pura no trasciende.

### 3.2 Baja temperatura: condición necesaria y suficiente (Prop. 2)

Definen el muestreo con temperatura $\tau > 0$ sobre la política aprendida:

$$
\hat f_\tau(\cdot \mid x) = \operatorname{softmax}\big(\hat f(\cdot \mid x); \tau\big), \qquad \operatorname{softmax}(q;\tau)_y = \frac{\exp(q_y/\tau)}{\sum_{y'} \exp(q_{y'}/\tau)}
$$

y el predictor arg-max $\hat f_{\max}(\cdot \mid x) = \operatorname{argmax}(\hat f(\cdot \mid x))$ (uniforme sobre las jugadas de probabilidad máxima). Como $\lim_{\tau \to 0} \operatorname{softmax}(q;\tau) = \operatorname{argmax}(q)$:

**Proposición 2.** $R_{p_{\text{test}}}(\hat f_{\max}) > \max_i R_{p_{\text{test}}}(f_i)$ **si y sólo si** existe $\tau \in (0,1)$ tal que para todo $\tau' \le \tau$, $R_{p_{\text{test}}}(\hat f_{\tau'}) > \max_i R_{p_{\text{test}}}(f_i)$.

Interpretación: tomar el arg-max de la mezcla $\frac{1}{k}\sum_i f_i$ es un **voto por mayoría** entre los expertos. Si la jugada más votada rinde más que el mejor experto, bajando la temperatura lo suficiente se trasciende. Esto conecta con la literatura de ensembles (bagging, boosting, model averaging).

### 3.3 Denoising de un único experto (Prop. 3)

Experto óptimo $f^*(y \mid x) = \delta(y \in Y^*_x)/|Y^*_x|$ con $Y^*_x = \arg\max_{y} r(x,y)$. Experto ruidoso con probabilidad de error $\rho \in (0,1)$:

$$
f_\rho(y \mid x) = \frac{\rho}{|\mathcal{Y}|} + (1-\rho)\, f^*(y \mid x)
$$

**Proposición 3.** Con datos generados sólo por $f_\rho$, existe $\tau$ tal que $\hat f_{\tau'}$ trasciende para todo $\tau' \le \tau$. (Trivial: el arg-max de $f_\rho$ es $f^*$, que le gana a $f_\rho$.) Un solo experto que se equivoca uniformemente al azar ya alcanza.

### 3.4 Múltiples expertos complementarios (Prop. 4)

Partición $\mathcal{X} = X_1 \,\dot\cup\, \dots \,\dot\cup\, X_k$. El experto $i$ es óptimo en $X_i$ y juega al azar afuera:

$$
f_i(y \mid x) = \frac{\delta(y \in Y^*_x)\,\delta(x \in X_i)}{|Y^*_x|} + \frac{\delta(x \notin X_i)}{|\mathcal{Y}|}
$$

**Proposición 4.** Si $p_{\text{test}}$ pone masa positiva en al menos dos subconjuntos $X_i \ne X_j$, existe $\tau$ tal que $\hat f_{\tau'}$ trasciende para todo $\tau' \le \tau$. Intuición: en cada $x \in X_i$, un experto vota por la jugada correcta y los otros $k-1$ reparten su masa uniformemente, así que el arg-max de la mezcla recupera la jugada óptima en **todo** $\mathcal{X}$, cosa que ningún experto individual logra. De acá sale la necesidad de **diversidad**.

## 4. Experimentos en ajedrez (Sección 4)

### Setup
- **Modelo:** transformer decoder autoregresivo de 50M parámetros ("ChessFormer"), next-token prediction sobre strings PGN (`1.e4 e5 2.Nf3 ...`), tokenización a nivel de carácter (32 símbolos). Juega "a ciegas": nunca ve el tablero ni las reglas, sólo el texto de las jugadas y el resultado. No recibe rating ni recompensa durante el entrenamiento.
- **Datos:** ~1B partidas humanas de lichess.org (ene–oct 2023). Para testear trascendencia **truncan por rating máximo**: ChessFormer 1000 / 1300 / 1500 ven sólo partidas de jugadores con rating $\le$ ese valor.
- **Evaluación:** rating Glicko-2 jugando contra Stockfish 16.1 niveles 1, 3 y 5 (100 partidas c/u, 300 en total). Primero calibran el rating de esos niveles de Stockfish en lichess contra los bots Maia (1552, 1842, 2142 aprox). Si el modelo no genera una jugada legal en 5 muestras, pierde. Reportan $R \pm 2\,RD$ como IC 95%.
- Para cerrar la brecha teoría–práctica (la teoría asume cobertura total de $\mathcal{X}$, imposible después de la jugada ~15), muestran un t-SNE de la última capa oculta que captura la ventaja relativa de la posición y la identidad de los jugadores: el modelo comprime a una representación latente que generaliza a estados no vistos.

### Resultado principal (Figura 1)
Barren temperaturas de $\tau = 0.001$ (casi determinista) a $1.0$ (distribución original) y $1.5$ (alta entropía).

| Modelo | Rating máx. en datos | Trasciende a $\tau = 0.001$? |
|---|---|---|
| ChessFormer 1000 | 1000 | **Sí**, llega a $\approx 1500$ |
| ChessFormer 1300 | 1300 | **Sí**, llega a $\approx 1500$ |
| ChessFormer 1500 | 1500 | **No** |

Confirma Prop. 1 y 2: a $\tau = 1$ no hay trascendencia, a baja temperatura sí (para 1000 y 1300).

### ¿Dónde mejora bajar la temperatura? La función *favor* (Sección 4.2, Fig. 4, Tabla 1)
Inspirada en el Performance Difference Lemma de RL, definen el *favor* de $f'$ sobre $f$:

$$
F(f', f; x) = \mathbb{E}_{x \sim d_{f'},\, y \sim f'(\cdot \mid x)}\big[r(x,y)\big] - \mathbb{E}_{x \sim d_{f'},\, y \sim f(\cdot \mid x)}\big[r(x,y)\big] \tag{4}
$$

con $d_{f'}$ la distribución de visita de estados al seguir $f'$. Baseline $f$ = modelo a $\tau = 1$; intervención $f'$ = mismo modelo a $\tau = 0.75$ o $0.001$. La recompensa $r$ es la **probabilidad de ganar según la red de evaluación de Stockfish**. Corren 100 partidas de ChessFormer 1000 a $\tau = 0.001$ vs Stockfish 1, y por cada jugada real muestrean 100 jugadas contrafácticas a $\tau = 1$ (n = 382.000 muestras por $\tau$).

Hallazgo: la distribución del favor se **sesga a la derecha con cola larga**. Bajar la temperatura no mejora un poquito en muchos estados, sino **mucho en pocos estados clave** (donde el jugador débil habría cometido un blunder).

| $\tau$ | $\mathbb{E}[P_\tau]$ (% win) | $\mathbb{E}[P_\tau - P_{1.0}]$ | Top-1 acc | Top-3 acc | Top-5 acc |
|---|---|---|---|---|---|
| 0.001 | 39.95 | **+2.15** | 29.61 | 54.26 | 66.86 |
| 0.75 | 38.79 | +0.99 | 25.08 | 47.84 | 60.37 |
| 1.0 | 37.80 | 0 | 22.61 | 44.00 | 56.27 |

Top-k acc = % de jugadas del modelo que están entre las top-k de Stockfish. Suben monótonamente al bajar $\tau$. Nota: aún a $\tau = 0.001$ la prob. de ganar es $< 50\%$, consistente con que Stockfish 1 (~1550) sigue estando arriba del modelo (~1450).

## 5. Diversidad y entropía (Sección 4.2, Figura 5)

Pregunta: ¿por qué ChessFormer 1500 no trasciende? Hipótesis: entre 1000 y 1500 la diversidad **no crece**. Un jugador de 1000 puede pensarse como un 1500 ruidoso, pero un 1500 **no** es un 2000 ruidoso.

Miden la diversidad del dataset como la **entropía normalizada de la distribución de acciones** por estado:

$$
H_f(Y \mid X) = \frac{\mathbb{E}_{y \sim f(y \mid x = X)}\big[-\log_2 f(y \mid x = X)\big]}{\log_2 |\mathcal{Y}|} \in [0, 1]
$$

donde $|\mathcal{Y}|$ es el número de jugadas legales en ese estado. Entropía alta = distribución de jugadas más uniforme (más diversidad); baja = más determinista. Promedian sobre los estados.

**Limitación metodológica importante:** después de la jugada ~16 casi todos los estados son únicos en el dataset (una sola acción observada), así que **sólo pueden medir en estados frecuentes** (aperturas, inicio de medio juego, finales). Toman 1.000.000 partidas de cada dataset y se quedan con estados que tienen $> 100$ acciones observadas (n = 2681, 3037, 3169 estados para 1000, 1300, 1500). La métrica es sobre frecuencias empíricas del dataset, **independiente del modelo**.

**Resultado:** entropía media $\text{(}\le 1000\text{)} > \text{(}\le 1300\text{)} > \text{(}\le 1500\text{)}$. El dataset $\le 1500$ es el menos diverso, lo que **correlaciona** con que ChessFormer 1500 no trascienda. Los autores lo presentan como confirmación de la hipótesis, pero como los datos son humanos, la evidencia es **correlacional**, no causal (no pueden manipular la diversidad manteniendo todo lo demás fijo). Este es uno de los huecos que tu propuesta ataca.

## 6. Settings adicionales (Sección 4.3)

- **SQuAD v2 (QA en lenguaje natural):** varios LLMs pretrained (163M a 7B) evaluados a distintas temperaturas en exact match, F1 y "semantic match" (juzgado por llama3.1). Bajar la temperatura mejora las métricas. Lo usan como evidencia de que el "temperature denoising" se generaliza a otros dominios.
- **Toy model lineal (Fig. 7):** clasificación de 10 clases con entradas gaussianas en $d = 100$. Ground truth $y = \arg\max_i W^*_i x$. $k = 5$ expertos etiquetan con $W = W^* + \xi$, $\xi_{ij} \sim \mathcal{N}(0, \sigma^2)$. Modelo lineal entrenado con 10K ejemplos, cada uno etiquetado por un experto al azar. Trascendencia aparece cuando $\sigma$ (diversidad) es alta y $\tau$ baja; con $\sigma$ chico no supera al mejor experto.

## 7. Limitaciones que declaran y relación con la propuesta

Limitaciones del paper (Sección 6):
- Supuestos fuertes: mismo $p$ para todos los expertos, soporte total, expertos uniformes. Sin esos supuestos podría haber trascendencia vía ponderación bayesiana (trabajo futuro).
- El marco asume que las condiciones de test coinciden con las de entrenamiento. No cubre composición ni razonamiento.
- Broader impact: el mecanismo es **denoising de errores**, no razonamiento novedoso; no hay evidencia de que el modelo produzca soluciones que un humano no podría idear.

Puntos que quedan abiertos y que motivan tus experimentos:
1. La relación diversidad → trascendencia es **correlacional** (datos humanos, no controlan la diversidad).
2. La entropía sólo se mide en estados frecuentes (aperturas/finales), no en el medio juego donde se deciden las partidas.
3. Ajedrez no está resuelto: tanto $r$ como el rating se estiman con Stockfish, no con la verdad.
4. No distinguen trascendencia en estados vistos vs no vistos.
5. Es un único mecanismo (cancelación de errores). Abreu et al. [2] luego extienden a selección y generalización.
