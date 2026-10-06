 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Fable 5.1 · Claude Team
 ▝▝   ▝▝   ~/Desktop/personal-hq/projects/unr-tesina-new


❯ /clear                                                                        

❯ /model                                                                        
  ⎿  Set model to Fable 5.1 and saved as your default for new sessions

❯ Quiero que trabajemos en diseñar e implementar el experimento1                
  El objetivo es completar ./experimento1/experimento1-v1.md con el diseño,     
  detalles de implementación y resultados del experimento1 tal y como lo vamos  
  a incluir en la tesina                                                        
                                                                                
  - Leer la propuesta v1 para tener más contexto.                               
  - Explorar exploracion-pre-propuesta para entender los experimentos           
  planteados. Sobre todo transcendencia_slides.html, el papper y los .md para   
  entender lo hecho. El resto de los archivos (codigo, logs, resultados, runs,  
  checkpoints) los ignoraría por ahora porque te van a introducir mucho ruido   
  en el contexto                                                                
  - Leer el ./experimento1/CURRENT_STATUS.md para ver comentarios de Pablo que  
  pueden ser relevantes a la hora de diseñar / implementar los experimentos.    
  - Leer los pappers [1] y [2] del directorio referencias para tomar como       
  ejemplo cómo se plantea un experimento en la academia y qué detalles es       
  importante incluir (modelo, modos de entrenamiento, training set, evaluación, 
  etc). De todas maneras, en cuanto al formato, como primer borrador quizás     
  escribimos algo mucho más fácil de parsear que el formato académico/papper (y 
  usamos enumeraciones, y un estilo más parecido a propuesta v1)                
                                                                                
  Dame algo por acá primero, luego vamos a iterar y escribir entre los dos el   
  .md                                                                           

⏺ Voy a leer la propuesta, la exploración pre-propuesta, el CURRENT_STATUS de
  experimento1 y los dos papers antes de proponerte un diseño.

  Read 15 files, listed 2 directories, ran 2 shell commands (ctrl+o to expand)

⏺ Ya leí todo: la propuesta v1, los .md y slides de la exploración, el paper
  sintético, el CURRENT_STATUS con la devolución de Pablo, y los dos papers
  completos. Abajo va mi propuesta de diseño para el experimento 1. No escribí
  nada en el .md todavía.

  Qué es el experimento 1 y qué predice

  Definición. Experimento 1 = objetivo 1 de la propuesta: cuantificar cómo la
  correlación de los errores entre expertos afecta la trascendencia por
  denoising a baja temperatura. Es el que Pablo comentó con la fórmula de
  varianza equicorrelacionada, y es el más riesgoso porque todos los demás
  reutilizan su pipeline.

  Mapeo de la fórmula de Pablo a nuestro dominio. Su identidad dice que al
  promediar n expertos con correlación ρ la varianza residual nunca baja de ρσ².
  En un espacio de acciones discreto el análogo es directo y conviene
  escribirlo así en la tesina:
  - La parte compartida del error pone masa β en la misma jugada errónea en
    todos los expertos. La mezcla hereda esa masa y el argmax no la elimina. Es
    el piso ρσ².
  - La parte independiente se reparte entre jugadas erróneas distintas. Al tomar
    el argmax desaparece, siempre que haya suficientes visitas al estado. Es el
    término (1−ρ)σ²/n.
  - Predicción cuantitativa antes de correr: acc(τ→0) ≈ 1 − β̂ y ganancia sobre
    el experto ≈ q̂, donde β̂ y q̂ son las tasas realizadas de error compartido e
    independiente sobre estados decidibles. A τ=1 no hay trascendencia para
    ningún valor, por la Proposición 1 de Zhang.

  Qué agregamos respecto de [1] y [2]. Zhang solo pudo correlacionar diversidad
  con entropía en datos humanos. Abreu varía la cantidad de expertos como proxy
  de descorrelación. Nosotros intervenimos la correlación directamente, a tasa
  de error fija, y la reportamos como correlación de Pearson medida entre los
  vectores de error de dos expertos sobre los mismos estados, que es exactamente
  lo que Pablo sugiere en la imagen 1.

  Diseño propuesto

  1. Dominio y verificador. Connect 4 estándar, solver de Pons en modo débil.
     Recompensa r ∈ {1, ½, 0} según la clase de resultado de la jugada. Un
     estado es "decidible" si tiene al menos dos clases de resultado entre sus
     jugadas legales. Solo ahí puede haber error. Son cerca de la mitad de los
     estados visitados, así que hay que definir todas las tasas sobre estados
     decidibles y reportar nominal y realizada. La exploración se tropezó con
     esto.
  2. Población de expertos. Cada partida la juegan ambos lados expertos
     muestreados de una misma población, como las partidas entre jugadores ≤1000
     de lichess. Dos parámetros: tasa total de error ρ_tot fija en todas las
     celdas, y fracción compartida π ∈ {0, 0.25, 0.5, 0.75, 1}. La tasa
     independiente q se calibra por celda para que la tasa total realizada quede
     constante. Así la única variable que cambia entre celdas es la estructura
     del error, no la cantidad.
  3. Decisión de diseño clave: el error compartido tiene que ser representable.
     En la exploración los "estados sesgados" se definían por un hash del
     tablero. Resultado: en estados nuevos el modelo generalizaba el error
     compartido hacia afuera y acertaba 0.41 a 0.56 donde la teoría predice 0.
     Eso mezcla dos efectos distintos, correlación y representabilidad, y hace
     que el punto π=1 no sea un control limpio. Propongo definir los estados
     sesgados por una regla simple de la secuencia, por ejemplo un conjunto de
     residuos del índice de jugada módulo 20 con frecuencia β, repartidos de
     forma pareja entre fases. La jugada errónea compartida también por regla
     simple, por ejemplo la columna legal más a la izquierda cuando no es
     óptima. La condición rule de la exploración mostró que esto se reproduce a
     tres decimales en toda fase. Dejo el hash como una única celda de contraste
     en π=1, que siembra el experimento de representabilidad más adelante.
  4. Datos. Por celda y semilla: 80k partidas de entrenamiento, alrededor de
     1.6M estados, y 3k partidas de test con semilla distinta, alrededor de 60k
     estados. Tokens: BOS, siete columnas, tres símbolos de resultado, PAD. El
     imitador ve solo la secuencia, nunca el tablero ni la identidad del
     experto, igual que el PGN de Zhang. La semilla varía dataset,
     inicialización y orden de batches.
  5. Imitador. Decoder tipo nanoGPT, 8 capas, 8 cabezas, ancho 256, 6.3M
     parámetros. AdamW, cosine schedule, batch 512, unos 10 epochs. Tabla
     completa de hiperparámetros al estilo del apéndice E de Zhang. Cambio
     obligatorio respecto de la exploración: evaluar el checkpoint de mejor val
     loss, no el final. La exploración mostró que pasar de 10 a 42 epochs con
     los mismos datos destruye la ganancia por memorización, así que el
     protocolo tiene que fijar early stopping y documentarlo.
  6. Evaluación. Dos distribuciones de test, porque la definición de
     trascendencia depende de p_test y los dos papers usan una distinta:
     - Estados visitados por los expertos: desde los logits, sin muestreo, para
       τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}. Métricas: E[r],
       probabilidad de jugada óptima, y ambas separadas en estados sesgados
       versus no sesgados para verificar el mecanismo estado por estado.
     - Juego propio: 300 partidas contra el bot experto y contra el jugador
       perfecto, colores alternados, cinco reintentos ante jugada ilegal, a τ→0
       y τ=1. Es el protocolo de Zhang.
     - Baselines analíticos: mejor experto, argmax de la mezcla como techo
       teórico, jugador perfecto, uniforme.
     - Reporte estratificado por fase: apertura, medio, final. Y etiqueta
       visto/no visto por tablero, que sale gratis de estas mismas corridas y
       alimenta el objetivo 3 sin entrenar nada más.
  7. Grilla y costo. Cinco valores de π por tres semillas a 80k son 15 corridas.
     Sumo un panel de 320k con una semilla para mostrar si la curva se acerca a
     la teoría con más datos, que es la objeción natural de Pablo cuando vea
     que capturamos un cuarto del techo.

  ┌──────────────────────┬──────────┬──────────────────┬────────────────────┐
  │        Panel         │ Corridas │  Generación de   │ Entrenamiento en   │
  │                      │          │      datos       │        4090        │
  ├──────────────────────┼──────────┼──────────────────┼────────────────────┤
  │ Principal, 80k, 3    │ 15       │ 5 h en 8 cores   │ 30 min             │
  │ semillas             │          │                  │                    │
  ├──────────────────────┼──────────┼──────────────────┼────────────────────┤
  │ Escala, 320k, 1      │ 5        │ 7 h en 8 cores   │ 40 min             │
  │ semilla              │          │                  │                    │
  ├──────────────────────┼──────────┼──────────────────┼────────────────────┤
  │ Contraste hash π=1   │ 3        │ 1 h              │ 6 min              │
  └──────────────────────┴──────────┴──────────────────┴────────────────────┘

  Costo total de GPU por debajo de 5 USD. El cuello de botella es la generación
  en CPU, que se hace de noche.

  8. Predicciones registradas antes de correr. La ganancia a τ→0 decrece
     monótonamente en π y en la correlación medida. La teoría predice signo
     positivo para todo π<1, pero la exploración vio el cruce por cero antes,
     cerca de π=0.75. Si se repite, es un hallazgo: el modelo finito alcanza el
     piso antes que la mezcla verdadera. En estados sesgados con regla, acierto
     ≈ 0 en toda fase, visto o no visto. En los no sesgados, acierto → 1 solo
     donde hay votos.

  Decisiones abiertas y riesgos

  Doy mi recomendación en cada una para que puedas decidir rápido:

  - Regla versus hash para el error compartido. Recomiendo regla como diseño
    principal y una celda hash de contraste. Sin esto el experimento 1 no aísla
    la correlación.
  - Fijar tasa de error o fijar E[r] del experto. Recomiendo fijar la tasa. El
    E[r] del experto va a variar un poco entre celdas porque el error compartido
    y el aleatorio cuestan distinto. Se reporta la ganancia relativa al experto
    de cada celda.
  - Eje "cantidad de expertos" de Pablo. En nuestra población los errores
    independientes se sortean en cada visita, así que n es efectivamente
    infinito. Si Pablo quiere ver el término 1/n hay que construir K expertos
    persistentes con errores fijos por estado. Recomiendo dejarlo como
    experimento 1b opcional y preguntarle antes de implementarlo.
  - Toy model gaussiano con ρ. Es la sugerencia literal de Pablo sobre el modelo
    de Zhang, cuesta una hora y da una figura puente entre teoría y Connect 4.
    Opcional, lo haría solo después de tener el principal.
  - Recompensa débil versus fuerte. Recomiendo mantener la clase de resultado.
    El score de jugadas hasta ganar queda como refinamiento.

  Riesgos que veo y que el diseño ya mitiga o debería mitigar: el régimen de
  entrenamiento decide el resultado, por eso early stopping fijo. La
  representabilidad confunde el control π=1, por eso regla. Las tasas nominales
  engañan, por eso todo sobre estados decidibles. Y el solver de Pons es AGPL y
  está vendored fuera de git, hay que documentar el build para reproducibilidad.

  Para el .md propongo este esqueleto, que sigue lo que incluyen [1] y [2] pero
  en enumeraciones: pregunta e hipótesis, marco teórico con el mapeo de la
  fórmula, dominio y verificador, expertos sintéticos, datos, imitador con tabla
  de hiperparámetros, evaluación, predicciones previas, grilla y costo,
  resultados, discusión y limitaciones, reproducibilidad. Si te cierra, el
  siguiente paso es que me digas qué decisiones tomás y arranco el .md con las
  secciones de diseño, dejando resultados como TODO hasta correr.

✻ Churned for 5m 42s · done Saturday 19 Sep at 6:03 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores entre expertos en Connect 4, y ya te propuse el diseño completo en el chat. Falta que decidas las opciones abiertas para que arranque el .md. (disable recaps in /config)

❯ El experimento que estamos definiendo sería esto o tiene algo distinto:       
  experimento1                                                                  
  El experimento que planeo hacer ahora como primero es agarrar el juego        
  propuesto Connect4 y entrenar un modelo en partidas sintéticas. En esas       
  partidas sintéticas son generadas por varios expertos. Esos expertos tienen   
  una probabilidad de equivocarse. Equivocarse es hacer una jugada perdedora.   
  Cuando se equivocan tienen P probabilidad de hacer un error compartido y      
  (1-P) un tipo de error que solo ellos hacen                                   
  Todavía estoy viendo un poco como definir un error compartido vs el que solo  
  ellos hacen pero tengo varias alternativas en mente                           
  La idea es variar P y ver como eso mejora la calidad de juego del modelo      
  entrenado (entendida como la accuracy en cada jugada jugando contra un        
  perfect player, accuracy es fácil de calcular porque sabemos que jugadas son  
  ganadoras y perdedoras )                                                      

⏺ Es el mismo experimento. Lo que propuse es tu descripción con las decisiones
  que vos dejás abiertas ya tomadas, más algunas precisiones. Hay una diferencia
  que es crítica y tres que son de definición.

  1. Crítica: el error compartido tiene que coincidir en ocurrencia, no solo en 
  tipo. Tu frase admite dos lecturas y solo una funciona:
  - Lectura A: cada experto tira su moneda de error, y si le sale error, con
    probabilidad P juega "la jugada sesgada" de ese estado. Acá dos expertos
    coinciden en el error solo con probabilidad ρ². La mezcla pone masa ρ·P en
    la jugada sesgada y 1−ρ en la óptima. Con ρ=0.3 el argmax sigue siendo
    óptimo para todo P, y la teoría predice trascendencia completa en todas las
    celdas. Variar P no mostraría nada.
  - Lectura B: existe un conjunto fijo de "estados sesgados", de medida P·ρ,
    donde todos los expertos juegan la misma jugada errónea. Ahí la mezcla pone
    masa 1 en el error y ningún voto lo saca. Esto es lo que hace que P tenga
    efecto, y es el equivalente exacto del término compartido ξ_shared de la
    fórmula de Pablo, que es una variable por estado común a todos.

  Mi diseño usa la lectura B. El error compartido es una propiedad del estado,
  no una moneda del experto.

  2. Definición de "equivocarse". Decís "hacer una jugada perdedora". La
  definición general es "jugada que empeora la clase de resultado respecto de la
  mejor disponible". Cubre tres casos: desde posición ganada, jugar tablas o
  perder. Desde tablas, jugar perdedora. Desde posición perdida, no hay error
  posible. Esto último importa: cerca de la mitad de los estados visitados no
  admiten error, así que la tasa de error hay que definirla sobre estados
  decidibles o la nominal te queda a la mitad de lo que creés.

  3. Qué es "un error que solo ellos hacen". Dos opciones, y en tu frase "varios
  expertos" sugiere la segunda:
  - Jugada errónea uniforme al azar, sorteada en cada visita. Es la Proposición
    3 de Zhang. La cantidad de expertos no importa, ya está implementada y
    validada. Es la que recomiendo para el experimento 1.
  - K expertos persistentes, cada uno con su propia jugada errónea fija por
    estado. Acá K sí importa y aparece el término 1/n de Pablo. Lo dejaría como
    experimento 1b si él lo pide.

  Para el error compartido recomiendo que sea representable, definido por una
  regla simple de la secuencia, por las razones que expliqué antes. Esa es la
  respuesta a tu "todavía estoy viendo cómo definirlo".

  4. Evaluación: accuracy contra el jugador perfecto tiene un problema. Un
  primer jugador perfecto gana siempre. Cuando el modelo juega segundo, todas
  sus posiciones están perdidas desde la jugada 1 y ningún movimiento cuenta
  como error. Cuando juega primero, tras su primer error la posición pasa a
  perdida y el resto tampoco cuenta. La métrica colapsa a "cuántas jugadas
  aguanta sin errar como primero". Por eso propongo como métrica principal la
  accuracy por estado desde los logits sobre los estados que visitan los
  expertos, donde la accuracy del experto en los mismos estados es analítica y
  la comparación define trascendencia. Las partidas contra el perfecto y contra
  el bot experto quedan como métrica secundaria de juego propio. Y hace falta el
  barrido de temperatura, que tu descripción no menciona: el fenómeno vive en
  la diferencia entre τ=1 y τ→0.

  Con esto, el experimento queda igual al tuyo en la pregunta y en la perilla P.
  Cambia cómo se construye el error compartido, cómo se cuenta un error, y en
  qué distribución de estados se mide.

✻ Worked for 1m 6s · done Saturday 19 Sep at 6:28 pm

❯ Tengo algunas dudas:                                                          
  - Que significa esto:                                                         
  la reportamos como correlación de Pearson medida entre los vectores de error  
  de dos expertos sobre los mismos estados, que es exactamente lo que Pablo     
  sugiere en la imagen 1.                                                       
  - Que significa "en modo débil" en "solver de Pons en modo débil"             
  - No entiendo que son las recompensas especificamente, podrías ampliar lo     
  siguiente:                                                                    
  Recompensa r ∈ {1, ½, 0} según la clase de resultado de la jugada.            
  - Que significa "estado decidible"? que puede dar dos resultados?             
    Me parece un poco confuso el termino elegido, es algo estándar de la        
  literatura de juegos? Si es así lo dejaría así                                
    A mí me confunde porque el termino decidibilidad ya tiene un significado en 
  la teoría de la computación.                                                  
  - No entiendo esto, ampliar                                                   
  las tasas sobre estados decidibles y reportar nominal y realizada. La         
  exploración se tropezó con esto.                                              
  - No entiendo esto:                                                           
  En la exploración los "estados sesgados" se definían por un hash del          
  tablero...                                                                    
  Creo que en la exploración hicimos algo de esto de los hashes y               
  representatibilidad pero como un experimento posterior (no el 1). Podrías     
  chequear el papper y las slides?                                              
  Me parece que el 1 era una propuesta de error compartido simple o no?         
  - Que es esto y en qué sumaría a las especificaciones del experimento         
  Grilla y costo. Cinco valores de π por tres semillas a 80k son 15 corridas.   
  Sumo un panel de 320k con una semilla para mostrar si la curva se acerca a la 
  teoría con más datos, que es la objeción natural de Pablo cuando vea que      
  capturamos un cuarto del tech                                                 
  - Que sería fijar E[r] del experto                                            
  - Qué sería Eje "cantidad de expertos" de Pablo.? Sería variar K tambien? (n  
  para la formulacion de Pablo)                                                 
  - Que sería Recompensa débil versus fuerte.                                   
  - Que significa el régimen de entrenamiento decide el resultado, por eso      
  early stopping fijo?                                                          
  - Que significa  Las tasas nominales engañan,                                 
  - Que significa Y el solver de Pons es AGPL y está vendored fuera de git, hay 
  que documentar el build para reproducibilidad.                                

  Ran 1 shell command (ctrl+o to expand)

