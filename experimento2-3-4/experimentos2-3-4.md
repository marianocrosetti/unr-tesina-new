# Experimentos 2, 3 y 4

Este documento define los experimentos 2 (selección de habilidades), 3 (posiciones vistas vs. no vistas) y 4 (generalización con soporte disjunto). Cubren los objetivos específicos 2 a 5 de la propuesta v2.2. El objetivo 3 (dependencia de la temperatura) no es un experimento aparte: se responde con el barrido de τ de los experimentos 1 y 2, y se explicita en la sección del experimento 2.

Todo lo definido en la sección "Elementos comunes a todos los experimentos" de `experimento1/experimento1-v1.md` aplica sin cambios: dominio, solver, notación (`estado`, `jugada`, `recompensa`, `estados no triviales`), conjunto de datos y vocabulario, modelo e hiperparámetros, regla de parada, métricas (`acc_τ`, `E[r]_τ`, `score`) y barrido de temperatura. Acá sólo se define lo que cambia respecto de eso: la población de expertos, las variables y constantes de cada configuración, las evaluaciones adicionales y las predicciones.

Convención que se repite en los tres: la exploración pre-propuesta ya corrió una versión de cada uno (hallazgos 2, 3 y 6 de `trascendencia_slides.html`). Donde el diseño de acá difiere del de la exploración, se indica con **Nota**. Las predicciones se registran antes de correr, como en el experimento 1.

---

# Experimento 2: selección de habilidades

## Objetivo

Cuantificar la trascendencia por el mecanismo de *selección* \[2\] al variar la proporción de datos generados por el experto competente, y contrastar su dependencia de la temperatura con la del mecanismo de cancelación de errores del experimento 1 (objetivo 3 de la propuesta).

## Diseño propuesto

### Descripción conceptual

En el experimento 1 todos los expertos son igualmente buenos en todos lados y sus errores son compartidos o independientes. Acá, en cambio, cada experto es competente en una región del espacio de estados y fuera de ella comete el mismo error que los demás expertos no competentes. Como el error fuera de la región es totalmente compartido, el voto del experimento 1 no lo puede cancelar: la única forma de que el modelo juegue bien en un estado es que el experto competente en ese estado haya generado la mayoría de los datos ahí. Eso es lo que controla la variable `α`: cuánto más habla cada experto de lo que sabe. La idea es variar `α` y ver a partir de qué punto el modelo supera al mejor experto.

### Definición más formal

* `K` expertos y una partición del conjunto de estados en `K` regiones `R_1, …, R_K`. Es una constante fija en `K = 4`.
* El experto `i` en un estado no trivial `e`:
  * Si `e ∈ R_i`: juega una jugada óptima al azar.
  * Si `e ∉ R_i`: juega `w(e)`, la misma jugada errónea compartida definida en el experimento 1 (columna legal más a la izquierda que no sea óptima).
  * En estados triviales juega al azar una jugada legal (como en el experimento 1).
* **Ruteo** `α ∈ [0, 1]`: en un estado `e ∈ R_j`, la jugada la genera el experto competente `j` con probabilidad `α + (1 − α)/K`, y cada uno de los otros `K − 1` expertos con probabilidad `(1 − α)/K`. `α = 0` es ruteo uniforme (cualquier experto genera la jugada con la misma probabilidad, sin importar el estado); `α = 1` es ruteo perfecto (siempre genera el competente).
  Es la variable a barrer entre configuraciones: `α ∈ {0, 0.2, 0.3, 0.4, 0.45, 0.7, 1}`.
* **Construcción de las regiones**: la región de un estado es `hash(estado) mod K`, con un hash determinista del tablero.
  **Nota:** a diferencia del experimento 1, acá no importa que la región sea representable. La mezcla en *todo* estado no trivial es la misma: masa `α + (1 − α)/K` en la jugada óptima y masa `(1 − α)(K − 1)/K` en `w(e)`. El modelo no necesita saber en qué región está para reproducir el argmax de la mezcla; sólo necesita, como en el experimento 1, poder representar `w(e)`. Por eso se mantiene el hash de la exploración para las regiones y se cambia únicamente `w(e)` para que coincida con el experimento 1 (la exploración usaba una jugada errónea definida por hash).
* Ambos jugadores de cada partida se generan con la misma población y el mismo ruteo, como en el experimento 1.

### Predicción teórica

