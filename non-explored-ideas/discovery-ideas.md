# ¿Se puede estudiar o aproximar el "descubrimiento"?

*Notas del 12 sep 2026, a partir de la revisión de la propuesta de tesina contra [1] Zhang et al. 2024 y [2] Abreu et al. 2025.*

## Qué dicen los papers

- [2] usa la palabra exacta: en la Discusión (Sec. 8) escriben "our framework does not capture the idea of *skill discovery*". Es un cuarto modo que su taxonomía no cubre.
- [1] no dice "discovery", pero delimita lo mismo en "Broader Impact" (Sec. 6): "the denoising effect addressed in this paper does not offer any evidence for a model being able to produce novel solutions that a human expert would be incapable of devising... we do not present evidence that low temperature sampling leads to novel abstract reasoning, but just denoising of errors".

## Por qué el marco lo excluye

A τ→0 el modelo juega el argmax de la mezcla que estimó. En un estado visto, si ninguna jugada m tiene masa en los datos, la mezcla verdadera le da masa cero y el argmax no puede ser m. Ya lo medimos: en la condición `blind` (nadie abre al centro en las primeras 4 jugadas), P(centro | tablero vacío) = 0.0001 a τ=1 y 0 a τ→0. Descubrimiento estricto en estados vistos: imposible por teoría, y confirmado.

## Lo que ya tenemos se parece a descubrimiento pero no lo es

En π=1 (sesgo por hash) el modelo juega la jugada óptima en estados nuevos donde todos los expertos se equivocan (acc en estados sesgados 0.007 en apertura, 0.41 / 0.56 en medio y final). Ahí ningún experto sabe la respuesta *en ese estado*, pero sí la saben en estados parecidos. Abreu lo llamaría *skill generalization*, y tiene razón.

Límite metodológico: en estados no vistos, descubrimiento y generalización son indistinguibles sin una noción de "estado parecido", y esa noción no la tenemos. Vale escribirlo en la propuesta.

## Tres aproximaciones honestas, de menor a mayor ambición

### 1. Definición operativa y medición como control cuantitativo

**Tasa de descubrimiento estricto**: fracción de estados vistos donde el argmax del modelo es una jugada con masa empírica cero en el entrenamiento en ese tablero exacto.

- Predicción: cero en todas las condiciones.
- Costo: nulo. Los datos ya tienen los conteos por tablero (`training_positions` en `c4/decompose.py` indexa tableros; falta guardar el conteo por jugada).
- Valor: convierte "no hay discovery" de anécdota en número. Entra en el objetivo 4 de la propuesta sin agregar experimentos.

### 2. El continuo de representabilidad

Entre la regla (`rule`, perfectamente aprendida a tres decimales desde el paso 200) y el hash (`iid` π=1, imposible de aprender) hay sesgos compartidos que son función del estado pero cuestan datos o capacidad: por ejemplo, un sesgo definido por una característica del tablero poco frecuente (paridad de fichas en una columna, presencia de cierto patrón local, hash de solo las primeras k jugadas).

- Métrica: cuánto del sesgo el modelo *no* aprende = cuánto juega bien donde todos los expertos juegan mal.
- Presentarlo como "generalización que vence a un sesgo mal aprendido", no como descubrimiento.
- Es un buen experimento para el objetivo 4 (representabilidad), y da una curva en vez de dos puntos extremos.

### 3. Condicionar por resultado: la única vía dentro de imitación pura

[1] lo nombra explícitamente en su Apéndice D.2 como "otra forma de trascendencia" a explorar: el Decision Transformer condiciona la generación al resultado de la trayectoria.

En nuestro pipeline el símbolo de resultado ya está en la secuencia, al final (`moves_to_tokens(b.moves, b.result_token())` en `c4/generate.py`). Moverlo al principio (o entrenar con un prefijo de condición) da una política p(jugada | prefijo, gana), que pesa las jugadas por resultado y no por frecuencia.

**Por qué puede superar el argmax de la mezcla.** En `selection` por debajo del umbral α* = 1/3, la jugada compartida errónea es la mayoría, pero las partidas donde el experto competente jugó bien se ganan más. Condicionar por "gana" podría dar vuelta el argmax justo donde el voto falla. Predicción optimista: la ganancia a τ→0 condicionada por "gana" es positiva para α < α*, donde la ganancia sin condicionar es negativa (−0.104 en α=0, −0.043 en α=0.2).

**Por qué puede fallar.** Paster et al. 2022 ("You can't count on luck") y Brandfonbrener et al. 2022: contra un oponente ruidoso, condicionar por "gana" también selecciona las partidas donde el rival se equivocó, y el modelo aprende a "contar con la suerte". Connect 4 es determinista dadas ambas jugadas, pero el oponente (un experto ruidoso) es estocástico desde el punto de vista del modelo: es exactamente el régimen donde RCSL falla. Predicción pesimista: el modelo condicionado juega jugadas que "ganaron" porque el rival erró después, y su E[r] por estado no mejora o empeora.

**Diseño mínimo.**
- Generación: mismo dataset, resultado al principio de la secuencia (o duplicar el token: principio y final).
- Evaluación: mismo `evaluate.py states` pero con el prefijo fijado en "gana P1" / "gana P2" según quién mueve; comparar contra (a) el modelo sin condicionar a τ→0, (b) el argmax de la mezcla (techo del voto), (c) el mejor experto.
- Condiciones: `sel_k4` con α ∈ {0, 0.2, 0.45} (donde el voto falla y donde funciona) y `iid` π=0 como control (ahí el voto ya es óptimo, el condicionamiento no debería agregar nada).
- Costo: un cambio en `generate.py`, reentrenar 4 condiciones × 3 semillas ≈ 12 corridas ≈ 20 min de GPU.

**Qué es y qué no es.** No es descubrimiento en sentido estricto: sigue eligiendo entre jugadas que están en los datos. Pero es un criterio de selección que la teoría de [1] no cubre (su Proposición 2 es sobre el argmax de la mezcla sin condicionar), y tiene dos predicciones opuestas en la literatura. Es la extensión más interesante y la más barata que encontré.

## Lo que no haría en una tesina

- **Búsqueda en inferencia** (usar el modelo como prior y su predicción de resultado como valor, estilo AlphaZero / MCTS). Ya no es imitación; [1] restringe explícitamente su alcance a "the specialized knowledge and capacities are already provided by cross-entropy loss".
- **Auto-juego iterado** (reentrenar sobre las partidas del modelo a τ→0, repetir). Converge al argmax de la mezcla y no agrega conocimiento; con sesgo compartido representable, lo conserva. Es la literatura de model collapse con otro nombre.

## Recomendación para la propuesta

- Mantener "no se estudia descubrimiento" en Alcance y limitaciones, atribuyendo bien: *skill discovery* es terminología de [2]; [1] habla de "novel solutions".
- Agregar (1) como métrica del objetivo 4.
- Agregar (3) como objetivo opcional al final, formulado como pregunta: "¿condicionar por resultado permite superar el argmax de la mezcla donde el voto falla, o el modelo aprende a contar con los errores del rival?".
- (2) como variante del objetivo 4 si el tiempo lo permite.
