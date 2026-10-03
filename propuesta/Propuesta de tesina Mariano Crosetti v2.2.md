# Propuesta de tesina

**Postulante:** Mariano Crosetti   
**Director:** Dante Zanarini   
**Codirector:** Pablo Granitto

## 1\. Situación del postulante

Al día 21/09/2026 tengo aprobadas todas las materias de la Licenciatura en Ciencias de la Computación y adeudo únicamente la tesina. Me encuentro trabajando en Aleph (getaleph.com), una empresa de software, con una dedicación de 40 horas semanales. Dedicaré a la tesina al menos **15** horas semanales.

## 2\. Título

Cuantificación del fenómeno de trascendencia en juegos con solución exacta

## 3\. Motivación y objetivo general

Los modelos generativos actuales, entre ellos los grandes modelos de lenguaje, se entrenan mayoritariamente mediante imitación, es decir, se ajustan sus parámetros para maximizar la probabilidad de un conjunto de datos. Cuando esos datos son generados por distintos expertos, la intuición sugiere que el modelo resultante no debería superarlos.

Zhang et al. \[1\] (2024, NeurIPS) mostraron un resultado que contradice esa intuición. Entrenaron un transformador con partidas de ajedrez de jugadores con rating de hasta 1000 y obtuvieron un modelo que, juega con un rating aproximado de 1500, mejor que el de cualquiera de los jugadores que produjeron sus datos. Denominaron a este fenómeno *trascendencia* y lo explicaron mediante un mecanismo de cancelación de errores: el modelo aprende la mezcla de las políticas de todos los jugadores y, cuando los errores de distintos jugadores no coinciden, la jugada más probable de esa mezcla tiende a ser la correcta. 

Abreu et al. \[2\] (2025, COLM) continuaron esta línea con una taxonomía de tres mecanismos mediante los cuales un modelo puede superar a sus fuentes, estudiada en un dominio sintético de grafos de conocimiento.

El fenómeno es relevante más allá del ajedrez: sugiere que la calidad de un modelo entrenado por imitación no está acotada por la calidad de sus fuentes individuales sino por la estructura de los errores del conjunto.

 Sin embargo, creemos que la evidencia disponible en ambos trabajos presenta limitaciones. En \[1\] los datos son humanos y no es posible intervenir en la correlación de errores entre jugadores. En \[2\] si bien hay control sobre los errores y verificación exacta, el dominio no es un juego de información perfecta sino un dominio estático: un grafo sintético de informacion, donde cada consulta es independiente de las anteriores, a diferencia de un juego, donde cada decisión condiciona las siguientes. Además los resultados sobre el tercer mecanismo de la taxonomía, denominado *habilidad de generalización*, son, como señalan los autores mismos, poco concluyentes.

El objetivo general de esta tesina es cuantificar el fenómeno de trascendencia en un dominio que combine ambos enfoques, partiendo de un juego de información perfecta, en el que sea posible construir expertos sintéticos con una estructura de errores controlada y medir la calidad de cada jugada del modelo sin aproximaciones. Esto permitirá responder preguntas que los trabajos anteriores dejan abiertas: cómo depende la magnitud de la trascendencia de la correlación de los errores entre expertos, en qué medida ocurre en posiciones vistas durante el entrenamiento y en posiciones nuevas, y si un modelo puede componer habilidades de expertos que nunca aparecen en las mismas posiciones.

## 4\. Fundamentos y estado de conocimiento sobre el tema

### 4.1. Modelos generativos entrenados por imitación

Un modelo generativo autorregresivo define una distribución de probabilidad sobre secuencias de símbolos y predice cada símbolo a partir de los anteriores; la arquitectura dominante para esta tarea es el transformador \[3\]. El entrenamiento estándar minimiza la entropía cruzada con respecto a un conjunto de datos, lo que equivale a maximizar la probabilidad que asigna el modelo a las secuencias observadas. Con datos y capacidad suficientes, el modelo aproxima la distribución que generó los datos; si estos provienen de varias fuentes, por ejemplo, partidas de distintos jugadores, la distribución aprendida es la mezcla ponderada de las distribuciones de esas fuentes, según la frecuencia con la que cada una aparece. Una vez entrenado, el modelo se utiliza muestreando de la distribución aprendida, habitualmente con un parámetro de temperatura: a temperatura 1 se muestrea la distribución tal como fue aprendida y, a medida que la temperatura tiende a cero, el muestreo se concentra en el símbolo más probable.