* Cada experto individual acierta sólo en su región: `acc(experto) ≈ 1/K = 0.25` sobre estados no triviales. El "mejor experto" son los `K` a la vez, por simetría.
* A `τ = 1` el modelo imita la mezcla: `acc_1 ≈ α + (1 − α)/K`, que supera a `1/K` para todo `α > 0`. Es decir: **hay trascendencia a temperatura 1 para todo `α > 0`**. Esto es lo que \[2\] afirma para el mecanismo de selección y lo que la Proposición 1 de \[1\] prohíbe para la cancelación de errores. Es el contraste central para el objetivo 3.
* A `τ → 0` el modelo juega el argmax de la mezcla, que es óptimo si y sólo si `α + (1 − α)/K > (1 − α)(K − 1)/K`, o sea:

  `α > α* = (K − 2)/(2K − 2)`; para `K = 4`, `α* = 1/3`.

  Por encima del umbral, bajar la temperatura lleva `acc` a 1 y amplifica la ganancia. **Por debajo del umbral, bajar la temperatura empeora al modelo** (lo compromete con `w(e)`), y a `τ → 0` queda *por debajo* del mejor experto. Es la predicción falsable que \[2\] no formula y que se deriva de la Proposición 2 de \[1\].
* Predicción sobre el modelo finito (registrada antes de correr): la exploración vio el cambio de signo entre `α = 0.2` y `α = 0.45`, y una transición suave alrededor de `α*` en vez de un escalón. Por eso el barrido incluye `0.3`, `0.4` y `0.45`: la forma de la transición es lo que agrega un modelo finito a la teoría.

### Configuraciones

| Constantes | Variables |
|---|---|
| `K = 4`, `w(e)` como en exp. 1, regiones por hash, tamaño de datos y régimen de entrenamiento como en exp. 1 | `α ∈ {0, 0.2, 0.3, 0.4, 0.45, 0.7, 1}` (7 configuraciones) |

### Evaluación (lo que se agrega a las métricas comunes)

* Las tres métricas comunes se reportan para todo el barrido de `τ`. La figura principal es `acc_τ` y `E[r]_τ` en función de `α` para `τ = 1` y `τ → 0`, con la línea del mejor experto y la línea vertical en `α*`.
* **Curva de temperatura por mecanismo** (objetivo 3): en una misma figura, ganancia sobre el mejor experto en función de `τ` para una configuración del experimento 1 (`P = 0`) y dos de este experimento (una con `α < α*` y otra con `α > α*`). La predicción es que las tres curvas tienen forma cualitativamente distinta: en cancelación la ganancia aparece sólo al bajar `τ`; en selección sobre el umbral es positiva ya en `τ = 1` y crece al bajar `τ`; en selección bajo el umbral es positiva en `τ = 1` y decrece hasta hacerse negativa.
* Para el `score` contra el bot, el bot juega la política de la población *ruteada* (la mezcla), que es lo que generó los datos.

### Control opcional: expertos complementarios (Teorema 4 de \[1\])

Mismo diseño pero, fuera de su región, cada experto juega una jugada legal al azar en vez de `w(e)` (error independiente en vez de compartido), con `α = 0`. Es el caso que \[1\] prueba que trasciende a `τ → 0`. Sirve para mostrar que la fuente de la dificultad del experimento 2 es que el error fuera de la región sea compartido. Una configuración. TODO: decidir si se incluye.

---

# Experimento 3: posiciones vistas vs. no vistas

## Objetivo

Cuantificar qué parte de la trascendencia ocurre en posiciones que aparecen en el entrenamiento y qué parte en posiciones nuevas, y cómo cambia esa descomposición con la cantidad de datos (objetivo 4 de la propuesta). Ni \[1\] ni \[2\] lo miden: \[2\] evalúa cancelación y selección sobre consultas vistas y generalización sobre no vistas con expertos sin error.

## Diseño propuesto

### Descripción conceptual

La Proposición 2 de \[1\] es un enunciado *por estado*: el argmax de la mezcla en el estado `e`. Un modelo finito sólo puede estimar esa mezcla en `e` si vio `e` (varias veces) durante el entrenamiento. En posiciones nuevas no hay votos: lo que hace el modelo es generalizar lo que aprendió en posiciones parecidas. Este experimento no entrena nada nuevo: toma los modelos del experimento 1, etiqueta cada estado de test como visto o no visto, y reporta las métricas por separado. La única variable es la cantidad de partidas de entrenamiento, para ver cómo la ganancia en no vistos depende de los datos.