⏺ Voy una por una. Sobre el hash chequeé el paper, el README y las slides, la
  respuesta está en el punto 6.

  1. Correlación de Pearson entre vectores de error. Tomás un conjunto fijo de
  estados de test. Para cada experto i y cada estado x anotás un 1 si el experto
  erra en x y un 0 si no. Eso da un vector binario por experto. La correlación
  de Pearson entre los vectores de dos expertos mide cuánto coinciden sus
  errores: 0 si son independientes, 1 si erran exactamente en los mismos
  estados. Es el ρ de la fórmula de Pablo, medido en vez de asumido. En la
  imagen 1 él escribe literalmente "usando algo como una correlación de Pearson
  entre los vectores de error de cada jugador sobre el mismo conjunto de
  posiciones". Nuestra perilla de diseño es P, pero el eje que Pablo entiende es
  ρ. Se puede calcular la relación entre ambos y reportar las dos.

  2. Solver de Pons en modo débil. El solver tiene dos modos. El fuerte devuelve
  un puntaje que dice quién gana y en cuántas jugadas. El débil devuelve solo
  la clase: gana, empata o pierde el que mueve. El débil es más rápido y alcanza
  para definir jugada óptima y error.

  3. Recompensa r ∈ {1, ½, 0}. Es la recompensa de una jugada, no de una
  partida. Estás en el estado x y jugás la columna y. La posición resultante
  tiene un resultado teórico con juego perfecto de ambos lados: ganás, empatás o
  perdés. Asignamos r = 1, ½, 0 respectivamente. Jugada óptima es la de mayor r
  entre las legales. Error es elegir una con r menor que ese máximo. La
  recompensa esperada de una política en x es la suma de r ponderada por la
  probabilidad que le da a cada columna. Zhang usa la probabilidad de ganar de
  Stockfish como recompensa; nosotros la tenemos exacta.

  4. "Estado decidible". Tenés razón, es un término mío y choca con
  computabilidad. No es estándar en juegos. Lo que quiero nombrar es un estado
  donde no todas las jugadas legales tienen la misma r, o sea donde existe al
  menos una jugada peor que la mejor y por lo tanto se puede errar. Propongo
  llamarlo "estado no trivial". El caso típico de estado trivial es una posición
  ya perdida: todo lo que juegues pierde, así que nada cuenta como error.

  5. Nominal versus realizada, y por qué "las tasas nominales engañan". El
  generador tiene un parámetro ρ = 0.3, la probabilidad de errar. Pero solo se
  puede errar en estados no triviales, que son cerca de la mitad de los
  visitados. Entonces sobre el total de jugadas la fracción de errores observada
  fue 0.15. Si predecís "acierto a τ→0 = 1 menos la tasa compartida" usando el
  0.3 nominal, la línea teórica queda mal ubicada. La exploración lo notó a
  mitad de camino y pasó a usar las tasas medidas en las líneas de teoría.
  Propuesta: definir ρ desde el inicio sobre estados no triviales, y en cada
  celda reportar el parámetro y la fracción medida en el test.

  6. El hash en la exploración. Confirmado: el hash estaba dentro del
  experimento 1, no en uno posterior. La definición de la condición iid(ρ, π) en
  el paper dice que los estados sesgados son "a hash of the position" y ahí
  todos los expertos juegan la misma jugada errónea. La tabla del barrido en π
  muestra la consecuencia: en los estados sesgados el modelo acertaba entre 0.29
  y 0.42 a τ→0, cuando la teoría dice 0. El modelo estaba deshaciendo parte del
  error compartido. La representabilidad se analizó después, comparando esa
  celda π=1 con la condición rule, que fue un control aparte.

  Qué es un hash acá: una función pseudoaleatoria determinista del tablero.
  Mismo tablero, mismo bit; tableros vecinos, bits sin relación. El modelo no
  puede aprenderla, así que en una posición nueva no sabe que es un estado
  sesgado y juega lo que juegan las posiciones parecidas, la óptima. Por eso
  propongo que en la tesina el error compartido sea una regla simple,
  aprendible, como fue rule. Ese "error compartido simple" que recordás existió,
  pero como control, no como el mecanismo del barrido.

  7. Grilla y costo. Grilla es la lista de celdas a correr: cada combinación de
  valores de parámetros por cada semilla. Suma a la especificación porque los
  dos papers reportan cuántas corridas, cuántas semillas y qué cómputo usaron, y
  porque hay que fijarlo antes de correr para no elegir después las celdas que
  dan bien. El panel de 320k partidas responde una objeción que Pablo va a hacer
  seguro: con 80k el imitador captura un cuarto de la ganancia teórica, y hay
  que mostrar si eso es un límite del modelo o falta de datos.

  8. Fijar E[r] del experto. Entre celdas con distinto P la tasa de error es la
  misma pero la fuerza del experto puede no serlo. El error compartido, jugar la
  columna de la izquierda, puede costar en promedio más o menos que un error
  aleatorio, por ejemplo perder en vez de empatar. "Fijar E[r]" sería calibrar
  las tasas para que el experto tenga la misma recompensa esperada en todas las
  celdas. Recomiendo no hacerlo, fijar la tasa, y medir la ganancia contra el
  experto de cada celda.

  9. Eje cantidad de expertos. Sí, es variar K, el n de Pablo. En el diseño
  actual no es una perilla porque el error idiosincrático se sortea de nuevo en
  cada visita, lo que equivale a una población infinita. Para que n importe
  hacen falta K expertos persistentes, cada uno con sus errores fijos por
  estado, y así en un estado repetido el voto es entre K. Lo dejaría como 1b
  opcional.

  10. Recompensa débil versus fuerte. Sigue del punto 2. Con el modo fuerte la
  recompensa distinguiría ganar en 3 de ganar en 20, y contaría como error
  demorar una victoria. Recomiendo la débil.

  11. Régimen de entrenamiento y early stopping fijo. La exploración vio que
  entrenar más tiempo sobre los mismos datos destruye el efecto. El modelo
  memoriza las partidas concretas con sus errores aleatorios y el argmax deja de
  ser un voto. Con los mismos 80k, pasar de 10 a 42 epochs bajó el acierto a
  τ→0 de 0.891 a 0.837, por debajo del experto en 0.845. O sea que el mismo
  experimento dice "trasciende" o "no trasciende" según cuánto entrenes. Por eso
  el protocolo tiene que fijar una regla de parada decidida de antemano e igual
  para todas las celdas: quedarse con el checkpoint de menor pérdida de
  validación. "Fijo" quiere decir eso, la misma regla en todas las celdas.

  12. AGPL, vendored y build. El código del solver de Pons tiene licencia AGPL,
  una licencia copyleft que obliga a redistribuir bajo la misma licencia lo que
  lo incluya. "Vendored" es que copiamos su fuente adentro de nuestro repo en
  lugar de instalarlo como dependencia. Y está en el .gitignore, así que quien
  clone el repo no lo recibe. Hay un script que lo descarga, lo compila y baja
  el libro de aperturas. Para reproducibilidad la tesina debería documentar la
  versión del solver, cómo se compila, qué archivo de libro usa y la nota de
  licencia. Es un ítem de checklist, no un problema.

✻ Baked for 1m 40s · done Sunday 20 Sep at 11:23 am

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores entre expertos en Connect 4, todavía en discusión por chat. Próximo paso: que confirmes las decisiones abiertas para empezar a escribir experimento1-v1.md. (disable recaps in /config)

❯ me pasarías un link al solver de pons?                                        

  Ran 1 shell command (ctrl+o to expand)

⏺ Los tres links relevantes, los dos primeros son los que usa el script de setup
  de la exploración:

  - Código fuente del solver: https://github.com/PascalPons/connect4
  - Libro de aperturas que descargamos:
    https://github.com/PascalPons/connect4/releases/download/book/7x6.book
  - Solver online y explicación del algoritmo paso a paso:
    http://connect4.gamesolver.org y http://blog.gamesolver.org

  El blog es útil para el marco teórico: explica negamax, poda alfa-beta,
  bitboards y tablas de transposición en lenguaje accesible, que es el nivel que
  Dante pide.

✻ Brewed for 23s · done Sunday 20 Sep at 11:40 am

※ recap: Estamos diseñando el experimento 1 de la tesina (correlación de errores entre expertos y trascendencia en Connect 4) para volcarlo en experimento1-v1.md. Falta que decidas las opciones abiertas (regla vs hash, panel 320k, K expertos) y arranco el .md. (disable recaps in /config)

❯ /export experimento1/conver1.md                                               
  ⎿  Conversation exported to:
     /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/explorac
     ion-pre-propuesta/generated/experimento1/conver1.md

❯ No entiendo por qué 1 1/2 0                                                   
  r(e, c) ∈ {1, ½, 0}                                                           

⏺ Es una convención de puntaje, no una consecuencia del juego. Lo único que el
  solver te da es la clase de resultado: ganás, empatás o perdés. Para convertir
  eso en un número hay que elegir tres valores con ganar > empatar > perder, y
  {1, ½, 0} es el puntaje estándar de ajedrez y torneos: una victoria vale un
  punto, unas tablas medio punto.

  Qué depende de la elección y qué no:

  - La accuracy no depende en absoluto. Jugada óptima es la de mejor clase,
    error es bajar de clase. Cualquier terna ordenada da lo mismo.
  - E[r] sí depende, pero solo en la escala. Con {1, ½, 0} un error de ganar a
    empatar cuesta 0.5 y de ganar a perder cuesta 1. Si usaras {1, 0, −1}
    obtendrías exactamente el doble menos uno en todas las celdas, y las
    comparaciones entre imitador y experto no cambian. La única elección con
    contenido real es dónde ponés el empate; en el medio dice "un empate vale
    medio triunfo", que es lo que asume el puntaje de torneos.
  - Coincide con la escala de Zhang. Ellos usan la probabilidad de ganar según
    Stockfish, que vive en [0, 1] con el empate cerca de ½. Con esta terna
    nuestros números se leen igual: E[r] es el puntaje esperado de la partida
    bajo juego perfecto a partir de esa jugada.
  - Bonus práctico. El score de una partida, victorias más medio punto por
    empate sobre partidas jugadas, queda en la misma escala que E[r], así que
    las dos métricas de trascendencia se comparan directo.

  Si querés podemos escribir en la tesina que la elección es arbitraria salvo
  por el orden, y que se adopta la del puntaje de torneos para que E[r] se lea
  como puntaje esperado.

  Una nota aparte: tu export cayó en
  exploracion-pre-propuesta/generated/experimento1/conver1.md porque mi shell
  había cambiado de directorio en una consulta anterior. Seguro lo querés en
  experimento1/ de la raíz.

✻ Brewed for 30s · done Sunday 20 Sep at 2:29 pm

❯ o sea esa cosa que es {1 1/2 0} como la llamaste?                             

⏺ La llamé recompensa de una jugada, y en la fórmula la escribí como r(x, y): el
  estado x, la columna y, y el valor en {1, ½, 0}. Es el término que usan Zhang
  y Abreu, reward function r : X × Y → ℝ, y lo tomamos de ahí para que la
  tesina hable el mismo idioma que los papers.

  En castellano, si querés algo más natural para Dante, la alternativa es
  puntaje de la jugada: el puntaje esperado de la partida bajo juego perfecto
  después de jugar esa columna. Yo mantendría "recompensa" en las fórmulas por
  fidelidad a la literatura y aclararía una vez que equivale al puntaje de
  torneos.

✻ Churned for 10s · done Sunday 20 Sep at 2:32 pm

