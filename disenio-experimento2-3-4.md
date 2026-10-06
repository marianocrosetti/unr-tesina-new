 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Fable 5.1 · Claude Team
 ▝▝   ▝▝   ~/Desktop/personal-hq/projects/unr-tesina-new


❯ /clear                                                                        

❯ /model fable                                                                  
  ⎿  Set model to Fable 5.1 and saved as your default for new sessions

❯ leyendo lo que hay hecho sobre todo las slides esas de la  exploracion y el   
  experimento1 cuantos experimentos me falta diseñar?                           

⏺ Voy a leer la propuesta, la exploración y el experimento 1 para contar qué
  experimentos quedan por diseñar.

  Read 2 files, listed 2 directories, ran 3 shell commands (ctrl+o to expand)

⏺ Leí la propuesta v2.2, las slides y el resumen de la exploración, el borrador
  de experimento 1 y la conversación de diseño. Respuesta corta: te faltan 3 
  experimentos por diseñar, y uno de ellos es casi gratis.

  Cómo mapea todo

  La propuesta v2.2 tiene 5 objetivos específicos, y el cronograma los agrupa en
  4 bloques de experimentos. La exploración pre-propuesta ya corrió una versión
  IA-generated de los 4 (más dos hallazgos extra que no están en la propuesta).

  ┌──────────────────────┬──────────┬─────────────┬─────────────────────────┐
  │ Bloque (cronograma)  │ Objetivo │ Exploración │  Diseño para la tesina  │
  ├──────────────────────┼──────────┼─────────────┼─────────────────────────┤
  │ Exp 1: correlación   │          │             │ Borrador hecho          │
  │ de errores (barrido  │ 1        │ Hallazgo 1  │ (experimento1-v1.md)    │
  │ en π)                │          │             │                         │
  ├──────────────────────┼──────────┼─────────────┼─────────────────────────┤
  │ Exp 2: selección     │          │             │                         │
  │ (barrido en α) +     │ 2 y 3    │ Hallazgo 2  │ Falta                   │
  │ temperatura          │          │             │                         │
  ├──────────────────────┼──────────┼─────────────┼─────────────────────────┤
  │ Exp 3: vistos vs no  │ 4        │ Hallazgo 3  │ Falta                   │
  │ vistos               │          │             │                         │
  ├──────────────────────┼──────────┼─────────────┼─────────────────────────┤
  │ Exp 4: composición   │          │             │                         │
  │ con soporte disjunto │ 5        │ Hallazgo 6  │ Falta                   │
  │  (familias A/B)      │          │             │                         │
  └──────────────────────┴──────────┴─────────────┴─────────────────────────┘

  Matices sobre los 3 que faltan

  - Exp 2 (selección) es el único que requiere un diseño nuevo de verdad:
    población de K expertos con regiones, parámetro α, y el umbral α* =
    (K−2)/(2K−2). El objetivo 3 (temperatura) no es un experimento aparte: el
    barrido en τ ya está en los "elementos comunes" de experimento 1, así que se
    cubre analizando las curvas de exp 1 y exp 2.
  - Exp 3 (vistos/no vistos) no necesita corridas nuevas. La etiqueta visto/no
    visto se calcula sobre los mismos modelos de exp 1. Lo único a diseñar es el
    panel de escala de datos (20k/80k/320k) y la estratificación por fase que
    ya anotaste en el CURRENT_STATUS. En draft.md ya lo llamás "experimento 3".
  - Exp 4 (composición) es el más largo (el cronograma le da 2 semanas) pero la
    exploración ya tiene el diseño completo: familia A aperturas óptimas
    truncadas en N, familia B bordes con final óptimo, controles solo-A, solo-B
    y control de soporte completo.

  Pendientes dentro del experimento 1 antes de darlo por diseñado:

  - La sección "Correlación de errores entre expertos" dice "Pendiente" (es la
    Pearson que pidió Pablo).
  - Epochs figura "por determinar".
  - La celda de contraste hash vs regla en π=1 está mencionada pero no
    especificada.
  - Las últimas 4 líneas del archivo (desde "nono usemos string y punto...")
    parecen un pegado accidental de otro contexto, no tienen que ver con la
    tesina.

  Los hallazgos 4 (representabilidad) y 5 (memorización) de la exploración no
  son objetivos de la propuesta: el primero queda absorbido como la celda hash
  de exp 1 y el segundo como el protocolo de early stopping en los elementos
  comunes.

✻ Baked for 1m 2s · done Saturday 26 Sep at 12:20 am

❯ bien querés escribir un solo archivo "experimentos2-3-4.md" va a tener TODOS  
  no hace falta que definamos cosas que vamos a definir de la misma forma que   
  el experimento1 o sea no repitas cosas que san iguales                        

⏺ Voy a mirar cómo definió la exploración los expertos de selección y las
  familias A/B para no inventar detalles distintos a lo que ya corrió.

  Searched for 1 pattern, listed 1 directory, ran 3 shell commands (ctrl+o to expand)

⏺ Ya tengo las definiciones exactas de selection y composition, la
  descomposición visto/no visto y el protocolo de evaluación del paper. Ahora
  escribo el archivo. · summary

