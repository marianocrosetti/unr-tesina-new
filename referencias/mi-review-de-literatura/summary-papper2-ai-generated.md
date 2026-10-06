# Resumen de [2] (pasada 1: con mis palabras, siguiendo la estructura del paper)

- Paper: Abreu, Zhang, Malach, Saphra. *A Taxonomy of Transcendence*. COLM 2025. https://arxiv.org/abs/2508.17669 (v1, 25 ago 2025).
- Código: no está linkeado desde el paper. Hay dos repos públicos de la primera autora: https://github.com/natalieabreu/transcendence (generación de expertos y datos, oct-2025) y https://github.com/natalieabreu/kg_multihop (fork del repo de Annabelle Carrell con entrenamiento y evaluación, versión anterior que sólo cubre denoising). Detalles constatados en `summary-papper2-v0.md`, sección "Constatación en el código".
- Dos de los autores son de [1] (Edwin Zhang, Eran Malach). Mismo grupo (Kempner, Harvard).

## 1. Idea en una frase

Un modelo entrenado por imitación no imita a *una* persona sino a un *grupo*. Un grupo puede superar a cada uno de sus miembros de tres maneras distintas, y el paper las formaliza como tres **modos de trascendencia**: (i) **skill denoising** (voto: los errores independientes se cancelan, lo que estudió [1]), (ii) **skill selection** (ruteo: cada entrada la responde el experto que la conoce, porque es el que más habla de ella), (iii) **skill generalization** (composición: se combina conocimiento de distintos expertos en un espacio latente compartido para responder lo que ningún experto sabe). Para cada modo dan una condición sobre los *datos de entrenamiento* y la verifican en un dominio sintético de grafos de conocimiento con expertos simulados. La tesis transversal: el modelo sólo trasciende si el conjunto de expertos es suficientemente **heterogéneo** (diversidad de errores, de expertise, de fraseo, de composiciones).

Matiz de la intro: mezclar muchas personas también puede amplificar sesgos compartidos (Bender et al. 2021, *stochastic parrots*); el paper estudia el lado positivo. Ejemplo motivador: un chatbot igual de competente en criptografía, derecho internacional y Dostoievski.

Contribuciones declaradas:
1. Formalizar los tres modos partiendo de las definiciones de [1].
2. Proponer condiciones sobre los datos para cada modo, con intuición en settings teóricos simples.
3. Confirmar empíricamente esas condiciones en el setting sintético de grafo de conocimiento, que además ofrecen como *testbed* controlado para trabajo futuro.

## 2. Definiciones (Sección 2)

### 2.1 Preliminares: qué cambia respecto de [1]

- $\mathcal{X} = \mathcal{T}^n$, $\mathcal{Y} = \mathcal{T}^m$: entradas y salidas son **secuencias de tokens** (no "prefijo de partida" y "jugada"). $\mathcal{F}$: funciones $\mathcal{X} \to \mathcal{P}(\mathcal{Y})$, $f(y \mid x)$.
- $k$ expertos $f_1, \dots, f_k$, **cada uno con su propia distribución de entradas** $p_i$ sobre $\mathcal{X}$. Esto es lo nuevo: en [1] había una única $p$.
- $\bar p(x) = \frac{1}{k}\sum_i p_i(x)$ es la distribución de entradas promedio; $\operatorname{supp}(\bar p)$ su soporte.
- **Mezcla**: $\bar f(y \mid x) = \sum_{i=1}^{k} g(i \mid x)\, f_i(y \mid x)$, donde $g(i \mid x)$ es "la probabilidad condicional de que la entrada $x$ haya sido observada bajo el experto $i$". El paper no escribe la fórmula, pero con prior uniforme sobre expertos (cada uno genera la misma cantidad de muestras) es Bayes: $g(i \mid x) = \frac{p_i(x)}{\sum_j p_j(x)} = \frac{p_i(x)}{k\,\bar p(x)}$. Si todos los $p_i$ son iguales, $g \equiv 1/k$ y se recupera la mezcla uniforme de [1].
- Cada experto induce $\mathcal{D}_i(x,y) = p_i(x) f_i(y \mid x)$; la distribución de datos es $\bar{\mathcal{D}} = \frac{1}{k}\sum_i \mathcal{D}_i$. Se verifica que $\bar{\mathcal{D}}(x,y) = \bar p(x)\, \bar f(y \mid x)$.
- Recompensa $r: \mathcal{X} \times \mathcal{Y} \to \mathbb{R}$; $r_x(f) = \mathbb{E}_{y \sim f(\cdot \mid x)}[r(x,y)]$; $R_p(f) = \mathbb{E}_{x \sim p}[r_x(f)]$. Igual que [1].
- **Learner**: ahora hay una **clase de hipótesis** $\mathcal{H} \subseteq \{h: \mathcal{X} \to \mathcal{P}(\mathcal{Y})\}$ (en [1] era toda $\mathcal{F}$):
$$h_{\bar{\mathcal{D}}} = \arg\min_{h \in \mathcal{H}} \mathbb{E}_{x \sim \bar p}\big[ H(\bar f(\cdot \mid x), h(\cdot \mid x)) \big]$$
Minimizar esto equivale a minimizar la cross-entropy sobre $\bar{\mathcal{D}}$. Si $\mathcal{H}$ es irrestricta, $h = \bar f$. Restringir $\mathcal{H}$ es lo que después permite hablar de *sesgo de simplicidad* en generalización.
- **Trascendencia**: misma definición que [1]: $R_{p_{\text{test}}}(h_{\bar{\mathcal{D}}}) > \max_{i} R_{p_{\text{test}}}(f_i)$ para alguna $p_{\text{test}}$.