❯ si le pongo valor v 1 1/2 0 a los estados segun ganadores, empates o          
  perdedores                                                                    
  r(e,c) = v(e') siendo e' el estado que se obtiene de jugar c en e ?           

⏺ Sí, exactamente, con un solo cuidado: el punto de vista. Hay dos formas de
  definir v y las dos funcionan si sos consistente:

  - v desde el que acaba de mover. v(e') es el resultado, con juego perfecto,
    para el jugador que llegó a e'. Entonces r(e, c) = v(e') tal como lo
    escribiste.
  - v desde el que tiene el turno. Es lo que devuelve el solver de Pons: el
    resultado para el que mueve en e'. Como en e' mueve el rival, r(e, c) = 1 −
    v(e').

  Con la primera convención, además, te queda la recursión minimax en una línea:
  v(e) = max_c r(e, c). Y eso da definiciones limpias para la tesina:

  - Jugada óptima en e: una c con r(e, c) = v(e). Conserva el valor del estado.
  - Error: una c con r(e, c) < v(e). Baja de clase.
  - Estado no trivial: existe c con r(e, c) < v(e). Si todas las jugadas dan
    v(e), no se puede errar.

  Los estados terminales entran sin caso especial: si c gana en el acto, e' es
  terminal con v(e') = 1 para el que movió.
✻ Crunched for 21s · done Sunday 20 Sep at 2:35 pm

❯ se te ocurre un mejor nombre que valor para v?                                

⏺ Yo mantendría valor. Es el término estándar: en teoría de juegos combinatorios
  se habla del game-theoretic value de una posición, y Allis usa exactamente
  esa expresión en su tesis sobre Connect 4. Si querés desambiguarlo de otros
  "valores" que aparezcan en el texto, las variantes usuales son:

  - valor teórico de la posición: el resultado con juego perfecto de ambos
    lados. Es la que más se usa cuando se explica a alguien no del área.
  - valor minimax: enfatiza cómo se calcula, v(e) = max_c r(e, c). Útil si en el
    marco teórico presentás la recursión.
  - resultado teórico: más llano, pero suena a resultado de una partida ya
    jugada y se confunde con el token de resultado que va al final de la
    secuencia.

  Mi recomendación: definirlo una vez como "valor teórico v(e)" y después
  escribir solo "valor".

✻ Brewed for 20s · done Sunday 20 Sep at 2:36 pm

※ recap: Estamos definiendo el experimento 1 de la tesina, el barrido de correlación de errores en Connect 4, aclarando términos como recompensa y valor teórico. Falta que decidas las opciones abiertas para que empiece a escribir experimento1-v1.md.

❯ Por qué tomamos estas elecciones:                                             
  Decoder tipo nanoGPT, 8 capas, 8 cabezas, ancho 256, 6.3M parámetros. AdamW,  
  cosine schedule, batch 512, unos 10 epochs. Tabla completa de hiperparámetros 
  al estilo del apéndice E de Zhang                                             
  [1] tomó la mismas? cual fue la razon nuestra?                                

  Searched for 2 patterns (ctrl+o to expand)

⏺ No, [1] no tomó las mismas. Tomamos la misma receta que [1] y la achicamos al
  tamaño del dominio. Los números concretos fueron los defaults razonables que
  puso el agente en la exploración, no salieron de una búsqueda. Conviene
  decirlo así en la tesina y justificarlos a posteriori, que es posible.

  Comparación con la tabla del apéndice E de Zhang:

  ┌─────────────────────┬──────────────────────┬────────────────────────────┐
  │   Hiperparámetro    │   ChessFormer [1]    │      Nuestro imitador      │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Arquitectura        │ decoder-only, base   │ igual                      │
  │                     │ nanoGPT              │                            │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Capas / cabezas /   │ 16 / 8 / 512         │ 8 / 8 / 256                │
  │ ancho               │                      │                            │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Parámetros          │ 50M                  │ 6.3M                       │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Optimizador         │ AdamW, β = (0.9,     │ igual                      │
  │                     │ 0.95)                │                            │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Learning rate,      │ 3e-4, 3e-5           │ 6e-4, 6e-5                 │
  │ mínimo              │                      │                            │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Schedule            │ cosine con warmup    │ cosine con warmup 200      │
  │                     │ 2000                 │                            │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Weight decay        │ 0.1                  │ 0.1                        │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Gradient clip       │ 1.0                  │ 1.0                        │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Dropout             │ 0                    │ 0                          │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Precisión           │ bfloat16             │ bfloat16                   │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Batch               │ 125K tokens          │ 512 partidas ≈ 22K tokens  │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Pasos               │ 100K                 │ 1600                       │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Datos               │ ~10⁹ partidas, una   │ 80k partidas, ~10 epochs   │
  │                     │ pasada               │                            │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │ Tokens              │ 32 caracteres del    │ 12: BOS, 7 columnas, 3     │
  │                     │ PGN                  │ resultados, PAD            │
  └─────────────────────┴──────────────────────┴────────────────────────────┘

  Qué es igual y por qué: decoder autorregresivo con next-token prediction sobre
  la transcripción, sin ver el tablero, AdamW con los mismos β, cosine, weight
  decay, clip y sin dropout. Eso es lo que hace comparable el mecanismo con el
  de [1] y lo que permite decir que el imitador es "el de Zhang, en chico".

  Por qué achicamos, y esto sí es un argumento y no un default:

  - El dominio es órdenes de magnitud más chico. Vocabulario de 12 tokens contra
    32 caracteres, secuencias de a lo sumo 44 tokens contra cientos, y unas 4.5
    × 10¹² posiciones legales contra 10⁴³ en ajedrez.
  - Los datos son más chicos. 80k partidas son ~2M tokens. Un modelo de 50M
    sobre 2M tokens memoriza en pocos pasos, y la exploración mostró que
    memorizar destruye el efecto.
  - Costo. Cada corrida son 30 minutos en la Mac o 2 minutos en una 4090, lo que
    permite 3 semillas por celda.

  Qué respaldo empírico ya tenemos de que los números no importan mucho: en el
  experimento de composición se corrió el mismo diseño con modelos de 0.1M, 0.8M
  y 6.3M parámetros y el resultado no cambió. Eso cubre el tamaño. El resto,
  lr, batch, warmup, no está ablacionado, y va en el paso 6 del plan de la
  propuesta.

  Dos cosas que sí cambiaría respecto de la exploración:

  - "Unos 10 epochs" no fue una elección, fue 1600 pasos por 512 por accidente 
    del default. Y resultó ser el parámetro que decide si hay trascendencia o
    no. En la tesina lo reemplazo por la regla de early stopping sobre
    validación, que no depende de acertar el número.
  - El lr es el doble que el de [1]. Es el default de nanoGPT para modelos
    chicos y funcionó, pero si Pablo pregunta, la respuesta honesta es esa. Si
    querés alinear todo, bajar a 3e-4 cuesta nada y lo probamos en el piloto.

✻ Cogitated for 59s · done Sunday 20 Sep at 2:42 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores entre expertos en Connect 4, y vengo aclarando tus dudas sobre el diseño. Siguiente paso: que decidas las opciones abiertas para que arranque el .md.

❯ Que hubiera pasado si no hubiéramos achicado el modelo?                       

⏺ No lo probamos, así que es una predicción, no un dato. Pero la exploración da
  bastante para predecir:

  Lo más probable: el mismo resultado si parás a tiempo, y peor si no. Un modelo
  de 50M sobre 2M tokens tiene 25 veces más parámetros que tokens. Ajusta el
  conjunto de entrenamiento en pocos epochs y después empieza a memorizar
  partidas concretas con sus errores aleatorios. Eso ya lo vimos con el de 6.3M
  al pasar de 10 a 42 epochs: la pérdida de validación se dispara y el acierto a
  τ→0 cae de 0.891 a 0.837, por debajo del experto. Un modelo 8 veces más
  grande llega a ese punto antes. Con 10 epochs fijos, es posible que ya
  estuviera adentro del régimen de memorización y el experimento diera "no
  trasciende" por una razón que no tiene nada que ver con la correlación de
  errores. Con early stopping sobre validación, el mejor checkpoint llegaría
  antes y probablemente con una ganancia parecida o algo mayor.

  Por qué memorizar rompe el voto. El imitador ve secuencias, no tableros. El
  voto funciona donde muchas partidas comparten prefijo y el modelo estima la
  frecuencia de cada continuación. Donde el prefijo es único, en el medio y
  final, un modelo con capacidad de sobra puede guardar "en esta partida se jugó
  tal columna" en vez de "en posiciones así se juega tal columna". El argmax
  pasa a reproducir el error de esa partida en vez de la mayoría de las
  posiciones parecidas. Es la dinámica de Arpit et al. 2017 sobre etiquetas
  ruidosas: las redes aprenden primero los patrones y después el ruido, y cuanta
  más capacidad, antes llegan al ruido.

  Costo. Unas 8 veces más cómputo por paso. De 2 minutos a unos 15 por corrida
  en la 4090. Sigue siendo viable, no fue la razón principal.

  Lo que sí sabemos hacia abajo. En composición se probó 0.1M, 0.8M y 6.3M a los
  mismos pasos. El resultado cualitativo no cambió, y el más grande fue
  levemente mejor en acierto a τ=1 y τ→0. Nada indica un quiebre, en ninguna
  dirección, dentro de ese rango.

  Consecuencia para la tesina. Es una ablación barata y conviene correrla en el
  paso 6: el mismo diseño con 16 capas y ancho 512, con early stopping. Mi
  predicción registrada: misma curva en P, mejor checkpoint más temprano. Si en
  cambio la ganancia cae, el hallazgo de que la trascendencia es una propiedad
  del régimen de entrenamiento gana peso, y también vale.

✻ Churned for 38s · done Sunday 20 Sep at 2:52 pm

❯ y en retrospectiva esa eleccion (8 / 8 / 256) es adecuada o deberia haber     
  sido mas chico incluso?                                                       

⏺ Adecuada, y si hubiera que moverla sería hacia arriba, no hacia abajo. Tres
  razones:

  1. Ya se probó más chico y fue peor. En composición se corrió el mismo diseño
  con 0.1M, 0.8M y 6.3M parámetros a los mismos pasos. En la condición control:

  ┌────────┬────────┬────────┬────────────────────┬─────────────────────────┐
  │ Modelo │  acc   │  acc   │ masa en columnas   │ score en juego propio   │
  │        │  τ=1   │  τ→0   │      ilegales      │       vs perfecto       │
  ├────────┼────────┼────────┼────────────────────┼─────────────────────────┤
  │ 0.1M   │ 0.923  │ 0.964  │ 1.1 %              │ 0.24                    │
  ├────────┼────────┼────────┼────────────────────┼─────────────────────────┤
  │ 0.8M   │ 0.942  │ 0.973  │ 0.4 %              │ 0.28                    │
  ├────────┼────────┼────────┼────────────────────┼─────────────────────────┤
  │ 6.3M   │ 0.953  │ 0.977  │ 0.1 %              │ 0.40                    │
  └────────┴────────┴────────┴────────────────────┴─────────────────────────┘

  El resultado cualitativo no cambió, pero el juego propio sí: los modelos
  chicos ponen más masa en jugadas ilegales y pierden partidas por eso.
  Representar el tablero a partir de la secuencia cuesta capacidad, y 0.1M no
  alcanza para hacerlo limpio.

  2. El síntoma que tiene el 6.3M es de poca capacidad efectiva, no de mucha. A
  τ=1 su acierto es 0.76 contra 0.845 del experto: la distribución que aprende
  es más plana que los datos. Eso es lo contrario de sobreajuste. El límite no
  era el tamaño sino el régimen: más pasos lo llevaban a memorizar antes de
  afinar. Un modelo algo más grande con early stopping podría reducir esa
  entropía residual sin memorizar. Es una hipótesis, no un dato.

  3. Está en el rango de los trabajos comparables. Othello-GPT usa 8 capas, 8
  cabezas y ancho 512 para un dominio de tamaño parecido, y los modelos chicos
  de Karvonen sobre ajedrez están en 8 capas y ancho 512. Nuestro 8 / 8 / 256 es
  la mitad de ancho que eso. Nadie va a objetar que sea grande.

  La conclusión para la tesina: el tamaño es una perilla de segundo orden. La
  elección se justifica por la tabla de arriba y por estar en el rango de la
  literatura, y el paso 6 la ablaciona hacia arriba con 16 / 8 / 512 para cerrar
  la pregunta.

✻ Crunched for 35s · done Sunday 20 Sep at 2:54 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores P en Connect 4, y venís haciendo preguntas de clarificación sobre el diseño. Próximo paso: que decidas las opciones abiertas y arranque el .md.

❯ Quiero hablar de los tokens ahora                                             
  No entiendo por qué necesitamos BOS y PAD y los 3 resultados: el PGN de [1]   
  incluye eso?                                                                  

⏺ Sí, el PGN de [1] incluye el resultado y un separador; el PAD es una decisión
  de implementación nuestra. Vamos por partes.

  Qué ve el modelo de [1]. Una partida es un string como 1.e4 e5 2.Nf3 Nc6 ... 
  1-0, tokenizado carácter por carácter con un vocabulario de 32 símbolos. Zhang
  dice explícitamente que el modelo solo ve "the moves and the outcome of the
  game". El código sobre el que construyen, el de Karvonen, concatena las
  partidas en un stream separadas por ;, así que el ; cumple el rol de nuestro
  BOS. No tienen PAD porque entrenan sobre bloques de 1024 caracteres cortados
  de ese stream, sin alinear con el inicio de partida.

  Por qué nosotros tokenizamos por jugada y no por carácter. En ajedrez una
  jugada son varios caracteres, Nf3, y no había alternativa razonable. En
  Connect 4 una jugada es una columna, un solo símbolo. Un token por columna es
  lo natural y evita que el modelo tenga que aprender a parsear.

  BOS. Un modelo autorregresivo predice el token t desde la posición t−1. La
  primera jugada necesita algo antes desde donde predecirse. Eso es BOS. En [1]
  lo hace el ;. Sin él no habría distribución sobre la jugada de apertura, y
  justamente el control de "nadie abre al centro" se mide ahí.

  Los tres tokens de resultado. Tres razones para mantenerlos, en orden de peso:
  - Fidelidad a [1]: su secuencia termina en 1-0, 0-1 o 1/2-1/2 y su pérdida
    cubre ese token. Copiamos eso.
  - Sirve de fin de secuencia: en juego propio el modelo tiene que saber cuándo
    terminó la partida, y un token de resultado es el EOS natural.
  - Es el gancho para la extensión opcional de condicionar por resultado, tipo
    Decision Transformer, que [1] menciona en su apéndice D.2 como otra vía de
    trascendencia. Moverlo al principio de la secuencia es un cambio de una
    línea si algún día lo hacemos.

  No los necesitamos para el experimento 1. Un único EOS alcanzaría. Los
  mantengo porque cuestan nada y mantienen la comparabilidad. Detalle: el empate
  en Connect 4 requiere llenar el tablero y es rarísimo entre expertos, así que
  ese tercer token casi no aparece. Es inofensivo.

  PAD. Entrenamos con una partida por fila, de largo fijo 44: BOS, hasta 42
  jugadas, resultado. Las partidas más cortas se rellenan con PAD, que se
  enmascara en la pérdida. Es la alternativa a concatenar en stream como
  Karvonen. Ventaja: cada fila es una partida completa alineada, lo que
  simplifica evaluar por jugada y por fase. Si preferís imitar [1] al pie de la
  letra, se concatena y desaparece el PAD. No cambia nada del experimento.

  Un detalle de evaluación que sale de esto. Al leer los logits en un estado, el
  softmax se restringe a los 7 tokens de columna. La masa que el modelo pone en
  tokens que no son jugadas, resultado o PAD, se reporta aparte como chequeo de
  sanidad. En la exploración fue alrededor del 1 %.

✻ Crunched for 40s · done Sunday 20 Sep at 3:01 pm

❯ - que significa que: entrenan sobre bloques de 1024 caracteres cortados de    
  ese stream, sin alinear con el inicio de partida                              
  - que sería "Si preferís imitar [1] al pie de la letra, se concatena y        
  desaparece el PAD"                                                            

⏺ Las dos preguntas son la misma cosa vista de los dos lados. Hay dos formas de
  armar los ejemplos de entrenamiento a partir de muchas partidas.

  Forma stream, la de Karvonen y [1]. Pegás todas las partidas una detrás de
  otra en un único texto larguísimo, con ; entre partida y partida:

  ;1.e4 e5 2.Nf3 ... 1-0;1.d4 d5 2.c4 ... 0-1;1.e4 c5 ...

  Después cortás ese texto en pedazos de largo fijo, 1024 caracteres, y cada
  pedazo es un ejemplo de entrenamiento. Los cortes caen donde caen: un pedazo
  puede empezar en la jugada 23 de una partida, contener dos partidas enteras y
  terminar a mitad de una tercera. Eso es "sin alinear con el inicio de
  partida". El modelo aprende igual, porque el ; le dice dónde empieza cada una
  y la atención causal le permite ignorar lo anterior. No hace falta rellenar
  nada porque todo pedazo tiene exactamente 1024 caracteres.

  Forma por partida, la nuestra. Cada ejemplo es exactamente una partida: BOS,
  sus jugadas, su resultado. Como las partidas tienen distinto largo y el batch
  necesita filas del mismo largo, las cortas se completan con PAD hasta 44, y
  esos PAD se excluyen de la pérdida.

  "Imitar [1] al pie de la letra" significa pasar a la forma stream: concatenar
  nuestras partidas separadas por BOS y cortar en bloques fijos. Ahí el PAD
  desaparece porque ya no hay filas cortas que rellenar.

  Por qué me quedo con la forma por partida: cada fila es una partida entera
  desde la jugada 1, así que la posición t de la fila es siempre la jugada t.
  Eso hace trivial evaluar por jugada, por fase, y saber qué tablero hay en cada
  posición. En la forma stream habría que reconstruir dónde empieza cada
  partida dentro del bloque. Para el modelo no cambia nada; para nuestro
  análisis, la forma por partida es más cómoda. Y el PAD es un costo nulo: con
  partidas de 21 jugadas en promedio, la mitad de cada fila es relleno que no se
  computa.

✻ Cogitated for 21s · done Sunday 20 Sep at 3:11 pm

❯ por qué en tu mensaje hay dos numeros en learning rate y por qué lo cmabiamos 
  respecto a de [1]                                                             

⏺ Son los dos extremos del schedule cosine. El learning rate no es constante:
  arranca en cero, sube linealmente durante el warmup hasta el valor máximo, y
  después baja siguiendo un coseno hasta el valor mínimo al final del
  entrenamiento. Los dos números son ese máximo y ese mínimo. En [1] son 3e-4 y
  3e-5; en el nuestro 6e-4 y 6e-5. En ambos el mínimo es un décimo del máximo,
  la proporción es la misma.

  Por qué el doble: no fue una decisión contra [1], fue el default. El agente
  tomó los valores de referencia de nanoGPT, cuya configuración estándar usa
  6e-4 con mínimo 6e-5, y no los tocó. La justificación a posteriori es la regla
  práctica de que los modelos más chicos toleran learning rates más altos, y
  6.3M es ocho veces más chico que el de [1]. Funcionó: el entrenamiento fue
  estable en todas las celdas. Pero es una justificación después del hecho, no
  un experimento.

  Qué haría: en el piloto correr una celda con 3e-4 y otra con 6e-4, quedarme
  con la de menor pérdida de validación, y anotar en la tabla de hiperparámetros
  cuál se usó y por qué. Cuesta cuatro minutos de GPU y saca la pregunta de la
  mesa antes de que la haga Pablo.

✻ Baked for 22s · done Sunday 20 Sep at 3:12 pm

❯ volviendo a la forma de armar los ejemplos: que ventajas tiene concatenar     
  entre partida y partida? no se aprendería mas rapido porque se aprovecha      
  computo?                                                                      

⏺ Sí, tu intuición es correcta, y es la ventaja principal. Pero a nuestra escala
  no importa, y para nuestro diseño concreto tiene un costo.

  Ventajas de concatenar:
  - Cómputo útil. Con filas de 44 y partidas de 21 jugadas en promedio, cerca de
    la mitad de cada fila es PAD. La atención y las capas se calculan igual
    sobre esos tokens aunque no aporten a la pérdida. Concatenando, cada paso
    procesa el doble de jugadas reales con los mismos FLOPs. En [1], con 10⁹
    partidas, esto es decisivo.
  - Pipeline más simple para datos enormes. Un solo archivo de texto, cortes
    fijos, sin manejar largos variables ni vocabulario extra.

  Por qué acá no pesa: una corrida son 2 minutos en la 4090 sobre 2M tokens.
  Ahorrar la mitad es un minuto por celda. Y si alguna vez importara, hay un
  truco intermedio: agrupar en cada batch partidas de largo parecido, lo que
  reduce el PAD sin cambiar el formato.

  Los costos de concatenar para nosotros:
  - La posición en la fila deja de ser el número de jugada. Con una partida por
    fila, el embedding posicional codifica directamente la jugada t. Eso es lo
    que hizo que la regla "cada 3 jugadas" se aprendiera a tres decimales desde
    el paso 200, y es lo que va a hacer representable nuestro error compartido
    definido por índice de jugada. En stream el modelo tendría que contar desde
    el último BOS con atención. Sigue siendo aprendible, pero menos trivial, y
    estaríamos agregando dificultad justo en la parte que queremos que sea
    fácil.
  - Fuga entre partidas. Dentro de un bloque el modelo atiende a las partidas
    anteriores salvo que enmascares por documento. Como nuestras partidas son
    independientes, no hay información que sacar de ahí, pero gasta atención en
    aprender a ignorarlas. Karvonen y [1] convivieron con esto.
  - Análisis más incómodo. Para evaluar por jugada, por fase, o etiquetar el
    tablero en cada posición hay que reconstruir dónde empieza cada partida
    dentro del bloque.

  Existe la solución que junta lo mejor de ambos, empaquetar varias partidas por
  fila con máscara de atención por partida y posiciones reiniciadas en cada
  BOS. Es lo que hace el entrenamiento moderno de LLMs. Para 2M tokens es
  sobre-ingeniería. Me quedo con una partida por fila y lo justifico en la
  tesina por la representabilidad del índice de jugada y la simplicidad del
  análisis.

✻ Brewed for 38s · done Sunday 20 Sep at 3:16 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores en Connect 4, aclarando cada decisión antes de escribir experimento1-v1.md. Falta que confirmes las decisiones abiertas para que arranque el .md.

❯ No entiendo estos numeros                                                     
   Batch                   │ 125K tokens                │ 512 partidas ≈ 22K    
  tokens Datos                   │ ~10⁹ partidas, una pasada  │ 80k partidas,   
  ~10 epochs                                                                    
⏺ Son dos formas de medir lo mismo, cuánto entra en cada paso y cuánto se
  recorre en total.

  Batch: cuánto procesa un paso de gradiente.
  - [1] lo mide en tokens porque entrena en stream: cada paso ve 125.000
    caracteres de PGN, que son unas 250 a 400 partidas de ajedrez según su
    largo.
  - Nosotros lo medimos en partidas porque entrenamos una partida por fila: cada
    paso ve 512 partidas. En tokens son 512 filas × 44 posiciones = 22.528
    casilleros, de los cuales cerca de la mitad son PAD. Tokens reales, con
    jugadas, BOS y resultado, unos 12.000 por paso.

  Así que nuestro batch es entre 6 y 10 veces más chico que el de [1], lo que es
  coherente con un modelo 8 veces más chico. El batch grande de [1] sale de las
  recetas de OPT-175B, que ellos mismos citan.

  Datos: cuánto se recorre en total.
  - [1] parte de la base de lichess de enero a octubre de 2023, alrededor de 10⁹
    partidas antes de filtrar por rating. Entrena 100.000 pasos × 125.000
    tokens = 1.25 × 10¹⁰ tokens. Una partida en PGN son unos 300 a 500
    caracteres, así que vieron del orden de 25 a 40 millones de partidas. Es
    menos que el dataset: ninguna partida se repite. "Una pasada" es generoso,
    en realidad es menos de una.
  - Nosotros: 80.000 partidas, 1.600 pasos × 512 partidas por paso = 819.200
    visitas a partidas, dividido 80.000 = 10.2. Cada partida se ve unas 10
    veces. Eso son los "10 epochs".

  Esta diferencia es la que explica por qué [1] nunca vio la memorización y
  nosotros sí: ellos no repiten ninguna partida, nosotros repetimos cada una
  diez veces. En la exploración, subir a 42 repeticiones destruyó la ganancia.
  Es también el argumento para el panel de 320k: mismos pasos, cada partida
  vista 2.6 veces, más cerca del régimen de [1].

✻ Crunched for 29s · done Sunday 20 Sep at 3:24 pm

❯ por eso necesitamos early stopping nosotros?                                  

⏺ Sí, exactamente por eso. Si cada partida se ve una sola vez, el modelo no
  puede memorizar partidas concretas: nunca vuelve a encontrarlas. [1] está en
  ese régimen y no necesita ninguna regla de parada, la pérdida de validación
  baja mientras entrena. Nosotros repetimos cada partida diez veces, y a partir
  de cierto punto el modelo empieza a guardar las partidas con sus errores en
  vez de estimar la mezcla. La pérdida de validación lo delata: en 80k partidas
  tocó su mínimo cerca del paso 2400 y después subió sin parar. Early stopping
  es quedarse con el checkpoint de ese mínimo, y es la regla que reemplaza el
  "10 epochs" arbitrario.

  Hay una alternativa que conviene tener presente, porque nuestros datos son
  sintéticos e ilimitados: en vez de repetir, generar más. Para 1600 pasos de
  512 partidas sin repetición harían falta 820k partidas por celda, unas 3.3
  horas de CPU en 8 cores cada una. Sería copiar el régimen de [1] al pie de la
  letra y eliminar la memorización por construcción. No lo propongo como
  principal por dos razones: la generación de 15 celdas se va a 50 horas de CPU,
  y la exploración mostró que repetir ayuda mientras no se memoriza, a 320k
  partidas 10 epochs dio mejor ganancia que 2.6. Early stopping captura ese
  punto óptimo solo, con cualquier tamaño de datos. El panel de 320k queda como
  el puente hacia el régimen de [1].

✻ Cooked for 23s · done Sunday 20 Sep at 3:38 pm

❯ A ver hagamos los calculos para no tener que memorizar: con cuántos datos     
  deberíamos entrenar nosotros? primero que nada: cuantos step deberiamos       
  hacer? y luego pensar cuántas partidas necesitaríamos                         
  Mi plan es una vez que tenga buena configuracion de conversar con vos ;       
  repetimos el experimento (quizas cambiando cosas como generar mas datos), no  
  te preocupes por el computo ; puedo pagar cloud computing                     

⏺ Buen plan, y el cálculo se puede hacer con lo que ya medimos. La cantidad
  invariante es partidas vistas = pasos × batch. Con batch 512, cada 1000 pasos
  consumen 512k partidas. Para no repetir ninguna, hace falta N ≥ pasos × 512.

  Cuántos pasos hacen falta. Lo que sabemos de la exploración, todo en π=0:

  ┌──────────┬───────┬────────┬─────────┬───────────────────────────────────┐
  │ Partidas │ Pasos │ Epochs │ acc τ→0 │        Mínimo de val loss         │
  ├──────────┼───────┼────────┼─────────┼───────────────────────────────────┤
  │ 80k      │ 1600  │ 10     │ 0.891   │ en el paso 1600, todavía bajando  │
  ├──────────┼───────┼────────┼─────────┼───────────────────────────────────┤
  │ 320k     │ 1600  │ 2.6    │ 0.888   │ en el paso 1600, todavía bajando  │
  ├──────────┼───────┼────────┼─────────┼───────────────────────────────────┤
  │ 320k     │ 6400  │ 10     │ 0.914   │ en el paso 6000                   │
  ├──────────┼───────┼────────┼─────────┼───────────────────────────────────┤
  │ 320k     │ 25600 │ 42     │ 0.865   │ en el paso 8400, después memoriza │
  └──────────┴───────┴────────┴─────────┴───────────────────────────────────┘

  Tres lecturas. Primero, a 1600 pasos da igual tener 80k o 320k: el modelo está
  limitado por pasos, no por datos. Segundo, con 320k el aprendizaje sigue
  hasta el paso 8400, y ahí lo corta la memorización, no la saturación. Tercero,
  el acierto a τ=1 subió con los datos, 0.763, 0.789, 0.807, sin llegar al
  0.845 del experto: seguía limitado por datos. Conclusión: el mínimo son más de
  8400 pasos, y no sabemos dónde satura porque nunca corrimos con datos frescos
  más allá de eso.

  Un ancla externa: la regla de Chinchilla de 20 tokens por parámetro da 126M
  tokens para 6.3M parámetros. A 23 tokens reales por partida son 5.5M partidas,
  unos 10.700 pasos. Es una heurística de modelos de lenguaje, pero cae en el
  mismo orden que el dato empírico.

  Propuesta: medir la saturación en vez de adivinarla. Un piloto en π=0, que es
  la celda donde el denoising tiene más margen:

  1. Generar 8M partidas, que alcanzan para 16.000 pasos sin repetir.
  2. Entrenar 16.000 pasos en una sola pasada, guardando checkpoint cada 500.
  3. En cada checkpoint medir val loss, acc a τ→0 y ganancia sobre el experto en
     el test fijo, separado en vistos y no vistos.
  4. Definir S* como el paso donde la ganancia deja de mejorar más de 0.002 en
     2000 pasos.

  Después, la grilla principal. N por celda y semilla = 1.2 × S* × 512, el 20 %
  de margen para que la cola del cosine también sea con datos frescos. Sin
  repetición, la pérdida de validación debería bajar monótonamente y el early
  stopping queda como chequeo, no como decisión.

  Costo, por celda y semilla. Generación a 40 ms por partida por core,
  entrenamiento a un minuto por 1000 pasos en una 4090:

  ┌─────┬────────────┬────────────────┬───────────────────┬────────────────┐
  │  S  │ N partidas │ CPU generación │ GPU entrenamiento │ Datos en disco │
  ├─────┼────────────┼────────────────┼───────────────────┼────────────────┤
  │ 4k  │ 2.0M       │ 23 core-h      │ 4 min             │ 90 MB          │
  ├─────┼────────────┼────────────────┼───────────────────┼────────────────┤
  │ 8k  │ 4.1M       │ 46 core-h      │ 8 min             │ 180 MB         │
  ├─────┼────────────┼────────────────┼───────────────────┼────────────────┤
  │ 16k │ 8.2M       │ 91 core-h      │ 16 min            │ 360 MB         │
  ├─────┼────────────┼────────────────┼───────────────────┼────────────────┤
  │ 32k │ 16.4M      │ 182 core-h     │ 32 min            │ 720 MB         │
  └─────┴────────────┴────────────────┴───────────────────┴────────────────┘

  Para la grilla completa, 5 valores de P por 3 semillas con datasets distintos,
  multiplicá por 15. En el escenario S=16k son unas 1400 core-horas de CPU, que
  en una máquina cloud de 64 cores son 22 horas, del orden de 30 a 50 USD. La
  GPU es despreciable. El cuello de botella es el solver, y hay dos formas de
  aliviarlo si hace falta: la caché de posiciones, que en apertura repite
  muchísimo, y generar las 3 semillas de cada P en paralelo.

  Dos consecuencias a tener en cuenta. Con más datos crece la fracción de
  estados de test que aparecen en entrenamiento, 0.41, 0.47 y 0.53 para 20k, 80k
  y 320k. La descomposición visto/no visto del objetivo 3 va a tener que
  hacerse a varios tamaños de datos, y este piloto ya la da gratis en función de
  los pasos. Y la predicción que vale registrar antes de correr: si la
  limitación era datos y régimen, con una pasada sobre millones de partidas la
  ganancia debería acercarse al techo teórico también en estados no vistos. Si
  se queda en un cuarto, el límite es el modelo, y esa es otra tesis.

✻ Worked for 1m 0s · done Sunday 20 Sep at 3:42 pm

❯ y por qué batch size es 512?                                                  

⏺ Fue un default del agente, no una decisión razonada. Pero cae en un lugar
  defendible, y por eso no lo cambiaría sin medir.

  Por qué es razonable. En partidas por paso es del mismo orden que [1]: sus
  125K caracteres de PGN son unas 300 partidas de ajedrez por paso. Nuestras 512
  partidas son 22K casilleros de tokens, que entran holgados en la memoria de
  cualquier GPU y hasta en la Mac. Y para un modelo de 6M el "batch crítico", el
  punto a partir del cual agrandar el batch deja de ayudar, es chico; 512 está
  probablemente cerca o por encima.

  Qué controla el batch en nuestro régimen. En una pasada sobre N partidas,
  batch × pasos = N. Entonces el batch decide cuántas actualizaciones de
  gradiente hacés con esas mismas partidas:
  - Batch chico: más pasos, gradientes más ruidosos, menor uso de la GPU por
    paso.
  - Batch grande: menos pasos, gradientes más estables, hay que subir el
    learning rate para compensar, y por debajo del batch crítico rinde igual que
    el chico a igual cantidad de partidas vistas.

  Lo que no cambia con el batch es la cantidad de partidas necesarias para no
  memorizar: esa cuenta es en partidas, no en pasos.

  Qué haría. En el piloto, una corrida con 512 y otra con 2048 y learning rate
  escalado por la raíz de 4, mismas partidas totales. Si dan lo mismo, 2048 y
  terminás cuatro veces más rápido en GPU. Si 512 es mejor, ya sabés que estás
  por encima del batch crítico y te quedás ahí. Es un par de corridas y deja la
  elección documentada en la tabla de hiperparámetros.

✻ Baked for 19s · done Sunday 20 Sep at 3:45 pm

❯ y por que no 128 o mas chico?                                                 

⏺ Se puede, y probablemente daría el mismo resultado por partida vista. Lo que
  cambia es el tiempo.

  Qué pasa al bajar el batch. Por debajo del batch crítico, el rendimiento
  depende de cuántas partidas viste, no de en cuántos pasos las repartiste. Con
  128 harías 4 veces más pasos sobre las mismas partidas, con gradientes 4 veces
  más ruidosos, y llegarías aproximadamente al mismo lugar. Pero cada paso en
  GPU cuesta casi lo mismo con 128 que con 512, porque la GPU está lejos de
  saturarse con un modelo de 6M. Entonces 4 veces más pasos son 4 veces más
  reloj: los 16 minutos de una corrida de 16k pasos pasan a una hora, sin
  ganancia esperable.

  Lo que sí podría aportar el batch chico, y por qué no lo cuento. El ruido del
  gradiente actúa como regularizador y a veces mejora la generalización. Ese
  efecto importa cuando repetís datos y el riesgo es sobreajustar. En una pasada
  sobre datos frescos no hay nada que regularizar: cada partida se ve una vez.

  Costos adicionales. Con batch chico hay que bajar el learning rate para que no
  se vuelva inestable, la curva de validación queda más ruidosa y cuesta más
  leer dónde satura, y las medidas cada 500 pasos cubren 4 veces menos partidas.

  Cuándo tendría sentido. Si el modelo fuera tan grande que 512 no entrara en
  memoria, o si quisiéramos más puntos en la curva de aprendizaje por partida
  vista. Ninguna de las dos aplica.

  Si querés cerrar la pregunta con datos, sumamos 128 al mismo piloto que 512 y
  2048. Mi predicción registrada: los tres coinciden en ganancia a igual
  cantidad de partidas, y difieren solo en reloj. Si 128 gana, es un hallazgo
  sobre el ruido del gradiente y también vale reportarlo.

✻ Churned for 21s · done Sunday 20 Sep at 3:46 pm

❯ Bueno entonces me perdí en cuántos datos necesaríamos generar para entrenar 1 
  sola epoch como [1]                                                           

⏺ La cuenta es una sola: partidas = pasos × batch, porque en una pasada cada
  partida se ve exactamente una vez.

  Con batch 512:

  ┌────────┬────────────────────┐
  │ Pasos  │ Partidas a generar │
  ├────────┼────────────────────┤
  │ 1.600  │ 0.8M               │
  ├────────┼────────────────────┤
  │ 8.400  │ 4.3M               │
  ├────────┼────────────────────┤
  │ 16.000 │ 8.2M               │
  ├────────┼────────────────────┤
  │ 32.000 │ 16.4M              │
  └────────┴────────────────────┘

  El batch no cambia la cantidad de partidas. Si usás 2048 en vez de 512,
  necesitás 4 veces menos pasos para las mismas partidas. La respuesta está en
  partidas, no en pasos.

  Y la incógnita real es cuántas partidas necesita el modelo para saturar, que
  no sabemos porque nunca corrimos con datos frescos más allá de 320k. Lo que sí
  sabemos: con 320k seguía aprendiendo cuando lo cortó la memorización, así que
  el número es mayor que 4.3M, que es lo que hubiera hecho falta para llegar a
  esos 8400 pasos sin repetir. La heurística de Chinchilla da 5.5M. Por eso
  propuse el piloto: generar 8M partidas para π=0, entrenar una pasada de 16.000
  pasos, y mirar en qué punto la ganancia deja de subir. Ese punto, con un 20 %
  de margen, es el N de la grilla.

  Costo de esas 8M: 91 core-horas, o sea una hora y media en una máquina de 64
  cores.

✻ Crunched for 15s · done Sunday 20 Sep at 3:48 pm

❯ los experimentos preliminares utilizaron cuanto?                              

⏺ Los preliminares usaron mucho menos y repitiendo datos:

  ┌───────────────────────────┬──────────┬──────────────┬──────────────────┐
  │          Corrida          │ Partidas │    Pasos     │ Veces que se vio │
  │                           │          │              │   cada partida   │
  ├───────────────────────────┼──────────┼──────────────┼──────────────────┤
  │ Grilla principal, todas   │ 80k      │ 1.600        │ 10               │
  │ las condiciones           │          │              │                  │
  ├───────────────────────────┼──────────┼──────────────┼──────────────────┤
  │ Descomposición visto/no   │ 20k      │ 400          │ 10               │
  │ visto, punto chico        │          │              │                  │
  ├───────────────────────────┼──────────┼──────────────┼──────────────────┤
  │ Estudio de escala         │ 80k y    │ 1.600, 6.400 │ de 2.6 a 167     │
  │                           │ 320k     │  y 25.600    │                  │
  ├───────────────────────────┼──────────┼──────────────┼──────────────────┤
  │ Composición, variante de  │ 20k      │ 400          │ 10               │
  │ pocos datos               │          │              │                  │
  └───────────────────────────┴──────────┴──────────────┴──────────────────┘

  El máximo de datos que se generó fue 320k partidas, y solo para π=0 y las
  condiciones del estudio de escala. Ninguna corrida fue de una sola pasada: la
  más cercana fue 320k con 1600 pasos, que vio cada partida 2.6 veces.

  Comparado con lo que estamos calculando, 8M partidas para el piloto es 25
  veces el dataset más grande de los preliminares y 100 veces el que se usó en
  la grilla principal. Es el salto que corresponde: los preliminares estaban
  diseñados para correr en una noche en la Mac, con 20 minutos de generación por
  dataset de 80k.

✻ Worked for 10s · done Sunday 20 Sep at 3:49 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores en Connect 4, y acabamos de fijar el régimen de datos: una pasada sin repetir partidas. Próximo paso: correr el piloto de 8M partidas en π=0 para medir dónde satura.

❯ que mostró el estudio a escala diferente respecto a cuando teníuamo 80K       
  partidas?                                                                     

⏺ Cuatro cosas, todo en π=0 y con una sola semilla en las celdas de escala,
  evaluando el checkpoint final:

  1. Más datos, más ganancia. Con 320k partidas y 10 epochs el acierto a τ→0
  subió de 0.891 a 0.914, la ganancia sobre el experto de +0.040 a +0.062, y el
  score contra el bot experto de 0.69 a 0.80. Fue la mejor celda de toda la
  exploración.

  2. A pasos fijos, los datos no importaron. Con 1600 pasos, 80k y 320k dieron
  lo mismo, 0.891 y 0.888. El modelo estaba limitado por pasos. Los datos solo
  pagaron cuando se los dejó entrenar más.

  3. Más epochs sobre los mismos datos destruyó la ganancia, y con más datos eso
  llegó más tarde.

  ┌──────────┬────────┬────────┬─────────┬────────────────────┐
  │ Partidas │ Pasos  │ Epochs │ acc τ→0 │ Mínimo de val loss │
  ├──────────┼────────┼────────┼─────────┼────────────────────┤
  │ 80k      │ 1.600  │ 10     │ 0.891   │ paso 1600          │
  ├──────────┼────────┼────────┼─────────┼────────────────────┤
  │ 80k      │ 6.400  │ 42     │ 0.837   │ paso 2400          │
  ├──────────┼────────┼────────┼─────────┼────────────────────┤
  │ 80k      │ 25.600 │ 167    │ 0.835   │ paso 2400          │
  ├──────────┼────────┼────────┼─────────┼────────────────────┤
  │ 320k     │ 1.600  │ 2.6    │ 0.888   │ paso 1600          │
  ├──────────┼────────┼────────┼─────────┼────────────────────┤
  │ 320k     │ 6.400  │ 10     │ 0.914   │ paso 6000          │
  ├──────────┼────────┼────────┼─────────┼────────────────────┤
  │ 320k     │ 25.600 │ 42     │ 0.865   │ paso 8400          │
  └──────────┴────────┴────────┴─────────┴────────────────────┘

  El experto acierta 0.845. Con 80k, a 42 epochs el modelo ya está por debajo
  del experto. Con 320k, a 42 epochs todavía está por encima, pero cayendo.

  4. La ganancia se reparte distinto entre estados vistos y no vistos según los 
  datos.

  ┌──────────┬────────┬────────────────┬────────┬───────────┬────────────────┐
  │ Partidas │ Epochs │ Ganancia total │ Vistos │ No vistos │ Fracción vista │
  ├──────────┼────────┼────────────────┼────────┼───────────┼────────────────┤
  │ 20k      │ 10     │ −0.031         │ +0.060 │ −0.093    │ 0.41           │
  ├──────────┼────────┼────────────────┼────────┼───────────┼────────────────┤
  │ 80k      │ 10     │ +0.040         │ +0.092 │ −0.006    │ 0.47           │
  ├──────────┼────────┼────────────────┼────────┼───────────┼────────────────┤
  │ 320k     │ 2.6    │ +0.035         │ +0.070 │ −0.004    │ 0.53           │
  ├──────────┼────────┼────────────────┼────────┼───────────┼────────────────┤
  │ 320k     │ 10     │ +0.062         │ +0.090 │ +0.030    │ 0.53           │
  └──────────┴────────┴────────────────┴────────┴───────────┴────────────────┘

  En estados vistos el voto llega al techo teórico de +0.055 desde 20k y no se
  mueve más. En estados no vistos el imitador pasa de ser peor que el experto a
  igualarlo y recién a 320k a superarlo. Todo el crecimiento con datos viene de
  los estados nuevos: es denoising por generalización, y necesita cuatro veces
  los datos con que satura el voto.

  Un detalle lateral: el acierto a τ=1 subió con los datos, 0.763, 0.789, 0.807,
  pero nunca alcanzó al experto. La distribución aprendida sigue siendo más
  plana que los datos incluso con 320k.

  Lo que esto dice para el piloto de 8M: la pregunta abierta es si la curva de
  los no vistos sigue subiendo hasta el techo o se aplana antes. La exploración
  solo llegó a ver que empezó a subir.

✻ Brewed for 29s · done Sunday 20 Sep at 4:13 pm

❯ Por qué en e decomposición visto/no visto usamos 20K ?                        

⏺ Para tener un punto por debajo de 80k y armar una curva en función de los
  datos con tres puntos separados por un factor 4: 20k, 80k, 320k. La base era
  80k, que ya estaba corrida, y se agregó un paso hacia abajo y otro hacia
  arriba en escala logarítmica.

  El punto de 20k resultó el más informativo de los tres, por una razón que no
  se anticipó: es la celda donde el imitador no trasciende en total, −0.031, y
  sin embargo en los estados vistos ya está en el techo teórico, +0.060. Es la
  demostración más limpia de que la ganancia por voto vive en los estados que se
  repiten y que el total puede ocultarla cuando los estados nuevos, donde el
  modelo es peor que el experto, pesan más. Si solo hubiéramos tenido 80k y
  320k, ambos con ganancia total positiva, el argumento sería menos nítido.

  También fue barato: 20k partidas son 5 minutos de generación y 400 pasos de
  entrenamiento, con 3 semillas.

  Para la versión de la tesina, con el piloto de una pasada, esta descomposición
  sale gratis de los checkpoints intermedios: cada checkpoint a S pasos es un
  modelo entrenado con S × 512 partidas frescas, así que la curva de visto/no
  visto en función de los datos se lee de una sola corrida en vez de tres.

✻ Crunched for 19s · done Sunday 20 Sep at 4:13 pm

❯ está bien que escriba esto en las notas del experimento 1?                    
  - Epochs: XXX                                                                 
    - Los experimentos preliminaron usaron 10 epoch con 80K partidas. Y por eso 
  nosotros debemos adoptar early stopping: valuar el checkpoint de mejor val    
  loss, no el final.                                                            
    - [1] entrena menos de una época, por eso no tiene riesgo de memorización.  
    - Un estudio de control con 320K muestra resultados todavía mejores que con 
  80K partidas, lo que indica que debimos haber generado más datos para         
  disminuir las epochs.                                                         
    - Nosotros tecnicamente podríamos generar suficientes datos como para no    
  tener que repetir partida. No es claro hasta qué punto generar datos tiene    
  sentido. La Chinchilla Laws para este tamaño de modelo da 5.5M                

⏺ Está bien en la dirección, pero tiene tres imprecisiones que Pablo va a
  marcar. Van y después te dejo una versión corregida.

  1. La causa del early stopping no son los 10 epochs. Los 10 epochs no fueron
  el problema; de hecho cayeron antes de la memorización y dieron el mejor
  resultado a 80k. El problema es repetir partidas, y la evidencia es que a 42
  epochs la ganancia desaparece. Early stopping es la respuesta a eso.

  2. El estudio de 320k no es de control, es de escala, y la lectura es más 
  fina. A igual cantidad de pasos, 1600, dio lo mismo que 80k. Mejoró solo
  cuando se lo dejó entrenar 6400 pasos, que con 80k ya hubieran sido 42 epochs.
  O sea: más datos sirven porque permiten más pasos sin memorizar, no por sí
  mismos. Y fue una semilla, evaluando el checkpoint final.

  3. Chinchilla es una heurística de modelos de lenguaje, no una ley para este 
  dominio. Vale como orden de magnitud y coincide con lo empírico, pero la
  respuesta la da el piloto.

  Versión corregida, en tu formato:

  - Regla de parada y cantidad de datos: TODO definir con el piloto
      - Los preliminares repitieron datos: 80k partidas × 10 epochs (1600 pasos 
  × 512).
        Repetir partidas expone a memorización: con los mismos 80k, a 42 epochs 
  el
        acierto a τ→0 cae de 0.891 a 0.837, por debajo del experto (0.845). El 
  modelo
        memoriza las partidas con sus errores y el argmax deja de ser el voto.
        Por eso adoptamos early stopping: evaluar el checkpoint de menor val 
  loss, no el final.
      - [1] ve cada partida a lo sumo una vez (menos de una época sobre ~10⁹ 
  partidas),
        así que no puede memorizar partidas concretas y no necesita regla de 
  parada.
      - Estudio de escala (π=0, 1 semilla, checkpoint final): con 320k partidas 
  y 10 epochs
        (6400 pasos) la ganancia sube de +0.040 a +0.062. A igual cantidad de 
  pasos (1600)
        da lo mismo que 80k. Lectura: más datos ayudan porque permiten más pasos
  sin
        memorizar. Los preliminares estaban limitados por pasos y después por 
  datos.
      - Como los datos son sintéticos, podemos generar suficientes para una sola
  pasada,
        como [1]: partidas = pasos × batch. Con batch 512, 16k pasos requieren 
  8.2M partidas.
        No sabemos dónde satura el modelo con datos frescos: con 320k seguía 
  aprendiendo
        cuando lo cortó la memorización (paso 8400). La heurística de Chinchilla
        (20 tokens/parámetro) da ~5.5M partidas; es una regla de LMs, sirve como
  orden de magnitud.
      - Piloto: 8M partidas en π=0, una pasada de 16k pasos, checkpoint cada 
  500,
        medir ganancia total y visto/no visto. S* = paso donde la ganancia se 
  aplana.
        N de la grilla = 1.2 × S* × 512.

✻ Churned for 31s · done Sunday 20 Sep at 4:16 pm
❯ Algo que no entiendo es que es semilla acá                                    
  > Por celda y semilla: 80k partidas de entrenamiento, alrededor de 1.6M       
  estados, y 3k partidas de test con semilla distinta, alrededor de 60k         
  estados.La semilla varía dataset, inicialización y orden de batches.          
  explicamelo de manera mas especifica y concreta                               

⏺ Una semilla es el número con el que se inicializa el generador de números
  aleatorios. Fijarla hace que todo lo "aleatorio" de una corrida sea
  reproducible: misma semilla, mismo resultado exacto. Cambiarla es repetir el
  experimento con otro sorteo.

  En nuestro experimento el azar entra en tres lugares, y la semilla los
  controla a los tres:

  1. Generación de datos. En cada estado no trivial, si el experto erra o no, y
     qué jugada errónea elige cuando el error es idiosincrático. Con otra
     semilla salen otras 80k partidas, generadas por la misma población de
     expertos con los mismos parámetros ρ y P, pero distintas partida por
     partida.
  2. Inicialización del modelo. Los pesos iniciales del transformer se sortean.
     Otra semilla, otro punto de partida.
  3. Orden de los batches. En qué orden se recorren las partidas durante el
     entrenamiento.

  Ejemplo concreto. La celda P=0.5 con 3 semillas son estas tres corridas
  independientes:

  ┌───────────┬─────────────────────┬────────────┬───────────┬────────────┐
  │  Corrida  │     Dataset de      │   Pesos    │ Orden de  │    Test    │
  │           │    entrenamiento    │ iniciales  │  batches  │            │
  ├───────────┼─────────────────────┼────────────┼───────────┼────────────┤
  │ P=0.5,    │ 80k partidas        │            │           │ mismo test │
  │ semilla 1 │ sorteadas con       │ sorteo 1   │ sorteo 1  │  para las  │
  │           │ semilla 1           │            │           │ tres       │
  ├───────────┼─────────────────────┼────────────┼───────────┼────────────┤
  │ P=0.5,    │ otras 80k con       │ sorteo 2   │ sorteo 2  │ mismo test │
  │ semilla 2 │ semilla 2           │            │           │            │
  ├───────────┼─────────────────────┼────────────┼───────────┼────────────┤
  │ P=0.5,    │ otras 80k con       │ sorteo 3   │ sorteo 3  │ mismo test │
  │ semilla 3 │ semilla 3           │            │           │            │
  └───────────┴─────────────────────┴────────────┴───────────┴────────────┘

  El test son 3k partidas generadas por los mismos expertos de P=0.5 pero con
  una semilla propia, distinta de las tres de entrenamiento, para que ninguna
  partida de test esté literalmente en el entrenamiento. Que un tablero de test
  aparezca igual en entrenamiento por otra partida es otra cosa, y es justamente
  lo que mide la etiqueta visto/no visto. Uso el mismo test para las tres
  semillas para que las diferencias entre ellas sean del modelo, no de los
  estados evaluados.

  Para qué sirve: cada celda reporta media y desvío entre sus 3 corridas. Si la
  ganancia en P=0.25 es +0.027 y en P=0.5 es +0.015, con desvíos de 0.002, la
  diferencia es real. Si los desvíos fueran 0.02, no podríamos distinguirlas. En
  la exploración los desvíos fueron de 0.001 a 0.005, muy por debajo de las
  diferencias entre celdas.

  Una aclaración: en la exploración no tengo confirmado que las 3 semillas
  cambiaran también el dataset o solo el entrenamiento. Lo que escribí es la
  propuesta para la tesina: variar los tres, porque es lo más exigente y lo que
  cualquier revisor asume.

✻ Cooked for 27s · done Sunday 20 Sep at 4:22 pm

❯ Y que hizo [1]?                                                               

⏺ [1] no repitió entrenamientos. Entrenó un modelo por corte de rating,
  ChessFormer 1000, 1300 y 1500, una sola vez cada uno. Los datos son partidas
  reales, así que no hay semilla de generación, y no reportan haber variado la
  inicialización.

  La incertidumbre que muestran es toda de evaluación, no de entrenamiento:

  - El rating Glicko-2 viene con su desvío RD, y reportan R ± 2·RD como
    intervalo del 95 %. Sale de 100 partidas contra cada uno de tres niveles de
    Stockfish, 300 partidas por temperatura.
  - Las bandas de la Figura 1 son ±1.96σ sobre ese mismo rating.
  - La Tabla 1 con la función favor usa bootstrap de 10.000 remuestreos sobre
    100 partidas a τ=0.001.

  Eso responde "cuánto varía el rating de este modelo según las partidas que le
  tocaron", no "cuánto variaría el modelo si lo entrenara de nuevo". Con 6 a 12
  horas de H100 por modelo, repetir era caro. [2] hace lo mismo: una corrida por
  configuración, sin semillas reportadas.

  Para nosotros esto tiene dos consecuencias. Primero, con 3 semillas por celda
  estamos siendo más estrictos que ambos papers, y conviene decirlo. Segundo,
  tenemos que reportar las dos fuentes de incertidumbre por separado: la de
  entrenamiento, con el desvío entre semillas, y la de evaluación, que en las
  métricas desde logits es casi nula porque evaluamos 60k estados sin muestrear,
  y en las partidas cabeza a cabeza se estima como en [1], con intervalo sobre
  las 300 partidas.

✻ Sautéed for 20s · done Sunday 20 Sep at 4:24 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores P, aclarando cada decisión antes de escribir experimento1-v1.md. Próximo paso: que confirmes las decisiones abiertas para que arranque el .md.

❯ mmm voy a anotar que para el experimento 1 no hagamos repeticiones de         
  experimento mi objetivo es alinearme con [1] y no hacer complejidad al pedo   
  Hacerlo con varias semillas puede tener sentido en un contexto dónde el split 
  de entrenamiento / test puede cambiar los resultados pero no en deep          
  learning con la cantidad de datos que manejamos y el split aleatorio          
  propuesto es insignificante                                                   

⏺ Es tu decisión y es pragmática, pero corregiría la justificación, porque tal
  como está escrita Pablo la puede objetar. Dos problemas:

  1. No hay split. El test no es una partición del dataset, es una generación
  aparte con su propia semilla. Así que el argumento de "el split aleatorio es
  insignificante" no aplica a nuestro diseño.

  2. Las semillas no son solo por los datos. En deep learning la variabilidad
  entre corridas viene también de la inicialización y del orden de los batches,
  y para efectos chicos sí importa. Ese es justamente nuestro caso: las
  diferencias entre celdas vecinas son de 0.01 a 0.02 en E[r].

  La justificación fuerte está en los datos de la exploración, y es la que
  anotaría:

  - Semillas: una corrida por celda, como [1] y [2], que entrenan un modelo por 
  configuración
    y reportan incertidumbre solo de evaluación.
      - Justificación empírica: en los preliminares se corrieron 3 semillas por 
  celda y el
        desvío entre semillas fue de 0.001 a 0.005 en E[r], contra diferencias 
  entre celdas
        vecinas de 0.01 a 0.02. El ruido de entrenamiento es 3 a 10 veces menor 
  que el efecto.
      - Con datasets de millones de partidas en una sola pasada, la varianza por
  muestreo de
        datos es menor todavía.
      - La incertidumbre de evaluación se reporta como en [1]: las métricas 
  desde logits se
        calculan sobre ~60k estados sin muestreo; las partidas cabeza a cabeza 
  con intervalo
        sobre 300 partidas.
      - Salvaguarda: si dos celdas quedan a menos de 0.005, se agregan semillas 
  solo para ese par.

  Con eso te alineás con [1], ahorrás tres veces el cómputo, y tenés una
  respuesta cuando pregunten por qué una sola corrida.

✻ Cooked for 22s · done Sunday 20 Sep at 4:28 pm

❯ Bien ahora vamos a escribir el diseño de experimento, esto que pusiste mas    
  arriba no lo entiendo:                                                        
  > Dos parámetros: tasa total de error ρ_tot fija en todas las celdas, y       
  fracción compartida π ∈ {0, 0.25, 0.5, 0.75, 1}. La tasa independiente q se   
  calibra por celda para que la tasa total realizada quede constante. Así la    
  única variable que cambia entre celdas es la estructura del error, no la      
  cantidad.                                                                     
  > El experimento que planeo hacer ahora como primero es agarrar el juego      
  propuesto Connect4 y entrenar un modelo en partidas sintéticas. En esas       
  partidas sintéticas son generadas por varios expertos. Esos expertos tienen   
  una probabilidad de equivocarse. Equivocarse es hacer una jugada perdedora.   
  Cuando se equivocan tienen P probabilidad de hacer un error compartido y      
  (1-P) un tipo de error que solo ellos hacen                                   
  >  Todavía estoy viendo un poco como definir un error compartido vs el que    
  solo ellos hacen pero tengo varias alternativas en mente                      
  >  La idea es variar P y ver como eso mejora la calidad de juego del modelo   
  entrenado (entendida como la accuracy en cada jugada jugando contra un        
  perfect player, accuracy es fácil de calcular porque sabemos que jugadas son  
  ganadoras y perdedoras )                                                      

⏺ Es tu misma descripción, con letras. Traduzco:

  - Tu "probabilidad de equivocarse" es ρ. La fijamos en 0.3 en todas las
    celdas.
  - Tu P es lo que llamé π. Es la única perilla que se barre.
  - q no es un parámetro nuevo: es un número derivado de ρ y P para que las
    cuentas cierren.

  El experto, en un estado no trivial e, hace esto:

  1. Si e pertenece al conjunto de estados sesgados B, juega la jugada errónea
     compartida w(e). Todos los expertos hacen lo mismo ahí.
  2. Si no, tira una moneda: con probabilidad q juega una jugada errónea al
     azar, con 1−q juega la óptima.

  B es un conjunto fijo que cubre una fracción β de los estados no triviales.
  Ahora las dos condiciones que queremos:

  - Tasa total de error = ρ. La tasa total es β + (1−β)·q, porque errás seguro
    en B y con probabilidad q afuera. Queremos que dé 0.3.
  - Fracción compartida = P. De todos los errores, los compartidos son β sobre
    ρ. Queremos que dé P.

  De la segunda sale β = P·ρ. De la primera sale q = (ρ − β)/(1 − β). Con
  números:

  ┌──────┬────────────────┬───────────────────────────────────┬────────────┐
  │  P   │ β, medida de B │ q, error independiente fuera de B │ tasa total │
  ├──────┼────────────────┼───────────────────────────────────┼────────────┤
  │ 0    │ 0              │ 0.300                             │ 0.30       │
  ├──────┼────────────────┼───────────────────────────────────┼────────────┤
  │ 0.25 │ 0.075          │ 0.243                             │ 0.30       │
  ├──────┼────────────────┼───────────────────────────────────┼────────────┤
  │ 0.5  │ 0.150          │ 0.176                             │ 0.30       │
  ├──────┼────────────────┼───────────────────────────────────┼────────────┤
  │ 0.75 │ 0.225          │ 0.097                             │ 0.30       │
  ├──────┼────────────────┼───────────────────────────────────┼────────────┤
  │ 1    │ 0.300          │ 0                                 │ 0.30       │
  └──────┴────────────────┴───────────────────────────────────┴────────────┘

  Eso es "calibrar q por celda": la última columna queda constante.

  Por qué hace falta. Si dejaras q = 0.3 fijo y le sumaras los estados sesgados
  encima, la tasa total sería 0.3 + 0.7·β y crecería con P. El experto de P=1
  erraría el doble que el de P=0. Entonces, cuando la trascendencia cayera con
  P, no podrías decir si fue porque los errores están más correlacionados o
  porque simplemente hay más errores. Fijar la tasa total elimina esa
  ambigüedad: entre celdas cambia solo la estructura del error, no la cantidad.
  Es el argumento de diversidad de Zhang, que ellos no pudieron hacer con datos
  humanos.

  Verificación. Podés chequear que esto reproduce tu descripción condicional: la
  probabilidad de errar es ρ, y dado que erró, la probabilidad de que el error
  sea el compartido es β/ρ = P. La única diferencia con tu frase es que "hacer
  un error compartido" no lo decide una moneda del experto sino el estado en el
  que está. Y "realizada" quiere decir que después de generar medimos en el test
  que la tasa total y la fracción compartida dieron efectivamente 0.3 y P, en
  vez de confiar en la fórmula.

✻ Brewed for 33s · done Sunday 20 Sep at 4:29 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de correlación de errores P en Connect 4, aclarando cada decisión antes de escribir experimento1-v1.md. Próximo paso: seguir con el diseño y volcar lo acordado al .md.

❯ que significa celda en es econtexto? son estados?                             

⏺ No, no son estados. Celda es una configuración experimental: una combinación
  concreta de valores de los parámetros que se barren. Viene de pensar el
  experimento como una tabla o grilla, donde cada casillero es una condición a
  correr.

  En el experimento 1 el único parámetro que se barre es P, así que hay cinco
  celdas: P=0, P=0.25, P=0.5, P=0.75 y P=1. Cada celda tiene su propio dataset
  generado con esos parámetros, su propio modelo entrenado, y sus propias
  métricas. "Calibrar q por celda" quiere decir que para cada uno de esos cinco
  valores de P se calcula el q de la tabla.

  Si además barriéramos otro parámetro, por ejemplo tamaño de datos con dos
  valores, la grilla sería 5 × 2 = 10 celdas. Y en la exploración, cuando había
  3 semillas, cada celda tenía tres corridas.

  Si te resulta más claro para la tesina, se puede decir "condición" en vez de
  "celda". Es el término que usa la literatura de diseño experimental y no tiene
  la connotación de tabla.

✻ Churned for 13s · done Sunday 20 Sep at 4:34 pm

❯ ρ y ρ_tot es lo mismo?                                                        

⏺ Sí, es lo mismo. Le puse el subíndice "tot" en el primer mensaje para
  distinguirla de la q, que es la tasa de error solo fuera de los estados
  sesgados, y de la ρ de la fórmula de Pablo, que es una correlación y no una
  tasa. Después lo dejé caer y quedó inconsistente.

  Para el .md propongo fijar una notación y no moverla más:

  - ρ: tasa total de error del experto sobre estados no triviales. Fija en 0.3.
  - P: fracción de esos errores que son compartidos. La perilla que se barre.
  - β = P·ρ: medida del conjunto de estados sesgados.
  - q = (ρ − β)/(1 − β): tasa de error independiente fuera de los estados
    sesgados. Derivada, no elegida.
  - r_Pearson: correlación medida entre los vectores de error de dos expertos.
    Es lo que Pablo llama ρ; conviene no usar esa letra para evitar el choque.

  Uso P y no π porque es la letra que ya venís usando y no se confunde con el
  número.

✻ Sautéed for 18s · done Sunday 20 Sep at 4:35 pm

❯ - En la literatura se usa hablar de "celda" o fue un invento tuyo?            
  - Por que la elección de 0.3 para ρ ?                                         

⏺ "Celda" es estándar en diseño de experimentos, no en papers de ML. En
  estadística, en diseños factoriales y ANOVA, cada combinación de niveles de
  los factores es una cell del diseño, y se habla de cell means. Zhang y Abreu
  no la usan: dicen setting o configuration. En la tesina yo usaría "condición"
  en el texto y reservaría "celda" para cuando hables de la tabla de resultados,
  donde sí es natural.

  ρ = 0.3 fue un default de la exploración, sin justificación registrada. Pero
  hay una justificación a posteriori que vale escribir, con una cota dura y dos
  criterios blandos:

  - **Cota dura: ρ < 0.5.** El voto por mayoría solo puede recuperar la jugada
    óptima si la mezcla le pone más masa que a cualquier jugada errónea. El peor
    caso es un estado no trivial con una sola jugada errónea disponible: ahí
    toda la masa de error
    ρ va a esa jugada, y el argmax es óptimo si y solo si 1−ρ > ρ. Con ρ ≥ 0.5
    la teoría deja de predecir trascendencia incluso en P=0, y el experimento
    pierde el control positivo.
  - Efecto medible. La ganancia teórica por denoising a P=0 es del orden de la
    tasa de error independiente realizada. Con ρ=0.3 nominal eso son unos 0.15
    de acierto, cómodo de medir contra desvíos de 0.005. Con ρ=0.1 el efecto
    sería 0.05 y el barrido en P se comprimiría en cinco puntos casi
    indistinguibles.
  - El experto sigue siendo experto. A ρ=0.3 el experto acierta 0.845 y le gana
    cómodo a un jugador aleatorio. Con ρ cerca de 0.5 sería un jugador mediocre
    y el título "supera al experto" perdería fuerza.

  Un detalle de la cota: la sección anterior del pipeline aplicaba ρ solo donde
  hay error posible, así que el ρ que entra en la cota es el de los estados no
  triviales, que es como lo definimos.

  Lo que no cubre esta justificación es cómo cambia la curva en P con ρ. Abreu
  barre su equivalente, la cobertura c, y en la fórmula de Pablo la tasa de
  error es la σ². Lo natural es fijar ρ en 0.3 para el experimento 1 y correr el
  barrido en P a un ρ distinto, por ejemplo 0.15, como ablación en el paso 6.
  Si Pablo lo pide antes, es una columna más en la grilla.

✻ Cogitated for 38s · done Sunday 20 Sep at 4:36 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido de la fracción P de errores compartidos entre expertos en Connect 4, y venís aclarando cada decisión antes de escribir el .md. Siguiente paso: redactar juntos experimento1-v1.md con las secciones de diseño.

❯ que es un estado trivial?                                                     

⏺ Un estado donde no se puede errar: todas las jugadas legales llevan al mismo
  valor. Formalmente, e es trivial si r(e, c) = v(e) para toda columna legal c.
  El caso opuesto, estado no trivial, es el que tiene al menos una jugada peor
  que la mejor, y solo ahí tiene sentido hablar de error de un experto.

  Los tres casos concretos en Connect 4:

  - Posición perdida. Con juego perfecto del rival perdés hagas lo que hagas.
    Todas las jugadas valen 0. Es el caso trivial más frecuente, porque el
    segundo jugador está perdido desde la jugada 1 contra un rival perfecto, y
    muchas posiciones de mediojuego ya están decididas.
  - Posición ganada donde todas las jugadas siguen ganando. Vale 1 juegues donde
    juegues. Pasa por ejemplo cuando tenés dos amenazas que el rival no puede
    parar.
  - Tablas forzadas por cualquier lado. Raro en Connect 4, pero posible cerca
    del final.

  Y un estado no trivial es, por ejemplo, una posición ganada donde solo una
  columna conserva la victoria y las otras la tiran: ahí el experto puede errar,
  y el error cuesta.

  Por qué importa para el diseño: en las partidas entre expertos cerca de la
  mitad de los estados visitados son triviales. Por eso definimos ρ sobre los no
  triviales, y por eso la accuracy se mide solo ahí. Contar aciertos en estados
  triviales inflaría el acierto de cualquier política, incluso la aleatoria.

✻ Worked for 20s · done Sunday 20 Sep at 5:00 pm

❯ β es la probabilidad de error compartido?                                     

⏺ Sí, con una precisión: β es la probabilidad de que un estado no trivial sea un
  estado sesgado, y en un estado sesgado el error compartido ocurre con
  certeza. Entonces β es también la probabilidad de error compartido por estado
  no trivial, y las dos lecturas coinciden.

  Lo que β no es: una probabilidad que el experto sortea. El experto no decide
  "ahora cometo el error compartido"; el estado ya está marcado como sesgado o
  no, igual para todos. Por eso lo llamé "medida del conjunto de estados
  sesgados": es la fracción de estados no triviales que caen en B.

  Los tres números, uno al lado del otro, por estado no trivial:

  - β = P·ρ: probabilidad de error compartido. Igual para todos los expertos en
    el mismo estado.
  - (1−β)·q: probabilidad de error independiente. Cada experto lo sortea por su
    cuenta.
  - ρ = β + (1−β)·q: probabilidad de error total.

✻ Cooked for 16s · done Sunday 20 Sep at 5:16 pm

❯ cual sería la definición de estado sesgado?                                   
⏺ Definición abstracta. Un estado sesgado es un estado no trivial que pertenece
  a un conjunto fijo B, elegido de antemano, en el que todos los expertos juegan
  la misma jugada errónea w(e). Dos propiedades lo definen:

  - B está fijo: es el mismo conjunto para todos los expertos y todas las
    partidas. Por eso los errores coinciden en ocurrencia.
  - w(e) está fija: es una función del estado, la misma para todos. Por eso los
    errores coinciden en dirección.

  Y B cubre una fracción β = P·ρ de los estados no triviales.

  Definición concreta que propongo. Falta elegir B y w, y acá entra la decisión
  de que sean representables:

  - B por índice de jugada. Un estado está en B si el número de jugada t cumple
    t mod 20 ∈ S, donde S es un conjunto de residuos de tamaño 20·β, repartidos
    de forma pareja para que las fases del juego queden cubiertas por igual.
    Para P=0.5 y ρ=0.3, β=0.15, S tiene 3 residuos, por ejemplo {0, 7, 14}. Para
    P=1, β=0.3, 6 residuos. Para P=0, S es vacío.
  - w(e) = la columna legal más a la izquierda que no sea óptima. Si el estado
    es no trivial, esa columna existe.

  Con esto, un experto en el estado e de la jugada t hace: si e es trivial,
  juega cualquier jugada; si t mod 20 ∈ S, juega w(e); si no, sortea el error
  independiente con probabilidad q.

  Por qué esta y no otra. El índice de jugada lo tiene el modelo directamente en
  el embedding posicional, así que puede aprender exactamente cuándo está en B.
  La exploración mostró que una regla así, "cada 3 jugadas", se reproduce a
  tres decimales. La alternativa de la exploración, definir B por un hash del
  tablero, hace que B sea imposible de aprender, y el modelo deshace el error
  compartido en estados nuevos. Eso confunde correlación con representabilidad,
  que es otro experimento.

  Un detalle para la medición: la regla del índice de jugada no sabe si el
  estado es trivial, así que la fracción de estados no triviales que caen en B
  es aproximadamente 20·β sobre 20, no exactamente. Por eso β se reporta
  realizada, midiendo en el test qué fracción de los estados no triviales
  efectivamente cayó en B.

✻ Cogitated for 21s · done Sunday 20 Sep at 5:17 pm

※ recap: Estamos definiendo el diseño del experimento 1 de la tesina, el barrido de la fracción P de errores compartidos, aclarando notación y decisiones antes de escribir experimento1-v1.md. Próximo paso: seguir con la definición de expertos y empezar el .md.

❯ - por qué el numero 20?                                                       

⏺ Fue una elección rápida y, mirándola con tus números, está mal para dos de las
  cinco condiciones. Te cuento el razonamiento y la corrección.

  La idea detrás del 20. Quería un período más corto que la partida, que dura
  hasta 42 jugadas y 21 en promedio, para que los estados sesgados aparezcan en
  apertura, medio y final, y no concentrados en una fase. Y quería que 20·β
  fuera entero, para que S tenga una cantidad exacta de residuos.

  El problema. Con ρ=0.3, los β de la grilla son 0, 0.075, 0.15, 0.225 y 0.3.
  Multiplicados por 20 dan 0, 1.5, 3, 4.5 y 6. Para P=0.25 y P=0.75 no hay
  cantidad entera de residuos. Además, el módulo hace algo que no queremos: como
  las partidas son de a lo sumo 42 jugadas, "mod 20" apenas se repite dos
  veces, y las jugadas tardías se visitan mucho menos que las tempranas, así que
  la fracción realizada de estados sesgados no sería |S|/20 de todas formas.

  Corrección: dejar el módulo y definir S como un conjunto fijo de números de 
  jugada. Un estado está en B si su número de jugada t ∈ S, con S ⊂ {1, …, 42}.
  Se elige S así:

  1. Con un dataset piloto de la población, medir qué fracción de los estados no
     triviales visitados ocurre en cada jugada t.
  2. Elegir S, repartido de forma pareja entre fases, de modo que la suma de
     esas fracciones sobre t ∈ S sea β.

  Sigue siendo una regla trivialmente representable, "estoy en la jugada t", y
  la calibración garantiza que β realizado sea el de la tabla para cualquier P y
  cualquier ρ, sin restricciones de divisibilidad. El piloto que ya vamos a
  correr para la saturación sirve para esta medición.

  La alternativa más simple, si no querés calibrar, es cambiar ρ a 0.4 para que
  20·β dé entero. Pero ataca el síntoma y no el problema de la visitación
  desigual. Prefiero la calibración.

✻ Worked for 34s · done Sunday 20 Sep at 7:11 pm

❯ Luego los expertos jugarán:                                                   
      - Si e es trivial, juega cualquier jugada                                 
      - Si e es no trivial:                                                     
          - Si t \in S juega w(e)                                               
          - Sino sortea el error independiente con probabilidad q.              
  ?                                                                             

⏺ Sí, es exactamente eso. Le agregaría tres precisiones para que quede sin
  ambigüedad en el .md:

  Dado un estado e en la jugada t, el experto juega:
      - Si e es trivial: una jugada legal uniforme al azar. Todas valen lo 
  mismo,
        pero hay que fijar cómo se elige porque afecta qué estados se visitan 
  después.
      - Si e es no trivial:
          - Si t ∈ S: juega w(e), la columna legal más a la izquierda que no es 
  óptima.
          - Si t ∉ S: con probabilidad q juega una jugada errónea uniforme al 
  azar
            entre las no óptimas; con probabilidad 1−q juega una jugada óptima,
            uniforme al azar si hay varias.

  Los tres agregados: cómo se elige en estados triviales, qué distribución tiene
  el error independiente, y qué pasa cuando hay más de una jugada óptima. Los
  tres son sorteos que la semilla controla.

  Y una observación que conviene escribir al lado: esta política es una única
  distribución f(c | e) para toda la población. Un "experto" es una muestra de
  esa distribución en cada jugada. Por eso la cantidad de expertos no aparece
  como parámetro, y por eso la mezcla que aprende el imitador es directamente f.

✻ Cooked for 15s · done Sunday 20 Sep at 7:22 pm

❯ P y π  es lo mismo?                                                           

⏺ Sí, es lo mismo. π fue la letra que usó la exploración y que yo arrastré en
  los primeros mensajes; P es la tuya. Hace unos mensajes propuse quedarnos con
  P para el .md y no volver a usar π. Donde veas π en lo que escribí antes, leé
  P.

✻ Brewed for 7s · done Sunday 20 Sep at 7:22 pm

❯ mi pregunta es si no es problemático que cuando t not in S igual se puede     
  elegir w(e) (error compartido) ya que se elije una errónea "al azar"          

⏺ No es problemático para el mecanismo, solo para la contabilidad. Y la
  contabilidad se arregla con la definición.

  Por qué no afecta al mecanismo. Lo que decide si el voto funciona es la masa
  que la mezcla pone en cada jugada en el estado e. Fuera de S, con m jugadas
  erróneas disponibles:

  - jugada óptima: 1 − q
  - cada jugada errónea, incluida w(e): q / m

  w(e) no recibe nada especial. Es una más entre las erróneas, con la misma masa
  que las otras. El argmax sigue siendo óptimo mientras 1 − q > q/m, que vale
  siempre que q < 0.5. Lo que hace "compartido" a un error no es qué columna se
  juega sino que todos los expertos la jueguen en ese estado, y eso solo pasa
  dentro de S. Fuera de S, que dos expertos coincidan en w(e) es coincidencia
  con probabilidad q²/m², igual que coincidir en cualquier otra errónea.

  Un caso límite lo hace evidente: en un estado con una sola jugada errónea, m =
  1, el error independiente es necesariamente w(e). No hay otra. Y el voto
  igual la elimina, porque la óptima tiene masa 1 − q.

  Dónde sí importa: al medir. Si contaras como "error compartido" cada vez que
  se jugó w(e), estarías sumando una fracción q/m de los errores independientes
  como si fueran compartidos, y β realizado te quedaría inflado. Por eso la
  definición operativa tiene que ser por pertenencia, no por jugada: error
  compartido es un error cometido en un estado con t ∈ S; error independiente es
  un error cometido con t ∉ S. Con eso las tasas realizadas se miden bien y la
  correlación de Pearson también.

  La alternativa que no recomiendo. Excluir w(e) de las opciones del error
  independiente. Haría los dos tipos disjuntos en dirección, pero en los estados
  con m = 1 el error independiente se volvería imposible y la q realizada
  bajaría justo en esos estados, de forma no uniforme. Es cambiar una prolijidad
  estética por un sesgo real.

✻ Crunched for 26s · done Sunday 20 Sep at 7:27 pm

❯ me explicarías que es q?                                                      
  noes simplemente (ρ − β)                                                      
  explicame con un ejemplo en concreto                                          

⏺ q es la probabilidad de errar dado que estás fuera de S. ρ − β es otra cosa:
  la fracción de todos los estados no triviales donde ocurre un error
  independiente. La diferencia es sobre qué total estás dividiendo.

  Ejemplo concreto con 1000 estados no triviales, ρ = 0.3 y P = 0.5:

  1. Queremos 300 errores en total, porque ρ = 0.3.
  2. β = P·ρ = 0.15, así que 150 estados están en S. En todos ellos hay error
     compartido: 150 errores.
  3. Faltan 300 − 150 = 150 errores, que tienen que ser independientes.
  4. Pero los errores independientes solo pueden ocurrir en los 850 estados que
     están fuera de S.
  5. Para que en esos 850 estados haya 150 errores, la probabilidad de errar ahí
     tiene que ser 150 / 850 = 0.176. Eso es q.

  Si usaras q = ρ − β = 0.15, en los 850 estados de afuera habría 0.15 × 850 ≈
  128 errores, y el total sería 150 + 128 = 278, o sea ρ realizado 0.278 en vez
  de 0.3. La tasa total dejaría de ser constante entre condiciones, y bajaría
  más cuanto mayor fuera P.

  En fórmula: ρ − β es la cantidad de errores independientes sobre el total de
  estados; dividirlo por 1 − β lo convierte en probabilidad sobre los estados
  donde efectivamente se pueden cometer. Por eso q = (ρ − β)/(1 − β), y por eso
  q siempre es un poco mayor que ρ − β salvo en P = 0, donde coinciden.

✻ Churned for 15s · done Sunday 20 Sep at 7:28 pm

❯ *la probabilidad de errar dado que estás fuera de B                           
  No?                                                                           

⏺ Sí, tenés razón. B es el conjunto de estados sesgados; S es el conjunto de
  números de jugada que lo define. Un estado está en B si y solo si su jugada t
  está en S, así que "fuera de S" y "fuera de B" señalan lo mismo, pero lo
  correcto es hablar de estados y decir fuera de B. q es la probabilidad de
  errar dado que el estado no trivial está fuera de B.

  Para el .md conviene fijar: B para el conjunto de estados, S para el conjunto
  de jugadas que lo genera, y usar B siempre que se hable de probabilidades
  sobre estados.

✻ Baked for 8s · done Sunday 20 Sep at 7:29 pm

❯ En la nota dijiste                                                            
  Nota importante: la "regla del índice de jugada" no sabe si el estado es      
  trivial, así que la fracción de estados no triviales que caen en B no es      
  exactamente 20·β (es un aproximado). Por eso β se reporta realizada, midiendo 
  en el test qué fracción de los estados no triviales efectivamente cayó en B.  
  Por que 20?? de donde sale ese 20                                             

⏺ Ese 20 es un resto de la versión con "t mod 20" que ya descartamos, y además
  está mal escrito: debería haber dicho |S|/20, la cantidad de residuos sobre el
  período, no 20·β. Con la definición actual, donde S es un conjunto fijo de
  números de jugada calibrado con el piloto, el 20 desaparece por completo.

  La nota corregida:

  Nota: la regla "t ∈ S" no sabe si el estado es trivial ni cuántas veces se 
  visita
  cada jugada, así que la fracción de estados no triviales que caen en B no es
  |S|/42 sino la suma, sobre t ∈ S, de la fracción de estados no triviales 
  visitados
  en la jugada t. Por eso S se calibra con un dataset piloto para que esa suma 
  dé β,
  y β se reporta realizada, midiendo en el test qué fracción de los estados no
  triviales efectivamente cayó en B.

✻ Worked for 9s · done Sunday 20 Sep at 7:31 pm

※ recap: Estamos definiendo el diseño del experimento 1 de la tesina, el barrido de la fracción P de errores compartidos, y acabamos de fijar la notación de expertos, B, S, β y q. Próximo paso: volcar el diseño en experimento1-v1.md.

❯ Cuando le expliqué a granitto el problema le dije                             
  Cuando se equivocan tienen P probabilidad de hacer un error compartido y      
  (1-P) un tipo de error que solo ellos hacen                                   
  notar que es distinto " un tipo de error que solo ellos hacen" de lo que      
  hacemos que es un error aleatorio                                             
  Esto está bien? que hicimos en la exploracion preliminar con la que           
  construimos el papper ese generado y las slides?                              

  Searched for 1 pattern (ctrl+o to expand)

⏺ Confirmado en el código: la exploración usó error aleatorio, no "un tipo de
  error que solo ellos hacen". En el modo iid, cuando el experto erra elige una
  jugada no óptima uniforme al azar, sorteada de nuevo en cada visita, y el
  identificador de experto ni se usa. No hay expertos distinguibles: hay una
  sola política estocástica de la que cada jugada es una muestra. El paper y las
  slides describen exactamente eso, "choosing a uniformly random non-optimal
  move".

  Lo que le dijiste a Granitto admite dos lecturas, y conviene aclarárselo:

  - Lectura A, independiente. "Un error que solo ellos hacen" en el sentido de
    que en ese momento nadie más lo comete. Es lo que hicimos. Formalmente es la
    Proposición 3 de Zhang: un experto ruidoso con errores uniformes al azar.
    La cantidad de expertos no es un parámetro porque una población infinita de
    expertos así es indistinguible de un único experto estocástico.
  - Lectura B, persistente. Cada experto i tiene su propio sesgo fijo: en el
    estado e siempre juega su jugada errónea w_i(e). Es lo que sugiere la
    fórmula de Pablo, con n expertos y un ξ_i por cada uno, y es lo que un
    jugador humano hace: repite sus errores. Acá la cantidad de expertos K sí
    importa, porque en un estado repetido el voto es entre K opiniones fijas, y
    aparece el término 1/n.

  Está bien haber hecho A? Sí para el experimento 1, porque la pregunta es la
  correlación entre expertos y A es el extremo de correlación cero con la
  construcción más simple y ya validada. Pero el enunciado a Pablo se acerca más
  a B, y si él después ve "uniforme al azar" va a pensar que cambiamos el
  diseño. Lo resolvería con dos cosas:

  1. En el .md, definir el error independiente sin ambigüedad: "jugada no óptima
     uniforme al azar, sorteada en cada visita, independiente entre expertos y
     entre partidas". Y escribir al lado que la cantidad de expertos no es un
     parámetro por esa razón.
  2. Decirle a Pablo explícitamente que hay dos versiones del error
     idiosincrático, que el experimento 1 usa la independiente, y que la
     persistente con K expertos queda como 1b si le interesa el eje de la
     cantidad de expertos. Es mejor que lo sepa antes que lo descubra en la
     tabla.

  Si Pablo prefiere B para el experimento 1, el cambio en el generador es chico:
  w_i(e) se define por un hash del tablero y del identificador i, y cada
  partida la juegan dos expertos sorteados de los K. Lo que crece es la grilla,
  porque K se suma a P como eje.

✻ Sautéed for 40s · done Sunday 20 Sep at 7:37 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, el barrido en P de correlación de errores, aclarando cada decisión antes de escribir experimento1-v1.md. Próximo paso: definir con Pablo si el error idiosincrático es aleatorio o persistente y empezar el .md.

❯ No entiendo esto que habías escrito bastante más arriba                       
  > Dos distribuciones de test, porque la definición de trascendencia depende   
  de p_test y los dos papers usan una distinta:                                 
  >   - Estados visitados por los expertos: desde los logits, sin muestreo,     
  para τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}. Métricas: E[r],          
  probabilidad de jugada óptima, y ambas separadas en estados sesgados versus   
  no sesgados para verificar el mecanismo estado por estado.                    
  >   - Juego propio: 300 partidas contra el bot experto y contra el jugador    
  perfecto, colores alternados, cinco reintentos ante jugada ilegal, a τ→0 y    
  τ=1. Es el protocolo de Zhang.                                                
  >   - Baselines analíticos: mejor experto, argmax de la mezcla como techo     
  teórico, jugador perfecto, uniforme.                                          
  >   - Reporte estratificado por fase: apertura, medio, final. Y etiqueta      
  visto/no visto por tablero, que sale gratis de estas mismas corridas y        
  alimenta el objetivo 3 sin entrenar nada más.                                 
⏺ Lo desarmo en partes, con un ejemplo concreto.

  Por qué "la definición depende de p_test". Zhang define la recompensa de una
  política como el promedio de r sobre estados sorteados de una distribución
  p_test. Cambiás sobre qué estados promediás y cambia el número. Un modelo
  puede ser excelente en aperturas y flojo en finales: si p_test tiene muchas
  aperturas "trasciende", si tiene muchos finales no. Zhang promedia sobre los
  estados que aparecen en las partidas del propio modelo contra Stockfish, que
  es lo que mide un rating. Abreu promedia sobre todas las consultas del grafo.
  Como no coinciden, medimos en las dos.

  Distribución 1: estados que visitan los expertos. Son los ~60k estados de las
  3k partidas de test entre expertos. Para cada estado e le damos al modelo el
  prefijo de jugadas y leemos sus logits sobre las 7 columnas. Con temperatura
  τ, softmax(logits/τ) da una distribución p_τ(c | e). De ahí, sin sortear
  ninguna jugada:

  - E[r] en e = Σ_c p_τ(c | e) · r(e, c)
  - acc en e = Σ de p_τ(c | e) sobre las c óptimas

  Ejemplo: estado no trivial donde la columna 3 gana, la 2 empata y las demás
  pierden. El modelo a τ=1 da p = {3: 0.6, 2: 0.25, 0: 0.15}. Entonces E[r] =
  0.6·1 + 0.25·½ + 0.15·0 = 0.725 y acc = 0.6. A τ→0 toda la masa va a la 3,
  E[r] = 1 y acc = 1. Promediamos sobre los 60k estados no triviales y repetimos
  para cada τ de la lista: eso da la curva "recompensa versus temperatura", la
  Figura 1 de Zhang pero exacta. "Sin muestreo" quiere decir eso: usamos la
  distribución completa, así que el número no tiene ruido de sorteo.

  La separación "sesgados versus no sesgados" es partir esos 60k estados en los
  que están en B y los que no. Verifica el mecanismo: en B esperamos acc ≈ 0 a
  τ→0, el error compartido sobrevive; fuera de B esperamos acc → 1, el voto lo
  elimina. Si el promedio total da lo predicho pero esta partición no, algo está
  mal.

  Distribución 2: juego propio. El modelo juega partidas completas. El rival es
  el bot experto, nuestra población con sus errores, o el jugador perfecto, el
  solver. 300 partidas, mitad como primero y mitad como segundo. En cada turno
  sorteamos una columna de p_τ; si sale una columna llena o un token que no es
  jugada, volvemos a sortear hasta 5 veces y si sigue ilegal la partida cuenta
  como perdida. Métrica: score = victorias más medio punto por empate, sobre
  300. Se hace a τ→0 y a τ=1. Esto es el protocolo literal de Zhang y su análogo
  del rating. Los estados que aparecen acá los genera el propio modelo, y no
  coinciden con los de la distribución 1.

  Baselines analíticos. Son los números contra los que se compara, y se calculan
  sin entrenar nada porque conocemos la política f de la población:

  - Mejor experto: E[r] y acc de f en los mismos 60k estados. Trascendencia es
    superar esto.
  - Argmax de la mezcla: lo que lograría un voto perfecto. En nuestro diseño es
    la óptima fuera de B y w(e) dentro. Es el techo teórico de τ→0.
  - Jugador perfecto: acc 1, techo absoluto.
  - Uniforme sobre legales: piso.

  Estratificación. Cada métrica se reporta además por fase, apertura hasta la
  jugada 8, medio de 9 a 20, final desde 21, y por etiqueta visto/no visto: un
  estado de test es "visto" si ese mismo tablero aparece en alguna partida de
  entrenamiento. Las dos particiones salen de las mismas corridas, sin entrenar
  nada más, y la de visto/no visto es directamente el objetivo 3 de la
  propuesta. Se reportan juntas porque están correlacionadas: las aperturas casi
  siempre son vistas, los finales casi nunca.

✻ Crunched for 38s · done Sunday 20 Sep at 7:55 pm

❯ Pero tiene sentido hacer jugar al modelo contra el bot experto?               
  Tengo una nota:                                                               
  accuracy contra el jugador perfecto tiene un problema. Un primer jugador      
  perfecto gana siempre. Cuando el modelo juega segundo, todas sus posiciones   
  están perdidas desde la jugada 1 y ningún movimiento cuenta como error.       
  Cuando juega primero, tras su primer error la posición pasa a perdida y el    
  resto tampoco cuenta. La métrica colapsa a "cuántas jugadas aguanta sin errar 
  como primero". Por eso propongo como                                          

⏺ Sí tiene sentido, y la nota no lo contradice: la nota es sobre otra métrica.
  Se mezclaron dos cosas distintas que pasan en el juego propio.

  La nota habla de accuracy por jugada en las propias partidas contra el 
  perfecto. Ahí el problema es que casi todos los estados que el modelo visita
  son triviales: perdidos de antemano si juega segundo, o perdidos después de su
  primer error si juega primero. Quedan pocos estados donde contar aciertos y
  la métrica degenera.

  El match contra el bot experto es otra cosa: mide el resultado de la partida, 
  no aciertos por jugada. Y no tiene ese problema porque el resultado se define
  aunque todos los estados intermedios sean triviales. Es la pregunta literal
  del título de Zhang en una oración: ¿el imitador le gana a los expertos de los
  que aprendió? Ellos la responden con un rating contra Stockfish; nosotros la
  podemos responder directo, haciéndolo jugar contra la población que generó sus
  datos. Como el bot experto erra, las partidas son disputadas y el score varía
  de forma informativa entre condiciones.

  El match contra el perfecto es más duro y menos informativo para este
  experimento. Como segundo pierde siempre, así que el máximo es 0.5. Como
  primero gana solo si no erra ni una vez en toda la partida, así que el score
  comprime toda la curva en "probabilidad de partida perfecta", que cae rápido
  con cualquier tasa de error y va a aplastar las diferencias entre valores de
  P. Sirvió en composición porque ahí la pregunta era si el modelo sabía jugar
  la partida completa. Para el experimento 1 lo dejaría opcional.

  Qué haría entonces. Métrica principal, la accuracy y E[r] desde logits sobre
  los estados de los expertos. Métrica secundaria, el score del match contra el
  bot experto a τ→0 y τ=1, con su intervalo sobre 300 partidas. Tené presente
  que con 300 partidas el intervalo es de unos ±0.05, así que este match
  confirma la dirección del efecto pero no distingue condiciones vecinas. Es el
  mismo rol que cumple el rating en Zhang, y por eso va segundo.

✻ Brewed for 27s · done Sunday 20 Sep at 8:25 pm

❯ A ver definime un poco mejor entonces las métricas porque en el comentario    
  que te pregunté antes no se entendía yo solo exribí esto:                     
  La métrica reportada es la suma de la probabilidad de elegir una jugada       
  óptima                                                                        
                                                                                
  Nota: [1] calcula una métrica que es el rating haciendo jugar al modelo       
  contra un bot.                                                                
  En nuestro caso al ser un juego resuelto y el bot que tenemos ser óptimo,     
  jugar contra el mismo no tiene mucho sentido.                                 
  Un primer jugador perfecto gana siempre:                                      
      - cuando el modelo juega segundo ningún movimiento cuenta como un error.  
      - cuando el modelo juega primero, la métrica colapsa a "cuántas jugadas   
  aguanta sin errar como primero"                                               
  Pero tambien tengo notas generadas por vos antes que no le encuentro el       
  sentido (la primera ya te lo pasé)                                            
   > Dos distribuciones de test, porque la definición de trascendencia depende  
  de p_test y los dos papers usan una distinta:                                 
    >   - Estados visitados por los expertos: desde los logits, sin muestreo,   
  para τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}. Métricas: E[r],          
  probabilidad de jugada óptima, y ambas separadas en estados sesgados versus   
  no sesgados para verificar el mecanismo estado por estado.                    
    >   - Juego propio: 300 partidas contra el bot experto y contra el jugador  
  perfecto, colores alternados, cinco reintentos ante jugada ilegal, a τ→0 y    
  τ=1. Es el protocolo de Zhang.                                                
    >   - Baselines analíticos: mejor experto, argmax de la mezcla como techo   
  teórico, jugador perfecto, uniforme.                                          
    >   - Reporte estratificado por fase: apertura, medio, final. Y etiqueta    
  visto/no visto por tablero, que sale gratis de estas mismas corridas y        
  alimenta el objetivo 3 sin entrenar nada más.                                 
  > Dos distribuciones de test, porque la definición de trascendencia depende   
  de p_test y los dos papers usan una distinta:                                 
  >   - Estados visitados por los expertos: desde los logits, sin muestreo,     
  para τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}. Métricas: E[r],          
  probabilidad de jugada óptima, y ambas separadas en estados sesgados versus   
  no sesgados para verificar el mecanismo estado por estado.                    
  >   - Juego propio: 300 partidas contra el bot experto y contra el jugador    
  perfecto, colores alternados, cinco reintentos ante jugada ilegal, a τ→0 y    
  τ=1. Es el protocolo de Zhang.                                                
  >   - Baselines analíticos: mejor experto, argmax de la mezcla como techo     
  teórico, jugador perfecto, uniforme.                                          
  >   - Reporte estratificado por fase: apertura, medio, final. Y etiqueta      
  visto/no visto por tablero, que sale gratis de estas mismas corridas y        
  alimenta el objetivo 3 sin entrenar nada más.                                 
                                                                                
  Métrica principal la accuracy por estado desde los logits sobre los estados   
  que visitan los expertos, donde la accuracy del experto en los mismos estados 
  es analítica y la comparación define trascendencia. Las partidas contra el    
  perfecto y contra el bot experto quedan como métrica secundaria de juego      
  propio. Y hace falta el barrido de temperatura, que tu descripción no         
  menciona: el fenómeno vive en la diferencia entre τ=1 y τ→0.                  

