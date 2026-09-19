## Título

"Propiedades de la trascendencia en modelos generativos entrenados por imitación: un estudio controlado en un dominio sintético de decisión secuencial con verificación exacta."

## Motivación y objetivos

El trabajo reciente (2024) de Zhang et al. \[1\] muestra un comportamiento antiintuitivo: un modelo entrenado con partidas de ajedrez de jugadores de rating \<= 1000[^1] juega con \~1500[^2].

El trabajo denomina a este fenómeno *“transcendencia”*.

En una segunda publicación \[2\], Abreu et al. analizan la *trascendencia* de un dominio sintético de grafos de conocimiento.

Nuestro objetivo es arrojar luz sobre aspectos del fenómeno, no cubiertos por la literatura. Particularmente en lo relativo a:

- Cuantificar cómo la correlación de los errores de los expertos afecta al fenómeno.  
- Testear el impacto de la composición entre expertos con habilidades disjuntas (\[2\] obtiene resultados débiles al respecto, y la literatura vecina predice resultados opuestos: colapso fuera del soporte de cada demostrador \[5, 6\] o transferencia composicional \[4\]).  
- Medir la diferencia en la magnitud de la *trascendencia* entre posiciones vistas o no durante el entrenamiento.[^3]  
- Diferenciarnos de \[2\] (que también analiza propiedades de la trascendencia en dominios sintéticos) mediante un "dominio con estado secuencial" (en el que una decisión afecta a las decisiones futuras, como en el ajedrez de \[1\]). En contraposición a un "dominio estático" como un grafo de conocimiento sintético utilizado en \[2\].

Nuestro dominio será:

- Un dominio sintético que podamos controlar (como el de \[2\]).  
- Un juego de información perfecta (análisis más fiel a \[1\], donde se presenta la idea original del concepto de *trascendencia*).  
- Pero a diferencia de \[1\], proponemos elegir un juego resuelto para poder contar con un verificador exacto.[^4]

## Fundamentos y estado del conocimiento sobre el tema

El objeto de estudio son los modelos generativos[^5] entrenados por el objetivo estándar de imitación: minimizar la cross-entropy respecto de los datos que los entrenan.

La teoría nos dice que en el límite[^6] aprenden la distribución de los datos.

Tal como se mencionó, \[1\] muestra que un modelo entrenado a imitar a una población de "expertos" puede rendir mejor que el mejor experto individual de esa población.

Concretamente, entrenan un transformer con partidas de ajedrez de jugadores de rating \<= 1000 y el modelo producido puede jugar[^7] con \~1500.

Llaman a este fenómeno *trascendencia*, y lo atribuyen a que el modelo entrenado cancela errores no correlacionados entre los expertos.

Abreu et al. \[2\] (testeando sobre un dominio sintético de grafos de conocimiento) analizan tres mecanismos propuestos de la *trascendencia*:[^8]

- Denoising por voto.  
- Selección de la fuente competente.  
- Composición de conocimiento disjunto entre fuentes.

### Áreas de la literatura adyacentes

El fenómeno de trascendencia se sitúa en la intersección de varias líneas de trabajo conocidas:

- El aprendizaje por imitación (behavioral cloning) y sus límites teóricos \[9, 10\].  
- Los métodos de ensamble (bagging, votación por mayoría) \[11\].  
- La literatura de la "sabiduría de las masas" \[12\].  
- La discusión sobre si los modelos de lenguaje entrenados sobre datos con errores o sesgos sistemáticos pueden filtrar ese ruido durante el entrenamiento o el muestreo \[13\].  
- La dinámica de memorización: se sabe que un modelo entrenado por un número suficiente de pasadas sobre un conjunto de datos finito eventualmente memoriza particularidades de la muestra (incluido el ruido) en lugar de la distribución subyacente \[3\].

## Metodología y plan de trabajo

Se propone realizar entregas semanales con copia al director (Dante Zanarini) y al codirector (Pablo Granitto).

&nbsp;

El director controlará la evolución general de los avances y supervisará la redacción final del informe.

&nbsp;

El codirector \-desde su expertise en aprendizaje automático y particularmente en aprendizaje profundo- supervisará a nivel conceptual que las hipótesis tengan sentido y estén a la altura de una tesina, que los experimentos planteados sean metodológicamente correctos, que sus especificaciones no omitan detalles relevantes y que los resultados sean expuestos de una forma coherente y completa.

