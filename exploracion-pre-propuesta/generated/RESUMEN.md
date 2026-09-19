# Resumen del trabajo: transcendencia en modelos imitadores, medida en Connect 4

*Dos días de trabajo (1 al 3 de septiembre de 2026). Repo: `~/Desktop/chess`. Paper en `paper/main.pdf`, diapositivas en `slides/`, log cronológico en `overnight/notes.md`.*

---

## 1. El punto de partida

Dos papers del mismo grupo (Harvard / Kempner):

- **Zhang et al. 2024, "Transcendence"** (arXiv 2406.11741). Entrenaron un transformer a imitar partidas de ajedrez de jugadores con rating ≤ 1000. Muestreado a temperatura baja, el modelo juega a ~1500: mejor que cualquier jugador que vio. A eso lo llaman **transcendencia**.
- **Abreu et al. 2025, "A Taxonomy of Transcendence"** (arXiv 2508.17669). Organizan el fenómeno en tres modos: *denoising* (voto por mayoría), *selection* (rutear al experto competente) y *generalization* (componer conocimiento que ningún experto tiene). Lo testean en un grafo de conocimiento sintético.

**La explicación de Zhang, en una línea.** El imitador aprende la *mezcla* (el promedio) de todos los expertos. A temperatura 1 muestrea igual que los datos y no puede superar al mejor experto. A temperatura → 0 elige la jugada más probable de la mezcla, que es un **voto por mayoría implícito**: si los expertos se equivocan en jugadas distintas, sus errores se reparten y la jugada correcta concentra la masa. Teorema 2: hay transcendencia si y solo si el argmax de la mezcla rinde más que el mejor experto individual.

**Lo que ambos papers dejan abierto:**
1. La teoría habla de la mezcla *verdadera*. Un modelo finito tiene una *estimación* por posición, con datos y capacidad finitos. ¿Dónde esa estimación alcanza para que el voto funcione?
2. Con datos humanos no se puede manipular la correlación de los errores. La necesidad de diversidad se infiere, no se prueba.
3. Zhang nombra su propia brecha: la teoría supone que cada experto está definido en todo el espacio de estados, "imposible después de la jugada 15". ¿El imitador compone habilidades de expertos que nunca aparecen en las mismas posiciones?

## 2. Qué construimos

Un **testbed exacto y controlable**:

- **Connect 4** (7×6) con el solver de Pascal Pons: en cada posición sabemos el resultado exacto (gana / empata / pierde) de cada jugada. La recompensa es exacta, sin motores heurísticos ni ratings.
- **Expertos sintéticos** que conocen el solver y a los que les inyectamos errores con la estructura que queremos:
  - `iid(ρ, π)`: tasa de error ρ; una fracción π de esos errores es **compartida** por todos los expertos (mismo error en las mismas posiciones, definidas por un hash), el resto es independiente.
  - `selection(K, α)`: K expertos, cada uno óptimo en una región y con el mismo error fuera de ella; α controla cuánto genera cada uno datos dentro de su región.
  - `rule`: todos juegan la columna más a la izquierda cada 3 jugadas (error compartido **aprendible**).
  - `blind`: nadie abre al centro (control de "discovery").
  - `composition`: familia A juega aperturas óptimas y su partida se **corta** en la jugada N (nunca muestra finales); familia B abre mal o con estilo restringido (bordes) y juega el final perfecto. Ningún transcript muestra un final después de una apertura buena.
- **Imitador**: transformer de 6.3M parámetros que **solo ve la secuencia de jugadas** (nunca el tablero), entrenado por next-token prediction. Por defecto 80 mil partidas, ~10 epochs, 3 semillas por condición.
- **Evaluación desde los logits**, sin muestrear: en ~60 mil posiciones nuevas, para cada temperatura, calculamos la recompensa esperada y la probabilidad de jugar una jugada óptima. La del experto en las mismas posiciones es analítica. También partidas cabeza a cabeza.