### Definición más formal

* **Estado visto**: un estado de test `e` es *visto* si el mismo tablero aparece en el conjunto de entrenamiento (no necesariamente por la misma secuencia de jugadas: el dominio admite transposiciones). La comparación es por tablero, no por prefijo de secuencia.
* **Fracción vista** `f_v`: fracción de los estados no triviales de test que son vistos. Se reporta por configuración; es la medida operativa del solapamiento entre entrenamiento y test.
* **Descomposición de la ganancia**: para cada métrica `m ∈ {acc_τ, E[r]_τ}` y su ganancia sobre el experto `g = m(modelo) − m(experto)`, vale

  `g = f_v · g_vistos + (1 − f_v) · g_no_vistos`

  con cada término calculado sobre el subconjunto correspondiente. Se reportan los tres.
* **Techo teórico**: `m(argmax de la mezcla verdadera)`, calculado analíticamente en cada estado de test con la distribución de los expertos (que es conocida por construcción). Es lo que un modelo con datos infinitos alcanzaría a `τ → 0`. Se reporta en vistos y no vistos por separado.
* **Fase**: apertura si `t < 8`, medio si `8 ≤ t < 20`, final si `t ≥ 20` (mismos cortes que la exploración). TODO: confirmar los cortes con la distribución de longitud de partida real.
* Variable: cantidad de partidas de entrenamiento `N ∈ {20K, 80K, 320K}`, manteniendo fija la cantidad de épocas (los pasos escalan con `N`) y la regla de parada del experimento 1.
  **Nota:** el experimento 1 deja "épocas por determinar" y contempla generar más datos. Si el experimento 1 termina usando `N` mayor a 80K, este barrido se corre alrededor de ese valor (`N/4`, `N`, `4N`).

### Configuraciones

| Constantes | Variables |
|---|---|
| Población del experimento 1 con `P = 0` (todos los errores independientes: es donde el voto tiene más que ganar), `ρ = 0.3`, modelo y régimen del exp. 1 | `N ∈ {20K, 80K, 320K}` (3 configuraciones; la de 80K es la del exp. 1 con `P = 0`, no se vuelve a entrenar) |

Se aplica además la misma descomposición, sin corridas nuevas, a las configuraciones `P = 1` del experimento 1 (regla) y a su celda de contraste con hash. Es lo que separa correlación de representabilidad: en estados sesgados `B` con regla, `acc → 0` en vistos y en no vistos; con hash, `acc → 0` en vistos pero `acc > 0` en no vistos, porque el modelo no puede saber que un estado nuevo está en `B` y juega lo que jugaría en un estado parecido.

### Evaluación (lo que se agrega a las métricas comunes)

* Tabla principal: para cada `N`, ganancia total, en vistos, en no vistos, `f_v` y techo teórico, a `τ → 0`.
* Todo lo anterior estratificado por fase. Cautela ya anotada en la propuesta: la fracción vista cae con la profundidad (las aperturas se repiten, los finales casi nunca), así que visto/no visto está correlacionado con la fase. Sin la estratificación se le atribuiría a la memorización lo que es un efecto de la profundidad.
* **Tercera población de estados, opcional**: los estados que el propio modelo alcanza jugando contra el bot (las 300 partidas del `score`). Sobre ellos se calcula `E[r]` del modelo y del experto contrafáctico en los mismos estados. La exploración encontró que `score` y `E[r]` por estado pueden discrepar (una configuración le ganaba al bot y a la vez tenía `E[r]` por estado menor que el experto sobre sus propias trayectorias): el resultado de una partida depende de *cuándo* se cometen los errores, no sólo de cuántos. Es la razón por la que las tres métricas comunes se reportan siempre. TODO: decidir si entra en la tesina o queda como observación.

### Predicciones (registradas antes de correr)

* En vistos, la ganancia alcanza el techo teórico ya con `N = 20K`.
* En no vistos, la ganancia es negativa con pocos datos (el modelo es peor que el experto en posiciones nuevas), se acerca a cero con `N = 80K` y se hace positiva con `N = 320K`.
* La ganancia total es la combinación ponderada por `f_v`, y `f_v` crece lentamente con `N` (la exploración vio 0.41, 0.47 y 0.53).
* Esto explica el "cuarto del techo" del experimento 1: el techo se alcanza donde hay votos, y la generalización recién aporta con datos abundantes. Es también una lectura del resultado de \[1\]: con una pasada sobre 10⁹ partidas, la componente de posiciones nuevas es la que ellos sí tenían.