&nbsp;

El trabajo es fundamentalmente experimental. Experimentos preliminares ya muestran que la dirección expuesta es prometedora (con resultados positivos).

### Programa tentativo de trabajo

1. El relevamiento de la literatura de trascendencia (y su marco circundante) ya se ha realizado para la presentación de la presente propuesta. **1 semana**  
2. Se comenzará a trabajar en el primer experimento hasta tener una formulación e implementación satisfactorias. Esto implicará resolver cuestiones comunes a todos los experimentos, como elegir un dominio de verificación exacta, implementar los generadores sintéticos, implementar el pipeline de entrenamiento y evaluación, etc. **1 semana**  
3. Se trabajará en una presentación de resultados satisfactoria de este primer experimento. Esto se hará antes de seguir haciendo experimentos: tener el punta a punta para uno ayudará a iterar con dirección en los demás. **1 semana**  
4. Se definirán conceptualmente los experimentos restantes. **1 semana**  
5. Se trabajará en tener el mismo punta a punta en cada uno de ellos. **1 semana**  
6. Análisis de sensibilidad y ablaciones sobre los resultados principales; reproducir resultados variando parámetros que suponemos no debieran afectar los resultados: tamaño/arquitectura del modelo, cantidad/representación de los datos. **1 semana**  
7. Para este punto, ya tendremos la presentación completa de resultados. Resta unirlos de forma coherente y formular conclusiones. **1 semana**  
8. Recién ahora, tras haber superado la parte más arriesgada del trabajo, comenzaremos a redactar el Marco Teórico. Se confeccionará un índice de secciones y subsecciones con una explicación breve de cada una: no más de 5 oraciones. **1 semana**  
9. Se proseguirá a la redacción completa del Marco Teórico. Se unirá todo de forma coherente en el informe final. **2 semanas**  
10. Se iterará en correcciones hasta que esté puesto a punto para la presentación y corrección. **2 semanas**

## REFERENCIAS

\[1\] E. Zhang, V. Zhu, N. Saphra, A. Kleiman, B. L. Edelman, M. Tambe, S. M. Kakade, E. Malach. *Transcendence: Generative Models Can Outperform The Experts That Train Them*. NeurIPS, 2024\. arXiv:2406.11741.

&nbsp;

\[2\] N. Abreu, E. Zhang, E. Malach, N. Saphra. *A Taxonomy of Transcendence*. COLM, 2025\. arXiv:2508.17669.

&nbsp;

\[3\] D. Arpit, S. Jastrzębski, N. Ballas, D. Krueger, E. Bengio, M. S. Kanwal, T. Maharaj, A. Fischer, A. Courville, Y. Bengio, S. Lacoste-Julien. *A Closer Look at Memorization in Deep Networks*. ICML, 2017\.

&nbsp;

\[4\] A. Mészáros, P. Reizinger, F. Huszár. *Out-of-distribution Tests Reveal Compositionality in Chess Transformers*. arXiv:2510.20783, 2025\.

&nbsp;

\[5\] K. Paster, S. McIlraith, J. Ba. *You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments*. NeurIPS, 2022\.

&nbsp;

\[6\] D. Brandfonbrener, A. Bietti, J. Buckman, R. Laroche, J. Bruna. *When Does Return-Conditioned Supervised Learning Work for Offline Reinforcement Learning?* NeurIPS, 2022\.

&nbsp;

\[7\] V. Allis. *A Knowledge-Based Approach of Connect-Four*. Tesis de maestría, Vrije Universiteit Amsterdam, 1988\.

&nbsp;