### 2.2 Skill denoising

Dos supuestos:
1. **Única distribución de entradas**: $p_i = \bar p$ para todo $i$.
2. **Test in-domain**: $\operatorname{supp}(p_{\text{test}}) \subseteq \operatorname{supp}(\bar p)$.

Es el setting de [1]: con errores no correlacionados, muestrear a baja temperatura devuelve la moda de la mezcla (voto por mayoría) y se trasciende.

### 2.3 Skill selection

Se elimina el supuesto 1 y se mantiene el 2. Los expertos tienen distintas $p_i$: son *especialistas*, cada uno con una *expertise* (subconjunto de entradas donde responde bien). Afirmación: hay trascendencia cuando la entrada $x$ es más probable de ser observada bajo los expertos que tienen mayor recompensa en $x$, o sea cuando $g(i \mid x)$ **depende de $x$** (el abogado habla más de derecho).

**Teorema 2.1** (dos expertos $a$, $b$). Para que haya trascendencia se debe cumplir
$$\mathbb{E}_{x \sim p_{\text{test}}}\big[ (r_x(f_a) - r_x(f_b))\,(g(a \mid x) - g(b \mid x)) \big] > 0 .$$
El exceso de presencia de $a$ en $x$ debe estar correlacionado con el exceso de recompensa de $a$ en $x$. Es condición **necesaria** (así lo enuncian y así lo prueban).

Prueba (Apéndice A.1), asumiendo $h_{\bar{\mathcal{D}}} = \bar f$ y evaluando **a temperatura 1**:
$R(\bar f) - R(f_a) = \mathbb{E}[g(a|x) r_x(f_a) + (1 - g(a|x)) r_x(f_b) - r_x(f_a)] = \mathbb{E}[g(b|x)(r_x(f_b) - r_x(f_a))] > 0$, simétricamente $\mathbb{E}[g(a|x)(r_x(f_a) - r_x(f_b))] > 0$; sumando se obtiene el enunciado. Observaciones mías:
- Las dos desigualdades intermedias son la condición exacta (necesaria y suficiente dado $h = \bar f$); el teorema las suma en una sola condición más débil.
- Esto es trascendencia **a temperatura 1**, que [1] probó imposible bajo $p$ compartida. Lo que la habilita es que $g$ dependa de $x$: ponderación bayesiana en vez de voto. Es exactamente la limitación que [1] dejó como trabajo futuro.
- Mezcla la distribución de entrenamiento ($g$ viene de los $p_i$ de train) con la de test ($\mathbb{E}$ bajo $p_{\text{test}}$).

### 2.4 Skill generalization