⏺ Write(experimentos2-3-4.md)
  ⎿  Wrote 187 lines to experimentos2-3-4.md
      1 # Experimentos 2, 3 y 4
      3 Este documento define los experimentos 2 (selección de habilidade
        s), 3 (posiciones vistas vs. no vistas) y 4 (generalización con s
        oporte disjunto). Cubren los objetivos específicos 2 a 5 de la pr
         un experimento aparte: se responde con el barrido de τ de los ex
        perimentos 1 y 2, y se explicita en la sección del experimento 2.
      5 Todo lo definido en la sección "Elementos comunes a todos los exp
        erimentos" de `experimento1/experimento1-v1.md` aplica sin cambio
        s: dominio, solver, notación (`estado`, `jugada`, `recompensa`, `
         hiperparámet
     … +415 lines (ctrl+o to expand)

⏺ Escribí experimentos2-3-4.md en la raíz del proyecto, al lado de draft.md. Lo
  puse ahí y no dentro de experimento1/ porque esa carpeta es del experimento 1;
  movelo si preferís otro lugar.

  Qué tiene el archivo

  - Un encabezado que remite a los "Elementos comunes" de experimento1-v1.md y
    no los repite: dominio, notación, datos, modelo, parada, métricas y barrido
    de τ se dan por definidos.
  - Experimento 2 (selección): K = 4 expertos con regiones, error compartido
    w(e) fuera de la región, ruteo α barrido en 7 valores con puntos extra
    alrededor de α* = 1/3 para ver la forma de la transición. Incluye la figura
    de "curva de temperatura por mecanismo" que resuelve el objetivo 3 de la
    propuesta contrastando exp 1 y exp 2.
  - Experimento 3 (vistos/no vistos): no entrena nada nuevo salvo 2 corridas de
    escala (20K y 320K). Define estado visto por tablero, la descomposición de
    la ganancia ponderada por la fracción vista, el techo teórico analítico y la
    estratificación por fase.
  - Experimento 4 (composición): familias A (aperturas óptimas truncadas en N
    = 8) y B (estilo bordes y final óptimo), 4 configuraciones principales más 2
    opcionales de gradiente de severidad. Define por separado "transferencia"
    (jugada a jugada en el final) y "composición" (partida completa contra el
    jugador perfecto), porque acá no hay un experto definido en todo el juego.
  - Predicciones registradas antes de correr en cada uno, tomadas de lo que vio
    la exploración.
  - Grilla total y orden sugerido: 3, luego 2, luego 4.

  Dos decisiones de diseño que tomé y conviene que mires

  - En exp 2 mantengo las regiones por hash como en la exploración, pero cambio
    la jugada errónea compartida a la w(e) del exp 1. La representabilidad de la
    región no afecta la predicción porque la mezcla tiene la misma forma en
    todos los estados; sólo w(e) tiene que ser representable.
  - En exp 4 el rival de las partidas es el jugador perfecto y no el bot de la
    población, porque ninguna familia tiene política definida en toda la
    partida. Eso pone el score máximo en 0.5.

  Quedan 5 TODO marcados dentro del archivo: el control opcional de expertos
  complementarios, los cortes de fase, la tercera población de estados en exp 3,
  si se reporta N = 14 y las robusteces de exp 4.

✻ Cogitated for 3m 37s · done Saturday 26 Sep at 12:26 am

※ recap: Estamos diseñando los experimentos de la tesina y acabo de escribir experimentos2-3-4.md en la raíz con el diseño completo de selección, vistos/no vistos y composición. Falta que lo revises y resuelvas los 5 TODO marcados. (disable recaps in /config)

❯ hay un experimento que alguna vez propusiste en nuestros dialogos de mover el 
  token de victoria derrota o empate al principio por qué eso cambiaría y por   
  qué es interesante?                                                           

  Searched for 1 pattern, ran 1 shell command (ctrl+o to expand)

⏺ Está escrito en non-explored-ideas/discovery-ideas.md, en la aproximación 3
  ("Condicionar por resultado"). Resumo qué cambia y por qué vale la pena.

  Qué cambia mecánicamente

  Hoy la secuencia es BOS, jugadas..., resultado. El token de resultado va al
  final, así que el modelo lo predice pero nunca lo usa para decidir una jugada:
  por el masking causal, ninguna jugada puede atender a algo que viene después.
  La política aprendida es p(jugada | prefijo).

  Si el resultado va al principio (BOS, 1-0, jugadas...), toda jugada puede
  atenderlo y la política aprendida pasa a ser p(jugada | prefijo, resultado).
  En inferencia fijás el prefijo en "gana el que mueve" y muestreás. Es la idea
  del Decision Transformer, que Zhang menciona en su apéndice D.2 como "otra
  forma de trascendencia" sin explorarla.

  Por qué es interesante para la tesina

  - Es la única palanca dentro de imitación pura que puede superar el argmax de 
    la mezcla. Todo el marco de [1] y [2] es sobre la mezcla sin condicionar: el
    voto elige la jugada más frecuente. Condicionar por "gana" pesa las jugadas
    por resultado y no por frecuencia. Es un criterio de selección que la
    Proposición 2 de [1] no cubre.
  - Tiene un lugar exacto donde probarlo: donde el voto falla. En selección con
    α < α* la jugada errónea compartida es la mayoría y el modelo a τ→0 queda
    por debajo del experto. Pero las partidas donde jugó el experto competente
    se ganan más seguido. Condicionar por "gana" podría dar vuelta el argmax
    justo ahí. La predicción optimista es ganancia positiva en α ∈ {0, 0.2},
    donde sin condicionar da negativa.
  - Hay dos predicciones opuestas en la literatura. Paster et al. 2022 y
    Brandfonbrener et al. 2022 muestran que en entornos estocásticos el
    condicionamiento por retorno aprende a "contar con la suerte": selecciona
    también las partidas que se ganaron porque el rival erró después. Nuestro
    rival es un experto ruidoso, así que desde el modelo el entorno es
    estocástico. Predicción pesimista: el E[r] por estado no mejora o empeora.
    Ambos papers ya están citados en la propuesta v2 como [10] y [11].
  - Es barato. Mismo generador con el token movido, reentrenar 4 configuraciones
    (selección α ∈ {0, 0.2, 0.45} más P = 0 del experimento 1 como control
    donde el voto ya es óptimo y el condicionamiento no debería sumar nada). La
    evaluación es la común con el prefijo fijado.

  Qué no es

  No es descubrimiento: sigue eligiendo entre jugadas que están en los datos. Y
  en el control P = 0 el voto ya alcanza el techo, así que no debería mostrar
  nada; su gracia es puramente el régimen α < α*.

  Un detalle a resolver si lo hacés

  Hay que decidir qué prefijo usás en evaluación cuando mueve el segundo
  jugador. Como el primero perfecto gana siempre, "gana el que mueve" para el
  segundo condiciona a partidas donde el primero se equivocó, que es exactamente
  el caso de contar con la suerte. Puede ser una feature: separar el resultado
  por color es la forma de medir el efecto pesimista directamente.

  En la nota lo recomendamos como objetivo opcional al final de la propuesta,
  formulado como pregunta. No está en la v2.2 ni en el archivo de experimentos 2
  a 4; si querés lo agrego como experimento 5 opcional.

✻ Cooked for 41s · done Sunday 27 Sep at 5:53 pm

❯ bien y como es que podríamos probar descubrimiento?                           

⏺ Corto: dentro de imitación pura, el descubrimiento estricto es imposible por
  teoría, así que lo que se puede hacer es medirlo para mostrar que da cero, y
  luego buscar la versión más débil que sí sea testeable. Lo que sigue está en
  parte en non-explored-ideas/discovery-ideas.md y en parte es nuevo.

  Por qué es imposible en sentido estricto

  A τ→0 el modelo juega el argmax de la mezcla que estimó. Si en un estado visto
  ninguna jugada m tiene masa en los datos, la mezcla verdadera le da cero y el
  argmax no puede ser m. Ya lo medimos en la exploración con la condición blind
  (nadie abre al centro): P(centro | tablero vacío) = 0 a τ→0. Esto no es un
  hallazgo, es la Proposición 2 de [1] funcionando. [2] lo dice explícito: su
  marco no captura skill discovery.

  Escalera de lo que sí se puede testear, de menos a más ambicioso

  1. Tasa de descubrimiento estricto como control cuantitativo. Fracción de
     estados vistos donde el argmax del modelo es una jugada con masa empírica
     cero en ese tablero exacto. Predicción: cero en todas las configuraciones.
     Costo nulo: sale de los conteos por tablero que ya necesita el
     experimento 3. Convierte "no hay descubrimiento" de anécdota en número.
  2. Punto ciego global. Una jugada buena que ningún experto juega nunca, en
     ningún estado, como el centro en blind. Acá ni la generalización puede
     ayudar, porque no hay estados parecidos donde la jugada aparezca. Es el
     control negativo más limpio y vale para todas las temperaturas y también
     para el modelo condicionado por resultado. Predicción: cero.
  3. Punto ciego local, que es generalización y no descubrimiento. En π = 1 con
     hash, todos los expertos erran en B pero el modelo acierta en estados de B
     no vistos. Ningún experto sabe la respuesta en ese estado, pero la saben en
     estados parecidos. Esto es lo más cerca de descubrimiento que da
     imitación, y hay que llamarlo generalización como hace [2]. Límite
     metodológico a dejar por escrito: en estados no vistos, descubrimiento y
     generalización son indistinguibles sin una noción de "estado parecido", y
     no la tenemos. El continuo de representabilidad (sesgos definidos por
     rasgos del tablero cada vez más difíciles de aprender) da una curva entre
     los dos extremos.
  4. Condicionar por resultado. Lo que hablamos antes. Puede superar el argmax
     de la mezcla, pero sigue eligiendo entre jugadas que están en los datos: no
     es descubrimiento.

  La única prueba que me parece genuinamente interesante y que no rompe el marco

  Separar lo que el modelo sabe de lo que juega. El modelo predice el token de
  resultado, así que aprende implícitamente una función de valor. La pregunta
  es: en el punto ciego global, ¿el modelo sabe que la jugada prohibida es buena
  aunque nunca la juegue?

  - Construcción: condición blind (nadie abre al centro). Evaluación: se le dan
    secuencias fuera de distribución que sí contienen el centro en la apertura,
    seguidas de la partida, y se lee qué resultado predice. Se compara la
    probabilidad de "gana" que asigna tras la apertura central contra la que
    asigna tras las aperturas que vio.
  - Si el valor implícito prefiere el centro, el conocimiento existe en la
    representación pero la política no lo usa. Eso es "descubrimiento latente":
    muestra que una búsqueda en inferencia podría extraerlo. Si no lo prefiere,
    el punto ciego es total.
  - Es la metodología de Mészáros et al. [15] (tests fuera de distribución sobre
    transformadores de ajedrez), ya citado en la propuesta. Costo: un modelo
    que ya existe y un script de evaluación.

  Lo que sería descubrimiento de verdad y por qué queda afuera

  Usar el modelo como prior y su predicción de resultado como valor para hacer
  búsqueda en inferencia, tipo MCTS, o hacer auto-juego iterado. Ahí sí podría
  aparecer el centro. Pero ya no es imitación: [1] restringe su alcance a lo que
  provee la pérdida de entropía cruzada, y el auto-juego converge al argmax de
  la mezcla y conserva los sesgos representables (es la literatura de model
  collapse). Para la tesina, lo dejaría como trabajo futuro con una oración: la
  prueba de valor latente del punto anterior es justamente lo que diría si vale
  la pena intentarlo.

  Mi recomendación, siguiendo el pragmatismo: 1 y 2 entran gratis en los
  experimentos ya diseñados; la prueba de valor latente es un experimento 5
  opcional chico; el resto va a "trabajo futuro".

✻ Brewed for 47s · done Sunday 27 Sep at 5:58 pm

❯ y si ignoramos el pragmatismo por un momento y nos ponemos creativos: hay     
  algo que se pueda testear facilmente pero que sea muy interesante como por    
  ejemplo algo en test time escaling? o reasoning?                              

⏺ Sí, hay varias, y lo lindo es que casi todas son sólo inferencia sobre modelos
  que ya vas a tener entrenados. Las ordeno por la relación interés/costo.

  1. Ensamble por simetría en test time (la más barata y la más linda). Connect4
  es simétrico al espejar el tablero. Evaluás p(jugada | secuencia) y
  p(espejo(jugada) | espejo(secuencia)) y promediás. Sin entrenar nada tenés un
  "segundo experto" cuyos errores están decorrelacionados por la transformación.
  El punto fuerte: el error compartido del experimento 1 ("columna legal más a
  la izquierda") es antisimétrico bajo espejo, así que el modelo espejado vota
  por la derecha, el original por la izquierda, y la jugada óptima, que es
  simétrica, queda como mayoría. Un sesgo compartido y representable, que la
  teoría dice que sobrevive a τ→0, se cancela con un promedio de dos pasadas.
  Predicción: en P = 1 con regla, la ganancia pasa de negativa a positiva; en P
  = 0 no cambia nada; con hash tampoco (el hash no tiene estructura bajo
  espejo). Es la fórmula de Pablo con un ρ que vos controlás por diseño de la
  transformación. Costo: una función de espejo y una tarde.

  2. Test-time scaling como voto sobre trayectorias. Zhang usa una unidad de
  cómputo por jugada: el argmax. Alternativa: desde el estado, hacé N rollouts
  con el propio modelo a τ = 1 jugando ambos lados hasta el final, y elegí la
  jugada con mejor resultado promedio. Curva de ganancia en función de N ∈ {1,
  4, 16, 64}. Es la versión juego de self-consistency y best-of-N, y acá tenés
  el techo exacto. Lo interesante es dónde probarlo: en selección con α < α*,
  donde el argmax empeora al modelo. Hipótesis: el voto sobre expertos falla
  ahí, pero el voto sobre trayectorias no, porque la jugada compartida errónea
  pierde deterministicamente contra un solver y eso se ve en los rollouts.
  Predicción pesimista, de la literatura de RCSL: el rival en los rollouts es el
  modelo mismo, ruidoso, así que el valor estimado premia jugadas que "ganaron
  porque el rival erró después". Dos predicciones opuestas y una curva que
  decide. Costo: sólo inferencia, un script.

  3. Crítico denoiseado vs. actor denoiseado. Todo el marco de trascendencia es
  sobre el voto en el espacio de acciones. Variante: los expertos anotan cada
  posición con un valor ruidoso (el del solver más ruido independiente por
  experto), y el modelo aprende también a predecir el valor. En inferencia hace
  búsqueda de una jugada: evalúa los 7 hijos con su propio valor y elige el
  mejor. Pregunta: ¿el voto en el espacio de valores trasciende donde el voto en
  acciones no? Podés diseñar que los errores de jugada sean compartidos (P = 1)
  y los errores de valor independientes, o al revés. Es "razonamiento" en su
  forma mínima, un ply de lookahead, con la ventaja de que separás dos canales
  de ruido que en datos humanos vienen mezclados. Costo: un token más por jugada
  en el generador y una cabeza de salida.

  4. Trazas de razonamiento en los datos. Cada experto, antes de jugar, emite
  una traza corta: la línea principal que él cree (una variante de d jugadas
  generada con su propia política ruidosa). El modelo aprende a generar la traza
  y luego la jugada. Variables: profundidad d en entrenamiento, y en test
  forzar trazas más largas que las vistas. Preguntas: ¿condicionar la jugada a
  una traza propia reduce el error respecto de jugar directo? ¿la traza se
  denoisea igual que la jugada? Es el análogo sintético de chain-of-thought con
  ground truth exacto para cada paso de la traza. Es la más cara de las cuatro
  porque cambia el vocabulario y la longitud de secuencia, pero sigue siendo un
  modelo de 6M.

  5. Cómputo adaptativo. Usar la entropía del modelo en cada estado como señal
  de "acá el voto está peleado" y gastar rollouts sólo ahí. Cruza el experimento
  3: la entropía debería ser alta justo en estados no vistos y cerca del umbral
  α*. Barato, pero es un refinamiento de 2 más que una pregunta nueva.

  Si tuviera que elegir una para meter en la tesina como capítulo extra, la 1:
  cuesta casi nada, tiene una predicción exacta derivada de la teoría, y da una
  frase memorable: un sesgo compartido que la temperatura no elimina se elimina
  con una simetría del dominio. La 2 es la más "de moda" y la que más le
  hablaría a alguien que viene de LLMs; la 3 es la que tiene más chance de ser
  un aporte conceptual real, porque nadie separó ruido en acciones de ruido en
  valores en esta línea.

✻ Crunched for 1m 21s · done Sunday 27 Sep at 6:02 pm

❯ bien y en general podés analizar todos los experimentos y ver si no hay algo  
  que nos reste hacer que es interesante y alguien podría decir "probaste       
  esto?"                                                                        

⏺ Hice el repaso con cabeza de revisor (Pablo, o un jurado que leyó los dos
  papers). Lo agrupo por qué tan probable es la pregunta y qué tan barato es
  cerrarla. Casi todo es sólo generar datos y correr configuraciones sobre el
  pipeline que ya existe.

  Las que casi seguro te preguntan

  1. "¿Verificaste la fórmula o un punto?" En el experimento 2 el umbral α* =
     (K−2)/(2K−2) se testea sólo en K = 4. Con K ∈ {2, 4, 8} verificás la
     dependencia en K (α* = 0, 1/3, 0.43). Tres configuraciones más.
  2. "¿Y cuando hay pocos expertos?" Pablo te mandó literalmente la fórmula con
     el término (1−ρ)σ²/n, y en el experimento 1 n es infinito porque el error
     independiente se sortea en cada visita. Con K expertos persistentes
     (errores fijos por estado y por experto, vía hash con semilla del experto)
     aparece el término 1/n y el voto se vuelve un voto entre K. Barrido K ∈ {2,
     3, 5, 10, ∞}. Es la pregunta más probable de Pablo.
  3. "¿Trasciende al mejor experto o al promedio?" Todos tus expertos tienen el
     mismo ρ, así que "mejor experto" y "experto típico" coinciden y la
     definición de [1] se testea en su caso más fácil. Con una población
     heterogénea (por ejemplo mitad ρ = 0.1 y mitad ρ = 0.5) la mezcla es
     arrastrada por los malos y la pregunta es si supera al mejor. Es
     exactamente la diferencia entre los datasets ≤1000 y ≤1500 de Zhang. Dos o
     tres configuraciones.
  4. "¿Qué pasa con ρ ≥ 0.5?" ρ está fijo en 0.3. Pero como el error
     independiente se reparte entre varias columnas, el argmax de la mezcla
     puede seguir siendo óptimo con ρ = 0.6 o 0.7. Es trascendencia con expertos
     mayoritariamente equivocados, el caso de Rolnick [6]. Barrido ρ ∈ {0.1,
     0.3, 0.5, 0.7} en P = 0. Predicción exacta disponible por estado.
  5. "¿Cuántos votos necesita el voto?" El experimento 3 etiqueta visto/no visto
     de forma binaria. Estratificar la ganancia por cantidad de visitas en
     entrenamiento (0, 1, 2 a 5, 6 a 20, más de 20) da la figura más directa de
     todo el trabajo: ganancia en función del número de votos por posición.
     Costo cero, sale de los conteos que ya hacés.
  6. "¿Reproducís la métrica de diversidad de Zhang?" [1] explica su resultado
     con la entropía media de la distribución de jugadas en posiciones
     frecuentes. Calculá esa misma entropía en cada dataset del barrido en P.
     Como el error compartido concentra masa en una jugada, la entropía baja con
     P. Mostrás su correlación y que la causa es la estructura del error. Es un
     cierre muy limpio con [1] y cuesta un script.

  Inconsistencias a resolver antes de que alguien las note

  7. Semillas. La propuesta v2.2 dice "todas las condiciones se repetirán con
     varias semillas"; el experimento 1 dice que no se repiten. La exploración
     midió desvíos de 0.001 a 0.005, o sea que 3 semillas cuestan poco y evitan
     la objeción. Decidí una y alineá los dos documentos.
  8. Regla de parada. Elegís el checkpoint de mejor val loss, pero val loss mide
     qué tan bien imita datos ruidosos, no cuánto trasciende. Reportá la curva
     de ganancia en función del paso junto con la val loss, para mostrar que el
     pico de trascendencia coincide con el mínimo. Ya tenés los checkpoints. Y
     el hallazgo de memorización (10 vs 42 épocas) tiene que estar en la tesina
     como justificación del régimen, hoy no está en ningún objetivo.

  Las que un jurado fino podría hacer

  9. Escuelas de expertos. "Los humanos no comparten errores todos o nadie: hay
     escuelas." Dos o tres clusters, cada uno con su error compartido en sus
     propios estados, con tamaños 50/50, 70/30, 90/10. El voto pasa a ser entre
     clusters y la trascendencia depende de la distribución de tamaños, no de la
     correlación pareada. Es el puente entre P y el ρ de Pablo.
  10. Composición con ruido. El experimento 4 no tiene errores. "¿Se compone y
      se cancela ruido a la vez?" Familia B con ρ = 0.3 independiente. Una
      configuración.
  11. Desplazamiento de valor en el experimento 4. Los finales de B vienen de
      aperturas de borde, que probablemente son posiciones perdidas para el
      primero; los finales tras aperturas óptimas son posiciones ganadas. Estás
      transfiriendo entre clases de valor distintas. Reportá la distribución
      ganada/empate/perdida en cada una de las tres distribuciones de
      evaluación. Costo cero, y si no lo reportás alguien lo va a señalar como
      confusor.
  12. Ablación del token de resultado. El modelo aprende a predecir el
      resultado. "¿Eso ayuda a trascender?" Entrenar sin el token en P = 0 y
      comparar. Una configuración. Conecta con la idea de condicionar por
      resultado.
  13. Escala en el barrido de P. El panel de 320K está sólo en P = 0. "¿La curva
      en P se acerca a la teoría con más datos?" Cinco configuraciones más, ya
      lo habías anotado en la conversación del experimento 1.
  14. Tamaño del modelo. Sólo 6M salvo en composición. Un barrido 0.1M, 0.8M, 6M
      en P = 0 cierra "¿es un efecto de capacidad?".

  Trabajo futuro, no lo haría

  Darle el tablero al modelo en vez de la secuencia (separa representación de
  voto, pero cambia la tokenización), y todo lo de test-time scaling y
  descubrimiento de los mensajes anteriores.

  Si tuviera que meter cinco y nada más: 2, 3, 5, 6 y 7. Las cuatro primeras son
  las que más le hablan a Pablo y a [1], y la séptima es una inconsistencia
  entre documentos.

✻ Brewed for 1m 29s · done Sunday 27 Sep at 6:53 pm

❯ ahora quiero que vayas 1 por 1 de los 22 citations que tiene el papper [1]    
  analizando si alguno de esos trabajos que se desprendieron no probaron algo   
  de lo que nosotros estamos probando                                           
⏺ Primero verifico qué son los 22: la bibliografía del PDF de [1] o los trabajos
  que lo citan.

  Ran 1 shell command (ctrl+o to expand)

⏺ La bibliografía de [1] tiene 37 entradas, no 22, así que interpreto que los 22
  son los trabajos que citan a [1]. Los busco en Semantic Scholar.

  Ran 2 shell commands (ctrl+o to expand)

⏺ Fetch(https://arxiv.org/abs/2602.04447)
  ⎿  Received 40.3KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2512.09152)
  ⎿  Received 41.1KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2410.04638)
  ⎿  Received 41.1KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2607.16097)
  ⎿  Received 43.8KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2512.24940)
  ⎿  Received 40.3KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2502.01612)
  ⎿  Received 41.5KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2410.03893)
  ⎿  Received 42KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2605.05742)
  ⎿  Received 40.6KB (200 OK)

⏺ Fetch(https://arxiv.org/abs/2410.09038)
  ⎿  Received 41.1KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2602.04447)
  ⎿  Received 0 bytes (404 Not Found)

⏺ Fetch(https://arxiv.org/html/2512.09152)
  ⎿  Received 442.1KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2410.04638)
  ⎿  Received 964.7KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2607.16097)
  ⎿  Received 726.7KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2512.24940)
  ⎿  Received 706.7KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2502.01612)
  ⎿  Received 489.9KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2410.03893)
  ⎿  Received 207.1KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2605.05742)
  ⎿  Received 950.2KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2510.21332)
  ⎿  Received 699.5KB (200 OK)
⏺ Fetch(https://arxiv.org/html/2508.17018)
  ⎿  Received 433.6KB (200 OK)

⏺ Fetch(https://arxiv.org/pdf/2602.04447)
  ⎿  Error: maxContentLength size of 10485760 exceeded

⏺ Fetch(https://arxiv.org/html/2408.15240)
  ⎿  Received 404.8KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2410.04571)
  ⎿  Received 465KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2405.16236)
  ⎿  Received 626.3KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2505.21444)
  ⎿  Received 356.8KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2510.20783)
  ⎿  Received 239.5KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2502.18822)
  ⎿  Received 231.8KB (200 OK)

⏺ Fetch(https://arxiv.org/html/2412.06636)
  ⎿  Received 280.3KB (200 OK)

⏺ Ya recorrí casi todos; me falta sólo el texto completo de Mixture of Masters,
  que es el más relevante para el experimento 2. Lo bajo con curl.

  Ran 3 shell commands (ctrl+o to expand)

⏺ Recorrí los trabajos que citan a [1] según Semantic Scholar. Son 29 entradas
  con 3 duplicados, o sea 26 únicos (el 22 que viste probablemente es de otro
  índice). Leí el texto completo de los que tenían alguna chance de solaparse y
  sólo el abstract de los que claramente no. Veredicto corto primero: nadie hizo
  lo que estamos haciendo, pero cinco trabajos tocan algo nuestro de costado y
  conviene citarlos o anticipar la pregunta.

  Los que se solapan parcialmente (leer y citar)

  1. Mixture of Masters (Frisoni et al. 2026). Lo más cercano al experimento 2.
     MoE de ajedrez con 5 expertos, uno por gran maestro, y una compuerta
     aprendida sobre el estado. Parten de los propios modelos de [1]. Resultado:
     la mezcla ruteada supera al mejor experto individual (+15.0 FIDEScore vs
     +11.5), y un control con particiones aleatorias de los mismos datos no lo
     logra: la ganancia viene de la especialización, no de la diversidad. Es
     selección de habilidades con ruteo explícito en la arquitectura y
     decodificación greedy. No hay umbral, no hay control de errores, no hay
     visto/no visto. Nuestro aporte queda claro por contraste: ruteo implícito
     en una sola red, con α como perilla y α* como predicción.
  2. Self-Improving Transformers (Lee et al. 2025). Citan "trascendencia" como
     generalizar un poco más allá de la dificultad de los datos. Filtran datos
     autogenerados por voto de mayoría entre k modelos y estudian tolerancia al
     ruido inyectado: el ruido estructurado daña más que el uniforme, y los
     modelos memorizan sus errores pasados sin que eso frene la generalización.
     Es nuestro "compartido y representable vs. independiente" y nuestro régimen
     de memorización, en aritmética y laberintos en vez de en un juego. No
     manipulan correlación. Citarlo en la discusión de representabilidad.
  3. Understanding temperature tuning in energy-based models (Fields et 
     al. 2025). Teoría de por qué bajar la temperatura corrige la
     sobreestimación de estados improbables cuando hay pocos datos, y cuándo
     conviene subirla. Es exactamente nuestra "entropía residual del modelo": la
     parte de la ganancia a τ→0 que no es voto sobre expertos sino corrección
     del estimador finito. Ellos no separan ruido de datos de ruido de
     estimación; nosotros sí podemos, porque tenemos la mezcla verdadera. Citar
     en el objetivo 3.
  4. Provable weak-to-strong via benign overfitting (Wu y Sahai 2024). El
     estudiante memoriza las pseudoetiquetas ruidosas y aun así generaliza, con
     dos fases (éxito o azar) según datos y dimensión. Citan a [1] por el rol de
     la temperatura. Es la contracara teórica de nuestro hallazgo de
     sobreentrenamiento: ellos dicen que memorizar ruido puede convivir con
     generalizar; nosotros medimos que en el argmax destruye el voto. Un jurado
     puede preguntar por esto; la respuesta es que ellos miran generalización de
     la clasificación y nosotros el argmax por estado. Un solo maestro, sin
     correlación.
  5. Weak-to-strong is nearly inevitable in linear models (Geng et al. 2026).
     Teorema: el estudiante supera al maestro si los errores de ambos están poco
     correlacionados en las direcciones ortogonales a la verdad. Es la
     condición de decorrelación de errores en otro formalismo. Un maestro, sin
     temperatura. Citar junto a la fórmula de Pablo.

  Tangenciales (una línea cada uno, no los probaron)

  6. A Taxonomy of Transcendence. Es [2]; ya cubierto.
  7. Mészáros et al. 2025. Ya citado como [15]. Confirmado: no hay composición
     entre demostradores con soporte disjunto ni visto/no visto; entrenan con
     etiquetas de Stockfish, no con humanos.
  8. Understanding Reasoning from Pretraining to Post-Training (Shen et 
     al. 2026). Ajedrez como testbed, modelos de 5M a 1B, RL sobre puzzles. Lo
     interesante: definen "tail discovery" como jugadas con p < 0.05 bajo la
     política SFT que el RL promueve al top-3. Es descubrimiento con refuerzo,
     no con imitación; y dejan trascendencia como trabajo futuro explícito. Sus
     datasets son disjuntos a nivel posición pero no analizan visto/no visto.
  9. Human-aligned chess with a bit of search (Allie, Zhang et al. 2024). Cabeza
     de valor entrenada con el resultado de la partida y MCTS adaptativo.
     Precedente directo de la idea de "valor latente" y de test-time compute
     sobre un imitador; muestrean a τ = 1. No comparan contra los jugadores de
     entrenamiento.
  10. Iterative Deployment (Corrêa et al. 2025). Reentrenar sobre trayectorias
      filtradas por éxito, generación tras generación; descubren planes más
      largos que el modelo inicial. Es condicionamiento por resultado a través
      de generaciones, y prueban que equivale a RL implícito. Citar en trabajo
      futuro si mencionamos auto-juego.
  11. Can Large Reasoning Models Self-Train (Shafayat et al. 2025). Voto de
      mayoría como recompensa; colapsa por reward hacking. No analizan
      correlación de errores.
  12. Free-Gate (Rossi et al. 2024). Composición de primitivas que
      individualmente no resuelven la tarea, con un "Remark: Transcendence"
      formal: la composición supera estrictamente a cada primitiva. Robótica,
      ruteo explícito. Buena cita para el experimento 4.
  13. Generative Verifiers (Zhang et al. 2024). Citan a [1] por el efecto de
      "ensamble" de entrenar con varios razonamientos por solución. Curvas de
      accuracy vs. número de votos. Test-time, no imitación.
  14. EnsemW2S (Agrawal et al. 2024). Ensamble de expertos débiles a nivel
      token, estilo AdaBoost. Sin análisis de diversidad ni de cuántos expertos
      hacen falta.
  15. RAVEN (Jeon et al. 2025). Combinación ponderada de modelos débiles con
      pesos aprendidos; asigna más peso al más preciso. No es ruteo por entrada.
  16. Somerstep et al. 2024 y 2025 (dos trabajos). Refinamiento para
      weak-to-strong; el error irreducible depende del sesgo sistemático del
      etiquetador débil, no del ruido aleatorio. Misma distinción que la
      nuestra, un solo etiquetador.
  17. SimpleStrat (Wong et al. 2024). Subir la temperatura para diversidad baja
      la calidad. Citan a [1] de pasada.
  18. Data-efficient multi-agent planning (Su et al. 2025). Rollouts mejoran
      sobre el imitador, en un problema de taxis. Cita genérica.

  Irrelevantes para nosotros (citan a [1] como ejemplo de "la IA puede superar a
  sus fuentes")

  19 a 26. Noospheric Technologies; The Future of AI in Ecosystem Modeling; AI
  as Governance; Language as a cognitive and social tool; AI Safety survey;
  Annotation Vocabulary (proteínas); Quantifying Conceptual Brittleness; y el
  duplicado de Self-Improving Transformers sin metadatos.

  Qué me llevo para la tesina

  - Nadie después de [1] y [2] corrió un experimento controlado sobre
    correlación de errores, ni descompuso visto/no visto, ni compuso
    demostradores de soporte disjunto. El hueco sigue abierto.
  - La pregunta "¿probaste esto?" más probable a partir de esta lista es Mixture
    of Masters para el experimento 2: hay que citarlo y marcar la diferencia
    entre ruteo explícito y ruteo implícito en los datos.
  - Fields 2025 y Geng 2026 dan dos citas teóricas que hoy no tenemos: una para
    la entropía residual del estimador y otra para la condición de
    decorrelación.
  - Lee 2025 es el precedente de "el ruido estructurado sobrevive, el uniforme
    no", que es nuestro hallazgo de representabilidad en otro dominio.

✻ Worked for 4m 0s · done Sunday 27 Sep at 7:13 pm

※ recap: Estamos diseñando los experimentos de la tesina: ya escribí experimentos2-3-4.md y revisé los 26 trabajos que citan a [1] sin hallar solapamiento. Próximo paso: decidir los TODO abiertos del archivo y agregar Mixture of Masters como cita. (disable recaps in /config)

❯ a granito no le convence el diseño del experimento1, escribió                 
  Lo que yo entiendo: en este juego hay un “estado” dado por la posición actual 
  del tablero, y hay una secuencia de jugadas que llevaron a ese estado. Hay    
  muchísimas más secuencias posibles que estados posibles. Pero lo que le       
  estamos mostrando a los learners son secuencias y no estados. Por lo que      
  forzamos al learner a aprender el estado en base a la secuencia No se si esto 
  traerá problemas de independencia entre train y test, cosa a pensar mejor.    
  No tengo claro que sería generar errores correlacionados en este contexto.    
  Quizás podría ser usando una definición espacial del tablero. Expertos que no 
  “entienden” tal zona. Si la jugada óptima depende de ocupar un casillero en   
  tal zona de 3x3, este experto se equivoca. Y todos estos se equivocan igual.  
  Pero no se si tiene sentido. Hay que entender mejor el rol de la conversión   
  secuencia-estado para entender la correlación, me parece.                     
  realmente no entiendo su punto yo le escribí:                                 
  Si, a los learners le suministramos las partidas                              
                                                                                
  Trabajos anteriores muestran que un modelo entrenado en partidas de ajedrez   
  tal como nosotros hacemos para predecir la siguiente jugada construye una     
  representación interna del tablero                                            
                                                                                
  Así que supongo que para nuestro caso que es más simple también lo hace       
                                                                                
  No obstante, cuando acá digo que hay estados repetidos me refiero a que hay   
  secuencias repetidas entre el train y test. Por ejemplo si entreno con 300K   
  partidas entonces el modelo seguro vio todas las partidas de longitud 2,3,4   
  etc                                                                           
                                                                                
  Eso es lo que me preocupaba: que tan válido son la resultados si la           
  intersección entre train y test es no vacía                                   
                                                                                
  Lo que vos mencionas es interesante. En este primer experimento no hago eso   
  porque no tengo N expertos sino que cada partida es un experto independiente. 
                                                                                
  Lo que vos sugerís es lo que hice para el experimento de selección: donde     
  tengo diferentes expertos en diferentes áreas y eso lo construyo como         
  expertos que juegan óptimo en cierta región del tablero                       
  y agregue por whatsapp                                                        
  [3:45 PM, 9/28/2026] .: Yo creo que habría que formalizar un poco más la idea 
  de "los errores no están correlacionados" porque no te estoy entendiendo.     
  O sea, entiendo tu idea intuitiva pero yo creo que sí son correlacionados y   
  no sé cómo desempatar                                                         
                                                                                
  Mi training set = { (X, y) }                                                  
  Donde X = secuencia de jugadas                                                
  y = siguiente jugada                                                          
                                                                                
  Cada elemento del training set se le puede calcular una ganancia r = {1, 0}   
  dependiendo si la jugada es óptima o no                                       
                                                                                
  Y la idea es tener 2 training set "sesgado" y "no sesgado"                    
  En ambos la accuracy media es igual (lo que es lo mismo a decir que la tasa   
  de error es la misma)                                                         
  Pero en "sesgado" están distribuidos de cierta manera.                        
  [3:47 PM, 9/28/2026] .: Hasta ahí estamos de acuerdo. Lo que pensás que es    
  incorrecto es que se pueda definir "sesgado" como                             
  "if longitud X es multiplo de 3 then jugar la posicion mas a la izquierda"    
                                                                                
  No estoy seguro pero creo entender que lo que no te convence es la parte de   
  "if longitud X es multiplo de 3"                                              
  [3:49 PM, 9/28/2026] .: Me parece que es obvio que guardan una correlacion    
  esos estados. Pero si quisiera, ademas mostrar que esa correlacion es         
  representable por el modelo podría entrenarlo para clasificar esas jugadas. O 
  sea { (X, y) } donde y = 1 o 0 dependiendo de si "if longitud X es multiplo   
  de 3"                                                                         
                                                                                
  Esto es lo que no entiendo, que vos digas que "no son estados                 
  correlacionados" cuando seguro que un clasificador los puede separar          
  [3:51 PM, 9/28/2026] .: Ahora bien, tu duda también iba por el lado de si     
  tenían la misma proporción de errores los 2 training set                      
  Eso por construcción es así, solo que en "no sesgado" los errores se          
  construyen siguiendo la regla: "if rand() < p_error entonces elegir random un 
  movimiento erróneo"                                                           
  ⎿  1 skill available

⏺ Creo que Pablo está diciendo dos cosas distintas y las respuestas se cruzaron
  con una tercera. Voy por partes y al final te dejo un borrador para
  contestarle.

  Qué dice Pablo, en mis palabras

  1. Secuencia vs. estado. El modelo ve secuencias, la teoría de [1] habla de
     estados, y muchas secuencias llevan al mismo estado. Su duda de
     "independencia entre train y test" es sobre si las unidades de análisis
     están bien definidas: ¿qué es "un ejemplo"? ¿Qué es "un estado repetido"?
     ¿Los prefijos de una misma partida son ejemplos independientes?
  2. Qué es "correlación de errores" acá. Él viene de la fórmula Var = ρσ² +
     (1−ρ)σ²/n, donde ρ es la correlación entre los errores de dos expertos en 
     el mismo input. Para que eso exista hacen falta expertos con identidad y
     varios expertos evaluados en el mismo estado. En tu diseño no hay expertos
     persistentes ("cada partida es un experto") y el error compartido es una
     función determinista del input. Para él eso no es "correlación entre
     expertos", es sesgo sistemático: un error que depende de x. Por eso dice
     "creo que sí son correlacionados y no sé cómo desempatar": en el set "no
     sesgado" no hay nada que correlacionar, y en el "sesgado" lo que hay es una
     función de x, no un ρ.

  Su propuesta de la zona 3×3 es su forma de decir "definí el error compartido
  como propiedad del estado, no de la secuencia", que es como piensa la teoría.

  Dónde se cruzaron los cables

  - Vos contestaste "estados repetidos" hablando de solapamiento de secuencias
    entre train y test. Es una preocupación válida pero es otra: es el
    experimento 3, no la correlación.
  - El argumento del clasificador prueba representabilidad (que el modelo puede
    detectar la regla), no correlación. Pablo no discute que sea representable;
    discute qué significa correlación cuando no hay expertos.
  - "Cada partida es un experto independiente" es exactamente lo que le hace
    ruido: con esa construcción, ρ entre expertos ni siquiera está definido.

  Cómo desempatar: las dos cosas son equivalentes, y se puede calcular

  Tu P y su ρ son el mismo objeto visto desde dos lados. Tomá dos expertos
  cualquiera de la población y su indicador de error en un estado no trivial. En
  los estados de B (fracción β = P·ρ) ambos erran seguro; afuera, erran
  independientemente con probabilidad q. Entonces:

  P(err_i) = β + (1−β)·q = ρ                 (por construcción)
  P(err_i ∧ err_j) = β + (1−β)·q²
  Pearson(err_i, err_j) = [β + (1−β)·q² − ρ²] / [ρ·(1−ρ)]

  Con ρ = 0.3:

  ┌──────┬───────┬───────┬─────────┐
  │  P   │   β   │   q   │ Pearson │
  ├──────┼───────┼───────┼─────────┤
  │ 0    │ 0     │ 0.300 │ 0.00    │
  ├──────┼───────┼───────┼─────────┤
  │ 0.25 │ 0.075 │ 0.243 │ 0.19    │
  ├──────┼───────┼───────┼─────────┤
  │ 0.5  │ 0.150 │ 0.176 │ 0.41    │
  ├──────┼───────┼───────┼─────────┤
  │ 0.75 │ 0.225 │ 0.097 │ 0.68    │
  ├──────┼───────┼───────┼─────────┤
  │ 1    │ 0.300 │ 0     │ 1.00    │
  └──────┴───────┴───────┴─────────┘

  O sea: P es una forma de barrer el ρ de Pablo entre 0 y 1, a tasa de error
  fija, y podés reportar el eje en ρ. Esto es la sección "Correlación de errores
  entre expertos" que está en "Pendiente" en experimento1-v1.md. La diferencia
  con su modelo equicorrelacionado es dónde se pone la parte compartida: él la
  reparte uniforme en todos los estados, nosotros la concentramos en un
  subconjunto. Y eso es deliberado: si la repartís uniforme con ρ = 0.3, la
  jugada óptima sigue teniendo masa 0.7 en todos los estados, el argmax nunca
  falla y variar la correlación no muestra nada (lo discutimos como "lectura A"
  cuando diseñamos el experimento). Concentrarla es lo que hace que el techo ρσ²
  aparezca en el argmax.

  Sobre secuencia vs. estado

  La respuesta es que la unidad de análisis es el estado, no la secuencia, y que
  lo medimos: la etiqueta visto/no visto es por tablero, con transposiciones
  incluidas. Y el solapamiento no es un defecto sino una condición de la teoría:
  el voto ocurre por estado, y necesita que el estado se repita. Por eso se
  reporta la ganancia en vistos y no vistos por separado. Sobre la no
  independencia de los prefijos de una misma partida: es la misma situación que
  [1] y que cualquier modelo de lenguaje; la evaluación es por estado sobre
  partidas generadas con otra semilla.

  Dos cosas que yo haría, por pragmatismo

  - Adoptar su definición espacial como construcción de B, o al menos incluirla.
    "Los expertos se equivocan cuando la jugada óptima cae en una zona del
    tablero" es una función del estado, es representable, se parece a un sesgo
    humano (punto ciego), y es lo que tu co-director entiende como correlación.
    Tu regla por número de jugada también es una función del estado (es la
    cantidad de fichas) pero se ve como una propiedad de la secuencia, y eso es
    lo que a él le chirría. Cambiarla no cuesta nada.
  - Agregar K expertos persistentes (el 1b que teníamos como opcional): cada
    partida la juega un experto con identidad, y sus errores independientes se
    fijan por estado con una semilla por experto. Entonces la Pearson de la
    tabla se mide sobre un conjunto común de estados, que es literalmente lo que
    él pidió en la imagen 1, y aparece el término 1/n. Es la pregunta que igual
    te iba a hacer.

  Borrador para contestarle

  ▎ Creo que estamos hablando de dos cosas y me confundí al responderte.
  ▎
  ▎ 1. Sobre correlación. Tenés razón en que, tal como lo escribí, "correlación 
  ▎ entre expertos" no está definida porque no hay expertos con identidad. Lo 
  ▎ formalizo así: para dos expertos cualquiera de la población, en un estado no
  ▎ trivial, con probabilidad β ambos cometen el mismo error (estados 
  ▎ "sesgados"), y con probabilidad 1−β cada uno erra independientemente con 
  ▎ probabilidad q. Fijamos la tasa total ρ = β + (1−β)q = 0.3 y variamos qué 
  ▎ fracción de ese error es compartida. La correlación de Pearson entre los 
  ▎ indicadores de error de dos expertos queda [β + (1−β)q² − ρ²] / [ρ(1−ρ)], 
  ▎ que va de 0 a 1 a medida que la fracción compartida va de 0 a 1. Es tu ρ de 
  ▎ la fórmula de la varianza. La única diferencia con el modelo 
  ▎ equicorrelacionado es que concentramos la parte compartida en un subconjunto
  ▎ de estados en vez de repartirla uniforme; si se reparte uniforme con ρ = 
  ▎ 0.3, la jugada óptima sigue siendo mayoría en todos los estados y el argmax 
  ▎ nunca falla, así que no habría nada que medir.
  ▎ 2. Sobre cómo definir los estados sesgados. Me gusta más tu versión espacial
  ▎ que la mía: "los expertos se equivocan cuando la jugada óptima cae en tal 
  ▎ zona del tablero". Es una función del estado y no de la secuencia, y se 
  ▎ parece a un punto ciego. La adopto.
  ▎ 3. Sobre secuencia vs. estado. La unidad de análisis es el estado (el 
  ▎ tablero), no la secuencia. Etiquetamos cada estado de test como visto o no 
  ▎ visto según si el mismo tablero aparece en entrenamiento, por cualquier 
  ▎ secuencia, y reportamos la ganancia por separado en cada grupo. El 
  ▎ solapamiento no lo evitamos porque la teoría lo necesita: el voto es por 
  ▎ estado.
  ▎
  ▎ Además pensaba agregar una variante con K expertos persistentes, cada uno 
  ▎ con sus propios errores fijos por estado, para poder medir esa correlación 
  ▎ directamente sobre un conjunto común de posiciones y ver el término 1/n. ¿Te
  ▎ parece?

  Si querés, actualizo experimento1-v1.md con la fórmula en la sección pendiente
  y la construcción espacial de B como alternativa.

✻ Worked for 1m 46s · done Tuesday 11:23 am

❯ bien creo que pablo quiere que diseñemos un error compartido mas              
  correlacionado segun el estado del tablero tipo en el ajedrez sería "este se  
  equivoca siempre moviendo alfiles" "este se equivoca siempre de X manera"     
  como clusters de error o expertos se entiende? pero la verdad no se me ocurre 
  y hasta estoy considerando cambiar de juego                                   

⏺ Se entiende, y no cambiaría de juego: el problema no es el Connect4 sino cómo
  definimos la familia de errores, y eso es independiente del juego. Toda la
  infraestructura (solver, generador, evaluación exacta) sirve igual. Lo que
  Pablo pide tiene traducción directa, y de hecho sale un experimento mejor que
  el actual.

  La receta general

  Un tipo de experto (una "escuela") se define por tres cosas:

  - Un predicado sobre el estado f_k(e) ∈ {0,1}: la condición bajo la cual la
    escuela k "no ve" la jugada correcta.
  - Una regla de jugada errónea w_k(e): qué juega cuando falla.
  - Un ruido residual q independiente fuera de esos estados, para mantener la
    tasa total en ρ.

  Todos los expertos de la escuela k comparten f_k y w_k: sus errores coinciden
  estado por estado (correlación 1 dentro de la escuela). Dos escuelas con
  predicados disjuntos nunca fallan en el mismo estado (correlación 0 o
  levemente negativa). La correlación poblacional entre dos expertos al azar es
  aproximadamente la probabilidad de que sean de la misma escuela. La perilla 
  pasa a ser la estructura de escuelas, y eso es lo que Pablo entiende como
  correlación.

  Cuatro familias concretas en Connect4, de más simple a más "humana"

  1. Zona del tablero (la de Pablo). La escuela k no ve las jugadas cuya casilla
     óptima cae en su zona ciega: columnas de borde, columnas centrales, filas
     altas. Cuando todas las jugadas óptimas caen en la zona, juega la mejor
     jugada fuera de ella. Trivial de implementar, disjunto por construcción, y
     la tasa por zona se calibra porque el centro es óptimo mucho más seguido
     que los bordes.
  2. Dirección de la línea (el "siempre se equivoca con alfiles"). La escuela no
     ve amenazas diagonales: cuando la jugada óptima completa o bloquea una
     línea diagonal, no la considera. Otra escuela no ve horizontales. Es lo más
     parecido a un sesgo de ajedrez y muy fácil de explicar. Costo: detectar la
     dirección de la línea involucrada, que es una función local del tablero.
  3. Horizonte de cálculo. La escuela h juega óptimo si el solver fuerte dice
     que la victoria o derrota está a h o menos jugadas, y fuera de eso juega
     una heurística fija (por ejemplo, centro). Es la más humana ("este calcula
     dos jugadas"), y los errores quedan anidados: todo lo que falla el de
     horizonte 4 lo falla el de horizonte 2. Da una correlación estructurada
     distinta de la disjunta. Requiere el solver en modo fuerte.
  4. Heurística de estilo. La escuela juega siempre "pegado a la última ficha",
     o "apila sobre propia", o "centro si está libre", y sólo cuando eso no es
     óptimo cuenta como error. Es una política, no un predicado, así que la tasa
     de error no es controlable directamente. La dejaría afuera.

  Recomiendo la 1 como principal y la 2 como variante si queda tiempo. La 3 es
  un experimento aparte muy lindo, pero es otro eje.

  Lo que cambia en el experimento 1, y por qué es mejor

  Con escuelas aparece una predicción que el diseño actual no tiene. En un
  estado donde la escuela k falla, la masa de la mezcla en la jugada errónea es
  el peso w_k de esa escuela en la población, y la masa en la óptima es lo que
  aportan las demás. El argmax es erróneo si y sólo si la escuela es 
  mayoritaria, w_k > 1/2 (ajustando por el ruido residual). Entonces:

  - Barrido natural: C escuelas de igual peso, C ∈ {1, 2, 3, 5, 10}. Con C = 1
    todos comparten el error, es tu P = 1. Con C grande cada error es
    minoritario y el voto lo cancela. La correlación poblacional es ≈ 1/C y la
    ganancia debería subir con C. Es la curva de Pablo con n = número de
    escuelas.
  - Barrido alternativo: dos escuelas con pesos (w, 1−w), w ∈ {0.5, 0.6, 0.7,
    0.9}. Predicción: trascendencia a τ→0 en los estados de la escuela
    minoritaria, y no en los de la mayoritaria; el cruce en 0.5. Es un umbral
    falsable del mismo tipo que α* en selección.
  - Frase para la tesina: "un sesgo compartido por la mayoría de la población no
    se corrige por imitación, por mucha diversidad que haya en el resto".

  Además la correlación se puede medir y no sólo calcular: con expertos con
  identidad, tomás dos, los evaluás sobre un mismo conjunto de estados y
  calculás la Pearson de sus vectores de error. Es lo que Pablo pidió en la
  imagen 1, palabra por palabra.

  Qué se conserva del diseño actual

  Todo lo demás: tasa fija ρ = 0.3 sobre estados no triviales, ruido residual
  independiente fuera del predicado, mismas métricas, mismo barrido de τ, la
  celda de contraste con hash (un predicado no representable) sigue teniendo
  sentido como control. El "cada partida es un experto independiente" se
  reemplaza por "cada partida la juegan dos expertos muestreados de la población
  de escuelas", que es más fiel a [1].

  Sobre cambiar de juego

  Lo desaconsejo. Ningún otro juego resuelto te da algo que Connect4 no tenga
  para esto, y "no ve diagonales" o "no ve el borde" es tan legible como "no
  mueve bien los alfiles". Cambiar implica rehacer solver, generador y
  evaluación, y viola el principio risk-first: el riesgo que hay que cerrar
  ahora es el diseño del error, no el dominio.

  Si te cierra, reescribo la sección "Definición más formal" del experimento 1
  con escuelas por zona, el barrido en C y en w, la fórmula de correlación y la
  predicción del umbral de mayoría, y te preparo un mensaje corto para Pablo con
  la propuesta.

✻ Crunched for 1m 22s · done Wednesday 6:00 pm

※ recap: Estamos rediseñando el experimento 1 de la tesina para que el error compartido sea por escuelas de expertos definidas sobre el estado del tablero, como pide Pablo. Falta que confirmes para reescribir la sección formal y redactarle la propuesta. (disable recaps in /config)