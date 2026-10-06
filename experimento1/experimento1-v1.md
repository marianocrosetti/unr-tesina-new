# Experimento 1

## Elementos comunes a todos los experimentos

## Terminología

El diseño de cada experimento propone entrenar y evaluar el modelo en distintas **configuraciones**.&nbsp;  
Luego, se presentarán los resultados de cada **configuración** en las tablas comparativas incluidas en los resultados. Cada configuración corresponderá a una celda de la tabla.&nbsp;  
En la sección de diseño de cada experimento definimos las constantes y variables que utilizaremos para definir cada configuración que lo compone.&nbsp;  
Llamaremos **variables** a los valores que varían según la configuración y **constantes** a los que conservan el mismo valor en todas las configuraciones.

## Dominio elegido

Como juego resuelto de información completa y de dos jugadores hemos elegido el Connect4:

* Grilla 2D de 6 de alto por 7 de ancho.  
* 2 Jugadores.  
* En cada turno, eligen una columna `c ∈ [1,7]` donde se "deja caer" una ficha: la posición de la misma será `(h, c),` donde `h` es la altura del primer casillero vacío de abajo hacia arriba de la columna `c`.  
* No se puede jugar en una columna llena.  
* Si un jugador forma una línea vertical, horizontal o diagonal de 4 fichas consecutivas, gana.  
* Si el tablero está lleno, hay empate.

## Solver