Se elimina el supuesto 2 y se asume algo más fuerte: $\operatorname{supp}(p_{\text{test}}) \cap \operatorname{supp}(\bar p) = \emptyset$. Las entradas de test nunca se vieron. ¿Cómo responder bien si ningún experto puede? Si el conocimiento de los expertos es representable en un espacio latente compartido, el modelo puede componer conocimiento de distintos expertos. Lo evalúan con *completado de hechos de dos saltos* (two-hop) sobre un grafo: cada experto conoce hechos de un salto y puede responder preguntas de dos saltos *dentro* de su conocimiento; las preguntas de test necesitan un salto de un experto y otro de otro. Si el learner tiene sesgo hacia soluciones simples y la estructura composicional es más simple que memorizar todas las entradas de dos saltos, generaliza componiendo. Formalizado en Apéndice A.2.

Figura 1 (ilustración): aristas azules/naranjas = hechos que cada experto sabe bien; el resto los sabe mal; la opacidad = probabilidad de que el experto genere una muestra de esa arista. Denoising: errores no sesgados y probabilidad uniforme de generar cada hecho. Selection: los especialistas generan más dentro de su expertise. Generalization: subcaso de selection, y por simplicidad la probabilidad de hecho incorrecto se fija en 0 (**expertos sin errores**).

## 3. Setting de grafo de conocimiento (Sección 3 y Apéndice B.1)

- Grafo verdad $G = (V, E)$: nodos = entidades, aristas = hechos (head, relation, tail).
- Estructura tomada del grafo basado en WIKIDATA de Cohen et al. 2023 (paper de *ripple effects of knowledge editing*). Las entidades se reemplazan por **nombres ficticios** generados con GPT-4o-mini, para garantizar que el modelo preentrenado no las vio. Procedimiento (B.1): se piden nombres de países ficticios como semilla, se asignan al azar a los países del grafo original, y se recorre el grafo tipo BFS pidiendo a GPT-4o-mini el nombre ficticio de cada nodo usando como contexto a sus vecinos ya renombrados, más una letra inicial aleatoria para diversidad. Resultado: **~25.000 entidades, 39 tipos de relación, 54.500 aristas**.
- Cada entidad tiene un **tipo semántico** (país, persona, ocupación, ...).
- $n_e$ expertos; el experto $i$ tiene un **grafo personal** $G_i$ con una cantidad predefinida de conocimiento correcto más creencias incorrectas.
- **Creencia incorrecta = arista corrupta**: se toma el hecho verdadero y se reemplaza el head *o* el tail por otra entidad **del mismo tipo** (para que sea sintácticamente plausible).
- Para selection y generalization: **clustering espectral** sobre las aristas → **5.000 clusters** de aristas = áreas de expertise potenciales. A cada experto se le asigna conocimiento de uno o más clusters.
- **Datos de entrenamiento**: cada muestra es un **párrafo sobre una entidad** (emula a un experto escribiendo sobre un tema). Para $N$ muestras con $n_e$ expertos, cada experto genera $N/n_e$ (salvo que se indique otra cosa). Para generar una muestra: se samplea un nodo uniformemente del grafo personal del experto y se escribe una oración templada por cada arista conectada a ese nodo ("The {relation} of {head} is {tail}."), en orden aleatorio.
- **Evaluación**: *query completion accuracy*. Para cada hecho del grafo verdad se arma el prompt "The {relation} of {head} is" y se compara la salida con el tail por **match exacto**; si hay varios tails correctos, vale cualquiera. Es el porcentaje de hechos verdaderos que el modelo **memorizó**. El test es siempre in-domain (son los mismos hechos sobre los que se escribió).
- **Setup**: salvo que se indique, *finetuning* de **GPT-2 preentrenado** (no dicen qué tamaño). AdamW, lr $10^{-3}$, weight decay 0.1, 1000 pasos de warmup, cosine decay, batch size 24. Cómputo (B.2): 1–4 H100 por 1–8 horas por corrida.
- No reportan semillas ni barras de error en ninguna figura.

## 4. Skill denoising (Sección 4)

**Idea**: si cada fuente se equivoca en hechos distintos, el voto colectivo acierta.

