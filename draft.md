
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