### 4.2. Trascendencia

Zhang et al. \[1\] define que un modelo trasciende cuando su recompensa esperada supera a la del mejor experto individual de la población que lo entrenó. Prueban que, a temperatura 1, la trascendencia es imposible, porque la mezcla de expertos nunca supera al mejor de ellos, y que, a baja temperatura, ocurre si y sólo si la acción más probable de la mezcla rinde más que la del mejor experto, lo que equivale a un voto por mayoría implícito entre los expertos. Empíricamente, el modelo entrenado con partidas de jugadores con rating de hasta 1000 alcanza un rating aproximado de 1500, mientras que el entrenado con partidas de jugadores con rating de hasta 1500 no muestra una mejora significativa. Atribuyen esta diferencia a que el segundo conjunto de datos presenta menor diversidad de jugadas, medida como la entropía media de la distribución de jugadas en las posiciones frecuentes. Como los datos son de origen humano, esta atribución es correlacional: los escenarios donde se le da la trascendencia coinciden con los de mayor diversidad, y viceversa: cuando la trascendencia no se da (((((entrenando con rating hasta 1500), coincide con diversidades más bajas. Además, dado que el ajedrez no es un juego resuelto, tanto la recompensa de cada jugada como el rating del modelo se estiman mediante el motor Stockfish.

Abreu et al. \[2\] proponen una taxonomía de tres mecanismos de trascendencia y la estudian en un grafo de conocimiento sintético, donde la respuesta correcta a cada consulta se conoce por construcción: (i) *cancelación de errores* por voto, en el que los errores independientes de distintos expertos se cancelan mutuamente; (ii) *selección* de la fuente competente, en el que cada experto es confiable en una región del dominio y el modelo aprende a rutear cada consulta hacia las capacidades aprendidas del experto adecuado, mecanismo para el cual dan una condición bajo la cual la trascendencia ocurre ya a temperatura 1; y (iii) *generalización*, en el que el modelo combina conocimiento de distintas fuentes para responder consultas que ningún experto podía responder, con resultados débiles. Los experimentos de cancelación de errores y de selección evalúan consultas vistas durante el entrenamiento, mientras que los de generalización evalúan consultas no vistas, pero con expertos sin errores. No se analiza cómo se distribuye la trascendencia entre casos vistos y no vistos cuando hay ruido, lo cual es la situación natural en un juego con expertos no óptimos.

### 4.3. Líneas de trabajo relacionadas

Sobre el mecanismo de cancelación de errores por voto, este conecta la trascendencia con los métodos de ensamble, en particular con los bosques aleatorios \[4\], donde la mejora obtenida al promediar predictores está acotada por la correlación entre sus errores, y con la "sabiduría de las masas" en equipos de agentes, donde la diversidad puede vencer a la fuerza individual \[5\]. Dos resultados sobre entrenamiento con datos ruidosos acotan cuándo puede funcionar ese voto: las redes neuronales aprenden la señal correcta aun cuando la mayoría de las etiquetas son erróneas, siempre que el error no sea sistemático \[6\], pero si se entrenan durante suficientes pasadas sobre un conjunto de datos finito terminan memorizando cada ejemplo con su error \[7\]. El voto implícito existe, por lo tanto, sólo con suficientes datos y sin sobreentrenamiento.

Sobre el mecanismo de selección, la idea de que distintos expertos sean confiables en distintas regiones del dominio y de que se aprenda a rutear cada entrada hacia el experto adecuado es la de las mezclas de expertos \[8\], donde una red de compuerta se entrena junto con los expertos locales; sus versiones a gran escala son los transformadores con capas de mezcla de expertos \[9\]. En la misma línea, se han entrenado modelos separados sobre distintos agrupamientos del corpus para combinarlos en la inferencia \[10\]. En todos estos casos la selección es explícita en la arquitectura. En la trascendencia por selección, en cambio, la arquitectura es una única red y la selección queda implícita en los datos: la condición de \[2\] es que la frecuencia con la que cada experto genera datos en una región del dominio esté correlacionada con su rendimiento en ella.

Sobre el mecanismo de generalización, por un lado, se sabe que los transformadores fallan al componer dos hechos que se conocen por separado \[11, 12\]. Cabe señalar que \[2\] obtiene, en su tarea de composición, sólo una mejora modesta sobre el azar. Por otro lado, en modelos entrenados con partidas de ajedrez, las representaciones aprendidas resultan robustas. Un modelo que recibe únicamente la secuencia de jugadas reconstruye el estado del tablero \[13, 14\]. \[15\] muestra que un transformador entrenado en posiciones de ajedrez realiza movimientos legales aun en configuraciones totalmente fuera de la distribución (puzzles raros, tableros sintéticos de tres damas, caballos y torres), lo que sugiere que las reglas se aprenden como algo componible y generalizable. A pesar de ello, también muestra que la estrategia no se transfiere bien a estas configuraciones ubicadas completamente fuera de la distribución.

### 4.4. Juegos con solución exacta como dominio de estudio

Un juego finito de dos jugadores con información perfecta tiene un valor teórico bien definido para cada posición: o bien es ganadora, o perdedora, o empata \[16\]. Si se conoce una forma de calcular dicho valor en cada posición, diremos que el juego está resuelto \[17\]. Disponer del valor exacto tiene dos consecuencias esenciales para nuestro estudio. En primer lugar, podremos evaluar, mediante una comparación directa, la predicción del modelo en cada jugada. Segundo, nos permite definir expertos sintéticos con errores controlados porque sabemos qué movimientos son un error y cuáles no degradan el valor de la posición.

Proponemos utilizar el Cuatro en línea, un juego de información perfecta para dos jugadores, sobre un tablero de siete columnas y seis filas, resuelto por Allis en 1988 \[18\]. Existen resolvedores exactos de dominio público que devuelven, para cualquier posición alcanzable, el resultado teórico de cada jugada legal \[19\].

## 5\. Objetivos específicos

1. Cancelación de errores: Cuantificar cómo varía la trascendencia como resultado del mecanismo de *cancelación de errores* al variar la proporción de errores compartidos entre los expertos.

2. Selección de habilidades: Cuantificar la trascendencia como resultado del mecanismo de *selección de* *habilidades* al variar la proporción de los datos generados por el experto competente.

3. Medir la ganancia de los mecanismos propuestos en 1 y 2, en función de la temperatura de muestreo, tomando como referencia la teoría de *cancelación de errores* según \[1\].

4. Cuantificar la trascendencia en dos conjuntos distintos: en posiciones vistas y en posiciones no vistas durante el entrenamiento.

5. Cuantificar la trascendencia como resultado del mecanismo de *generalización*, donde \[2\] obtuvo resultados débiles, con dos subpoblaciones de expertos de soporte disjunto.

## 6\. Metodología y plan de trabajo

El trabajo es fundamentalmente experimental y sigue el orden de los objetivos específicos. Se proponen los siguientes pasos:

1. Implementar el sistema que aplique estrategias óptimas y definir los detalles de la infraestructura: el modelo de transformador a utilizar, así como las modalidades de entrenamiento y de evaluación. Se seguirá el criterio utilizado \[1\] como referencia, realizando los ajustes correspondientes al tamaño de nuestro dataset.

2. Diseñar, implementar y realizar los experimentos de los objetivos 1, 2, 3, 4 y 5 (ver sección anterior *objetivos específicos*) en la misma infraestructura, incluyendo, en cada caso, condiciones de control.

3. Reproducir los resultados principales variando el tamaño del modelo, la cantidad de datos y los pasos de entrenamiento, y redactar el informe.

Todas las condiciones se repetirán con varias semillas aleatorias y se seleccionará el punto de control con la menor pérdida en la validación. Si algún experimento requiriera más cómputo del previsto, se reduciría el tamaño del modelo o de los datos, dado que los efectos son observables con modelos pequeños.

### 6.1. Cronograma de trabajo

1. Relevamiento de la literatura: 2 semana.  
2. Implementación y validación del sistema de juego óptimo y banco de pruebas ; y  definición del proceso de entrenamiento y evaluación: 1 semana.  
3. Experimentos de correlación de errores: 1 semana.  
4. Experimentos de selección y temperatura: 1 semana.  
5. Descomposición entre posiciones vistas y no vistas: 1 semana.  
6. Experimentos de composición con soporte disjunto: 2 semanas.  
7. Análisis de sensibilidad y consolidación de resultados: 3 semanas.  
8. Redacción del marco teórico y del informe final: 3 semanas.  
9. Revisión y correcciones: 2 semanas.

La duración total estimada es de 16 semanas, aproximadamente cuatro meses.

## Referencias

\[1\] E. Zhang, V. Zhu, N. Saphra, A. Kleiman, B. L. Edelman, M. Tambe, S. M. Kakade, E. Malach. *Transcendence: Generative Models Can Outperform The Experts That Train Them*. NeurIPS, 2024\. arXiv:2406.11741.

\[2\] N. Abreu, E. Zhang, E. Malach, N. Saphra. *A Taxonomy of Transcendence*. COLM, 2025\. arXiv:2508.17669.

\[3\] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, I. Polosukhin. *Attention Is All You Need*. NeurIPS, 2017\.

\[4\] L. Breiman. *Random Forests*. Machine Learning, 45:5–32, 2001\.

\[5\] L. S. Marcolino, A. X. Jiang, M. Tambe. *Multi-agent Team Formation: Diversity Beats Strength?* IJCAI, 2013\.

\[6\] D. Rolnick, A. Veit, S. Belongie, N. Shavit. *Deep Learning is Robust to Massive Label Noise*. arXiv:1705.10694, 2017\.

\[7\] D. Arpit, S. Jastrzębski, N. Ballas, D. Krueger, E. Bengio, M. S. Kanwal, T. Maharaj, A. Fischer, A. Courville, Y. Bengio, S. Lacoste-Julien. *A Closer Look at Memorization in Deep Networks*. ICML, 2017\.

\[8\] R. A. Jacobs, M. I. Jordan, S. J. Nowlan, G. E. Hinton. *Adaptive Mixtures of Local Experts*. Neural Computation, 3(1):79–87, 1991\.

\[9\] W. Fedus, B. Zoph, N. Shazeer. *Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity*. Journal of Machine Learning Research, 23(120):1–39, 2022\.

\[10\] S. Gururangan, M. Li, M. Lewis, W. Shi, T. Althoff, N. A. Smith, L. Zettlemoyer. *Scaling Expert Language Models with Unsupervised Domain Discovery*. arXiv:2303.14177, 2023\.

\[11\] O. Press, M. Zhang, S. Min, L. Schmidt, N. A. Smith, M. Lewis. *Measuring and Narrowing the Compositionality Gap in Language Models*. Findings of EMNLP, 2023\. arXiv:2210.03350.

\[12\] S. Yang, E. Gribovskaya, N. Kassner, M. Geva, S. Riedel. *Do Large Language Models Latently Perform Multi-Hop Reasoning?* ACL, 2024\. arXiv:2402.16837.

\[13\] S. Toshniwal, S. Wiseman, K. Livescu, K. Gimpel. *Chess as a Testbed for Language Model State Tracking*. AAAI, 2022\.

\[14\] A. Karvonen. *Emergent World Models and Latent Variable Estimation in Chess-Playing Language Models*. arXiv:2403.15498, 2024\.

\[15\] A. Mészáros, P. Reizinger, F. Huszár. *Out-of-distribution Tests Reveal Compositionality in Chess Transformers*. arXiv:2510.20783, 2025\.

\[16\] E. Zermelo. Über eine Anwendung der Mengenlehre auf die Theorie des Schachspiels. Proceedings of the Fifth International Congress of Mathematicians, vol. 2, pp. 501–504. Cambridge University Press, 1913\.

\[17\] L. V. Allis. Searching for Solutions in Games and Artificial Intelligence. Tesis doctoral, Rijksuniversiteit Limburg, Maastricht, 1994\.

\[18\] V. Allis. *A Knowledge-Based Approach of Connect-Four*. Tesis de maestría, Vrije Universiteit Amsterdam, 1988\.

\[19\] P. Pons. *Connect 4 Game, Solver*. [http://connect4.gamesolver.org](http://connect4.gamesolver.org), 2019\.