**Metodología**: todos los expertos comparten un **nivel de cobertura** $c \in [0,1]$ = fracción del grafo que cada experto sabe correctamente. Para armar $G_i$ se recorre cada arista del grafo verdad: con probabilidad $c$ se incluye correcta, con $1-c$ se incluye corrupta. Se varía $n_e$ **como proxy de errores no correlacionados**: como los errores se samplean uniforme e independientemente por experto, más expertos → distribución de errores más uniforme en el dataset. Con un solo experto no hay nada que cancelar: su creencia errónea sobre una arista es determinista.

**Resultados** (10M muestras por configuración, ≈400 párrafos por entidad; greedy decoding salvo que se especifique temperatura):
- Con suficientes expertos el modelo supera ampliamente la cobertura individual. Con $c = 0.2$ y 100 expertos: **>80 % de accuracy**.
- Figura 4 (cobertura vs accuracy, para 1, 10, 100, 1000 expertos): con 1 experto la curva es la diagonal (accuracy = cobertura); con 10 está por encima; con 100 y 1000 se satura cerca de 1 para $c \gtrsim 0.4$.
- Figura 3 (temperatura vs accuracy, para 1, 10, 100 expertos y coberturas de ~0.05 a 1): con baja temperatura la accuracy sube; a temperatura 1 queda **cerca del nivel de cobertura** de los expertos (la mezcla rinde como el experto promedio, como predice [1]); a 1.5 baja. Con 1 experto las curvas son planas.

**Takeaway**: la diversidad en forma de **errores no correlacionados** permite trascender vía "sabiduría de las masas" con baja temperatura.

## 5. Skill selection (Sección 5)

**Motivación**: en la realidad los no-expertos comparten sus *misconceptions*, así que los errores están correlacionados y el voto no garantiza nada. Pero el modelo puede igual superar a todos si elige la respuesta de la fuente con la expertise relevante. Para eso los datos tienen que tener a los expertos **hablando más de lo que saben que de lo que no saben**.

**Metodología**:
- 5.000 clusters de aristas = expertises potenciales. Cobertura $c$ compartida.
- Cada experto $i$ tiene un **vector de cobertura** $s_i = (s_i^{(1)}, \dots, s_i^{(5000)})$, $s_i^{(j)} \in [0,1]$ = accuracy del experto en las aristas del cluster $j$, con la restricción $\sum_j s_i^{(j)} |C_j| = c\,|E|$. Para cada arista $e \in C_j$: con probabilidad $s_i^{(j)}$ se incluye correcta, con $1 - s_i^{(j)}$ corrupta. (No especifican cómo se eligen los valores de $s_i^{(j)}$: qué clusters, si son 0/1 o intermedios.)
- Generación: se samplea un nodo uniforme del grafo personal, pero ahora cada hecho conectado se escribe con probabilidad
$$p = \alpha\, s_i^{(j)} + (1 - \alpha), \qquad \alpha \in [0,1],$$
donde $j$ es el cluster de la arista. $\alpha$ interpola entre "escribir con probabilidad igual a la expertise" ($\alpha = 1$) y "escribir todo por igual" ($\alpha = 0$). Es la perilla de **cuánto habla cada experto de lo que no sabe**.

**Resultados** (1M párrafos por corrida, 10 épocas; coberturas $c \in \{0.01, 0.1\}$; $\alpha$ entre 0.8 y 1; expertos de 1 a 1000; Figura 5):
- Para ambas coberturas, con suficientes expertos la accuracy llega a casi 1.
- La accuracy mejora consistentemente con $\alpha$. Con $c = 0.01$ la transición es abrupta: sólo cerca de $\alpha = 1$ (con 1000 expertos llega a ~1; con 100 a ~0.65). Con $c = 0.1$ es más gradual (con 100 expertos: de ~0.7 en $\alpha = 0.8$ a ~1 en $\alpha = 1$; con 10 expertos de ~0.1 a ~0.5).
- Más expertos = más diversidad de expertises.

**Takeaway**: con errores sesgados (misconceptions compartidas) la trascendencia la habilita la diversidad de **expertises**. Para garantizarla, los expertos deben escribir más sobre lo que dominan que sobre lo que no.

