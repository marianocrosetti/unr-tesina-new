# Sesión previa: auditoría de la propuesta (Desktop)

- Sesión de Claude Code `da272be7` (carpeta de origen: `~/Desktop`)
- Período: 2026-09-12 02:15 → 2026-09-12 03:36 (UTC)
- Mensajes: 24 del usuario, 26 del asistente (se omiten llamadas a herramientas y sus resultados)

---

## 👤 Mariano · 2026-09-12 02:15

ok ahora vamos a cubrir la auditoria que hiciste
La idea y quiero que la repases y vuelvas a hacer a ver si está todo bien y no nos olvidamos de nada era leer lo hecho en Desktop/chess y leer la propuesta /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina/propuesta-transcendencia-edited.md

y tener leido los dos trabajos [1] y [2]
[1] E. Zhang, V. Zhu, N. Saphra, A. Kleiman, B. L. Edelman, M. Tambe, S. M. Kakade, E. Malach. *Transcendence: Generative Models Can Outperform The Experts That Train Them*. NeurIPS, 2024. arXiv:2406.11741.

[2] N. Abreu, E. Zhang, E. Malach, N. Saphra. *A Taxonomy of Transcendence*. COLM, 2025. arXiv:2508.17669.

Terminó la auditoría. Lo que falta o está flojo en la propuesta, ordenado por lo que más vale incorporar. Ojo con la primera sección: como la propuesta es previa al trabajo, esto debería entrar como hipótesis o preguntas, no como resultados.

y quiero que me hagas sugerencias concretas a agregar en la propuesta
ultrathink

</auditorio>
A. Hallazgos del prototipo que la propuesta debería anticipar como hipótesis

1. Selection y denoising difieren en si necesitan baja temperatura. En el prototipo, la mezcla ruteada ya supera al mejor experto a τ=1 para todo α>0; el voto solo aparece a τ→0. La propuesta trata la temperatura como condición única. Pregunta a agregar: "¿qué mecanismos requieren argmax y cuáles no?"
2. Umbral cuantitativo de selection, α*=(K−2)/(2K−2). Es derivable del Teorema 2 de Zhang y Abreu no lo formula; el testbed lo hizo falsable (flip entre α=0.2 y 0.45 con K=4 → 1/3). Hoy aparece solo como "variante de ruteo" en el cronograma, sin decir que es una predicción numérica nueva.
3. Dos métricas de trascendencia que pueden discrepar: recompensa por estado vs. resultado de partida. El modelo π=1 no trasciende por estado (−0.017) pero gana 59% de los partidos. El rating de Zhang mide una cosa y la accuracy de Abreu otra. La propuesta debería anticipar que se miden ambas.
4. El modelo a τ=1 queda por debajo del experto (0.76 vs 0.845): la distribución aprendida es más plana que los datos, así que parte de la ganancia τ=1→τ→0 elimina entropía propia del modelo, no de los expertos. Contamina la lectura del 1000→1500 de Zhang. Riesgo de interpretación que hoy no está.
5. Sobreentrenar tiene tres síntomas distintos según la condición (destruye el voto en π=0, deja de generalizar el sesgo en π=1, no cambia nada en rule). El objetivo 6 habla de "persistencia o desaparición" en singular.

B. Decisiones de diseño que conviene fijar en la propuesta

6. El imitador solo ve la secuencia de jugadas, nunca el tablero. Decisión con consecuencias fuertes (debe construir la representación del estado) y que hace más notable la composición. No está.
7. Evaluación desde logits, sin muestrear, con política del experto y argmax de la mezcla calculados analíticamente. "Evaluar exactamente" no explica que esto elimina ruido de muestreo.
8. Definición operativa de "posición vista": mismo tablero, no misma secuencia. El objetivo 4 depende de esto.
9. Tasa de error realizada ≈ mitad de la nominal (~52% de las posiciones no admiten error bajo recompensa por clase). Un evaluador lo va a preguntar.
10. Se necesitan dos construcciones de sesgo compartido (hash: compartido pero no representable; rule: compartido y representable) para separar correlación-entre-expertos de estructura-en-el-estado. El objetivo 4 menciona representabilidad pero no que hacen falta las dos.
11. Definir bien el hueco de soporte es lo difícil del objetivo 5. Aperturas aleatorias no crearon hueco (visitan tableros centrales igual); hicieron falta estilos estructurados (nocenter/edges). La propuesta dice "solapamiento controlable" como si fuera trivial.
12. Tres semillas por celda y evaluación en el checkpoint de mejor val loss (el prototipo evaluó el final y lo lista como limitación). Ninguna de las dos está.

C. Limitaciones a declarar como riesgos

13. Los errores sintéticos son independientes o perfectamente compartinguno de los dos.
14. La recompensa es una clase de resultado (gana/empata/pierde), no un valor fino.
15. El dominio hace plausible la predicción optimista sobre composicisimista fuera plausible sería un test más fuerte.

D. Cronograma

16. Costo real: ~20 min por dataset de 80k (CPU), 1.7 min por run en U en total para ~130 corridas. Las 14 semanas son holgadas en cómputo;
    el cuello es diseño e interpretación. Vale decirlo para justifica

E. Bibliografía que falta