---

# Experimento 4: generalización con soporte disjunto (composición)

## Objetivo

Cuantificar la trascendencia por el mecanismo de *generalización* \[2\], donde \[2\] obtuvo resultados débiles, con dos subpoblaciones de expertos cuyos soportes no se solapan: una que sólo muestra aperturas y otra que sólo muestra finales tras aperturas de otro estilo (objetivo 5 de la propuesta). Es la brecha que \[1\] nombra explícitamente: su teoría asume que cada experto está definido en todo el espacio de estados, lo que "es imposible después de la jugada 15".

## Diseño propuesto

### Descripción conceptual

La familia A juega aperturas perfectas y sus partidas se cortan en la jugada `N`: nunca muestra un final. La familia B abre con un estilo restringido (sólo columnas de borde) y juega el final perfecto. Ninguna secuencia de entrenamiento muestra un final después de una apertura buena. La pregunta es si el modelo, jugando él mismo una apertura buena (aprendida de A), sabe jugar el final que le sigue (aprendido de B en otras posiciones). Dos posiciones informadas predicen lo contrario: la composición de dos hechos falla en transformadores \[11, 12\] y \[2\] obtiene resultados débiles; pero los transformadores de ajedrez generalizan reglas a posiciones fuera de distribución \[15\]. La teoría de la mezcla no predice nada acá porque la señal de entrenamiento es *silenciosa*, no contradictoria, en las posiciones en cuestión.

### Definición más formal

* Cada partida la juega una sola familia por ambos lados.
* **Familia A** (fracción `f_A` de las partidas): jugada óptima al azar en todo `t < N`. La secuencia se **trunca** en la jugada `N`: no incluye el resto de la partida ni el token de resultado (se rellena con `PAD`).
* **Familia B** (fracción `1 − f_A`): en `t < N` juega una columna legal al azar dentro del conjunto permitido por su **estilo**; en `t ≥ N` juega una jugada óptima al azar hasta el final, con token de resultado.
  Estilos de B, ordenados por severidad del desplazamiento respecto de las aperturas óptimas:
  * `óptimo`: jugada óptima al azar (control: los finales tras aperturas óptimas *sí* están en el soporte).
  * `aleatorio`: columna legal uniforme.
  * `sin centro`: columnas `{1, 2, 3, 5, 6, 7}`.
  * `bordes`: columnas `{1, 2, 6, 7}`. Es el estilo principal.
  Si ninguna columna permitida es legal, juega cualquier legal.
* Constantes: `N = 8`, `f_A = 0.5`. TODO: `N = 8` corta la apertura temprano; la exploración probó `N = 14` sin cambio en la penalidad. Decidir si se reporta como robustez.
* No hay error aleatorio en ninguna familia: el experimento aísla el hueco de soporte, sin cancelación de errores encima.

### Configuraciones

| Constantes | Variables |
|---|---|
| `N = 8`, `f_A = 0.5` (salvo en los controles solo-A y solo-B), datos y régimen del exp. 1 | Cuatro configuraciones principales: **control** (A + B `óptimo`), **A + B `bordes`**, **solo A** (`f_A = 1`), **solo B `bordes`** (`f_A = 0`) |
| | Opcional, gradiente de severidad: A + B `aleatorio`, A + B `sin centro` (2 configuraciones más) |

### Qué es "experto" y qué es "trascender" acá

A diferencia de los experimentos 1 a 3, no hay un experto definido en todo el juego con el que comparar jugada a jugada: A no sabe jugar finales y B no sabe abrir. Por eso se distinguen dos objetos:

* **Transferencia** (jugada a jugada, en el final): `acc` del modelo en estados con `t ≥ N` comparada con la del control. El experto de referencia en el final es B, que ahí es óptimo (`acc = 1`); lo que se mide no es trascendencia sobre B sino cuánto se pierde por el hueco de soporte, `Δ = acc(configuración) − acc(control)`.
* **Composición** (partida completa): el modelo trasciende si, sobre sus propias trayectorias, juega mejor la partida entera que cualquiera de las dos familias. Es la definición de \[1\] con `p_test` = distribución de estados del propio modelo. Operativamente: `score` contra el jugador perfecto mayor que el de solo-A y el de solo-B, y `acc` alta en todas las fases de sus propias partidas.