⏺ Tenés razón en que quedó confuso, y además tu nota tiene un error: el bot
  contra el que tiene sentido jugar no es el óptimo sino el bot experto, la
  población ruidosa que generó los datos. Te dejo la sección de métricas escrita
  de cero para pegar en el .md, y al final la nota corregida.

  ## Evaluación

  ### Conjunto de evaluación
  3k partidas de test generadas por la misma población de expertos con semilla 
  propia
  (~60k estados). Se evalúa solo en los estados no triviales. Para cada estado e
  se le
  da al modelo el prefijo de jugadas, se leen los logits de las 7 columnas y se 
  calcula
  p_τ(c | e) = softmax(logits / τ). No se sortea ninguna jugada: se usa la 
  distribución
  completa, así que las métricas no tienen ruido de muestreo.

  ### Métrica principal: accuracy
      acc_τ(e) = Σ p_τ(c | e) sobre las columnas c óptimas en e
      acc_τ    = promedio de acc_τ(e) sobre los estados no triviales de test

  Es la probabilidad de que el modelo, a temperatura τ, juegue una jugada 
  óptima.
  Para el experto es analítica: acc(experto) = 1 − ρ realizado. Hay 
  trascendencia en
  accuracy si acc_τ(modelo) > acc(experto).

  ### Métrica complementaria: recompensa esperada
      E[r]_τ(e) = Σ_c p_τ(c | e) · r(e, c)
      E[r]_τ    = promedio sobre los estados no triviales de test

  Es la definición literal de [1]. A diferencia de acc, pesa cada error por su 
  costo:
  tirar una victoria a empate cuesta ½, a derrota cuesta 1. Se reporta junto con
  acc;
  la ganancia sobre el experto se define como E[r]_τ(modelo) − E[r](experto).

  ### Barrido de temperatura
  τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}. Los dos puntos que importan 
  son
  τ=1 (el modelo imita la distribución de los datos; [1] predice que no puede
  trascender) y τ→0 (argmax; donde el voto opera). El resto dibuja la curva.

  ### Descomposiciones (mismas corridas, sin entrenar nada más)
  - Dentro de B / fuera de B: verifica el mecanismo. Predicción a τ→0: acc ≈ 0 
  en B
    (el error compartido sobrevive), acc → 1 fuera de B (el voto elimina el 
  independiente).
  - Por fase: apertura (jugadas 1-8), medio (9-20), final (21+).
  - Visto / no visto: un estado de test es visto si el mismo tablero aparece en 
  el
    entrenamiento. Es el objetivo 3 de la propuesta. Se reporta junto con fase 
  porque
    están correlacionados.

  ### Referencias analíticas
  Se calculan sin entrenar, porque la política f de la población es conocida:
  - Experto: acc y E[r] de f en los mismos estados. Trascender es superarlo.
  - Argmax de la mezcla: óptima fuera de B, w(e) dentro. Techo teórico de τ→0.
  - Jugador perfecto: acc = 1, E[r] máximo. Techo absoluto.
  - Uniforme sobre legales: piso.

  ### Métrica secundaria: partidas contra el bot experto
  Protocolo de [1]: el modelo juega 300 partidas completas contra un bot que 
  juega la
  política f de la población, 150 como primero y 150 como segundo, a τ→0 y a 
  τ=1.
  En cada turno se sortea una columna de p_τ; ante una salida ilegal se resortea
  hasta 5 veces y luego la partida cuenta como perdida.
      score = (victorias + ½ empates) / 300
  Es el análogo del rating de [1] y responde la pregunta directa: ¿el imitador 
  le gana
  a la población que lo entrenó? Se reporta con intervalo de confianza sobre las
  300
  partidas (±0.05 aprox.), por lo que confirma la dirección del efecto pero no
  distingue condiciones vecinas. Por eso es secundaria.

  ### Chequeos de sanidad
  Masa de p_τ en tokens que no son columnas y en columnas llenas, a τ=1. Debe 
  ser
  del orden de 1 % o menor.

  Y tu nota, corregida:

  Nota: [1] mide un rating haciendo jugar al modelo contra Stockfish. Nuestro 
  análogo
  es el score contra el bot experto, no contra el jugador perfecto. Jugar contra
  el
  perfecto no sirve para este experimento: un primer jugador perfecto gana 
  siempre,
  así que como segundo el modelo pierde todas, y como primero gana solo si no 
  erra
  ni una vez en toda la partida. El score contra el perfecto colapsa a 
  "probabilidad
  de partida sin errores" y aplasta las diferencias entre condiciones. Contra el
  bot
  experto las partidas son disputadas y el score varía de forma informativa.