17. Las cuatro importantes: Mészáros/Reizinger/Huszár 2025 (composicimers, el bando optimista) y Paster 2022 / Brandfonbrener 2022 (fallas
    de stitching en Decision Transformers, el bando pesimista). Son livo 5 como pregunta genuinamente abierta ("dos bandos serios predecían
    lo opuesto"). Secundarias: Allis 1988 y Pons 2019 (solver), Bergl Allen-Zhu & Li 2023.

Mi criterio de prioridad: 1, 3, 6, 11 y 17 son las que más cambian la propuesta; el resto son ajustes de una línea. Además el fork notó que ~/Desktop/chess/propuesta.md es otra versión de la propuesta con texts de estos puntos, por si querés reciclar. ¿Querés que redacte lospárrafos para 1, 3, 6, 11 y 17 (acá, sin tocar el archivo)?
</auditoria>

## 🤖 Claude · 2026-09-12 02:15

Voy a releer la propuesta, el prototipo en `Desktop/chess` y los dos papers, y después contrastar punto por punto la auditoría anterior para confirmar, corregir y completar.

## 🤖 Claude · 2026-09-12 02:21

Rehice la auditoría desde cero contra la propuesta, el prototipo (docs, código y log cronológico) y los dos papers. Los 17 puntos anteriores se sostienen; encontré además tres cosas nuevas que importan más que varios de los 17.

**Veredicto sobre la auditoría anterior**

- Los 17 puntos están verificados contra las fuentes. Los datos citados (umbral 1/3, flip entre α=0.2 y 0.45, τ=1 por debajo del experto, aperturas aleatorias que no crean hueco, tres semillas, evaluación desde logits, ~52 % de posiciones sin error posible) coinciden con el código y los resultados.
- Un error de detalle: el cronograma suma 11 semanas, no 14. Además el primer ítem dice que el relevamiento "ya se realizó" y le asigna una semana.

**Lo nuevo, que la auditoría anterior no vio**

1. **La propuesta afirma algo falso sobre [2].** Dice que Abreu "no evalúa condiciones out-of-distribution". Sí lo hace: su modo de generalización asume por definición soporte de test disjunto del de entrenamiento. Lo que [2] no hace es descomponer, dentro de una misma condición, cuánto de la ganancia ocurre en entradas vistas y no vistas. Un evaluador que leyó [2] lo va a marcar. Redacté el reemplazo.
2. **Falta el caso negativo de [1].** La propuesta cuenta el éxito (≤1000 → ~1500) pero no que el modelo entrenado con ≤1500 no trasciende, ni que Zhang lo atribuye a menor entropía de jugadas de forma correlacional. Ese fracaso es la motivación directa del objetivo 3 y hoy no aparece.
3. **Visto/no visto está confundido con la fase del juego.** En un juego secuencial las aperturas se repiten casi siempre y los finales casi nunca, así que la etiqueta "visto" correlaciona con la profundidad. El objetivo 4 tiene que prometer estratificar por fase, o el resultado se puede atribuir a la profundidad y no a la memorización.

Otros ajustes menores nuevos: la nota 3 ("debe usarse baja temperatura") solo vale para denoising con muestreo uniforme de expertos, y el Teorema 2.1 de [2] da trascendencia a temperatura 1 para selection. Los enunciados de [1] son Proposiciones, no Teoremas. Rating Glicko-2 y jugadores ≤1000, no "~1000 ELO". La sección "Fundamentos" aparece dos veces. Y un control concreto para el punto 4 de la auditoría: una condición con expertos sin error mide la ganancia por temperatura que no es trascendencia.

**Entregable**

Escribí todos los párrafos listos para pegar, con indicación de dónde va cada uno y qué texto reemplaza, en:

```
/Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina/propuesta-transcendencia-sugerencias.md
```

Cubre las correcciones de precisión sobre [1] y [2], los cinco puntos A como hipótesis, los siete puntos B como decisiones de diseño, una subsección nueva de alcance y limitaciones, el párrafo de costo de cómputo, y la bibliografía. Verifiqué los dos IDs de arXiv dudosos (Mészáros 2025 y Krestnikov 2026) y son correctos. Agregué referencias para las líneas que la sección "Fundamentos" nombra sin citar (Ross & Bagnell, Breiman, Marcolino/Tambe, Rolnick, Karvonen, Toshniwal).

No toqué el archivo de la propuesta.

## 👤 Mariano · 2026-09-12 02:22

inclui las sugerencias y cambios en el archivo original pero como citations
> citation
> citation continues
o sea agregá no borrés ni sobre-escribas

## 🤖 Claude · 2026-09-12 02:23

Voy a insertar cada sugerencia como cita (`>`) justo después del pasaje al que se refiere, sin borrar ni modificar nada del texto original.

## 🤖 Claude · 2026-09-12 02:26

Listo. Las 27 sugerencias quedaron insertadas como citas (`> **[Sugerencia — ...]**`) en `propuesta-transcendencia-edited.md`, cada una justo debajo del pasaje al que se refiere. No se borró ni modificó ninguna línea original: lo verifiqué comparando contra una copia previa y las 101 líneas originales siguen presentes y en orden.

Cada cita arranca con una etiqueta que dice qué hacer con ella:
- **"agregar a continuación"**: párrafo nuevo para pegar después del texto.
- **"reemplazaría ..."**: cita el fragmento original que sustituiría, sin haberlo tocado.
- **"editorial"**: tipeos, encabezado duplicado, oración incompleta, inconsistencias del cronograma.

Dónde quedaron, por sección:
- **Motivación**: caso negativo de [1], precisión Glicko-2 / ≤1000 / Proposiciones, corrección de la afirmación sobre [2] y out-of-distribution, precisión de los números de composición de [2].
- **Objetivos 1 a 6**: tasa realizada y definición de "óptimo"; dos métricas de trascendencia y evaluación desde logits; denoising vs selection según temperatura y umbral α*; control con expertos sin error, definición de "visto" con su confusión con la fase, dos construcciones de sesgo y control de descubrimiento; hueco de soporte medible con controles y el párrafo de los dos bandos; síntomas del sobreentrenamiento por condición. Después de los objetivos, la subsección nueva "Alcance y limitaciones".
- **Metodología y programa**: pipeline existente y costo de cómputo, semillas y checkpoint, la suma de 11 semanas, el párrafo de contingencia restaurado.
- **Notas al pie**: imitador a ciegas (nota 1), reemplazo de la nota 3, doble rol de Stockfish (nota 4).
- **Referencias**: las 15 referencias nuevas numeradas [4] a [18], agrupadas por prioridad.

El archivo separado `propuesta-transcendencia-sugerencias.md` sigue existiendo con el mismo contenido organizado por tema, por si preferís leerlo ahí.

## 👤 Mariano · 2026-09-12 02:29

Todos los cambios de la bibliografía agragalos todos o sea saca los cites de la seccion ## REFERENCIAS

## 🤖 Claude · 2026-09-12 02:30

Hecho. La sección REFERENCIAS ya no tiene la cita: las 15 referencias nuevas quedaron como entradas normales, numeradas [4] a [18] a continuación de [3], con el mismo formato que las tres originales.

Orden en que quedaron:
- [4] a [6]: Mészáros 2025, Paster 2022, Brandfonbrener 2022 (los dos bandos sobre composición, citados en la sugerencia del objetivo 5).
- [7] y [8]: Allis 1988 y Pons 2019 (el dominio y el solver).
- [9] a [15]: Ross & Bagnell 2010, DAgger 2011, Breiman 1996, Marcolino/Jiang/Tambe 2013, Rolnick 2017, Karvonen 2024, Toshniwal 2022 (las líneas que "Fundamentos" nombra sin citar).
- [16] a [18]: Berglund 2023, Allen-Zhu & Li 2023, Krestnikov 2026 (secundarias).

Quedan 25 bloques de sugerencia como citas en el resto del documento. Las que mencionan estas referencias por autor (objetivo 5 y nota 1) ahora pueden citarse por número si preferís, por ejemplo [4]–[6] y [14]–[15].

## 👤 Mariano · 2026-09-12 02:39

en esta frase
> Texto propuesto: Medir cómo se reparte la magnitud de la *trascendencia* entre posiciones vistas y no vistas durante el entrenamiento. En [2] la distinción entre entradas dentro y fuera del soporte de entrenamiento es un supuesto que separa modos (denoising y selection asumen soporte contenido; generalization asume soporte disjunto), no una variable que se mida dentro de una misma condición. Nosotros proponemos etiquetar cada posición de evaluación como vista o no vista y descomponer la ganancia en ambas componentes, en cada condición experimental.
siento que esto no lo entiendo
o. En [2] la distinción entre
  entradas dentro y fuera del soporte de entrenamiento es un supuesto que separa modos (denoising y selection asumen soporte contenido; generalization asume soporte
  disjunto),
en cambio lo que sigue esta explicado con palabras mas sencillas Nosotros proponemos etiquetar cada posición de evaluación como vista o no vista y descomponer
  la ganancia en ambas componentes, en cada condición experimental.

## 🤖 Claude · 2026-09-12 02:39

Tenés razón, esa oración está comprimida. La idea, en palabras simples:

En [2] cada experimento decide de antemano si las consultas de test aparecen o no en el entrenamiento. En los experimentos de denoising y selection, todas las consultas de test son hechos que sí aparecen en los datos (algunos expertos los dicen bien y otros mal). En el experimento de generalization, todas las consultas de test son hechos que nunca aparecen (combinan conocimiento de dos expertos). O sea que en [2] "visto" o "no visto" es una propiedad de todo el experimento, elegida por diseño. Nunca toman un mismo experimento y separan su conjunto de test en consultas vistas y no vistas para ver de dónde sale la ganancia. Eso es lo que nosotros proponemos hacer.

Lo reemplazo en el archivo por una versión que diga eso.

## 👤 Mariano · 2026-09-12 02:39

no hagas cambios mostrame por aca como lo reemplazarias

## 🤖 Claude · 2026-09-12 02:40

Así lo reemplazaría, sin tocar nada más del bloque:

> Texto propuesto: Medir cómo se reparte la magnitud de la *trascendencia* entre posiciones vistas y no vistas durante el entrenamiento. En [2], que las consultas de test hayan aparecido o no en los datos de entrenamiento es una decisión de diseño de cada experimento, no algo que se mida: en los experimentos de denoising y de selection, todas las consultas de test son hechos que sí aparecen en el entrenamiento (algunos expertos los dicen bien y otros mal); en el experimento de generalization, todas las consultas de test son hechos que nunca aparecen (combinan conocimiento de dos expertos distintos). En ningún caso toman un mismo experimento y separan su conjunto de test en consultas vistas y no vistas para ver de dónde sale la ganancia. Nosotros proponemos exactamente eso: etiquetar cada posición de evaluación como vista o no vista y descomponer la ganancia en ambas componentes, en cada condición experimental.

Si te parece largo, la versión corta:

> Texto propuesto: Medir cómo se reparte la magnitud de la *trascendencia* entre posiciones vistas y no vistas durante el entrenamiento. En [2] eso no se mide: cada experimento fija por diseño si sus consultas de test aparecen en el entrenamiento (denoising y selection) o no aparecen nunca (generalization), y nunca se separa un mismo conjunto de test en vistas y no vistas. Nosotros proponemos etiquetar cada posición de evaluación como vista o no vista y descomponer la ganancia en ambas componentes, en cada condición experimental.

## 👤 Mariano · 2026-09-12 02:40

no entiendo: si se mide entonces en 2 (si aparece vs no aparece) o no?

## 🤖 Claude · 2026-09-12 02:41

Buena pregunta, porque las dos cosas son ciertas a la vez y la frase las mezcla. Separémoslas:

**En [2] sí se evalúa sobre consultas no vistas.** El experimento de generalization mide acierto sobre hechos de dos saltos que ningún experto tiene y que no están en el entrenamiento. Por eso la frase original de la propuesta ("[2] no evalúa condiciones out-of-distribution") es falsa.

**En [2] no se compara visto contra no visto dentro de un mismo modelo.** Cada experimento entrena un modelo y lo evalúa sobre un solo tipo de consulta: el de denoising, solo sobre consultas vistas; el de generalization, solo sobre consultas no vistas. Son modelos distintos, entrenados con datos distintos, con preguntas distintas. Nunca agarran un modelo, le pasan un conjunto de test que tiene consultas de los dos tipos, y reportan "acá ganó tanto en las vistas y tanto en las no vistas".

Lo que nosotros proponemos es lo segundo: un solo modelo, un solo conjunto de evaluación, cada posición etiquetada como vista o no vista, y la ganancia partida en dos.

Una analogía: [2] hace dos exámenes distintos a dos alumnos distintos, uno con preguntas repetidas de la guía y otro con preguntas nuevas. Nosotros le hacemos un solo examen a un solo alumno, con preguntas de los dos tipos mezcladas, y después vemos en cuáles le fue mejor.

Con eso claro, la frase quedaría así:

> Texto propuesto: Medir cómo se reparte la magnitud de la *trascendencia* entre posiciones vistas y no vistas durante el entrenamiento. [2] sí evalúa sobre consultas no vistas (su modo generalization), pero nunca compara ambas cosas en un mismo modelo: cada uno de sus experimentos entrena un modelo distinto y lo evalúa sobre un solo tipo de consulta, o todas vistas (denoising, selection) o todas no vistas (generalization). Nosotros proponemos evaluar un mismo modelo sobre un conjunto que contiene posiciones de ambos tipos, etiquetar cada una como vista o no vista, y descomponer la ganancia en esas dos componentes, en cada condición experimental.

## 👤 Mariano · 2026-09-12 02:41

pero si se evalua sobre consultas no vista se compara con las vistas no?

## 🤖 Claude · 2026-09-12 02:42

Tenés razón, y me obliga a ser más preciso. En [2] hay una comparación, aunque indirecta: reportan acierto casi perfecto en hechos de un salto (que están en el entrenamiento) y 34 % en hechos de dos saltos entre expertos (que no están). Así que "no compara visto con no visto" es exagerado. Lo que sí es cierto es más específico, y es lo que importa para nuestra propuesta:

**En [2] el ruido y lo no visto nunca conviven en el mismo experimento.** En los experimentos de denoising, todos los hechos de test están en el entrenamiento; no hay entradas no vistas. En el experimento de generalization, los autores ponen la probabilidad de error de los expertos en cero (lo dicen explícitamente en la Figura 1: "for simplicity in our generalization experiments, we set the probability of an expert generating an incorrect fact to 0"). O sea que en [2] el denoising se mide solo sobre entradas vistas, y la generalización se mide solo sin ruido.

Nuestra pregunta es justamente el cruce que ellos no pueden hacer: cuando los expertos son ruidosos, ¿la ganancia por voto aparece también en posiciones que el modelo nunca vio, o solo en las que se repiten? En un juego eso sale solo, porque un mismo modelo entrenado con expertos ruidosos enfrenta posiciones vistas (aperturas) y no vistas (finales) en una misma partida.

La frase quedaría así:

> Texto propuesto: Medir cómo se reparte la magnitud de la *trascendencia* entre posiciones vistas y no vistas durante el entrenamiento. En [2] esta pregunta no se puede formular: en sus experimentos de denoising todas las consultas de test aparecen en el entrenamiento, y en su experimento de generalization los expertos no cometen errores (los autores fijan la probabilidad de error en cero). El ruido y las entradas no vistas nunca conviven en un mismo experimento. En un juego sí conviven: un mismo modelo entrenado con expertos ruidosos enfrenta en cada partida posiciones que se repiten en el entrenamiento y posiciones nuevas. Proponemos etiquetar cada posición de evaluación como vista o no vista y descomponer la ganancia en esas dos componentes, en cada condición experimental.

## 👤 Mariano · 2026-09-12 02:43

es coertp qie "El ruido y las entradas no vistas nunca conviven en un mismo experimento"

## 🤖 Claude · 2026-09-12 02:44

Sí, es correcto como descripción del diseño de [2], con un matiz que conviene saber. Lo verifiqué contra el texto:

- **Denoising (Sec. 2.2 y 4).** Supuesto 2, explícito: el soporte de la distribución de test está contenido en el de entrenamiento. Todas las consultas de test son entradas que aparecen en los datos. Hay ruido (cobertura c menor a 1).
- **Selection (Sec. 2.3 y 5).** Dice textualmente "This setting maintains Assumption 2". Hay ruido. Entradas en soporte.
- **Generalization (Sec. 2.4 y 6).** Supone soporte de test disjunto del de entrenamiento. Y la leyenda de la Figura 1 dice: "For simplicity in our generalization experiments, we set the probability of an expert generating an incorrect fact to 0". Sin ruido.

Así que en ningún experimento hay a la vez expertos ruidosos y consultas de test fuera del soporte. La frase es cierta.

**El matiz.** "En soporte" en denoising y selection es un supuesto del marco, no algo que midan. Con pocos expertos y cobertura baja (por ejemplo un experto con cobertura 0,01 en la Figura 5), muchos hechos no los escribe nadie, y en la práctica algunas consultas de test no aparecen en el entrenamiento. Además, en denoising con un solo experto, la entrada aparece pero la respuesta correcta puede no aparecer nunca (el experto solo la escribió corrompida). Eso es "etiqueta no vista", distinto de "entrada no vista", y la taxonomía define visto y no visto sobre las entradas.

Para que la propuesta no quede expuesta a ese matiz, cambiaría "nunca conviven" por una formulación anclada en cómo ellos lo definen:

> En [2] esta pregunta no se puede formular: sus experimentos de denoising y selection asumen por diseño que toda consulta de test está en el soporte del entrenamiento (su Supuesto 2), y en su experimento de generalization, el único con consultas fuera de soporte, los expertos no cometen errores (los autores fijan la probabilidad de error en cero). Por construcción, el ruido y las entradas fuera de soporte no aparecen juntos en ningún experimento de [2].

## 👤 Mariano · 2026-09-12 02:48

y poner
- Medir la diferencia en la magnitud de la *trascendencia* entre posiciones vistas o no durante el entrenamiento.
pero aclarar abajo como nota al pie
Tal como explicamos en la sección siguiente: en [2] tratan de establecer una taxonomía de las causas de la trascendencia.
Los experimentos que evalúan denoising y selección, entrenan con expertos ruidosos pero toda la evaluación es de casos vistos en entrenamiento.
En cambio los experimentos de generalization evalúan casos no vistos en entrenamiento pero fijan la probabildiad de error de los expertos en cero.
No se plantea una comparación que diga muestre como se reparte la magnitud de la trascendencia cuando entre posiciones vistas y no vistas en un contexto donde hay ruido como un juego.

## 🤖 Claude · 2026-09-12 02:48

Aplico las dos cosas dentro de las citas (el bullet nuevo reemplaza mi sugerencia anterior, y la nota va como cita nueva al final de las notas al pie), sin tocar el texto original.

## 👤 Mariano · 2026-09-12 02:49

no apliques decime si está bien

## 🤖 Claude · 2026-09-12 02:49

No apliqué nada: el script falló antes de escribir, así que el archivo quedó igual que antes.

Sobre tu texto: **está bien en el fondo**, es fiel a lo que hace [2]. Tres ajustes chicos que haría:

1. **"toda la evaluación es de casos vistos en entrenamiento"**: es cierto como supuesto del marco (su Supuesto 2), no como algo que ellos verifiquen. Con pocos expertos y cobertura baja, en la práctica hay consultas que nadie escribió. Lo protegería con "por diseño" o "por supuesto".
2. **"fijan la probabilidad de error en cero"**: correcto, lo dicen en la leyenda de la Figura 1. Vale citar dónde para que un evaluador no lo tenga que buscar.
3. **Gramática**: "probabildiad", "que diga muestre", "cuando entre posiciones". Y "Tal como explicamos en la sección siguiente" funciona solo si en Fundamentos seguís nombrando los tres mecanismos de [2], que hoy sí están.

Versión corregida, mismo contenido:

> - Medir la diferencia en la magnitud de la *trascendencia* entre posiciones vistas o no durante el entrenamiento.^7

> (7) Tal como explicamos en la sección siguiente, [2] trata de establecer una taxonomía de las causas de la trascendencia. Sus experimentos de denoising y selección entrenan con expertos ruidosos, pero por diseño toda la evaluación es sobre casos vistos en el entrenamiento (su Supuesto 2). Sus experimentos de generalization, en cambio, evalúan casos no vistos, pero fijan la probabilidad de error de los expertos en cero (Figura 1 de [2]). No se plantea una comparación que muestre cómo se reparte la magnitud de la trascendencia entre posiciones vistas y no vistas en un contexto con ruido, como ocurre en un juego.

## 👤 Mariano · 2026-09-12 02:57

Preguntas:

"No se estudia *descubrimiento* (que el modelo supere lo que los expertos saben en conjunto). Denoising y selection son formas de ensamble implícito; la composición combina piezas que ya estaban en los datos. Los propios autores de [1] y [2] delimitan su marco de la misma manera."

alguno de los ppaers lo nombra con esa palabra (descubrimiento?)

## 🤖 Claude · 2026-09-12 02:58

Sí, los dos, aunque con matices:

- **[2] usa la palabra exacta.** En la Discusión (Sec. 8, última página): "our framework does not capture the idea of *skill discovery*". Lo escriben en cursiva como un cuarto modo que su taxonomía no cubre.
- **[1] no dice "discovery", pero delimita lo mismo.** En "Broader Impact" (Sec. 6): "the denoising effect addressed in this paper does not offer any evidence for a model being able to produce novel solutions that a human expert would be incapable of devising. In particular, we do not present evidence that low temperature sampling leads to novel abstract reasoning, but just denoising of errors."

Así que la frase de la propuesta es correcta, pero conviene atribuir bien: la palabra *skill discovery* es de [2]; [1] habla de "novel solutions". Lo reescribiría así:

> No se estudia *descubrimiento* (*skill discovery* en la terminología de [2]: que el modelo supere lo que los expertos saben en conjunto). Denoising y selection son formas de ensamble implícito; la composición combina piezas que ya estaban en los datos. Los propios autores delimitan su marco de la misma manera: [2] señala que su taxonomía no captura el *skill discovery*, y [1] aclara que el denoising no es evidencia de que el modelo produzca soluciones novedosas que un experto humano no podría concebir.

## 👤 Mariano · 2026-09-12 02:58

podriamos estudiar o tratar de aproximarnos al descubrieimeitno ade alguna manera?

## 🤖 Claude · 2026-09-12 03:00

Se puede, pero con cuidado con la palabra. Lo que sale de la teoría y del prototipo:

**Por qué el marco lo excluye.** A τ→0 el modelo juega el argmax de la mezcla que estimó. En un estado visto, si ninguna jugada m tiene masa en los datos, la mezcla verdadera le da masa cero y el argmax no puede ser m. Eso ya lo medimos: en la condición "ciega" (nadie abre al centro), P(centro | tablero vacío) es 0,0001 a τ=1 y 0 a τ→0. Descubrimiento estricto en estados vistos: imposible por teoría, y confirmado.

**Lo que ya tenés se parece a descubrimiento pero no lo es.** En π=1 (sesgo por hash) el modelo juega la jugada óptima en estados nuevos donde todos los expertos se equivocan. Ahí ningún experto sabe la respuesta *en ese estado*, pero sí la saben en estados parecidos. Abreu lo llamaría generalization, y tiene razón. En estados no vistos, descubrimiento y generalización son indistinguibles sin una noción de "estado parecido", y esa noción no la tenemos. Ese es un límite metodológico que vale escribir en la propuesta.

**Tres aproximaciones honestas, de menor a mayor ambición:**

1. **Definición operativa y medición como control cuantitativo.** Tasa de descubrimiento estricto: fracción de estados vistos donde el argmax del modelo es una jugada con masa empírica cero en el entrenamiento en ese tablero exacto. Predicción: cero en todas las condiciones. Es barato (los datos ya tienen los conteos por tablero) y convierte "no hay discovery" de anécdota en número. Entra en el objetivo 4 sin agregar experimentos.

2. **El continuo de representabilidad.** Entre la regla (perfectamente aprendida) y el hash (imposible de aprender) hay sesgos compartidos que son función del estado pero cuestan datos o capacidad: por ejemplo, un sesgo definido por una característica del tablero poco frecuente. Cuánto del sesgo el modelo *no* aprende mide cuánto juega bien donde todos los expertos juegan mal. Es un buen experimento para el objetivo 4, pero hay que presentarlo como "generalización que vence a un sesgo mal aprendido", no como descubrimiento.

3. **Condicionar por resultado (la única vía dentro de imitación pura).** Zhang lo nombra explícitamente en su Apéndice D.2 como "otra forma de trascendencia" a explorar: el Decision Transformer condiciona la generación al resultado de la partida. En nuestro pipeline el símbolo de resultado ya está en la secuencia, al final. Moverlo al principio y pedirle al modelo "partida ganada" da una política p(jugada | prefijo, gana), que pesa las jugadas por resultado y no por frecuencia. Eso sí puede superar el argmax de la mezcla: en selection por debajo del umbral, la jugada compartida errónea es la mayoría, pero las partidas donde el experto competente jugó bien se ganan más, así que el condicionamiento podría dar vuelta el argmax. Y Paster y Brandfonbrener, que ya están en la bibliografía, predicen lo contrario: contra un oponente ruidoso, condicionar por "gana" también selecciona las partidas donde el rival se equivocó, y el modelo aprende a "contar con la suerte". Dos predicciones opuestas, un experimento de costo casi nulo (un cambio en la generación y reentrenar), y no es descubrimiento en sentido estricto: sigue eligiendo entre jugadas que están en los datos, pero con un criterio que la teoría de [1] no cubre.

**Lo que no haría en una tesina:** búsqueda en inferencia (usar el modelo como prior y su predicción de resultado como valor, estilo AlphaZero) o auto-juego iterado. Lo primero ya no es imitación; lo segundo converge al argmax de la mezcla y no agrega conocimiento.

**Recomendación para la propuesta.** Mantener "no se estudia descubrimiento" en Alcance, pero agregar (1) como métrica del objetivo 4, y (3) como objetivo opcional al final, formulado como pregunta: "¿condicionar por resultado permite superar el argmax de la mezcla donde el voto falla, o el modelo aprende a contar con los errores del rival?". Es la extensión más interesante que encontré, y la más barata.

## 👤 Mariano · 2026-09-12 03:06

agregalo a Desktop/chess/discovery-ideas.md

## 🤖 Claude · 2026-09-12 03:07

Guardado en `~/Desktop/chess/discovery-ideas.md` (sin commitear, queda como archivo nuevo en el repo).

Contiene, en este orden: qué dicen [1] y [2] sobre discovery con las citas textuales y su ubicación; por qué el marco lo excluye y el dato de la condición ciega que lo confirma; por qué el hallazgo de π=1 es generalización y no descubrimiento; las tres aproximaciones (tasa de descubrimiento estricto, continuo de representabilidad, condicionamiento por resultado) con predicciones, diseño mínimo y costo; lo que no haría (búsqueda en inferencia, auto-juego); y la recomendación de cómo entra cada una en la propuesta.

Para el condicionamiento por resultado dejé el diseño concreto: resultado al principio de la secuencia en la generación, evaluación con prefijo fijo, condiciones selection α ∈ {0, 0.2, 0.45} más iid π=0 como control, unas 12 corridas.

## 👤 Mariano · 2026-09-12 03:08

respecto a /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina/propuesta-transcendencia-edited.md
podés editar tranquilamente con la sugerencias los objetivos especificos (ya era todo ia antes)

## 🤖 Claude · 2026-09-12 03:10

Ya está: la sección de objetivos quedó reescrita con las sugerencias integradas como texto corrido, y el resto del archivo lo dejé como vos lo tenías (vi que ya habías incorporado las demás citas a mano).

**Qué cambió en Objetivos específicos**

- Cada objetivo tiene ahora un título en negrita y el texto original más las sugerencias fundidas: tasa realizada en 1; dos métricas y evaluación desde logits en 2; denoising vs. selection según temperatura y el umbral α* en 3; los tres ejes (visto/no visto con la cautela de fase, representabilidad con control negativo y tasa de descubrimiento estricto, entropía residual con el control sin error) como sub-bullets en 4; hueco de soporte medible, diseño tentativo, controles y los dos bandos con citas [4], [5, 6] en 5; síntomas por condición en 6.
- Agregué la subsección "Alcance y limitaciones" después del párrafo de cierre, con la atribución correcta de *skill discovery* a [2] y "novel solutions" a [1].
- No agregué el objetivo opcional de condicionar por resultado. Queda en `chess/discovery-ideas.md` por si querés sumarlo.

**Cosas que vi en el resto del archivo y no toqué**, por si querés ajustarlas:

- En Motivación, la primera oración dice "rating <= 1000^6": la nota 6 es la de cuatro en línea; la de Glicko-2 es la 7.
- Notas 3 y 4 tienen una línea que arranca con `> ` que quedó de la cita y se va a renderizar como bloque aparte.
- Nota 8 conserva los tipeos que marqué antes ("probabildiad", "que diga muestre", "cuando entre posiciones"), y "toda la evaluación es de casos vistos" convendría matizarlo con "por diseño (su Supuesto 2)".
- Sigue el encabezado "Fundamentos..." duplicado, y en ese segundo Fundamentos todavía dice "~1000 ELO" mientras que Motivación ya dice "<= 1000".
- Programa: "1 semanas", "primero experimento", y la suma sigue dando 11 semanas.

## 👤 Mariano · 2026-09-12 03:12

bien moví todo esa seccion a /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina/propuesta-trascendencia-objetivos-especificos.md
porque por ahora no va a formar parte de la propuesta

me dirías por acá como lograr pie de pagina en markdown?

## 🤖 Claude · 2026-09-12 03:12

En Markdown hay dos formas, según qué renderer uses:

**1. Notas al pie nativas** (soportadas por GitHub, Obsidian, Pandoc, Typora, VS Code con la extensión Markdown Footnotes; no por CommonMark puro):

```markdown
El modelo juega con ~1500[^4].

[^4]: Como el ajedrez no es un juego resuelto, Zhang et al. [1] utiliza Stockfish.
```

- La marca es `[^id]` en el texto y `[^id]: texto` en cualquier lugar del archivo (por convención, al final).
- El `id` puede ser número o palabra: `[^glicko]`.
- El renderer numera automáticamente en orden de aparición, así que no importa si tus ids no son consecutivos.
- Una nota de varios párrafos: indentá las líneas siguientes con 4 espacios.

```markdown
[^8]: Tal como explicamos en la sección siguiente, [2] establece una taxonomía.

    Los experimentos de denoising y selección entrenan con expertos ruidosos...
```

**2. Lo que tenés ahora** (`^4` en el texto y una sección "Notas al pie" a mano): funciona en cualquier renderer porque es texto plano, pero el `^4` no es superíndice ni enlace. Si querés superíndice sin depender del soporte de footnotes, usá HTML inline: `<sup>4</sup>`.

Para convertir lo que ya tenés, el cambio mecánico es: `^4` → `[^4]` en el texto, y en la sección de notas `(4) ...` → `[^4]: ...`. Si después pasás a PDF con Pandoc, las notas quedan como pies de página reales.

## 👤 Mariano · 2026-09-12 03:13

ok podes hacer que las 
## Notas al pie
tengan ese formato (no entiendo si las tenes que distribuir por el texto o no

## 🤖 Claude · 2026-09-12 03:13

Listo. No hace falta distribuirlas por el texto: las definiciones pueden quedar todas juntas al final, como las tenías. El renderer las enlaza por el identificador y las numera él solo.

Qué cambié:

- En el texto, cada marca `^N` pasó a `[^N]`. Las ocho notas quedaron referenciadas exactamente una vez cada una.
- En "Notas al pie", cada `(N) texto` pasó a `[^N]: texto`. Las notas de varias líneas (1, 7 y 8) llevan las líneas siguientes indentadas con cuatro espacios, que es lo que el formato exige para que sigan perteneciendo a la misma nota. La lista con guiones de la nota 7 también quedó indentada y se renderiza como lista dentro de la nota.
- Un arreglo de contenido que hice porque si no la nota 7 quedaba huérfana: en Motivación, "rating <= 1000^6" apuntaba a la nota de cuatro en línea; ahora apunta a la 7, que es la de Glicko-2. El otro `^6` (el del verificador exacto) sigue apuntando a la 6, que es la correcta.

Un detalle de renderizado: el encabezado "## Notas al pie" ya no es necesario, porque los renderers con soporte de footnotes las ponen solos al final del documento con su propia línea separadora. Si lo dejás, en GitHub u Obsidian vas a ver el título y debajo, además, la sección automática de notas. En Pandoc a PDF el encabezado quedaría vacío. Lo dejé porque en un renderer sin soporte de footnotes (CommonMark puro) sirve como título de la lista, pero si tu destino es GitHub, Obsidian o Pandoc, conviene borrarlo.

## 👤 Mariano · 2026-09-12 03:14

Por ultimo algo que vamos a hacer es aplicar este skill pero para corregir el español:

# Grammar-only correction

Correct the grammar, spelling, punctuation, agreement, and obvious typos of the text the user references. If the text is inside a file, apply the corrections in the file.
Do NOT rewrite for style, tone, clarity, or conciseness. Do not reorder sentences, swap synonyms, or "improve" phrasing.
If you spot non-grammar issues (unclear phrasing, factual doubts), mention them at the end as suggestions clearly separated from the applied changes — but never apply them. Use enumerated bullet for this so the user can answer easily referring to each of them.
Keep the user's formatting, line breaks, capitalization style, emojis, and markdown intact.
Show in chat a list of one bullet per change: `"before" → "after"` with a short reason.

## 🤖 Claude · 2026-09-12 03:15

Apliqué 30 correcciones en el archivo. Solo gramática, ortografía, concordancia y puntuación; no toqué estilo ni orden.

**Cambios aplicados**

- "juega con ~1500[^4]" → "juega con ~1500[^4]." — punto final faltante.
- "En una segunda publicación [2] Abreu et al. (2025) se analiza" → "En una segunda publicación [2], Abreu et al. (2025) analizan" — concordancia: sujeto plural explícito con "se analiza" impersonal; coma tras el inciso.
- "apectos" → "aspectos" — tipeo.
- "Particularmente en relativo a:" → "Particularmente en lo relativo a:" — falta el artículo en la locución.
- "los datos que lo entrenan" → "los datos que los entrenan" — concordancia con "modelos".
- "Tal como se mencionó [1] muestra" → "Tal como se mencionó, [1] muestra" — coma tras subordinada inicial.
- "Concretamente entrenan" → "Concretamente, entrenan" — coma tras conector.
- "con ~1500 ELO" (fin de párrafo) → "con ~1500 ELO." — punto final.
- "Abreu et al. [2] (...) analiza" → "analizan" — concordancia con "et al.".
- "distribución subyacente [3]" → "distribución subyacente [3]." — punto final.
- "co-director" → "codirector" (dos veces) — ortografía: el prefijo va unido.
- "-desde su expertise ... profundo-" → "—desde su expertise ... profundo—" — rayas en lugar de guiones para el inciso.
- "todos los experimentos como elegir" → "todos los experimentos, como elegir" — coma antes de la ejemplificación.
- "**1 semanas**" → "**1 semana**" — concordancia de número.
- "este primero experimento" → "este primer experimento" — apócope obligatoria ante sustantivo.
- "Se definirá conceptualmente los experimentos" → "Se definirán" — concordancia con sujeto plural.
- "auto-regresivos" → "autorregresivos" — ortografía.
- "También al igual que [1] el imitador" → "También, al igual que [1], el imitador" — comas del inciso.
- "de los errores. Sino que analiza" → "de los errores, sino que analiza" — "sino que" no inicia oración; es coordinación adversativa.
- "Abreu et al. [2]" (fin de nota 5) → "Abreu et al. [2]." — punto final.
- "posibildiad" → "posibilidad"; "trabjo" → "trabajo" — tipeos.
- "combinatorios chicos), podrían servir" → "chicos) podrían servir" — coma entre sujeto y verbo.
- "Zhang et al. [1] utiliza Stockfish" → "utilizan" — concordancia con "et al.".
- "evaluador (con la que calcula" → "(con el que calcula" — concordancia con "evaluador".
- "en la sección siguiente: en [2] tratan" → "en la sección siguiente, en [2] tratan" — dos puntos indebidos entre subordinada y principal.
- "denoising y selección, entrenan" → "denoising y selección entrenan" — coma entre sujeto y verbo.
- "En cambio los experimentos" → "En cambio, los experimentos" — coma tras conector.
- "probabildiad" → "probabilidad" — tipeo.
- "que diga muestre como se reparte ... cuando entre posiciones ... hay ruido como un juego" → "que muestre cómo se reparte ... entre posiciones ... hay ruido, como un juego" — palabra duplicada ("diga"), tilde en "cómo" interrogativo indirecto, "cuando" sobrante, coma antes del ejemplo.

**Sugerencias no aplicadas** (no son gramática):

1. Motivación dice "rating <= 1000" y "~1500" sin unidad; Fundamentos dice "~1000 ELO" y "~1500 ELO", y la nota 7 aclara que es Glicko-2. Conviene unificar.
2. El encabezado "Fundamentos y estado del conocimiento sobre el tema" sigue duplicado.
3. "Alcance y limitaciones" quedó dentro de Fundamentos y menciona "objetivo 5", pero los objetivos ya no están en este archivo.
4. Programa: el primer ítem dice que el relevamiento "ya se ha realizado" y asigna 1 semana; el total suma 11 semanas.
5. Último ítem del programa: "para la presentación para ser corregido" repite "para".
6. Nota 4: "Le atribuye la diferencia a que" tiene el pronombre redundante ("Atribuye la diferencia a que"). Y "analiza la correlación entre las jugadas" no es exacto: [1] mide la entropía de la distribución de jugadas en posiciones frecuentes, no una correlación.
7. Nota 8: "toda la evaluación es de casos vistos en entrenamiento" es un supuesto de diseño de [2] (su Supuesto 2), no algo que verifiquen; convendría "por diseño".
8. Bullets de la segunda sección de Fundamentos: tres sin punto final y dos con punto. Es consistencia, no gramática.

## 👤 Mariano · 2026-09-12 03:18

1. si, corregir
2. ahi lo corregí yo
3. ahi borre la seccion
4. esta bien esto, dejalo asi
5. si, corregir
6. proponer cambio por aca
7. propone cambio por aca
8. si, corregi

## 🤖 Claude · 2026-09-12 03:19

Aplicados los puntos 1, 5 y 8:

- **1.** En Fundamentos, "rating ~1000 ELO ... con ~1500 ELO" → "rating <= 1000 ... con ~1500", igual que en Motivación. Saqué "ELO" porque la nota 7 ya aclara que es Glicko-2.
- **5.** "puesto a punto para la presentación para ser corregido" → "puesto a punto para la presentación y corrección".
- **8.** Punto final en los tres bullets que no lo tenían (imitación, ensamble, sabiduría de las masas).

Propuestas para 6 y 7, sin aplicar:

**6. Nota 4.** Texto actual:

> El mismo trabajo reporta que el modelo entrenado con partidas de jugadores de hasta 1500 *no trasciende*. Le atribuye la diferencia a que ese conjunto de datos tiene menos diversidad de jugadas. Como son datos de partidas reales, no se puede intervenir sobre la estructura de correlación de los errores, sino que analiza la correlación entre las jugadas.

Propuesta:

> El mismo trabajo reporta que el modelo entrenado con partidas de jugadores de hasta 1500 *no trasciende*. Atribuye la diferencia a que ese conjunto de datos tiene menos diversidad de jugadas, medida como la entropía media de la distribución de jugadas en las posiciones frecuentes. Como son datos de partidas reales, no se puede intervenir sobre la estructura de correlación de los errores; la relación entre diversidad y trascendencia queda establecida por correlación, no por manipulación.

Dos cambios de fondo: saco el "Le" redundante, y reemplazo "analiza la correlación entre las jugadas" por lo que [1] hace en realidad (Figura 5: entropía normalizada de la distribución de acciones en posiciones con más de 100 jugadas registradas).

**7. Nota 8.** Texto actual:

> Los experimentos que evalúan denoising y selección entrenan con expertos ruidosos pero toda la evaluación es de casos vistos en entrenamiento.

Propuesta:

> Los experimentos que evalúan denoising y selección entrenan con expertos ruidosos, pero por diseño toda la evaluación es sobre casos vistos en el entrenamiento (su Supuesto 2: el soporte de la distribución de evaluación está contenido en el de entrenamiento).

El resto de la nota 8 queda igual. Si querés, también agregaría al final de la frase de generalization la fuente: "(lo declaran en la leyenda de su Figura 1)".

## 👤 Mariano · 2026-09-12 03:23

las referencias están bien citadas? y bien referenciadas

## 🤖 Claude · 2026-09-12 03:24

Revisé las dos cosas por separado.

**Citas en el texto: hay un problema.** En el cuerpo solo se citan [1], [2] y [3]. Las entradas [4] a [18] están en REFERENCIAS pero ninguna se cita, porque las que las usaban ([4], [5], [6]) estaban en los objetivos que moviste al otro archivo, y las demás nunca tuvieron cita en el texto. Una lista de referencias con quince entradas huérfanas es lo primero que marca un evaluador.

Dos detalles menores de estilo de cita:
- Línea 11: "En una segunda publicación [2], Abreu et al. (2025) analizan" mezcla numérico y autor-año. Sobra el "(2025)".
- Línea 7: "El trabajo reciente (2024) de Zhang et al. [1]" tiene la misma redundancia, más leve.

**Entradas de REFERENCIAS: están bien.** Verifiqué autores, sedes, años e identificadores de arXiv de las 18. Todo correcto. Única inconsistencia de formato: [1] y [2] traen sede más arXiv; [4], [13], [14], [16], [17] y [18] traen solo arXiv. [16] (Reversal Curse) además se publicó en ICLR 2024, si querés agregarlo.

**Cómo resolver las huérfanas.** Cada una tiene un lugar natural en el texto actual, salvo tres:

- Sección "Áreas de la literatura adyacentes": imitación → [9, 10]; ensamble → [11]; sabiduría de las masas → [12]; filtrar ruido → [13]. Memorización ya cita [3].
- Nota 1 (el imitador solo ve la secuencia y debe construir el estado): [14, 15].
- Nota 6 (cuatro en línea como dominio preliminar): [7, 8].
- Bullet de composición en Motivación ("[2] obtiene resultados débiles al respecto"): agregar la frase de los dos bandos con [4] y [5, 6], o mover esas tres al archivo de objetivos, donde ya se citan.
- [16], [17], [18] no tienen dónde ir en esta versión. Las sacaría de acá y las dejaría en el archivo de objetivos específicos.

Si me decís que sí, aplico las citas en esos lugares y saco las tres sin hogar.

## 👤 Mariano · 2026-09-12 03:24

dale agregá las referencias

## 🤖 Claude · 2026-09-12 03:25

Listo. Ahora las 15 entradas de REFERENCIAS se citan en el texto, y no hay ninguna huérfana.

Dónde quedó cada cita:

- **Motivación, bullet de composición**: agregué "y la literatura vecina predice resultados opuestos: colapso fuera del soporte de cada demostrador [5, 6] o transferencia composicional [4]".
- **Áreas de la literatura adyacentes**: imitación [9, 10], ensamble [11], sabiduría de las masas [12], filtrado de ruido [13]. Memorización ya tenía [3].
- **Nota 1** (el imitador construye el estado desde la secuencia): [14, 15].
- **Nota 6** (cuatro en línea como dominio preliminar): [7, 8].

Además saqué el "(2025)" redundante junto a "Abreu et al. [2]" en Motivación. Dejé el "(2024)" de la primera oración porque ahí funciona como fecha del trabajo, no como cita.

Las tres entradas sin lugar en esta versión ([16] Berglund, [17] Allen-Zhu y Li, [18] Krestnikov) las moví al final de `propuesta-trascendencia-objetivos-especificos.md`, bajo un encabezado que aclara que salieron de la propuesta por no estar citadas. Ahí tampoco se citan todavía. Si en algún momento incorporás el objetivo de representabilidad o el de descubrimiento, [18] es la que tiene uso natural.

## 👤 Mariano · 2026-09-12 03:25

luego para cada item de ### Áreas de la literatura adyacentes
explicame breve y concisamente de que va cada uno y si la relacion es muy tangencial y bolazo o esta bien

## 🤖 Claude · 2026-09-12 03:26

Los cinco, en orden. Para cada uno: de qué va, qué dice la referencia citada, y cuán real es la conexión con la tesina.

**1. Aprendizaje por imitación y sus límites teóricos [9, 10]**
Behavioral cloning es entrenar una política con supervisión sobre las acciones de un demostrador. Ross y Bagnell (2010) prueban que los errores se acumulan: si el imitador se equivoca con probabilidad ε por paso, el costo total crece como T²ε porque cada error lo lleva a estados que nunca vio, donde se equivoca más. DAgger (2011) es la solución: dejar que el imitador juegue y pedirle al experto que etiquete sus propios estados.
**Conexión: sólida.** Es exactamente la distinción entre evaluar en la distribución de estados del experto y en la del propio modelo, y explica por qué la tasa de acierto por estado y el resultado de partida pueden discrepar. La trascendencia es el caso opuesto al que estudian ellos (el imitador rinde *más* que el demostrador), lo cual la hace interesante en este marco.

**2. Métodos de ensamble [11]**
Breiman (1996): entrenar muchos modelos sobre remuestreos de los datos y promediar sus predicciones reduce la varianza. Funciona porque los errores de los distintos modelos no coinciden.
**Conexión: sólida y directa.** El argumento de Zhang es literalmente que el argmax de la mezcla es un voto por mayoría entre expertos, y que funciona solo si sus errores no están correlacionados. Es la misma matemática. El propio [1] cita a Breiman por esto.

**3. Sabiduría de las masas [12]**
La observación de que el promedio de muchas estimaciones independientes suele ser mejor que la de cualquier individuo. Marcolino, Jiang y Tambe (2013) lo llevan a agentes de Go: un equipo de agentes distintos que votan le gana a un equipo de copias del mejor agente, y prueban condiciones para que eso pase.
**Conexión: buena.** Es la versión "agentes que juegan" del punto 2, y Tambe es coautor de [1], que lo cita como antecedente. El único matiz: en la tesina el voto es implícito (lo hace el modelo al aprender la mezcla), no un comité explícito. Es una analogía cercana, no el mismo objeto.

**4. Filtrar ruido de etiquetas durante el entrenamiento [13]**
Rolnick et al. (2017): las redes profundas siguen aprendiendo bien aunque la mayoría de las etiquetas sean incorrectas, siempre que el ruido sea aleatorio y no sistemático; lo que las hunde es el ruido correlacionado con la entrada.
**Conexión: sólida.** Es el mismo fenómeno visto desde clasificación: ruido aleatorio se promedia, ruido estructurado se aprende. La condición "compartido y representable" de la tesina es la traducción exacta a un dominio secuencial. Lo tangencial es la frase de la propuesta ("modelos de lenguaje ... durante el entrenamiento o el muestreo"): Rolnick habla de clasificadores de imágenes, no de modelos de lenguaje. Yo sacaría "de lenguaje".

**5. Dinámica de memorización [3]**
Arpit et al. (2017): una red primero aprende los patrones compartidos por muchos ejemplos y solo después, con más pasadas, memoriza ejemplos individuales, incluidas las etiquetas ruidosas.
**Conexión: sólida.** Es la razón por la que sobreentrenar destruye el voto: cuando el modelo memoriza cada partida con sus errores, el argmax deja de ser la mayoría. Y explica por qué [1] nunca lo ve: una sola pasada sobre mil millones de partidas nunca llega a esa fase.

**Veredicto.** Ninguna es bolazo. Las cinco están en la genealogía intelectual de [1] (tres son citas directas de ese paper). La más floja es la 3, por ser analogía y no mecanismo idéntico. El único ajuste que haría es el de la 4: "modelos de lenguaje" sobra, la evidencia es de clasificación general.

## 👤 Mariano · 2026-09-12 03:27

bien y está bien en markdown referenciar con [1] [2] [9,10] ?

## 🤖 Claude · 2026-09-12 03:28

Sí, está bien. Markdown no tiene sintaxis propia de citas, así que `[1]` es texto plano y se renderiza tal cual. El estilo numérico entre corchetes es el estándar tipo IEEE y es lo normal en una propuesta.

Dos cosas a tener en cuenta para que no se rompa el renderizado:

- `[texto](url)` y `[texto][etiqueta]` son enlaces. Solo se activan si van pegados, sin espacio. `[2] (2025)` y `[1] [2]` con espacio no son enlaces. Igual, si dudás, no pongas paréntesis ni corchetes inmediatamente después de una cita.
- `[1]` solo se convierte en enlace si existe en algún lado una definición `[1]: http://...`. Vos no tenés ninguna, así que quedan literales. Las notas al pie usan `[^1]:`, que es otra cosa y no choca.

Sobre la forma: `[9, 10]` con coma y espacio está bien, y ahora todas las citas múltiples del archivo siguen ese formato. Lo importante es no mezclar `[9, 10]` con `[9,10]` o con `[9][10]`.

Si más adelante pasás el documento a PDF con Pandoc, la alternativa es `[@zhang2024]` con un archivo `.bib`: Pandoc numera, ordena y genera la bibliografía solo. Para una propuesta en Markdown que se va a leer tal cual, lo que tenés es lo correcto.

## 👤 Mariano · 2026-09-12 03:31

quiero discutir lo siguiente por acá (no edites):

creo que habria que agregar al programa en algun momento hacer ablation studies

tambien otro tipo de experimentos que ponele sería en vez de usar un transformer usar otra cosa y ver que los resultados se replican (que no son particular a la arquitectura). Eso no es un ablation study como se llama?

Cuando pondría todo eso?

## 🤖 Claude · 2026-09-12 03:32

Tres cosas: terminología, qué vale la pena acá, y dónde va en el programa.

**Terminología.** Un *ablation study* es sacar o desactivar una pieza de tu propio sistema para medir cuánto aporta: quitar el token de resultado, achicar el modelo, sacar el weight decay. Cambiar el transformer por otra arquitectura y ver si los resultados se replican no es ablación: es un **análisis de sensibilidad** o **control de arquitectura** (en los papers suele aparecer como "robustness to architecture choice" o "the result is not specific to transformers"). En la práctica mucha gente mete todo bajo "ablations", pero en una propuesta conviene distinguirlos porque responden preguntas distintas: la ablación pregunta "¿qué parte de mi sistema produce el efecto?", el control de arquitectura pregunta "¿el efecto es del objetivo de imitación o del modelo?".

**Qué vale la pena en este trabajo.** El prototipo ya hizo sensibilidad a tamaño de modelo (0.1M, 0.8M, 6M), a datos (20k, 80k, 320k) y a pasadas, así que eso sería formalizarlo, no inventarlo. Lo que agregaría, ordenado por cuánto informa:

1. **Representación de entrada: secuencia vs. tablero.** Hoy el imitador solo ve las jugadas y tiene que construir el estado. Darle el tablero directamente es la ablación de esa decisión de diseño. Importa sobre todo para composición (objetivo 5): si el modelo ve el tablero, componer finales tras aperturas nuevas es casi trivial porque la política es función local del tablero; el resultado interesante es que funcione a ciegas. Esta ablación dice cuánto del mérito es de la representación aprendida.
2. **Arquitectura: transformer vs. red recurrente sobre la secuencia.** Para denoising y selection, la teoría dice que cualquier estimador consistente de la mezcla vota igual, así que replicar es lo esperado y un fallo sería lo informativo. Para composición sí es un experimento de verdad, porque ahí la respuesta depende del sesgo inductivo del modelo, no de la teoría.
3. **Token de resultado al final: con y sin.** Barata y conecta con la discusión de descubrimiento: el modelo hoy aprende implícitamente a predecir quién gana. Si sacarlo no cambia nada, es una pieza menos que explicar.

Lo que no haría: barrer todo contra todo. Un evaluador valora dos ablaciones limpias sobre los resultados principales (la curva en π y la composición) más que diez sobre todas las condiciones.

**Dónde va.** Después de tener el punta a punta de todos los experimentos y antes de unir resultados y sacar conclusiones, porque las conclusiones tienen que decir "esto no depende de la arquitectura" y eso hay que medirlo antes de escribirlo. En tu programa, entre el ítem "Se trabajará en tener el mismo punta a punta en cada uno de ellos" y "ya tendremos toda la presentación de resultados", una semana. El cómputo lo permite: cada corrida son minutos, y son unas 20 corridas. Redacción tentativa del ítem:

> Análisis de sensibilidad y ablaciones sobre los resultados principales: reproducir la curva de correlación de errores y la condición de composición variando tamaño del modelo, cantidad de datos, arquitectura del imitador y representación de entrada (secuencia de jugadas vs. tablero), para separar lo que depende del objetivo de imitación de lo que depende del modelo concreto. **1 semana**

Eso deja el total en 12 semanas. Alternativa si no querés tocar la cuenta: meterlo dentro del objetivo 6 (régimen de entrenamiento), que ya es "condiciones de contorno del fenómeno", y ampliarlo a "régimen de entrenamiento y elecciones de modelo". Pero como ítem propio del cronograma se ve mejor: muestra que sabés que hay que hacerlo y cuándo.

## 👤 Mariano · 2026-09-12 03:36

bien ahora hace que 
### Programa tentativo de trabajo sea una enumeracion

## 🤖 Claude · 2026-09-12 03:36

Listo: los diez ítems del programa ahora están numerados del 1 al 10, con el texto y las semanas de cada uno sin cambios.

Un tipeo que vi en el ítem 6 que agregaste vos: "arquitetura" → "arquitectura". No lo toqué porque no me pediste corrección ahí; decime y lo aplico.
