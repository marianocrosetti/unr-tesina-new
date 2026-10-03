# Propuesta de tesina

**Postulante:** Mariano Crosetti&nbsp;  
**Director:** Dante Zanarini&nbsp;  
**Codirector:** Pablo Granitto

## 1\. Situación del postulante

Al día 21/09/2026 tengo aprobadas todas las materias de la Licenciatura en Ciencias de la Computación y adeudo únicamente la tesina. Me encuentro trabajando en Aleph (getaleph.com), una empresa de software, con una dedicación de 40 horas semanales. Dedicaré a la tesina al menos NN horas semanales.

## 2\. Título

Cuantificación del fenómeno de trascendencia en juegos con solución exacta

## 3\. Motivación y objetivo general

Los modelos generativos actuales, entre ellos los grandes modelos de lenguaje (LLM), se entrenan mayoritariamente por imitación: se ajustan sus parámetros para maximizar la probabilidad de un conjunto de datos. Cuando esos datos son producidos por distintos expertos, la intuición indica que el modelo resultante no debería superarlos: la teoría nos dice que, en el límite, aprende la distribución de los datos.

Zhang et al. \[1\] (2024, NeurIPS) mostraron un resultado que contradice esa intuición. Entrenaron un transformer con partidas de ajedrez de jugadores con rating de hasta 1000 y obtuvieron un modelo que, al muestrear sus jugadas a baja temperatura, juega con un rating aproximado de 1500, mejor que el de cualquiera de los jugadores que produjeron sus datos. Denominaron a este fenómeno *trascendencia* y lo explicaron mediante un mecanismo de cancelación de errores: el modelo aprende la mezcla de las políticas de todos los jugadores y, cuando los errores de distintos jugadores no coinciden, la jugada más probable de esa mezcla (la que se elige al muestrear con temperatura 0\) tiende a ser la correcta. Abreu et al. \[2\] (2025, COLM) continuaron esta línea con una taxonomía de tres mecanismos mediante los cuales un imitador puede superar a sus fuentes, estudiada en un dominio sintético de grafos de conocimiento.

El fenómeno es relevante más allá del ajedrez: sugiere que la calidad de un modelo entrenado por imitación no está acotada por la calidad de sus fuentes individuales sino por la estructura de los errores del conjunto. Sin embargo, la evidencia disponible presenta limitaciones. En \[1\] los datos son humanos y no es posible intervenir en la correlación de errores entre jugadores, por lo que el rol de la diversidad se infiere pero no se prueba en un escenario controlado, ni se analiza cuál es su límite; tampoco se dispone de un evaluador exacto, ya que la calidad de cada jugada se estima mediante un motor heurístico. En \[2\] sí hay control sobre los errores y verificación exacta, pero el dominio es estático (cada consulta es independiente de las anteriores, a diferencia de un juego, donde cada decisión condiciona las siguientes), el modelo es un GPT-2 preentrenado ajustado sobre un dataset sintético introducido en el mismo trabajo, y los resultados sobre el tercer mecanismo de la taxonomía (*generalización*) son, como señalan los autores, poco concluyentes.

El objetivo general de esta tesina es cuantificar el fenómeno de trascendencia en un dominio que combine ambos enfoques: un juego de información perfecta con solución exacta conocida, en el que sea posible construir expertos sintéticos con una estructura de errores controlada y medir la calidad de cada jugada del imitador sin aproximaciones. Esto permitirá responder preguntas que los trabajos anteriores dejan abiertas: cómo depende la magnitud de la trascendencia de la correlación de los errores entre expertos, en qué medida ocurre en posiciones vistas durante el entrenamiento y en posiciones nuevas, y si un imitador puede componer habilidades de expertos que nunca aparecen en las mismas posiciones.

## 4\. Fundamentos y estado de conocimiento sobre el tema

### 4.1. Modelos generativos entrenados por imitación