✻ Baked for 35s · done Sunday 20 Sep at 8:31 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, correlación de errores versus trascendencia en Connect 4, aclarando cada elemento del diseño antes de escribir experimento1-v1.md. Próximo paso: seguir cerrando definiciones o empezar a redactar el .md con lo acordado.

❯ no entiendo                                                                   
  No se sortea ninguna jugada: se usa la distribución                           
  completa, así que las métricas no tienen ruido de muestreo.                   

⏺ Hay dos formas de medir "qué tan bien juega el modelo en el estado e" a partir
  de su distribución p_τ(c | e):

  Forma 1, sorteando. Tirás una jugada al azar según p_τ y anotás 1 si fue
  óptima, 0 si no. Repetís muchas veces y promediás. El promedio se acerca a la
  probabilidad de jugar óptimo, pero con ruido: con 100 sorteos podés obtener
  0.57 o 0.63 para la misma distribución. Zhang hace algo así en su Tabla 1, con
  100 jugadas sorteadas por estado.

  Forma 2, sumando. Como ya tenés la distribución completa, la probabilidad de
  jugar óptimo es simplemente la suma de p_τ sobre las columnas óptimas. Es el
  valor exacto al que la forma 1 se acercaría con infinitos sorteos.

  Ejemplo: en un estado la columna 3 es la única óptima y el modelo a τ=1 da p =
  {3: 0.6, 2: 0.25, 0: 0.15}. La forma 2 dice acc = 0.6, exacto, en una
  operación. La forma 1 necesitaría cientos de sorteos para estabilizarse
  alrededor de 0.6.

  Lo mismo vale para E[r]: en vez de sortear una jugada y anotar su r, sumás
  p_τ(c | e) · r(e, c) sobre todas las columnas.

  "Sin ruido de muestreo" quiere decir que usamos la forma 2. Si corrés la
  evaluación dos veces sobre el mismo modelo y los mismos estados, da
  exactamente el mismo número. La única fuente de variabilidad que queda es
  cuáles estados cayeron en el test, y con 60k estados es despreciable.

  El match contra el bot experto sí usa la forma 1, porque para jugar una
  partida hay que elegir una jugada concreta en cada turno. Por eso tiene
  intervalo de confianza y la métrica desde logits no.

