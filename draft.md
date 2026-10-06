
## Teoría de correlacion compartida por granito
La teoría dice que al promediar n expertos con correlación ρ la varianza residual nunca baja de ρσ²
Predicciones cuantitativas:
- acc(τ→0) ≈ 1 − β̂ 
- ganancia sobre el experto ≈ q̂
Donde β̂ y q̂ son las tasas realizadas de error compartido e independiente sobre estados decidibles. 
A τ=1 no hay trascendencia para ningún valor, por la Proposición 1 de Zhang.


## Aporte original que quizás tiene nuestro trabajo
- [1] solo pudo correlacionar diversidad con entropía en datos humanos. 
- [2] varía la cantidad de expertos como proxy de descorrelación. 
- Nuestro diseño nos permite variar la correlación directamente (variando la proporción de errores compartidos) manteniendo fija la tasa de error.

## Duda acerca de desventaja de nuestro trabajo
Nota: [1] calcula una métrica que es el rating haciendo jugar al modelo contra un bot.
En nuestro caso al ser un juego resuelto y el bot que tenemos ser óptimo, jugar contra el mismo no tiene mucho sentido.
Un primer jugador perfecto gana siempre:
    - cuando el modelo juega segundo ningún movimiento cuenta como un error.
    - cuando el modelo juega primero, la métrica colapsa a "cuántas jugadas aguanta sin errar como primero"



Quiero que trabajemos en diseñar e implementar el experimento1
  El objetivo es completar ./experimento1/experimento1-v1.md con el diseño, detalles de implementación y resultados del experimento1 tal y como lo vamos a incluir en la tesina

  - Leer la propuesta v1 para tener más contexto.
  - Explorar exploracion-pre-propuesta para entender los experimentos planteados. Sobre todo transcendencia_slides.html, el papper y los .md para entender lo hecho. El resto de los archivos (codigo, logs, resultados, runs, checkpoints) los ignoraría por ahora porque te van a introducir mucho ruido en el contexto
  - Leer el ./experimento1/CURRENT_STATUS.md para ver comentarios de Pablo que pueden ser relevantes a la hora de diseñar / implementar los experimentos.
  - Leer los pappers [1] y [2] del directorio referencias para tomar como ejemplo cómo se plantea un experimento en la academia y qué detalles es importante incluir (modelo, modos de entrenamiento, training set, evaluación, etc). De todas maneras, en cuanto al formato, como primer borrador quizás escribimos algo mucho más fácil de parsear que el formato académico/papper (y usamos enumeraciones, y un estilo más parecido a propuesta v1)

  Dame algo por acá primero, luego vamos a iterar y escribir entre los dos el .md