Un modelo generativo autorregresivo define una distribución de probabilidad sobre secuencias de símbolos, prediciendo cada símbolo a partir de los anteriores; la arquitectura dominante para esta tarea es el Transformer \[3\]. El entrenamiento estándar minimiza la entropía cruzada respecto de un conjunto de datos, lo que equivale a maximizar la probabilidad que el modelo asigna a las secuencias observadas. Con datos y capacidad suficientes, el modelo se aproxima a la distribución que generó los datos; si estos provienen de varias fuentes, por ejemplo partidas de distintos jugadores, la distribución aprendida es la mezcla de las distribuciones de esas fuentes, ponderada según la frecuencia con la que cada una aparece. Una vez entrenado, el modelo se utiliza muestreando de la distribución aprendida, habitualmente con un parámetro de temperatura: a temperatura 1 se muestrea la distribución tal como fue aprendida y, a medida que la temperatura tiende a cero, el muestreo se concentra en el símbolo más probable.

El aprendizaje por imitación de políticas de decisión, conocido como *behavioral cloning*, tiene límites teóricos bien conocidos: los errores del imitador se acumulan a lo largo de una trayectoria y pueden conducirlo a estados no cubiertos por los datos \[4, 5\]. El fenómeno de trascendencia muestra que, en ciertas condiciones, ocurre lo contrario.

### 4.2. Trascendencia

Zhang et al. \[1\] definen que un modelo trasciende cuando su recompensa esperada supera a la del mejor experto individual de la población que lo entrenó. Prueban que, a temperatura 1, la trascendencia es imposible, porque la mezcla de expertos nunca supera al mejor de ellos, y que, a baja temperatura, ocurre si y sólo si la acción más probable de la mezcla rinde más que la del mejor experto, lo que equivale a un voto por mayoría implícito entre los expertos. Empíricamente, el modelo entrenado con partidas de jugadores con rating de hasta 1000 alcanza un rating aproximado de 1500, mientras que el entrenado con partidas de jugadores de hasta 1500 no produce una mejora significativa. Atribuyen esta diferencia a que el segundo conjunto de datos presenta menor diversidad de jugadas, medida como la entropía media de la distribución de jugadas en las posiciones frecuentes. Como los datos son de origen humano, esta atribución es correlacional. Además, dado que el ajedrez no es un juego resuelto, tanto la recompensa de cada jugada como el rating del modelo se estiman mediante el motor Stockfish.

Abreu et al. \[2\] proponen una taxonomía de tres mecanismos de trascendencia y la estudian en un grafo de conocimiento sintético, donde la respuesta correcta a cada consulta se conoce por construcción: (i) *denoising* por voto, en el que los errores independientes de distintos expertos se cancelan mutuamente; (ii) *selección* de la fuente competente, en el que cada experto es confiable en una región del dominio y el modelo aprende a rutear cada consulta hacia el experto adecuado, mecanismo para el cual dan una condición bajo la cual la trascendencia ocurre ya a temperatura 1; y (iii) *generalización*, en el que el modelo combina conocimiento de distintas fuentes para responder consultas que ningún experto podía responder, con resultados débiles. Los experimentos de denoising y selección evalúan consultas vistas durante el entrenamiento, mientras que los de generalización evalúan consultas no vistas, pero con expertos sin errores. No se analiza cómo se distribuye la trascendencia entre casos vistos y no vistos cuando hay ruido, que es la situación natural en un juego con expertos no óptimos.

### 4.3. Líneas de trabajo relacionadas

El denoising por voto conecta la trascendencia con los métodos de ensamble, en particular con el *bagging* \[6\], donde la mejora obtenida al promediar predictores está acotada por la correlación entre sus errores, y con la "sabiduría de las masas" en equipos de agentes, donde la diversidad puede vencer a la fuerza individual \[7\]. La robustez de las redes neuronales al ruido de etiquetas \[8\] y la dinámica de memorización sobre datos finitos \[9\] determinan bajo qué régimen de entrenamiento se sostiene el voto implícito. Sobre el mecanismo de generalización hay posiciones informadas en desacuerdo: la literatura de aprendizaje condicionado al retorno documenta fallas al combinar trayectorias de distintos expertos \[10, 11\], lo que predice colapso fuera del soporte de cada uno, mientras que se ha reportado generalización composicional en transformers de ajedrez evaluados fuera de distribución \[12\], lo que predice transferencia. Por último, un imitador que recibe únicamente la secuencia de jugadas construye internamente una representación del estado \[13, 14\], y toda generalización a posiciones nuevas es generalización de dicha representación.

### 4.4. Cuatro en línea como dominio de estudio