✻ Baked for 17s · done Sunday 20 Sep at 8:35 pm

❯ que nombre le podemos poner a p_τ                                             

⏺ Le pondría política del imitador a temperatura τ, y en el texto simplemente
  "la política a temperatura τ" o "la política templada".

  Sobre la notación, dos opciones:

  - f̂_τ(c | e): es la de [1]. Ellos llaman f̂ al modelo aprendido y f̂_τ a su
    versión con temperatura. Alinea la tesina con el paper y deja f para la
    política de los expertos, así que la comparación "f̂_τ contra f" se lee sola.
  - p_τ(c | e): más neutra y más fácil de leer para quien no vio el paper.

  Yo iría con f̂_τ por consistencia con [1], y la primera vez que aparece la
  definiría así: "f̂_τ(c | e) = softmax(logits(e)/τ), la política del imitador a
  temperatura τ; a τ=1 coincide con la distribución que aprendió, a τ→0
  concentra toda la masa en su jugada más probable".

✻ Crunched for 12s · done Sunday 20 Sep at 8:36 pm

※ recap: Estamos diseñando el experimento 1 de la tesina, la trascendencia en función de la correlación de errores, y venimos cerrando definiciones para escribir experimento1-v1.md. Lo último fue la sección de métricas y la notación f̂_τ. Siguiente paso: pasar todo el diseño al .md.