## 3. Qué encontramos

### 3.1 Las dos teorías se cumplen en signo, en todas las celdas

| Experimento | Predicción | Resultado (3 semillas, desvíos ≤ 0.005) |
|---|---|---|
| Ganancia a τ→0 vs fracción compartida π | decrece con π, cambia de signo | +0.040, +0.027, +0.015, +0.003, −0.017 para π = 0, .25, .5, .75, 1. Casi lineal. |
| Selection vs ruteo α (K=4) | umbral en α* = 1/3 | −0.105, −0.040, +0.126, +0.169, +0.169 para α = 0, .2, .45, .7, 1. Flip entre 0.2 y 0.45. |
| Expertos complementarios (Teo. 4) | transciende | +0.076 |

Esto es lo que el paper de ajedrez no podía hacer: **manipular** la correlación de errores. La diversidad es causal.

### 3.2 Tres propiedades del estimador que la teoría no predice

**a) La ganancia vive en las posiciones que se repiten.** Separando las posiciones de test en "vistas en el entrenamiento" y "no vistas":

| Partidas de entrenamiento | Ganancia total | En vistas | En no vistas |
|---|---|---|---|
| 20k | −0.031 | +0.060 | −0.093 |
| 80k | +0.040 | +0.092 | −0.006 |
| 320k | +0.062 | +0.090 | +0.030 |

En posiciones vistas el voto llega al techo teórico (+0.055) desde 20k partidas. En posiciones nuevas el imitador es peor que el experto hasta que hay 4× más datos. Un voto por posición necesita votos por posición.

**b) Un error compartido sobrevive solo si es representable.** El error por hash (compartido pero impredecible desde la posición) se reproduce en la apertura (posiciones vistas, acierto 0.006) y se **generaliza hacia afuera** en posiciones nuevas (acierto 0.41–0.56). La regla aprendible se reproduce a **tres decimales** en todas las fases, con cualquier cantidad de datos. La ceguera al centro: P(centro | tablero vacío) = 0.0000. **No hay discovery.**

**c) Composición con soporte disjunto: funciona.** La habilidad de final demostrada solo tras aperturas de bordes se aplica a finales tras aperturas óptimas con acierto 0.925 (control: 0.950). Penalidad ≤ 0.03, graduada con la severidad del desplazamiento, insensible a tamaño de modelo (0.1M a 6M), datos (20k a 80k) y profundidad del corte (N = 8 o 14). Controles: solo-B pierde **todas** las partidas contra un oponente perfecto (aperturas malas); solo-A no sabe jugar finales; **A+B gana ~70 % de sus partidas como primer jugador contra un oponente perfecto**, algo que ninguna de las dos poblaciones puede hacer.

### 3.3 Un resultado de régimen

**Entrenar de más destruye la ganancia.** Con 80k partidas, pasar de 10 a 42 epochs baja el acierto a τ→0 de 0.891 a 0.837, por debajo del experto (0.845). El modelo memoriza las partidas concretas con sus errores. Es la dinámica clásica de memorización de etiquetas ruidosas (Arpit 2017). El paper de ajedrez hizo una sola pasada sobre mil millones de partidas: nunca entró en ese régimen.

## 4. Qué significa

**Una lente para todo:** el argmax aprendido es un *estimador* del argmax de la mezcla verdadera. Es exacto donde una posición se repite, sesgado hacia funciones del estado, con varianza alrededor del margen de la mezcla, y sobreajustado si se entrena de más. Cada desvío de la teoría es una de esas cuatro cosas.

**Sobre el paper original:** el salto 1000 → 1500 mezcla tres componentes: voto en posiciones recurrentes, generalización en posiciones nuevas (que recién ayuda con muchísimos datos, que ellos tenían), y eliminación de la entropía residual del propio modelo (que no es transcendencia sobre los expertos).