Cuatro en línea es un juego de información perfecta para dos jugadores sobre un tablero de siete columnas y seis filas, resuelto por Allis en 1988 \[15\]: el primer jugador gana con juego perfecto. Existen resolvedores exactos de dominio público que devuelven, para cualquier posición alcanzable, el resultado teórico de cada jugada legal \[16\]. Esto permite conocer la calidad exacta de cada decisión sin evaluaciones heurísticas, construir expertos sintéticos óptimos a los que se les inyectan errores con la estructura deseada y calcular analíticamente la recompensa esperada de cada experto en cualquier conjunto de posiciones. A la vez, conserva la característica esencial del ajedrez que el dominio de \[2\] no tiene: el estado es secuencial y cada jugada condiciona las posiciones futuras.

## 5\. Objetivos específicos

1. Construir un banco de pruebas sobre cuatro en línea con expertos sintéticos de estructura de errores parametrizable, un imitador transformer que sólo reciba la secuencia de jugadas y evaluación exacta mediante el resolvedor.

2. Cuantificar cómo varía la trascendencia por denoising con la fracción de errores compartidos entre expertos.

3. Cuantificar la trascendencia por selección de la fuente competente en función de la fuerza del ruteo, contrastando con el umbral que predice la teoría, y caracterizar la dependencia de ambos mecanismos respecto de la temperatura.

4. Descomponer la trascendencia entre posiciones vistas y no vistas durante el entrenamiento, y estudiar cómo cambia esa descomposición con la cantidad de datos.

5. Evaluar si el imitador compone habilidades de subpoblaciones de expertos con soporte disjunto.

## 6\. Metodología y plan de trabajo

El trabajo es fundamentalmente experimental y sigue los objetivos específicos. Una exploración preliminar sobre cuatro en línea confirmó la viabilidad del banco de pruebas y de su costo computacional, con entrenamientos del orden de minutos en una GPU de consumo, y arrojó resultados en la dirección esperada para los objetivos 2 y 3\. Esa exploración será reimplementada y revisada como parte de la tesina. Se proponen los siguientes pasos:

1. Implementar el banco de pruebas. Los expertos sintéticos jugarán la jugada óptima según el resolvedor de Pons \[16\], salvo en las posiciones donde se les inyecte un error de estructura controlada. El imitador será un transformer del orden de millones de parámetros entrenado por predicción del siguiente símbolo sobre transcripciones de partidas; siguiendo a \[1\], recibirá sólo la secuencia de jugadas, sin tablero, identidad del experto ni recompensa. Se medirá la recompensa esperada exacta y la probabilidad de jugada óptima del imitador en posiciones de prueba, para cada temperatura, y se la comparará con la de los expertos, calculada analíticamente. Se complementará con partidas contra los expertos y contra el jugador perfecto.

2. Construir poblaciones de expertos en las que una fracción controlada de los errores es común a todos y el resto es independiente, y medir la trascendencia a baja temperatura en función de esa fracción. La teoría de \[1\] y la cota clásica de los ensambles predicen una ganancia decreciente que cambia de signo cuando los errores son totalmente compartidos. Se incluirá un control en el que todos los expertos evitan una jugada buena, para verificar que el imitador no descubre lo que ningún experto muestra.

3. Construir K expertos, cada uno óptimo en una región del espacio de estados y con un error compartido fuera de ella, y variar la probabilidad de que en cada región genere los datos el experto competente. La teoría de \[1\] implica un umbral de esa probabilidad por encima del cual bajar la temperatura mejora al imitador y por debajo lo empeora; se contrastará esa predicción y se medirá la curva de recompensa en función de la temperatura para denoising y para selección.

4. Etiquetar cada posición de prueba como vista o no vista según el tablero aparezca en el entrenamiento, descomponer las métricas anteriores según esa etiqueta y repetir para distintos tamaños del conjunto de entrenamiento, estratificando por fase de la partida.

5. Construir dos subpoblaciones con soporte disjunto: una que juega aperturas óptimas con transcripciones truncadas antes del final y otra que juega aperturas de estilo restringido y finales óptimos. Medir la calidad del imitador en finales alcanzados desde aperturas óptimas, que ninguna transcripción muestra, y su rendimiento contra el jugador perfecto, con controles entrenados con cada subpoblación por separado. La literatura ofrece predicciones opuestas, colapso \[10, 11\] o transferencia \[12\], por lo que es el paso de resultado más incierto.