❯ [1] usa acc o E[r] ?                                                          

⏺ Las dos, pero con roles distintos.

  La teoría de [1] está toda en recompensa. La Definición 1 de trascendencia y
  las Proposiciones 1 a 4 hablan de R, el promedio de r sobre p_test. Nuestro
  E[r] es la instancia exacta de eso.

  Lo empírico principal es el rating, que no es ninguna de las dos: es Glicko-2
  contra Stockfish, o sea resultado de partidas. Nuestro análogo es el score
  contra el bot experto.

  En la Tabla 1 aparecen las dos métricas por jugada:
  - Recompensa esperada: probabilidad de ganar según la evaluación de Stockfish,
    y la función favor, que es el cambio de esa recompensa entre τ y τ=1. Son
    E[r] con Stockfish en lugar de solver.
  - Top-1, Top-3 y Top-5 accuracy: si la jugada del modelo está entre las k
    mejores según Stockfish. Es accuracy, pero aproximada, porque en ajedrez no
    hay jugada óptima exacta.

  [2] usa solo accuracy, la tasa de consultas completadas correctamente, con
  decodificación greedy.

  Para la tesina: E[r] es la métrica que conecta con la definición formal de
  [1], y acc la que conecta con [2] y con la lectura intuitiva "cuántas veces
  juega bien". Como el solver nos da las dos exactas, reportamos ambas y
  definimos trascendencia con E[r], que es la letra de [1]. En la práctica van a
  dar el mismo ordenamiento entre condiciones; si no lo dan, eso mismo es un
  resultado, porque significa que las condiciones difieren en qué tan caros son
  sus errores y no solo en cuántos.

✻ Cooked for 23s · done Sunday 20 Sep at 8:40 pm

❯ tiene sentido τ = 1.5                                                         

⏺ Sentido científico tiene poco; sentido práctico, sí, y cuesta nada.

  Qué muestra. A τ>1 la política del imitador se aplana: reparte más masa entre
  jugadas que lo que hacen los datos. El punto 1.5 dibuja el otro lado de la
  curva y muestra que τ=1 no es un mínimo ni un máximo local, sino un punto en
  una curva monótona: cuanto más agudo, mejor; cuanto más plano, peor. Es la
  forma de la Figura 1 de Zhang, cuyo eje va de 0.001 a 1.5, y por eso lo
  incluí.

  Qué no aporta. Ninguna predicción teórica vive ahí. Las Proposiciones de [1]
  hablan de τ=1 y de τ→0. En 1.5 lo único que esperamos es que acc y E[r] estén
  por debajo del experto en todas las condiciones, y sería raro que no.

  Costo. Un softmax más por estado sobre logits que ya tenés. Segundos.

  Lo dejaría por comparabilidad visual con la Figura 1 de [1], y si en algún
  momento la grilla de τ molesta, es el primer punto que sacaría. Si preferís
  una grilla más chica, con {0.001, 0.1, 0.5, 1} alcanza para todo lo que se
  discute.

✻ Crunched for 18s · done Sunday 20 Sep at 8:41 pm

※ recap: Estamos definiendo el diseño del experimento 1 de tu tesina, la correlación de errores entre expertos en Connect 4, aclarando cada concepto para el .md. Siguiente paso: cerrar la sección de métricas y empezar a escribir experimento1-v1.md juntos.

❯ - Que significa esto:                                                         
  la reportamos como correlación de Pearson medida entre los vectores de error  
  de dos expertos sobre los mismos estados, que es exactamente lo que Pablo     
  sugiere en la imagen 1.                                                       

⏺ Voy con un ejemplo concreto sobre nuestro diseño.

  Qué se mide. Tomás los estados no triviales del test, digamos 30.000. Sorteás
  dos expertos de la población, o sea dos muestras independientes de la política
  f, y los hacés jugar en cada uno de esos estados. Para cada experto armás un
  vector de 30.000 ceros y unos: 1 si erró en ese estado, 0 si no. La
  correlación de Pearson entre esos dos vectores es un número entre 0 y 1 que
  dice cuánto coinciden sus errores:

  - 0: que el experto A haya errado en un estado no dice nada sobre si B erró
    ahí.
  - 1: erraron exactamente en los mismos estados.

  Por qué es lo que pide Pablo. Su fórmula habla de n expertos con errores de
  correlación ρ entre pares. Esa ρ es esto. Y en la imagen 1 lo dice con estas
  palabras: "una correlación de Pearson entre los vectores de error de cada
  jugador sobre el mismo conjunto de posiciones". Nosotros barremos P, pero la
  letra que él entiende es la correlación, así que la calculamos y reportamos
  las dos.

  Cómo se relacionan P y la correlación en nuestro diseño. Dos expertos erran
  juntos en un estado si está en B, probabilidad β, o si está fuera y ambos
  sortean error, probabilidad (1−β)·q². De ahí sale la correlación en cerrado.
  Con ρ = 0.3:

  ┌──────┬───────┬───────┬────────────────────────┐
  │  P   │   β   │   q   │ Correlación de Pearson │
  ├──────┼───────┼───────┼────────────────────────┤
  │ 0    │ 0     │ 0.300 │ 0                      │
  ├──────┼───────┼───────┼────────────────────────┤
  │ 0.25 │ 0.075 │ 0.243 │ 0.19                   │
  ├──────┼───────┼───────┼────────────────────────┤
  │ 0.5  │ 0.150 │ 0.176 │ 0.41                   │
  ├──────┼───────┼───────┼────────────────────────┤
  │ 0.75 │ 0.225 │ 0.097 │ 0.68                   │
  ├──────┼───────┼───────┼────────────────────────┤
  │ 1    │ 0.300 │ 0     │ 1                      │
  └──────┴───────┴───────┴────────────────────────┘

  No es lineal en P: en los extremos coinciden, en el medio la correlación va
  por debajo. Por eso vale la pena reportarla medida y no solo P, y por eso la
  curva de ganancia contra correlación va a tener otra forma que la curva contra
  P. Si Pablo quiere ver "la ganancia cae linealmente con ρ", el eje correcto
  es este.

  Una precisión. Esta correlación es de ocurrencia: erraron en el mismo estado.
  Dentro de B además erran en la misma dirección, w(e); fuera de B coinciden en
  dirección solo por azar. Se puede calcular también la correlación de "misma
  jugada errónea", que en nuestro diseño da casi lo mismo porque fuera de B las
  coincidencias son raras. Alcanza con reportar la de ocurrencia y aclararlo.

✻ Cooked for 26s · done Sunday 20 Sep at 8:53 pm

❯ lee                                                                           
  /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/draft.md y 
  proponé por acá como expl;icar hacer esto y en donde                          

  Read 1 file (ctrl+o to expand)

⏺ Leído. Propongo meter la correlación en tres lugares, con un rol distinto en
  cada uno, y borrar la duda del final.

  1. En "Definición más formal", justo después de q. Es una cantidad derivada de
  P, ρ y q, así que va con ellas. Texto para pegar:

  - **Correlación de errores entre expertos** (`r_err`): P es nuestra perilla de
  diseño,
    pero la magnitud que la literatura de ensambles usa para hablar de "errores
    correlacionados" es la correlación entre los errores de dos expertos. La 
  definimos así:
    para dos expertos A y B sorteados de la población y un conjunto de estados 
  no triviales,
    sea `err_A(e) = 1` si A erra en `e` y `0` si no, y lo mismo para B. `r_err` 
  es la
    correlación de Pearson entre los vectores `err_A` y `err_B` sobre esos 
  estados.
    Vale 0 si errar A no dice nada sobre si erra B, y 1 si erran exactamente en 
  los
    mismos estados.

    En nuestro diseño se calcula en cerrado. Dos expertos erran juntos en `e` si
  `e ∈ B`
    (probabilidad β) o si `e ∉ B` y ambos sortean error (probabilidad (1−β)·q²).
  Entonces:

        r_err = [β + (1−β)·q² − ρ²] / [ρ·(1−ρ)]

    Con ρ = 0.3:

    | P    | β     | q     | r_err |
    |------|-------|-------|-------|
    | 0    | 0     | 0.300 | 0     |
    | 0.25 | 0.075 | 0.243 | 0.19  |
    | 0.5  | 0.150 | 0.176 | 0.41  |
    | 0.75 | 0.225 | 0.097 | 0.68  |
    | 1    | 0.300 | 0     | 1     |

    No es lineal en P: coinciden en los extremos y en el medio `r_err` va por 
  debajo.
    Por eso los resultados se grafican contra ambos ejes.

    Nota: es correlación de *ocurrencia*, erraron en el mismo estado. Dentro de 
  B además
    coinciden en dirección, `w(e)`; fuera de B coinciden en dirección solo por 
  azar.

  2. En "Evaluación", como una referencia analítica más. Agregá una línea a la
  lista de referencias analíticas, porque se mide sobre el mismo test:

  - Correlación de errores realizada: sobre los estados no triviales del test se
  sortean
    dos expertos de la población y se calcula `r_err` empírica. Debe coincidir 
  con la
    tabla; se reporta junto con β̂ y q̂ realizados.

  3. En "Teoría", como el puente con la fórmula de Pablo. Ahí es donde r_err
  paga: es la ρ de su identidad. Reemplazá la primera línea de la sección por
  esto:

  La identidad clásica de ensambles dice que al promediar n expertos con errores
  de
  varianza σ² y correlación ρ entre pares, la varianza residual es ρσ² + 
  (1−ρ)σ²/n:
  nunca baja de ρσ², sin importar cuántos expertos se promedien. Nuestra `r_err`
  es esa ρ,
  medida. Y el análogo en acciones discretas es directo:
  - El piso ρσ² es la masa β que la mezcla pone en `w(e)` dentro de B. Ningún 
  voto la saca.
  - El término (1−ρ)σ²/n es la masa de los errores independientes fuera de B, 
  repartida
    entre jugadas distintas. El argmax la elimina donde hay suficientes visitas.

  Y en las predicciones, después de "decrece monótonamente en P", agregá "y en
  r_err".

  4. En los resultados, cuando existan, una columna r_err al lado de P en la
  tabla principal, y la figura de ganancia contra P duplicada con r_err en el
  eje x. Es lo que Pablo va a querer mirar.

  Después borrá la duda de la sección DUDAS. Las otras dos dudas que quedan ahí,
  "fijar E[r] del experto" y "eje cantidad de expertos", ya las respondí más
  arriba; si querés las convierto en notas para "Notas a futuro" en el mismo
  formato.

  Aparte de esto, vi tres bloques que todavía tienen la versión vieja que ya
  corregimos: la sección Epochs, la justificación de repeticiones, y la nota de
  TODOS sobre el bot óptimo. Cuando quieras te paso los tres reemplazos juntos.

✻ Worked for 50s · done Sunday 20 Sep at 8:58 pm

❯ otra cosa que no entiendo es el apartado teoria que escribimos que es         
  producto casi copy paste de cosas que dijiste, realmente no tengo idea        
  Teoría                                                                        
                                                                                
  La teoría dice que al promediar n expertos con correlación ρ la varianza      
  residual nunca baja de ρσ²                                                    
  Predicciones cuantitativas:                                                   
  - acc(τ→0) ≈ 1 − β̂                                                            
  - ganancia sobre el experto ≈ q̂                                               
    Donde β̂ y q̂ son las tasas realizadas de error compartido e independiente    
  sobre estados decidibles.                                                     
    A τ=1 no hay trascendencia para ningún valor, por la Proposición 1 de       
  Zhang.                                                                        
                                                                                
  > Predicciones registradas antes de correr. La ganancia a τ→0 decrece         
  monótonamente en π y en la correlación medida. La teoría predice signo        
  positivo para todo π<1, pero la exploración vio el cruce por cero antes,      
  cerca de π=0.75. Si se repite, es un hallazgo: el modelo finito alcanza el    
  piso antes que la mezcla verdadera. En estados sesgados con regla, acierto ≈  
  0 en toda fase, visto o no visto. En los no sesgados, acierto → 1 solo donde  
  hay votos.                                                                    
