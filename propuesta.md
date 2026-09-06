

Hola [nombre],

Me gustaría

Mi idea sería agarrar o bien un dataset académico o bien un dataset sintético y hacer un trabajo acotado (pero metodológicamente correcto), formulando hipótesis a testear simples (pero claras), y mostrar el proceso de diseñar experimentos que aislen y controlen variables, presentar resultados y conclusiones claras.

Por ejemplo esta saga, donde el primero es el famoso papper que entrenan un transformer con jugadas de ajedrez de rating ELO ≤ 1000 y el modelo termina jugando con ELO ~ 1500. A este fenómeno donde "el modelo entrenado juega mejor que los datos" lo denominaron "trascendencia" (en mi opinión, un nombre un poco grandilocuente para algo que probablemente sea más un efecto simplemente de denoising). Luego hicieron un segundo papper estudiando el fenómeno en un grafo de conocimiento sintético.

Mi propuesta sería trabajar con partidas sintéticas en una juego mucho más simple (el "cuatro en linea") y probar propiedades sobre la denominada "trascendencia". Las ventajas de la alternativa que planteo son:
- El juego está resuelto. Puedo usar el solver exacto.
- Puedo manipular la estructura de los errores: qué fracción del error es "compartida" entre las pertidas de entrenamiento, hacer que cierta proporción de los expertos fallen en determinadas zonas del tablero ("dominios de expertise"), jugar con errores representables (como jugar en los bordes) vs aleatorios (dificiles de representar y aprender), etc.
- La evaluación es exacta (vs el solver exacto): en el papper del ajedrez usaron la evaluación de Stockfish.

Mis resultados preliminares muestran algunas cosas interesantes:

Es un trabajo chico y varios de los resultados son los que uno esperaría en retrospectiva. Por otro lado son huecos auténticos que tenían los pappers originales.

Referencias:
- Zhang et al. 2024, Transcendence: Generative Models Can Outperform The Experts That Train Them* (NeurIPS)
- Abreu et al. 2025, A Taxonomy of Transcendence (COLM). Segunda versión


========== ZONA IA debajo de esta linea ==========

Te escribo para proponerte un cambio de tema para la , con un trabajo preliminar hecho que te resume abajo.

**Por qué el giro.** Lo que venía haciendo (extracción y verificación de firmas en telegramas electorales) es un trabajo de aplicación: construir el dataset, calibrar el pipeline, adaptar el modelo a cada cambio de formato. Aprendí mucho de ingeniería con eso, pero me quedó la sensación de que la tesina debería mostrar que sé hacer *research*: plantear una pregunta, diseñar un experimento que la aísle, y sacar una conclusión que se sostenga. Con datos reales y un pipeline grande eso es difícil, porque cada resultado tiene diez explicaciones posibles. Con un dataset sintético o académico, donde controlo todas las variables, se pueden hacer experimentos chicos, limpios y reproducibles. Sigo queriendo hacer algo de machine learning, pero de ese tipo.

**Lo que leí.** Dos papers recientes del mismo grupo (Harvard):

- Zhang et al. 2024, *Transcendence: Generative Models Can Outperform The Experts That Train Them* (NeurIPS). Entrenan un transformer a imitar partidas de ajedrez de jugadores de rating ≤ 1000 y, muestreado a temperatura baja, el modelo juega a ~1500. Lo explican con un teorema: el imitador aprende la mezcla de los expertos, y elegir la jugada más probable equivale a un voto por mayoría que cancela los errores si estos no coinciden.
- Abreu et al. 2025, *A Taxonomy of Transcendence* (COLM). Organizan el fenómeno en tres modos (denoising, selection, generalization) y lo testean en un grafo de conocimiento sintético.

Las dos teorías describen el argmax de la mezcla *verdadera*. Ninguna dice qué pasa con un modelo finito que la estima a partir de datos finitos, y con datos humanos no se puede manipular la estructura de los errores para probar que la diversidad es la causa. Zhang además nombra su propia brecha: su teorema de expertos complementarios supone que cada experto está definido en todo el espacio de estados, cosa "imposible después de la jugada 15".

**Lo que se me ocurrió.** Repetir el experimento en un dominio donde todo es exacto: Connect 4. El juego está resuelto, así que un solver da el resultado exacto de cada jugada en cada posición. Eso permite (a) expertos sintéticos a los que les inyecto errores con la estructura que quiera (qué fracción es compartida, si son aprendibles o no, en qué región del juego), (b) un imitador chico (transformer de 6M parámetros que solo ve la secuencia de jugadas) y (c) evaluación exacta desde los logits, sin ratings ni motores heurísticos. Todo corre en una laptop más unas horas de GPU alquilada.

**Cómo se hace un experimento.** Siempre igual: programo expertos que consultan el solver y juegan perfecto salvo donde les inyecto el error que quiero estudiar; los hago jugar 80 mil partidas entre sí y guardo solo las secuencias de columnas; entreno un transformer chico (6M de parámetros) a predecir la siguiente columna, sin que vea el tablero ni el resultado; y lo evalúo en 60 mil posiciones nuevas leyendo su distribución sobre las 7 columnas y comparando, con el solver, contra lo que haría el experto en las mismas posiciones. Tres semillas por condición. Generar un dataset tarda 20 minutos en la laptop; entrenar, 2 minutos en una GPU alquilada. Todo costó unos 17 dólares de cómputo. Lo que cambia entre experimentos es cómo se equivocan los expertos:

**Hallazgo 1: la diversidad de errores es la causa, y el efecto es lineal.** Experimento: fijo la tasa de error de los expertos (se equivocan en el 15 % de las posiciones donde es posible equivocarse) y varío qué fracción π de esos errores es *compartida*: en las posiciones compartidas todos los expertos juegan la misma columna equivocada; en las demás, cada uno se equivoca por su cuenta. Cinco valores de π entre 0 y 1. Resultado: la ganancia del modelo a temperatura baja sobre el experto cae en línea recta con π (+0.040, +0.027, +0.015, +0.003, −0.017) y cambia de signo donde el Teorema 2 dice que debe. Con π = 0 el modelo elimina el 30 % de los errores del experto; con π = 1, ninguno. Misma cantidad de errores en los cinco casos: lo que importa es si coinciden.

**Hallazgo 2: el ruteo a la expertise tiene un umbral, y está donde la teoría lo predice.** Experimento: cuatro expertos, cada uno perfecto en una región del espacio de posiciones y equivocado *igual que los otros tres* fuera de ella (acá el voto no puede ayudar). Un parámetro α controla cuánto genera cada experto datos dentro de su región. El Teorema 2 predice que la temperatura baja ayuda si y solo si α > 1/3. Resultado: ganancia −0.105 y −0.040 con α = 0 y 0.2; +0.126, +0.169, +0.169 con α = 0.45, 0.7 y 1. El flip cae donde tenía que caer en las tres semillas. Debajo del umbral bajar la temperatura *empeora* al modelo. Esto es más una validación del testbed que un descubrimiento.

**Hallazgo 3: la ganancia vive en las posiciones que se repiten.** Experimento: tomo el modelo del hallazgo 1 con π = 0 y separo las 60 mil posiciones de test según si ese tablero exacto aparece o no en las partidas de entrenamiento (la apertura se repite casi siempre; el final casi nunca). Repito con 20 mil, 80 mil y 320 mil partidas. Resultado: en las posiciones vistas el modelo llega al techo teórico del voto desde 20 mil partidas (+0.09); en las no vistas es peor que el experto con 20 mil (−0.09), igual con 80 mil (−0.006) y mejor recién con 320 mil (+0.03). La ganancia total es el promedio ponderado de las dos. Un voto por posición necesita votos por posición; la generalización a posiciones nuevas recién aporta con muchos datos.

**Hallazgo 4: un error compartido sobrevive solo si el modelo puede representarlo.** Experimento: dos tipos de error compartido por todos los expertos. Uno definido por un hash de la posición (nada en el tablero lo predice); otro definido por una regla simple (cada tres jugadas, todos juegan la columna de más a la izquierda). Resultado: el error por hash se reproduce en la apertura (posiciones vistas, acierto 0.6 %) pero en posiciones nuevas el modelo juega bien el 41 al 56 % de las veces, porque no tiene forma de saber que esa posición era "sesgada" y hace lo que hace en posiciones parecidas. La regla se reproduce a tres decimales en todas las fases, con cualquier cantidad de datos. La condición del Teorema 2 no es "error compartido" sino "compartido y representable". Control adicional: expertos que nunca abren al centro; el modelo tampoco lo hace jamás. No hay descubrimiento.

**Hallazgo 5: compone habilidades de expertos que nunca aparecen en las mismas posiciones.** Es la brecha que Zhang nombra en su paper. Experimento: una familia A juega aperturas perfectas y su partida se corta en la jugada 8 (nunca muestra un final); una familia B abre solo por las columnas de los bordes y juega el final perfecto. Ninguna partida muestra un final después de una apertura buena. Resultado: el modelo juega finales tras aperturas buenas con acierto 0.925 (el control que sí los vio: 0.950), y la penalidad no cambia con el tamaño del modelo, la cantidad de datos ni la profundidad del corte. Controles: entrenado solo con B pierde todas las partidas contra un jugador perfecto (abre mal); solo con A no sabe jugar finales; con A y B gana el 70 % de sus partidas como primer jugador contra un jugador perfecto, cosa que ninguna de las dos familias puede hacer.

**Hallazgo 6 (menor): entrenar de más destruye la ganancia.** Experimento: mismos 80 mil partidas, 10 vs 42 vs 167 epochs. Resultado: el acierto a temperatura baja baja de 0.891 a 0.837, por debajo del experto (0.845), mientras la loss de validación explota. El modelo memoriza las partidas con sus errores y el argmax deja de ser un voto. Con 4× datos la ganancia vuelve y crece. Es la dinámica conocida de memorización de etiquetas ruidosas; lo relevante es que el paper de ajedrez no lo ve porque hace una sola pasada sobre mil millones de partidas.

Soy consciente de que es un trabajo chico y de que varios de estos resultados son los que uno esperaría en retrospectiva. El valor que le veo es que están medidos con ground truth exacto en los huecos que los dos papers dejaron abiertos, y que el punto 4 responde una pregunta sobre la que había desacuerdo genuino en la literatura.

**Lo que faltaría para cerrarlo:** evaluar en el mejor checkpoint en vez del final, más semillas en el estudio de escala, un enunciado formal de muestra finita para el Teorema 2, y el marco teórico escrito en forma de tesina. Tengo un borrador de paper de 10 páginas, diapositivas, y el código con todas las corridas versionado; te los adjunto.

[Opcional: Para las corridas y el análisis usé un asistente de IA de forma intensiva; las decisiones de diseño y la interpretación son mías. Lo menciono porque me parece relevante para la evaluación del trabajo.]