## 6. Skill generalization (Sección 6 y Apéndice B.3)

**Idea**: en selection al menos un experto sabe la respuesta; en generalization **ninguno**. El modelo tiene que componer conocimiento de varios expertos usando representaciones compartidas. Tarea: completar hechos de **dos saltos**.

**Metodología**:
- Versión simplificada de los expertos de selection: **cada experto conoce un único cluster**, y (por la Figura 1) **sin errores**. Cada experto genera muestras en proporción al tamaño de su cluster. Los datos son párrafos de un salto como antes.
- Marco de evaluación de Yang et al. 2024 (*Do LLMs latently perform multi-hop reasoning?*): capacidad composicional *latente* = responder el hecho de dos saltos **sin generar la entidad intermedia**, conociendo los hechos de un salto.
- **Across-expertise**: hechos de dos saltos cuyas dos aristas están en clusters distintos (ningún experto los conoce). **Within-expertise**: las dos aristas en el mismo cluster.
- Para enseñar el formato de dos saltos, se incluyen en el entrenamiento hechos within-expertise de dos saltos (hasta **80.000**). Se retienen **~6.000** within-expertise como validación (6.133 en B.3.1). El test across-expertise tiene **64.811** hechos.
- Tres métricas: accuracy de un salto; accuracy en la validación within-expertise no vista; accuracy en el test across-expertise.
- **Baselines** tipo "atajo" (de Yang et al. 2024): *direct connection* (¿hay una arista directa head–tail? cuenta los pares head–tail que co-ocurren en hechos de un salto: 528/6.133 = 0.086 en validación, 5.666/64.811 = 0.087 en across; la co-ocurrencia en el set de dos saltos de entrenamiento da <5 % y la omiten) y *relation majority* (responder la entidad del tipo correcto más frecuente para la segunda relación: 0.20 across, 0.15 within).
- **Modelo**: LLaMA 3.2 de **1B** (tarea más difícil). Experimentos preliminares: agrandar el modelo mejora poco el two-hop (consistente con Yang et al. 2024 y Allen-Zhu & Li 2024b). Entrenan sobre **6M párrafos** de un salto + el set de dos saltos within-expertise, **repetido 20 veces por época** para saturar la accuracy en train, **10 épocas**.

**Resultados** (Figura 6, across-expertise; Figura 7, within-expertise validación):
- La accuracy across-expertise crece aproximadamente **lineal** con la cantidad de ejemplos de dos saltos within-expertise en train: de ~0.25 (20.000) a **0.34** (80.000), contra **0.20** de relation majority y 0.09 de direct connection. Un salto: casi perfecto en todos los modelos.
- Within-expertise (validación): 0.36 → **0.70** en el mismo rango. O sea, componer dos hechos del mismo experto ya es difícil, y cruzar expertos cuesta otro tanto (0.70 vs 0.34).
- **Desafío central**: la cantidad de hechos de dos saltos que un experto individual conoce es finita, no se puede seguir agrandando el set de train. Por eso prueban dos alternativas.

**Phrasing diversity** (inspirado en Allen-Zhu & Li 2024a, *Physics of LMs 3.1*: la augmentación hace que el modelo forme mejores representaciones latentes en vez de memorizar contexto):
- Cuatro niveles (Tabla 1): (1) un template por relación (estándar); (2) cuatro templates por relación, uno al azar por arista; (3) GPT-4o-mini reescribe el párrafo de nivel 1 con baja creatividad ("rewrite the facts"); (4) GPT-4o-mini reescribe el de nivel 2 con alta creatividad ("use creative word choices and phrasing"). En niveles 1 y 2 los hechos multi-salto van en un único template.
- Los hechos de dos saltos también se refrasean con GPT-4o-mini.
- Modelos "Data diversity": 1,5M párrafos × 4 niveles = 6M muestras (mismo total que el estándar). Más los dos saltos refraseados, repetidos 20×/época junto con los templados.
- **Resultado**: diversidad en párrafos de un salto: across 0.34 → **0.37** (within 0.70 → 0.79); diversidad en los hechos de dos saltos: **sin efecto**. Dejan para futuro augmentaciones más principled.