⏺ Tenés razón, esa sección junta tres cosas distintas sin explicar ninguna. Te
  las explico de a una y después te dejo la sección reescrita. Y hay un error
  mío en la predicción de la ganancia que aprovecho para corregir.

  Qué dice la teoría, en tres pasos

  Paso 1: qué aprende el modelo. Zhang prueba que un modelo entrenado por
  cross-entropy con datos infinitos aprende exactamente la distribución de los
  datos. Si los datos los generan varios expertos, aprende su promedio, la
  "mezcla". En nuestro diseño todos los expertos son muestras de la misma
  política f, así que la mezcla es f misma: a τ=1 el modelo ideal juega igual
  que el experto. Misma tasa de error, misma accuracy 1−ρ. No hay trascendencia.
  Eso es la Proposición 1.

  Paso 2: qué pasa a τ→0. Bajar la temperatura a cero es jugar siempre la
  columna más probable según f, el argmax. Zhang prueba que hay trascendencia si
  y solo si esa política argmax es mejor que el experto. Eso es la Proposición
  2. Y acá nuestro diseño permite calcular el argmax exacto, estado por estado:

  - Fuera de B: la óptima tiene masa 1−q, cada errónea a lo sumo q. Como q <
    0.5, el argmax es la óptima. El error independiente desaparece.
  - Dentro de B: w(e) tiene masa 1. El argmax es w(e). El error compartido
    sobrevive.

  Entonces la política argmax acierta en todos los estados fuera de B y en
  ninguno de B: acc(τ→0) = 1 − β = 1 − P·ρ. Y la ganancia sobre el experto es (1
  − P·ρ) − (1 − ρ) = ρ·(1 − P). Acá estaba mi error: había escrito "ganancia ≈
  q", pero q es una probabilidad condicional. La ganancia es la fracción de
  estados no triviales con error independiente, que es ρ − β.

  Con ρ = 0.3 las predicciones son una recta:

  ┌──────┬───────────┬───────────┬──────────┐
  │  P   │ acc a τ=1 │ acc a τ→0 │ ganancia │
  ├──────┼───────────┼───────────┼──────────┤
  │ 0    │ 0.70      │ 1.00      │ +0.30    │
  ├──────┼───────────┼───────────┼──────────┤
  │ 0.25 │ 0.70      │ 0.925     │ +0.225   │
  ├──────┼───────────┼───────────┼──────────┤
  │ 0.5  │ 0.70      │ 0.85      │ +0.15    │
  ├──────┼───────────┼───────────┼──────────┤
  │ 0.75 │ 0.70      │ 0.775     │ +0.075   │
  ├──────┼───────────┼───────────┼──────────┤
  │ 1    │ 0.70      │ 0.70      │ 0        │
  └──────┴───────────┴───────────┴──────────┘

  Esto es lo que se puede probar con el experimento: que la ganancia cae
  linealmente con P, con pendiente −ρ, y se anula exactamente en P=1.

  Paso 3: la fórmula de Pablo es la misma idea con otras palabras. Su identidad
  de ensambles dice que al promediar n expertos con errores de correlación
  ρ_corr, la varianza residual es ρ_corr·σ² + (1−ρ_corr)·σ²/n. El segundo
  término se va con n grande; el primero no, es un piso. En nuestro caso el piso
  es β, la masa en w(e) dentro de B, que ningún promedio elimina. Y el término
  que se va es ρ − β, los errores independientes, que el argmax elimina porque
  se reparten entre jugadas distintas. Es el mismo enunciado en acciones
  discretas.

  Lo que la teoría asume y nosotros no tenemos. Todo lo anterior vale para el
  modelo ideal, que aprendió f exactamente. Nuestro modelo tiene datos y
  capacidad finitos, así que su argmax es una estimación del argmax verdadero.
  La exploración vio dos desvíos: a τ=1 el modelo es más plano que f, acc 0.76
  contra 0.845 del experto; y a τ→0 capturó un cuarto de la ganancia teórica,
  con el cruce por cero cerca de P=0.75 en vez de P=1. La distancia entre la
  recta de arriba y lo medido es exactamente lo que el experimento cuantifica.

  Sección reescrita para el .md

  ## Teoría y predicciones

  ### Qué predice [1] para nuestro diseño
  - **A τ=1** el modelo ideal aprende la política f de la población y juega 
  igual que el
    experto: acc = 1 − ρ para todo P. No hay trascendencia (Proposición 1 de 
  [1]).
  - **A τ→0** el modelo ideal juega el argmax de f en cada estado (Proposición 2
  de [1]).
    En nuestro diseño ese argmax se calcula exacto:
      - fuera de B la óptima tiene masa 1−q > q ≥ masa de cualquier errónea → 
  argmax = óptima
      - dentro de B, w(e) tiene masa 1 → argmax = w(e)
    Por lo tanto:
        acc(τ→0) = 1 − β = 1 − P·ρ
        ganancia sobre el experto = ρ·(1 − P)
    La ganancia cae linealmente con P, con pendiente −ρ, y se anula en P=1.

  ### Puente con la identidad de ensambles
  Al promediar n expertos con errores de varianza σ² y correlación ρ_corr, la 
  varianza
  residual es ρ_corr·σ² + (1−ρ_corr)·σ²/n. El primer término es un piso que 
  ningún
  promedio elimina; el segundo desaparece con n. En nuestro dominio discreto:
  - el piso es β, la masa que f pone en w(e) dentro de B;
  - el término que desaparece es ρ − β, los errores independientes, que el 
  argmax
    elimina porque se reparten entre jugadas distintas.
  `r_err` (ver Definición) es la ρ_corr de esta fórmula, medida.

  ### Predicciones registradas antes de correr
  Valores con ρ = 0.3, β̂ y q̂ realizados sobre estados no triviales del test.
  1. A τ=1: acc ≈ 0.70 y sin trascendencia en ninguna configuración.
  2. A τ→0: acc ≈ 1 − β̂, ganancia ≈ ρ̂ − β̂. Decreciente y aproximadamente lineal 
  en P;
     también decreciente en r_err, pero no lineal.
  3. Dentro de B, a τ→0: acc ≈ 0 en todas las fases, vistos y no vistos, porque 
  la regla
     t ∈ S es representable. Fuera de B: acc → 1.
  4. Desvío esperado del modelo finito: a τ=1 más plano que f (en los 
  preliminares 0.76
     contra 0.845), y a τ→0 una fracción de la ganancia teórica, con el cruce 
  por cero
     antes de P=1 (en los preliminares, cerca de 0.75). La distancia entre la 
  recta
     teórica y lo medido es lo que este experimento cuantifica; su 
  descomposición en
     vistos / no vistos es el objetivo 3.

  Y en la sección Definición, corregí la frase "β es la probabilidad de que un
  estado no trivial ocurra un error compartido" que dice "|β| / |Estados no
  triviales|": debería ser |B| / |estados no triviales|.

✻ Churned for 54s · done Sunday 20 Sep at 9:50 pm

※ recap: Estamos escribiendo el diseño del experimento 1 de la tesina en draft.md. Te dejé la sección "Teoría y predicciones" reescrita para pegar, con la ganancia corregida a ρ·(1−P); el siguiente paso es que la reemplaces y sigamos con los bloques viejos de Epochs, semillas y bot óptimo. (disable recaps in /config)

❯ Habiamos especificado                                                         
  Es muy relevante para nuestro experimento que habla de "proporción de error"  
  o "probabilidad de equivocarse":                                              
  Hay que tener en cuenta que se trata de una fracción de los estados no        
  triviales, no de los estados totales.                                         
  es asi o en realidad es proporcion de errores y hay que hacer la construccion 
  apra tnern en cuenta los trivlaes son muchos?                                 

⏺ Es así como lo escribimos, y es una decisión de diseño, no un hecho. La nota
  es correcta; lo que conviene es dejar claro por qué se eligió.

  Las dos opciones.

  - ρ sobre estados no triviales, la nuestra: "cuando el estado permite errar,
    el experto erra con probabilidad 0.3". La regla del experto es literalmente
    esa: en un estado no trivial fuera de B, tira una moneda con probabilidad q.
    En los triviales no hay moneda.
  - ρ sobre todos los estados: "de todas las jugadas de una partida, el 30 % son
    errores". Para implementarla habría que errar con una probabilidad mayor en
    los no triviales, ajustada por la fracción de triviales, para que el
    promedio sobre el total dé 0.3. Y como esa fracción cambia con la fase y con
    P, el ajuste sería distinto por configuración.

  Por qué la primera. Tres razones: es la que se implementa directo, sin ajuste;
  es la que hace que las predicciones teóricas salgan limpias, acc(τ→0) = 1 −
  P·ρ, sin factores de corrección; y es consistente con las métricas, que
  también se promedian solo sobre estados no triviales. Todo el experimento
  habla el mismo idioma: "de las veces que se podía errar".

  Lo que la exploración hizo mal fue mezclar las dos: el parámetro ρ = 0.3 se
  aplicaba en los no triviales, pero las predicciones se escribieron como si
  fuera sobre el total, y salían corridas. Lo arreglaron midiendo tasas
  realizadas. Nosotros lo evitamos definiendo desde el inicio.

  Una consecuencia para la redacción. Cuando digamos "el experto acierta el 70
  %", es sobre estados no triviales. Sobre todos los estados, contando los
  triviales donde acertar es gratis, el mismo experto acierta cerca del 85 %.
  Conviene reportar ambos números una vez, para que nadie compare el nuestro con
  el de otro trabajo que use el total.

  Así que la nota queda como está, agregándole una línea: "Es una decisión de
  diseño: la tasa se define condicional a que el error sea posible, porque así
  se implementa el experto y así se promedian las métricas".

✻ Sautéed for 27s · done Monday 21 Sep at 12:38 am

❯ Está bien como le reescribí?                                                  
  Cerca de la mitad de los estados son triviales. Es muy relevante para nuestro 
  experimento que hablaremos de ρ como "proporción de error" o "probabilidad    
  de equivocarse". Para nosotros la probabilidad aplicará sólo a estados no     
  triviales. O sea, “de todos las jugadas de una partida dónde era posible      
  equivocarse (estados no triviales), qué fracción son errores”.                
  En caso contrario de no hacer esta salvedad, las predicciones teóricas no     
  coincidirían con los resultados experimentales.                               
  Notar que “la probabilidad de equivocarse en una jugada aleatoria” será un    
  número menor: ajustada por la fracción que los no triviales representan del   
  total de estados.                                                             

⏺ Está bien en contenido. Dos ajustes de precisión y uno de redacción:

  1. "En caso contrario... no coincidirían" sugiere que definirla sobre el total
     sería incorrecto. No lo es: es otra definición válida. El riesgo es la
     inconsistencia, definir de una forma y predecir con la otra, que es lo que
     pasó en los preliminares. Lo diría así.
  2. "un número menor: ajustada por la fracción" conviene darle el número,
     porque es la mitad y sorprende: ρ multiplicado por la fracción de estados
     no triviales, aproximadamente 0.15.
  3. "de todos las jugadas" y "jugada aleatoria" → "de todas las jugadas" y "una
     jugada cualquiera".

  Versión ajustada:

  Cerca de la mitad de los estados visitados son triviales. Esto es relevante 
  porque
  hablaremos de ρ como "proporción de error" o "probabilidad de equivocarse", y 
  para
  nosotros esa probabilidad es condicional a que el error sea posible: "de todas
  las
  jugadas de una partida donde era posible equivocarse (estados no triviales), 
  qué
  fracción son errores". Es una decisión de diseño: así se implementa el experto
  (la
  moneda se tira solo en estados no triviales) y así se promedian las métricas.
  Definirla sobre el total de estados también sería válido, pero entonces habría
  que
  ajustar la implementación y las predicciones; lo que no se puede hacer es 
  definir de
  una forma y predecir con la otra, que fue el tropiezo de los experimentos 
  preliminares.
  Notar que "la probabilidad de equivocarse en una jugada cualquiera de la 
  partida" es un
  número menor: aproximadamente ρ multiplicado por la fracción de estados no 
  triviales,
  cerca de 0.15 para ρ = 0.3.

✻ Churned for 25s · done Monday 21 Sep at 7:31 am

※ recap: Estamos escribiendo el diseño del experimento 1 (efecto de la fracción P de errores compartidos sobre la trascendencia) en draft.md, sección por sección. Próximo paso: reemplazar en el draft los tres bloques viejos: Epochs, repeticiones y la nota sobre el bot óptimo.

❯ sampleará em espanol?                                                         

⏺ En español formal es muestrear y muestreo: "se muestrea una columna de f̂_τ",
  "muestreo a baja temperatura", "sin ruido de muestreo". Es el término que usa
  la literatura estadística en castellano y el que va a esperar Dante.

  "Samplear" se entiende y se usa en la jerga, pero en la tesina lo evitaría.
  Donde ya escribiste "sampling" o "samplea" en el draft, por ejemplo en la
  sección del rating contra expertos, cambiaría a "se muestrea una columna de
  f̂_τ; ante una salida ilegal se vuelve a muestrear hasta 5 veces".

✻ Cooked for 10s · done Monday 21 Sep at 7:48 am

❯ está bien esto?                                                               
  Diseño propuesto                                                              
  Descripción conceptual                                                        
  El experimento que planeo hacer ahora, como primer paso, consiste en usar el  
  juego Connect4 propuesto y entrenar un modelo con partidas sintéticas.        
  Esas partidas sintéticas son generadas por varios expertos.                   
  Esos expertos tienen probabilidad de equivocarse.                             
  Equivocarse es hacer una jugada perdedora.                                    
  Cuando se equivocan, tienen probabilidad P de cometer un error compartido y   
  probabilidad (1-P) de cometer un error propio.                                
  La idea es variar P y ver cómo mejora la calidad del juego del modelo         
  entrenado.                                                                    
  Definición más formal                                                         
  Definiremos el conjunto de estados sesgados (notaremos como B) como un        
  subconjunto de los estados no triviales. En este subconjunto todos los        
  expertos jugarán la misma jugada errónea w(e). Son "los estados en los que    
  todos los expertos se equivocan de la misma manera", "los estados de error    
  compartido". Más abajo definiremos cómo construiremos B para cada             
  configuración; primero, necesitamos introducir algunos conceptos adicionales. 
  ρ_total es la tasa de error del experto en estados no triviales. Es una       
  constante fija en 0.3 para todas las configuraciones (tiene que ser menor que 
  0.5 de lo contrario no se da las condiciones para que el voto de la mayoría   
  sea mejor que cada experto, por lo cual no habría trascendencia incluso       
  cuando no haya errores compartidos)                                           
  P fracción de los errores de ρ_total que son compartidos (ejemplo: si P=0.2   
  entonces los expertos en estados no triviales cometen errores compartidos con 
  probabilidad 0.06 y errores no compartidos con probabilidad 0.24 ;            
  manteniendo una tasa de error total de 0.3 en estados no triviales)           
  Es la variable a barrer entre configuraciones: P ∈ {0, 0.25, 0.5, 0.75, 1}    
  β = P·ρ es la probabilidad de que, en un estado no trivial, se produzca un    
  error compartido.                                                             
  Intuitivamente β = |B| / |Estdos no triviales|                                
  q = (ρ − β)/(1 − β) es la probabilidad de errar (estando en un estado no      
  trivial) dado que estás fuera de B                                            
  Construcción de B y w(e):                                                     
  Un estado está en B si el número de la jugada t pertenece a S ⊂ {1, …, 42}.   
  Coloquialmente: S es el índice de las jugadas que están en B                  
  El 42 surge que ninguna jugada tiene más de longitud 42 (6x7)                 
  ¿Cómo definimos S? Queremos que:                                              
  Cada t esté representado por igual                                            
  Siendo no triviales(t) la fracción de estados no triviales que ocurren en t,  
  queremos que:                                                                 
   sumatoria de no triviales(t) = β para t ∈ S                                  
  Definiremos w(e) como la columna legal más a la izquierda que no sea óptima.  
  Nota: Durante los experimentos preliminares, probamos construir B a partir de 
  un hash de los estados. Pero estimamos que la nueva construcción es más       
  fácil de aprender. Proponemos realizar una comparativa del mismo experimento, 
  definiendo B mediante un hash del estado y comparando cómo la                 
  representabilidad de B afecta los resultados.                                 
  Luego los expertos jugarán:                                                   
  Si e es trivial, juega al azar una jugada legal.                              
  Si e es no trivial:                                                           
  Si t \in S juega w(e)                                                         
  Si no:                                                                        
  Con probabilidad q juega una jugada errónea al azar .                         
  Con probabilidad 1−q juega una jugada óptima al azar.                         
  Nota importante: la regla t ∈ S, si bien creemos que será fácilmente          
  representable para el modelo, no indica si el estado es trivial ni cuántas    
  veces se ve durante el entrenamiento, así que la fracción de estados no       
  triviales que caen en B no es |S|/42, sino la suma, sobre t ∈ S, de la        
  fracción de estados no triviales visitados en la jugada t. Por eso S se       
  calibra con un dataset piloto para que esa suma dé β, y el β efectivo se      
  reporta midiendo en el test qué fracción de los estados no triviales          
  efectivamente cayó en B.                                                      

⏺ Está bien en la estructura. Marqué ocho puntos, tres de contenido y cinco de
  precisión, con el reemplazo para cada uno.

  Contenido

  1. "Equivocarse es hacer una jugada perdedora" contradice la definición formal
     de error, que es "jugada no óptima" e incluye tirar una victoria a empate.
     Reemplazo: "Equivocarse es hacer una jugada no óptima, una que empeora el
     valor de la posición."
  2. "error propio" es la lectura persistente que discutimos, y no es lo que
     implementamos. Reemplazo: "probabilidad (1−P) de cometer un error
     independiente, al azar".
  3. La justificación de ρ < 0.5 está bien en la idea pero imprecisa. Reemplazo:
     "tiene que ser menor que 0.5: en un estado con una única jugada errónea,
     toda la masa de error va a esa jugada, y con ρ ≥ 0.5 la mezcla le pondría
     más masa que a la óptima. El argmax dejaría de ser óptimo incluso con P=0,
     y el experimento perdería su control positivo."

  Precisión

  4. ρ_total y ρ aparecen como dos nombres para lo mismo. Usá ρ en todos lados.
  5. El ejemplo de P=0.2: 0.06 y 0.24 son correctos, pero 0.24 es la tasa
     incondicional ρ−β y alguien puede confundirla con q. Agregá: "(q, la
     probabilidad de errar condicional a estar fuera de B, es 0.24/0.94 ≈
     0.255)".
  6. "β = |B| / |Estdos no triviales|": además del typo, no es un cociente de
     conjuntos sino de visitas. Reemplazo: "Intuitivamente, β es la fracción de
     los estados no triviales visitados que caen en B."
  7. "Cada t esté representado por igual" no es lo que queremos; queremos S
     repartido entre fases. Reemplazo: "S repartido de forma pareja entre
     apertura, medio y final, para que el error compartido no se concentre en
     una fase del juego." Y "El 42 surge que ninguna jugada tiene más de
     longitud 42" → "El 42 es el máximo de jugadas de una partida: 6 × 7
     casilleros."
  8. La nota sobre el hash dice "estimamos que es más fácil de aprender" sin
     decir por qué importa. Reemplazo:

  Nota: en los experimentos preliminares B se definió con un hash del estado. Un
  hash no es
  aprendible: en estados nuevos el modelo no puede saber que está en B, hace lo 
  que hacen los
  estados parecidos, y deshace parte del error compartido (acc en B de 0.3 a 0.4
  en vez de ≈0).
  Eso mezcla dos efectos, correlación y representabilidad. La regla t ∈ S es 
  aprendible, así
  que el error compartido debería reproducirse como predice la teoría y el 
  experimento aísla
  la correlación. La comparación regla contra hash queda como experimento 
  aparte, sobre
  representabilidad.

  Dos detalles menores: en la definición de w(e) agregá "(existe porque e es no
  trivial)", y en la nota importante "cuántas veces se ve durante el
  entrenamiento" → "cuántas veces se visita cada jugada t", que es lo que hace
  que |S|/42 no sea la fracción correcta.

✻ Brewed for 44s · done Monday 21 Sep at 8:23 am

※ recap: Estamos escribiendo el diseño del experimento 1 en draft.md, sección por sección, y acabo de revisarte "Diseño propuesto" con ocho correcciones. Próximo paso: que apliques esas correcciones y sigamos con las tres secciones que aún tienen texto viejo.