### Evaluación (lo que cambia respecto de las métricas comunes)

`acc_τ` y `E[r]_τ` en el final (`t ≥ N`) se calculan sobre tres distribuciones de estados, a `τ → 0` y `τ = 1`:

1. **Finales en soporte**: estados con `t ≥ N` de partidas de test generadas por la propia familia B de la configuración (semilla distinta). Verifica que el modelo aprendió el final donde lo vio.
2. **Finales tras aperturas óptimas** (fuera del soporte): estados con `t ≥ N` de partidas de test generadas por la familia de control (apertura óptima + final óptimo). Ninguna de estas posiciones aparece en el entrenamiento de las configuraciones con B `bordes`, `sin centro` o `aleatorio`. Es la métrica principal de transferencia.
3. **Juego propio**: los estados que el modelo alcanza en 300 partidas **contra el jugador perfecto** (solver), 150 con cada color. `acc` por fase sobre esas trayectorias y `score`.
   **Nota:** acá el rival es el jugador perfecto y no el bot de la población, porque no hay una política de población definida en toda la partida. Como el primer jugador perfecto gana siempre al Connect4, el `score` máximo alcanzable es `0.5` (ganar todas como primero, perder todas como segundo). Un `score` de `0.35` equivale a ganar el 70 % de las partidas como primer jugador. Se reporta también, por separado, el resultado con cada color.

Además, para la etiqueta visto/no visto del experimento 3, se reporta la fracción de estados de la distribución 2 que aparecen en el entrenamiento de cada configuración. Debe ser ≈ 0 en las configuraciones con estilo restringido; es la verificación de que el hueco de soporte es real.

### Predicciones (registradas antes de correr)

* **Transferencia con penalidad chica y graduada**: `acc` en la distribución 2 baja respecto del control en el orden `aleatorio < sin centro < bordes`, y la penalidad con `bordes` es menor a `0.03`. No hay colapso en ninguna configuración.
* **Solo B transfiere igual que A + B** en la distribución 2: los datos de A no aportan al final. Lo que A aporta es la apertura.
* **Solo B pierde todas las partidas** contra el jugador perfecto (abre por los bordes). **Solo A colapsa en el final** (`acc` cae con `t`, más allá de donde vio datos). **A + B juega la partida completa**: apertura y final cerca de 1, `score` cerca de `0.35`. Ninguna de las dos familias puede hacer eso: es la composición.
* La penalidad no depende del tamaño del modelo, de la cantidad de datos ni de `N`. TODO: decidir si alguna de estas robusteces se corre (la exploración las corrió: modelos de 0.1M y 0.8M, 20K partidas, `N = 14`).
* Observación lateral esperada: solo A, sin haber visto una jugada más allá de `N`, juega el medio juego razonablemente antes de colapsar en el final: extrapola la estructura de la apertura óptima más allá de su soporte.

### Limitación a dejar por escrito

Connect4 es un juego de estado totalmente observable donde las características relevantes del tablero son locales; en ese dominio la predicción optimista (transferencia) era la plausible. El resultado dice que la política de final aprendida es una función del tablero y no una tabla sobre las trayectorias de B, aun cuando el modelo sólo ve secuencias y tiene que construir esa representación a partir de historiales de bordes. No dice nada sobre componer conocimiento declarativo, donde los resultados de \[2\] siguen siendo la evidencia relevante.

---

# Grilla total y orden de ejecución

| Experimento | Corridas nuevas | Reutiliza |
|---|---|---|
| 2: selección | 7 (+1 control opcional) | nada |
| 3: vistos / no vistos | 2 (`N = 20K` y `320K` con `P = 0`) | los modelos del exp. 1 (`P = 0`, `P = 1` regla, `P = 1` hash) |
| 4: composición | 4 (+2 gradiente de severidad) | nada |

Orden sugerido, siguiendo el principio risk-first: 3 primero (no entrena casi nada y su resultado condiciona cómo se lee el experimento 1), después 2, después 4. El experimento 4 es el más largo y el más independiente: su pipeline de expertos (familias, truncado) y su evaluación (tres distribuciones, rival perfecto) son los únicos que no comparten nada con el experimento 1 más allá de los elementos comunes.