**Sobre la taxonomía:** la condición "errores correlacionados no se pueden denoisear" necesita el calificador "y representables". Y el modo *generalization* tiene ahora contenido empírico positivo en un juego con estado observable.

**Lo que NO es:** discovery. Nada de esto supera lo que los expertos saben en conjunto. Denoising y selection son ensembling (voto por mayoría, mixture-of-experts implícito). La composición combina piezas que ya estaban.

**Honestidad sobre la novedad:** las validaciones confirman teoría publicada; la memorización es Arpit 2017 con otro nombre; las tres propiedades del estimador son lo que un practicante habría predicho. El valor es que están **medidas con ground truth exacto en las brechas que los dos papers dejaron**, y que la composición responde una pregunta donde dos bandos serios predecían lo opuesto. Da para un workshop paper honesto, no para un main track.

## 5. Cómo se hizo

- **Día 1 (noche):** Mac M4 con MPS. 13 condiciones, una semilla. Generación de datos en CPU (2 ms por posición, ~20 min por dataset de 80k), entrenamiento 30 min por run.
- **Día 2:** RTX 4090 en RunPod (0.74 USD/h). Semillas 2 y 3 de todo, estudio de escala (80k vs 320k × 1600/6400/25600 pasos), descomposición visto/no visto, 16 condiciones de composición × 3 semillas. Un run de 1600 pasos tarda 1.7 min. El pod anuncia 96 vCPU pero el cgroup lo limita a 10; la subida de datos desde la Mac va a 200 KB/s.
- **Costo total:** ~17 USD de GPU. 62 runs base + 12 de escala + 48 de composición + 8 descomposiciones.
- **Método:** todo el ciclo (diseño, código, colas nocturnas, análisis, paper, diapositivas) con Claude como asistente autónomo, con revisión humana en cada decisión de diseño e interpretación. Dos errores corregidos en el camino: entusiasmarse con la "ventana de entrenamiento" antes de reconocerla como memorización con otro nombre, y evaluar el checkpoint final en vez del de mejor val loss.
- **Búsqueda bibliográfica** con un agente: nadie corrió un experimento sintético controlado de transcendencia después de la taxonomía; el espacio está vacío, no saturado, pero las preguntas interesantes están cubiertas por literaturas vecinas (model collapse, RCSL, OOD generalization). La única con incertidumbre genuina era la composición, que corrimos.

## 6. Qué haría falta para seguir

- Evaluar en el checkpoint de mejor val loss y 3 semillas en la tabla de escala.
- Un dominio donde la predicción pesimista sobre composición sea la plausible (acá la optimista lo era).
- Un enunciado de muestra finita para el Teorema 2: cuándo el argmax aprendido coincide con el verdadero.
- Repo público y URL real en el paper (hoy es un placeholder).

## 7. Glosario mínimo

- **Modelo generativo / autoregresivo:** predice la distribución del siguiente símbolo dado el prefijo. Entrenado por imitación (cross-entropy), sin recompensa.
- **Temperatura τ:** divide los logits antes del softmax. τ=1 copia los datos; τ→0 elige el argmax; τ>1 es más aleatorio.
- **Mezcla de expertos:** el promedio de las políticas de los expertos. Es lo que el imitador aprende en el límite.
- **Transcendencia:** el imitador rinde más que el mejor experto individual de su dataset.
- **Denoising / selection / generalization:** los tres modos de la taxonomía (voto, ruteo, composición).
- **Estado visto / no visto:** una posición de test que aparece (o no) en el conjunto de entrenamiento.
- **Soporte disjunto:** dos familias de expertos cuyas posiciones no se superponen (una solo aperturas, otra solo finales tras malas aperturas).
- **Solver exacto:** programa que calcula el resultado teórico de cualquier posición de Connect 4 con juego perfecto.
- **Representable:** que el modelo puede expresar como función de la secuencia que ve (una regla simple sí; un hash no).
