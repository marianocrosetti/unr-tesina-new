**Asunto:** Propuesta de tesina: cuándo un modelo imitador supera a sus expertos, medido en un juego resuelto

Hola [nombre],

Te escribo para proponerte un cambio de tema para la tesina, con un trabajo preliminar hecho que te resume abajo.

**Por qué el giro.** Lo que venía haciendo (extracción y verificación de firmas en telegramas electorales) es un trabajo de aplicación: construir el dataset, calibrar el pipeline, adaptar el modelo a cada cambio de formato. Aprendí mucho de ingeniería con eso, pero me quedó la sensación de que la tesina debería mostrar que sé hacer *research*: plantear una pregunta, diseñar un experimento que la aísle, y sacar una conclusión que se sostenga. Con datos reales y un pipeline grande eso es difícil, porque cada resultado tiene diez explicaciones posibles. Con un dataset sintético o académico, donde controlo todas las variables, se pueden hacer experimentos chicos, limpios y reproducibles. Sigo queriendo hacer algo de machine learning, pero de ese tipo.

**Lo que leí.** Dos papers recientes del mismo grupo (Harvard):

- Zhang et al. 2024, *Transcendence: Generative Models Can Outperform The Experts That Train Them* (NeurIPS). Entrenan un transformer a imitar partidas de ajedrez de jugadores de rating ≤ 1000 y, muestreado a temperatura baja, el modelo juega a ~1500. Lo explican con un teorema: el imitador aprende la mezcla de los expertos, y elegir la jugada más probable equivale a un voto por mayoría que cancela los errores si estos no coinciden.
- Abreu et al. 2025, *A Taxonomy of Transcendence* (COLM). Organizan el fenómeno en tres modos (denoising, selection, generalization) y lo testean en un grafo de conocimiento sintético.

Las dos teorías describen el argmax de la mezcla *verdadera*. Ninguna dice qué pasa con un modelo finito que la estima a partir de datos finitos, y con datos humanos no se puede manipular la estructura de los errores para probar que la diversidad es la causa. Zhang además nombra su propia brecha: su teorema de expertos complementarios supone que cada experto está definido en todo el espacio de estados, cosa "imposible después de la jugada 15".

**Lo que se me ocurrió.** Repetir el experimento en un dominio donde todo es exacto: Connect 4. El juego está resuelto, así que un solver da el resultado exacto de cada jugada en cada posición. Eso permite (a) expertos sintéticos a los que les inyecto errores con la estructura que quiera (qué fracción es compartida, si son aprendibles o no, en qué región del juego), (b) un imitador chico (transformer de 6M parámetros que solo ve la secuencia de jugadas) y (c) evaluación exacta desde los logits, sin ratings ni motores heurísticos. Todo corre en una laptop más unas horas de GPU alquilada.

**Lo que muestran los experimentos preliminares** (tres semillas por condición, desvíos ≤ 0.005):

1. Las dos teorías se cumplen en signo. La ganancia por baja temperatura cae linealmente con la fracción de errores compartidos, a igual cantidad de errores. El umbral de *selection* predicho por el Teorema 2 (α* = 1/3) aparece donde tiene que aparecer. Esto valida el testbed.
2. La ganancia vive en las posiciones que se repiten en el entrenamiento. Ahí el voto llega al techo teórico desde 20 mil partidas; en posiciones nuevas el modelo es peor que el experto hasta que hay 4× más datos. Un voto por posición necesita votos por posición.
3. Un error compartido por todos los expertos sobrevive a la baja temperatura solo si es representable como función del estado. Una regla simple se reproduce a tres decimales; un error pseudoaleatorio se generaliza hacia afuera en posiciones nuevas. Es un matiz que la taxonomía no hace.
4. Composición con soporte disjunto (la brecha de Zhang): una familia de expertos que solo muestra aperturas y otra que solo muestra finales tras aperturas malas. El imitador juega finales tras aperturas buenas, que nunca vio, con una penalidad ≤ 0.03, insensible a tamaño de modelo, datos y profundidad. Y gana ~70 % de sus partidas como primer jugador contra un oponente perfecto, algo que ninguna de las dos poblaciones de expertos puede hacer.
5. Entrenar más allá de la memorización destruye la ganancia; el paper de ajedrez no lo ve porque hace una sola pasada sobre mil millones de partidas.

Soy consciente de que es un trabajo chico y de que varios de estos resultados son los que uno esperaría en retrospectiva. El valor que le veo es que están medidos con ground truth exacto en los huecos que los dos papers dejaron abiertos, y que el punto 4 responde una pregunta sobre la que había desacuerdo genuino en la literatura.

**Lo que faltaría para cerrarlo:** evaluar en el mejor checkpoint en vez del final, más semillas en el estudio de escala, un enunciado formal de muestra finita para el Teorema 2, y el marco teórico escrito en forma de tesina. Tengo un borrador de paper de 10 páginas, diapositivas, y el código con todas las corridas versionado; te los adjunto.

[Opcional: Para las corridas y el análisis usé un asistente de IA de forma intensiva; las decisiones de diseño y la interpretación son mías. Lo menciono porque me parece relevante para la evaluación del trabajo.]

¿Te parece que con esto se puede armar una tesina? Si sí, me gustaría charlar cómo encuadrarla y qué le agregarías. Si te parece que el tema es flojo o que el giro no conviene, también prefiero saberlo ahora.

Gracias,
Mariano