\[8\] P. Pons. *Connect 4 Game Solver*. [http://connect4.gamesolver.org](http://connect4.gamesolver.org), 2019\.

&nbsp;

\[9\] S. Ross, D. Bagnell. *Efficient Reductions for Imitation Learning*. AISTATS, 2010\.

&nbsp;

\[10\] S. Ross, G. Gordon, D. Bagnell. *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS, 2011\.

&nbsp;

\[11\] L. Breiman. *Bagging Predictors*. Machine Learning, 24:123–140, 1996\.

&nbsp;

\[12\] L. S. Marcolino, A. X. Jiang, M. Tambe. *Multi-agent Team Formation: Diversity Beats Strength?* IJCAI, 2013\.

&nbsp;

\[13\] D. Rolnick, A. Veit, S. Belongie, N. Shavit. *Deep Learning is Robust to Massive Label Noise*. arXiv:1705.10694, 2017\.

&nbsp;

\[14\] A. Karvonen. *Emergent World Models and Latent Variable Estimation in Chess-Playing Language Models*. arXiv:2403.15498, 2024\.

&nbsp;

\[15\] S. Toshniwal, S. Wiseman, K. Livescu, K. Gimpel. *Chess as a Testbed for Language Model State Tracking*. AAAI, 2022\.

&nbsp;

\[16\] L. Berglund, M. Tong, M. Kaufmann, M. Balesni, A. C. Stickland, T. Korbak, O. Evans. *The Reversal Curse: LLMs Trained on "A is B" Fail to Learn "B is A"*. arXiv:2309.12288, 2023\.

&nbsp;

\[17\] Z. Allen-Zhu, Y. Li. *Physics of Language Models: Part 3.2, Knowledge Manipulation*. arXiv:2309.14402, 2023\.

&nbsp;

\[18\] K. Krestnikov. *Truth as a Compression Artifact in Language Model Training*. arXiv:2603.11749, 2026\.

&nbsp;

&nbsp;

[^1]: \[1\] utiliza rating Glicko-2 de lichess (similar a Elo). Como el ajedrez no es un juego resuelto, Zhang et al. \[1\] utilizan Stockfish como:

    evaluador (con el que calcula la "recompensa por estado")

    oponente (partidas de las que se estima el rating Glicko-2)

    &nbsp;

[^2]: El mismo trabajo reporta que el modelo entrenado con partidas de jugadores de hasta 1500 *no trasciende*. Le atribuye la diferencia a que ese conjunto de datos tiene menos diversidad de jugadas. Como son datos de partidas reales, no se puede intervenir sobre la estructura de correlación de los errores. Sino que mide la diversidad como la entropía media de la distribución de jugadas en las posiciones frecuentes y establecer una correlación: para jugadores de rating 1500 esta medida de diversidad es más baja que para los de rating 1000\.

    &nbsp;

[^3]: Tal como explicamos en la sección siguiente, en \[2\] tratan de establecer una taxonomía de las causas de la trascendencia. Los experimentos que evalúan denoising y selección entrenan con expertos ruidosos pero toda la evaluación es de casos vistos en entrenamiento. En cambio, los experimentos de generalization evalúan casos no vistos en entrenamiento pero fijan la probabilidad de error de los expertos en cero. No se plantea una comparación que muestre cómo se reparte la magnitud de la trascendencia entre posiciones vistas y no vistas en un contexto donde hay ruido, como un juego.

[^4]: Sondeando la posibilidad de este trabajo hemos basado los experimentos preliminares en "cuatro en línea" \[7, 8\], lo mencionamos aquí aunque no tiene por qué ser este juego el elegido por el trabajo. Incluso dominios no lúdicos con verificación exacta (por ejemplo, ciertos problemas combinatorios chicos) podrían servir igual de bien al mismo propósito, y la elección final dependerá de un balance entre expresividad del dominio (que admita construir las condiciones experimentales de interés) y practicidad de implementación.

    &nbsp;

[^5]: Particularmente trabajaremos con modelos autorregresivos. Y más específicamente con arquitecturas transformers como la literatura en la que nos basamos. También, al igual que \[1\], el imitador recibe únicamente la secuencia de jugadas, nunca el tablero, ni la identidad del experto, ni señal de recompensa. Debe construir internamente una representación del estado a partir de la secuencia \[14, 15\].

    &nbsp;

[^6]: "En el límite" quiere decir: si tuviéramos infinitos datos de entrenamiento y un modelo con capacidad infinita para representar cualquier función.

    &nbsp;

[^7]: La expresión *"puede jugar"* ha sido elegida de forma deliberada: en el mecanismo de denoising, \[1\] prueba que la trascendencia es imposible a temperatura 1 y requiere muestreo a baja temperatura (argmax). Para el mecanismo de selección, en cambio, \[2\] da una condición bajo la cual la trascendencia ocurre ya a temperatura 1\.

    &nbsp;

[^8]: Los mecanismos tal como los listamos son una traducción literal de la terminología que crean los autores en Abreu et al. \[2\].