**Chain-of-Thought** (B.3.4): formato QA con la entidad intermedia antes de la respuesta final ("What is the award received by the screenwriter of Glyndor Aetheralis? Ithryndor Glaciaris; Xyphorian Starblossom."). En evaluación se le permite generar el paso intermedio antes del punto y coma y se juzga sólo la respuesta final. **Resultado**: across **0.62**, within 0.92. Observación conceptual del paper: cuando el modelo nombra explícitamente el nodo intermedio, **reduce el problema de generalización a uno de selección** (cada salto lo sabe algún experto).

**Takeaway**: generalización es el modo más difícil pero los LMs lo logran. Se promueve con diversidad de formas superficiales (fraseo) y, más notoriamente, con **diversidad de composiciones** en los datos de entrenamiento.

## 7. Análisis formal de generalización (Apéndice A.2)

Caso de estudio para dar intuición, basado en el setting del grafo:
- $G = (V, E)$, $R$ tipos de relación, arista $e = (a, r, b)$. $F^{(1)} = E$ = hechos de un salto. Supuesto: mapeo determinista, para cada prefijo $(a, r)$ hay a lo sumo un $b$. $(a, r)$ es una "entrada de un salto".
- Hecho de dos saltos $(a, r_1, r_2, c)$ con entidad puente $b$: $(a, r_1, b), (b, r_2, c) \in F^{(1)}$. Conjunto $F^{(2)}$. Función $f^*: V \times R \times R \to V$, definida sólo donde existe puente. $(a, r_1, r_2)$ es una "entrada de dos saltos".
- $f^*$ es **composicional**: $f^*(a, r_1, r_2) = g^*(g^*(a, r_1), r_2)$ con $g^*(a, r) = b$.
- $\mathcal{X}$ = entradas de dos saltos válidas; $\mathcal{Y} = V \cup \{\epsilon\}$ ($\epsilon$ = etiqueta nula).
- Partición de los hechos de un salto en $k$ expertos $F_i^{(1)}$. Espacio de entrada del experto $i$: $\mathcal{X}_i = \{(a, r_1, r_2) \mid \exists b, c: (a, r_1, b), (b, r_2, c) \in F_i^{(1)}\}$ (ambos saltos en su partición). $p_i$ con soporte total en $\mathcal{X}_i$. El experto siempre etiqueta bien. Dataset $D$ de $N$ muestras únicas.
- Clase de hipótesis $\mathcal{H} = \mathcal{H}_{\text{mem}} \cup \mathcal{H}_{\text{comp}}$: memorizadores con una tabla $T^{(2)}$ de tamaño $V \times R \times R$, y composicionales $h(a, r_1, r_2) = g(g(a, r_1), r_2)$ con una tabla $T^{(1)}$ de tamaño $V \times R$.
- Complejidad $\kappa(T)$ = número de entradas no nulas de la tabla; $\kappa$ de una función de lookup = $\kappa$ de su tabla; componer cuesta un overhead fijo: $\kappa(f(f(\cdot), \cdot)) = \kappa(f) + \kappa_{\text{comp}}$.
- ERM: $h_D \in \arg\min_{h \in \mathcal{H}} \mathbb{E}_D[H(y, h(x))]$. Es realizable, así que hay un conjunto $\mathcal{H}^*_D$ de hipótesis con loss cero; cualquier memorizador de $D$ está ahí pero no generaliza a dos saltos entre particiones.
- **Sesgo de simplicidad**: $h_D \in \arg\min_{h \in \mathcal{H}^*_D} \kappa(h)$.
- Memorizador: $\kappa(h) \geq |D|$. Composicional: $\kappa(h) \leq |F^{(1)}| + \kappa_{\text{comp}}$. **Condición suficiente** para preferir la solución composicional: $|D| \geq |F^{(1)}| + \kappa_{\text{comp}}$.
- Cota de $|D|$: sólo hay hechos de dos saltos within-partition. Con $d_{\text{in}}(v), d_{\text{out}}(v)$ los grados: $|F^{(1)}| = \sum_v d_{\text{in}}(v) = \sum_v d_{\text{out}}(v)$; cada nodo induce $d_{\text{in}}(v) \cdot d_{\text{out}}(v)$ hechos de dos saltos; y
$$|D| \leq \sum_{i=1}^{k} |\mathcal{X}_i| = \sum_{i=1}^{k} \sum_{v \in V} d^{(i)}_{\text{in}}(v)\, d^{(i)}_{\text{out}}(v)$$
con grados restringidos a la partición $i$.
- **Condición final**: $\sum_v d_{\text{in}}(v) + \kappa_{\text{comp}} < \sum_i \sum_v d^{(i)}_{\text{in}}(v)\, d^{(i)}_{\text{out}}(v)$. Intuición: tienen que existir suficientes hechos de dos saltos válidos dentro del dominio de un solo experto. Como el conocimiento está estructurado en un espacio latente compartido (representaciones reutilizables de un salto), la composición es eficiente y el learner con sesgo de simplicidad prefiere generalizar.
- Esto es lo que "motiva" el experimento de agrandar el set de dos saltos: hacen crecer el lado $|D|$ de la desigualdad.

