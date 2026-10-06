 ▐▛███▛█   Claude Code v2.1.278
▝▜██████▀  Fable 5.1 · Claude Team
  ▝▝ ▝▝    ~/…/projects/unr-tesina-new/exploracion-pre-propuesta/generated


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

✻ Churned for 5m 42s · done Saturday 6:03 pm

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

✻ Worked for 1m 6s · done Saturday 6:28 pm

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

✻ Baked for 1m 40s · done 11:23 am

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

✻ Brewed for 23s · done 11:40 am

※ recap: Estamos diseñando el experimento 1 de la tesina (correlación de errores entre expertos y trascendencia en Connect 4) para volcarlo en experimento1-v1.md. Falta que decidas las opciones abiertas (regla vs hash, panel 320k, K expertos) y arranco el .md. (disable recaps in /config)