Solver utilizado: [https://github.com/PascalPons/connect4](https://github.com/PascalPons/connect4).&nbsp;  
Nos devuelve si una posición es ganadora, perdedora o de empate (para el jugador que debe jugar en ese momento).

## Notación y Terminología

* Utilizaremos `estado` para registrar la configuración del tablero en un turno específico.  
* Utilizaremos `columna` para indicar la elección de la columna en la que dejar caer la ficha en cada turno; también llamaremos "**jugada"**.  
* **Jugadas legales**: para un estado el conjunto de columnas que no están llenas (y por ende podemos jugar):  
  `legales(estado) ⊆ [1,7]`  
* **El valor** de una posición es `valor(estado) ∈ {1, ½, 0},` según si `estado` es ganador, empatador o perdedor, respectivamente.&nbsp;  
  Nota: se podría haber utilizado otra convención como `{1, 0, -1}`. Lo importante es ser consistentes. Utilizar los valores elegidos es una decisión deliberada, en línea con \[1\], que utiliza la probabilidad de ganar (un número entre 0 y 1\) proporcionada por Stockfish.  
* **recompensa** de una jugada `columna` en un estado `estado`: `recompensa(estado, columna) ∈ {1, ½, 0}` según si lleva al oponente un estado ganador, empatador o perdedor:

`recompensa(estado, columna) = 1 - valor(estado')`

Siendo `estado’`, el estado obtenido al jugar en `columna,` estando en `estado`.

* **Jugadas óptimas**: las de máxima `recompensa`  entre las legales disponibles.  
* **Error**: acto de realizar una jugada legal pero no óptima.  
* **Estado trivial**: es el `estado` en el que todas las jugadas son óptimas.&nbsp;  
  Nos van a interesar sobre todo los *estados no triviales*, lo cual es equivalente a decir que:  
  * Los estados en los que tiene al menos una jugada cuya recompensa es inferior a la de la jugada óptima.  
  * Los estados en los que es factible equivocarse.&nbsp;

Cerca de la mitad de los estados son triviales. Es muy relevante para nuestro experimento que hablaremos de ρ como "proporción de error" o "probabilidad de equivocarse". Para nosotros la probabilidad aplicará sólo a estados no triviales. O sea, “de todas las jugadas de una partida donde era posible equivocarse (estados no triviales), qué fracción son errores”.&nbsp;  
De no hacer esta salvedad, las predicciones teóricas no coincidirían con los resultados experimentales.  
Notar que “la probabilidad de equivocarse en una jugada aleatoria” será un número menor: ajustada por la fracción que los no triviales representan del total de estados.&nbsp;

> ### Conjunto de datos

* Nuestros conjuntos de datos estarán compuestos por secuencias. Cada secuencia representará una partida.

* El **vocabulario** de las secuencias será los **12 tokens**: `{BOS, PAD, 1-0, 0-1, 1/2-1/2} ∪ [1,7]` (vs los 32 caracteres de la notación PGN  que utiliza \[1\]):

  * `BOS` es el token de inicio de secuencia  
  * `1-0`, `0-1` y `1/2-1/2` son los tokens de fin de secuencia que, además, indican el resultado de la partida. PGN utilizado en \[1\] también incluye los resultados, por eso los incluimos.  
  * `PAD`: token de padding para batching (ver sección de batching)  
* **Datos**: Cada partida se representa como una secuencia de los tokens mencionados. Al igual que \[1\], el modelo ve sólo la secuencia: ni el tablero ni la identidad del experto.

* **Batching:** a diferencia de \[1\] que construye batches concatenando partidas, nosotros proponemos utilizar padding ya que:

  * El padding sólo desperdicia cómputo, pero no influye en la escala que manejamos.  
  * Si tenemos múltiples partidas por fila, el modelo puede atender partidas anteriores (a menos que lo solucionemos a nivel de masking: si bien es posible, requeriría usar un masking complicado y dependiente de cada fila del batch)  
  * Razón principal: en nuestra representación, la posición en la dimensión de la secuencia corresponde al número de la jugada, por lo que estimamos que es más fácil para el embedding posicional codificar "estamos en la jugada t".&nbsp;  
    En nuestro diseño de error compartido utilizaremos patrones como "cada 3 jugadas", que estimamos que resultan *más fácilmente aprendibles* para el modelo con esta elección de batching.

### Modelo y entrenamiento

* Modelo:  decoder-only, base nanoGPT (idem \[1\]).  
* Hiperparámetros que mantuvimos de \[1\]:  
  * Optimizador AdamW, β \= (0.9, 0.95)  
  * Schedule cosine con warmup 200  
  * Weight decay 0.1  
  * Gradient clip 1.0  
  * Dropout 0  
  * Precision bfloat16  
  * Learning rate, (máximo y mínimo respectivos del schedule cosine utilizado): 3e-4, 3e-5  
* Hiperparámetros que escalamos a nuestro dominio:  
  * (Capas, cabezas, ancho): (8, 8, 256\) respectivamente (6,3 M de parámetros).  
    \[1\] Utiliza (16, 8, 512\) (50M de parámetros), nosotros lo achicamos porque tenemos un dominio dramáticamente más pequeño.&nbsp;  
* Batch size: 512 filas (recordar que para nosotros 1 fila : 1 partida), aproximadamente 22K tokens&nbsp;  
  Nota: \[1\] cuantifica el batch size en tokens ya que entrena concatenando partidas; ellos hacen batches de 125K tokens cada batch (\~300 partidas por batch). Nuestro batch es entre 6 y 10 veces más pequeño que \[1\], en línea con un modelo 8 veces más pequeño.  
* Epochs: Por determinar  
  * Los experimentos preliminares usaron 10 épocas de 80K partidas cada una. Y por eso debimos adoptar *early stopping*: evaluar el checkpoint con el mejor val loss, no el del final.  
  * \[1\] Entrena menos de una época; por eso no presenta riesgo de memorización.  
  * Un estudio de control con 320K muestra resultados aún mejores que con 80K partidas, lo que indica que debimos haber generado más datos para reducir el número de épocas.  
  * Técnicamente, podríamos generar suficientes datos como para no tener que repetir la partida. No está claro hasta qué punto generar datos tiene sentido. Chinchilla Laws para este tamaño de modelo da 5.5M  
* Repeticiones de entrenamiento: al igual que en \[1\], no repetiremos los entrenamientos. Hacerlo con varias semillas puede tener sentido en un contexto donde la elección de conjuntos de entrenamiento/test puede cambiar los resultados, pero no en deep learning con la cantidad de datos que manejamos y con la manera en que generamos los conjuntos de desarrollo y test (aleatoriamente, leer la última sección de este documento).

### Evaluación. (Recomiendo leer la definición más formal del experimento primero ya que usamos variables en las métricas que están definidas ahí)

Para la evaluación se tienen en cuenta sólo estados no triviales.

Se define la política a temperatura tal como define \[1\]:&nbsp;

`p_τ(c | e) = softmax(logits / τ)`

Vamos a definir tres métricas y cada una induce una noción distinta de trascendencia:&nbsp;

* Accuracy: es la probabilidad de que el modelo, a la temperatura τ, juegue una jugada óptima.  
* Recompensa esperada: matchea la definición teórica de trascendencia de \[1\]  
* Rating contra expertos

#### **Accuracy**

`acc_τ(e) = Σ p_τ(c | e)` sobre las jugadas `c` óptimas en `e`

`acc_τ    = promedio de acc_τ(e)` sobre los estados no triviales de test

Se deduce analíticamente que para la población de expertos vale:&nbsp;  
`acc(experto) = 1 − ρ`&nbsp;

Definimos *"trascendencia en accuracy"* si `acc_τ(modelo) > acc(experto)`

#### **Recompensa esperada**

`E[r]_τ(e) = Σ_c p_τ(c | e) · r(e, c)`

`E[r]_τ    =` promedio sobre los estados no triviales de test

A diferencia de `acc`, esta métrica pondera cada error por su costo: tirar una victoria a empate cuesta ½; a derrota, 1\.  
Análogamente se define “*trascendencia en recompensa"* si `E[r]_τ > E[experto]_τ`&nbsp;

#### **Rating contra expertos**

Es un paralelismo con lo que hace \[1\] para presentar su resultado principal: que el rating del modelo entrenado es superior al de los expertos haciendo jugar realmente al modelo entrenado contra expertos en vez de hacer el análisis estado a estado.&nbsp;  
En nuestro caso, lo calcularemos haciendo jugar 300 partidas completas (el mismo número que \[1\]) contra un bot que sigue la política de la población entrenada:

* 150 lo hará como primer jugador&nbsp;  
* 150 lo hará como segundo jugador

Para “jugar con el modelo” en cada estado se muestrea una columna de p\_τ&nbsp;  
Al igual que en \[1\], ante una salida ilegal se muestrea hasta 5 veces y luego la partida se considera perdida.&nbsp;  
Luego se define el score obtenido como:&nbsp;

`score = (victorias + ½ empates) / 300`

Hay trascendencia si `score > 0.5` (o sea: los resultados esperados del modelo son mejores que si hubiera jugado el experto contra sí mismo)

### Barrido de temperatura

En cada configuración del experimento se entrenará un modelo. (más adelante, en diseño del experimento, definimos las variables barridas en las configuraciones)  
Luego, para cada modelo entrenado se harán diferentes evaluaciones a diferentes τ (notar que todas las métricas dependen de τ).  
Para cada configuración, reportaremos las métricas para τ ∈ {0.001, 0.01, 0.1, 0.3, 0.5, 0.75, 1, 1.5}.&nbsp;  
En el análisis pondremos especial énfasis en:&nbsp;

* τ=1 (el modelo imita la distribución de los datos; \[1\] predice que no puede trascender  
* τ→0 (argmax; donde opera el voto).&nbsp;

(El resto del barrido es para dibujar la curva)

## Experimento 1 propiamente dicho

## Objetivo

Cuantificar cómo la proporción de errores compartidos entre expertos incide en la trascendencia.

## Diseño propuesto

### Descripción conceptual

El experimento que planeo hacer ahora, como primer paso, consiste en usar el juego Connect4 propuesto y entrenar un modelo con partidas sintéticas.&nbsp;  
Esas partidas sintéticas son generadas por varios expertos.&nbsp;  
Esos expertos tienen probabilidad de equivocarse.&nbsp;  
Equivocarse es realizar una jugada no óptima (una que empeora la posición)&nbsp;  
Cuando se equivocan, tienen probabilidad `P` de cometer un error compartido y probabilidad `(1-P)` de cometer un error independiente, al azar.&nbsp;  
La idea es variar `P` y ver cómo mejora la calidad del juego del modelo entrenado.

### Definición más formal

* Definiremos el conjunto de estados sesgados (notaremos como `B`) como un subconjunto de los estados no triviales. En este subconjunto todos los expertos jugarán la misma jugada errónea `w(e)`. Son "los estados en los que todos los expertos se equivocan de la misma manera", "los estados de error compartido". Más abajo definiremos cómo construiremos `B` para cada configuración; primero, necesitamos introducir algunos conceptos adicionales.  
* `ρ` es la tasa de error del experto en estados no triviales. Es una constante fija en 0.3 para todas las configuraciones (tiene que ser menor que 0.5 de lo contrario no se da las condiciones para que el voto de la mayoría sea mejor que cada experto, por lo cual no habría trascendencia incluso cuando no haya errores compartidos)  
* `P` fracción de los errores de `ρ` que son compartidos  
  Es la variable a barrer entre configuraciones: `P ∈ {0, 0.25, 0.5, 0.75, 1}`

  Ejemplo: si `P=0.2` entonces los expertos, cuando están en estados no triviales tienen probabilidad:  
  * `0.06` de cometer errores compartidos.  
  * `0.24` de cometer errores independientes.

La probabilidad total de errar en un estado no trivial se mantiene en de `0.3`  
&nbsp;La probabilidad de errar dado que está no solo en un estado no trivial, sino en `B` es de `0.24/0.94 = 0.255` (definiremos como `q` más adelante)

* `β = P·ρ` es la probabilidad de que, en un estado no trivial, se produzca un error compartido.&nbsp;  
  Intuitivamente, `β` es la fracción de los estados no triviales visitados que caen en `B`.  
* `q = (ρ − β)/(1 − β)` es la probabilidad de errar (estando en un estado no trivial) dado que estás fuera de `B`  
* Construcción de `B` y `w(e)`:  
  * Un estado está en `B` si el número de la jugada `t` pertenece a `S` `⊂ {1, …, 42}`.  
    Coloquialmente: `S` es el índice de las jugadas que están en `B`  
    El 42 surge que ninguna jugada tiene más de longitud 42 (6x7)  
    ¿Cómo definimos `S`? Queremos que:  
    * `S` sea repartido de forma pareja entre apertura, medio y final, para que el error compartido no se concentre en una fase del juego.  
    * Siendo `no triviales(t)` la fracción de estados no triviales que ocurren en `t,` queremos que:  
      &nbsp;`sumatoria de no triviales(t) = β` para `t ∈ S`  
  * Definiremos `w(e)` como la columna legal más a la izquierda que no sea óptima.&nbsp;

**Nota:** en los experimentos preliminares, `B` se definió mediante un hash del estado. Un hash es difícil de aprender (ya de por sí el modelo no recibe de entrada el estado, así que debería reconstruirlo y aprender a calcular el hash). Por lo que en estados nuevos el modelo no puede saber que está en `B`, hace lo que hacen los estados parecidos.  
La regla `t ∈ S` es aprendible, así que el error compartido debería reproducirse incluso en estados de `B` no vistos durante el entrenamiento.  
Proponemos realizar una comparativa del mismo experimento, definiendo `B` mediante un hash del estado y comparando cómo la representabilidad de `B` afecta los resultados.

Luego los expertos jugarán:&nbsp;

* Si `e` es trivial, juega al azar una jugada legal.&nbsp;  
* Si `e` es no trivial:&nbsp;  
  * Si `t \in S` juega `w(e)`&nbsp;  
  * Si no:  
    * Con probabilidad `q` juega una jugada errónea al azar .  
    * Con probabilidad `1−q` juega una jugada óptima al azar.

**Nota importante:** la regla `t ∈ S`, si bien creemos que será fácilmente representable para el modelo, no indica si el estado es trivial ni cuántas veces se ve durante el entrenamiento, así que la fracción de estados no triviales que caen en `B` no es `|S|/42`, sino la suma, sobre `t ∈ S`, de la fracción de estados no triviales visitados en la jugada `t`. Por eso `S` se calibra con un dataset piloto para que esa suma dé `β`, y el `β` efectivo se reporta midiendo en el test qué fracción de los estados no triviales efectivamente cayó en `B`.

### Conjunto de entrenamiento, validación y test

Los tres se generan con el mismo generador y la misma configuración de expertos

(ρ, P, S) fija, difieren únicamente en la semilla aleatoria para generarlos

### Correlación de errores entre expertos

Pendiente


 nono usemos string y punto para la lectura ; no hace falta que haya paridad
  tiene que haber paridad de field Names
  y tiene que ser valores de writs \subset_equal valores de read
  pero podemos leer cosas que no podamos escribir