6. Reproducir los resultados principales variando tamaño del modelo, cantidad de datos y pasos de entrenamiento, y redactar el informe.

Todas las condiciones se repetirán con varias semillas aleatorias. Como la exploración preliminar indica que entrenar muchas pasadas sobre un conjunto fijo destruye la trascendencia por memorización de los errores \[9\], se seleccionará el punto de control de menor pérdida de validación. Si algún experimento requiriera más cómputo del previsto, se reducirá el tamaño del modelo o de los datos, dado que los efectos son observables con modelos pequeños.

### 6.1. Cronograma de trabajo

1. Implementación y validación del banco de pruebas (paso 1): 2 semanas.  
2. Experimentos de correlación de errores (paso 2): 2 semanas.  
3. Experimentos de selección y temperatura (paso 3): 1 semana.  
4. Descomposición entre posiciones vistas y no vistas (paso 4): 1 semana.  
5. Experimentos de composición con soporte disjunto (paso 5): 2 semanas.  
6. Análisis de sensibilidad y consolidación de resultados: 2 semanas.  
7. Redacción del marco teórico y del informe final: 4 semanas.  
8. Revisión y correcciones: 2 semanas.

La duración total estimada es de 16 semanas, aproximadamente cuatro meses.

## Referencias

\[1\] E. Zhang, V. Zhu, N. Saphra, A. Kleiman, B. L. Edelman, M. Tambe, S. M. Kakade, E. Malach. *Transcendence: Generative Models Can Outperform The Experts That Train Them*. NeurIPS, 2024\. arXiv:2406.11741.

\[2\] N. Abreu, E. Zhang, E. Malach, N. Saphra. *A Taxonomy of Transcendence*. COLM, 2025\. arXiv:2508.17669.

\[3\] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, I. Polosukhin. *Attention Is All You Need*. NeurIPS, 2017\.

\[4\] S. Ross, D. Bagnell. *Efficient Reductions for Imitation Learning*. AISTATS, 2010\.

\[5\] S. Ross, G. Gordon, D. Bagnell. *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS, 2011\.

\[6\] L. Breiman. *Bagging Predictors*. Machine Learning, 24:123–140, 1996\.

\[7\] L. S. Marcolino, A. X. Jiang, M. Tambe. *Multi-agent Team Formation: Diversity Beats Strength?* IJCAI, 2013\.

\[8\] D. Rolnick, A. Veit, S. Belongie, N. Shavit. *Deep Learning is Robust to Massive Label Noise*. arXiv:1705.10694, 2017\.

\[9\] D. Arpit, S. Jastrzębski, N. Ballas, D. Krueger, E. Bengio, M. S. Kanwal, T. Maharaj, A. Fischer, A. Courville, Y. Bengio, S. Lacoste-Julien. *A Closer Look at Memorization in Deep Networks*. ICML, 2017\.

\[10\] K. Paster, S. McIlraith, J. Ba. *You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments*. NeurIPS, 2022\.

\[11\] D. Brandfonbrener, A. Bietti, J. Buckman, R. Laroche, J. Bruna. *When Does Return-Conditioned Supervised Learning Work for Offline Reinforcement Learning?* NeurIPS, 2022\.

\[12\] A. Mészáros, P. Reizinger, F. Huszár. *Out-of-distribution Tests Reveal Compositionality in Chess Transformers*. arXiv:2510.20783, 2025\.

\[13\] S. Toshniwal, S. Wiseman, K. Livescu, K. Gimpel. *Chess as a Testbed for Language Model State Tracking*. AAAI, 2022\.

\[14\] A. Karvonen. *Emergent World Models and Latent Variable Estimation in Chess-Playing Language Models*. arXiv:2403.15498, 2024\.

\[15\] V. Allis. *A Knowledge-Based Approach to Connect-Four*. Tesis de maestría, Vrije Universiteit Amsterdam, 1988\.

\[16\] P. Pons. *Connect 4 Game, Solver*. [http://connect4.gamesolver.org](http://connect4.gamesolver.org), 2019\.

&nbsp;