## 8. Trabajo relacionado (Sección 7)

- **Trascendencia**: [1] (voto a baja temperatura; ajedrez 1000 → 1500). Este trabajo extiende a casos con errores correlacionados. Cunningham 2023 (post de blog) también delineó formas en que un imitador supera al humano.
- **Diversidad de datos y adquisición de conocimiento**: Allen-Zhu & Li 2024a (biografías sintéticas, augmentación → extracción flexible; acá además composición multi-salto); Zhu et al. 2025 (formatos diversos); Allen-Zhu & Li 2024b (CoT crítico para manipulación de conocimiento); Naik et al. 2024 (diversidad de prompting en inferencia); Chang et al. 2024 (entidades ficticias para estudiar adquisición durante el entrenamiento); literatura de composicionalidad y diversidad: Berlot-Attwell et al. 2024, Levy et al. 2023, Oren et al. 2021, Rahimi et al. 2024.
- **Fallas de composición en transformers**: Dziri et al. 2023; Press et al. 2023 (*compositionality gap* no se achica con escala); Wang et al. 2024 (path finding: no aprenden alcanzabilidad por transitividad); Yang et al. 2024 (la escala ayuda al primer salto, no al segundo); Saparov et al. 2023.
- **Generalización / regularización implícita**: Goldblum et al. 2024 (sesgo hacia baja complejidad de Kolmogorov); Zadrozny 2000 (MDL: memorizar se vuelve de alta complejidad al crecer el corpus → emerge composición).
- **Ensembling y fusión de modelos**: el modelo se puede ver como un ensemble implícito de los expertos que generaron sus datos. Majority voting sobre salidas (Wang et al. 2023 self-consistency; Li et al. 2024); MoE (Lepikhin 2020, Fedus 2022) y ensembles (Liu 2021, Li 2022, Gururangan 2023) diseñan la selección en la **arquitectura**, mientras que acá los expertos están en los **datos** y la arquitectura es simple; fusión (Wan 2024, Mavromatis 2024); Li 2022 y Gururangan 2023 entrenan modelos separados por clusters de documentos y los combinan en inferencia.

## 9. Discusión y limitaciones (Sección 8)

- Resumen: denoising → baja temperatura si errores no correlacionados; selection → los expertos generan dentro de su expertise; generalization → sesgo de simplicidad, con datos suficientemente complejos (fraseo diverso, ejemplos de composición).
- El setup controlado aísla fenómenos pero es limitado; piden trabajo en settings reales.
- El marco **no captura *skill discovery*** (descubrir algo que ningún experto ni su composición sabe).

## 10. Lo que el paper no especifica (ver la v0 para lo que se pudo constatar en el código)

- Tamaño de GPT-2 usado.
- Cómo se construye el vector de cobertura $s_i$ (qué clusters recibe cada experto, si los valores son 0/1).
- Si las corrupciones son independientes entre expertos en selection (la motivación habla de misconceptions *compartidas*, pero el procedimiento descrito corrompe al azar por experto).
- Cuántos expertos hay en generalization (¿uno por cluster, 5.000?).
- Formato exacto de los datos de entrenamiento con CoT.
- Semillas, varianza, barras de error: no hay.
