# solver

Infraestructura de Connect 4 compartida por todos los experimentos: reglas del juego y acceso al
solver exacto de Pascal Pons. Es la implementación de la sección "Solver" y de la terminología
(estado `e`, jugada `c`, jugadas legales, recompensa `r(e, c)`, jugada óptima, error, estado
decidible) definida en `experimento1`.

## Instalación

```bash
./solver/setup.sh   # clona Pons, compila c4solver, baja el libro de aperturas, verifica
uv sync             # instala el paquete python `c4solver` (editable) y pytest
uv run pytest       # 17 tests: reglas del juego + hechos conocidos del solver
```

`setup.sh` deja todo en `solver/third_party/connect4/`, que está en el `.gitignore` (el código de
Pons es AGPL v3 y el libro pesa 33 MB). Fija el commit `d6ba50d` del repo
`PascalPons/connect4` y baja `7x6.book` de las releases de ese repo. En una máquina sin claves SSH:
`C4_REPO_URL=https://github.com/PascalPons/connect4.git ./solver/setup.sh`.

## Uso

```python
from c4solver import Position, Solver, Outcome

pos = Position("4453")          # secuencia de columnas 1..7, notación de Pons
pos.legal_moves()               # [1, 2, 3, 4, 5, 6, 7]
pos.player_to_move              # 1
pos = pos.play(4)               # inmutable: devuelve una posición nueva
pos.is_terminal(), pos.winner() # (False, None)
print(pos)                      # tablero ASCII

with Solver() as s:             # modo débil por defecto (solo gana/empata/pierde)
    s.outcome(pos)              # Outcome.WIN / DRAW / LOSS para quien mueve
    s.move_outcomes(pos)        # {1: Outcome.LOSS, 2: ..., 7: ...} por jugada legal
    s.reward(pos, 4)            # r(e, c) ∈ {1.0, 0.5, 0.0}
    s.optimal_moves(pos)        # jugadas de recompensa máxima (puede haber varias)
    s.is_decidable(pos)         # ¿hay al menos dos clases de resultado entre las legales?
```

Inspección rápida desde la terminal: `uv run python -m c4solver 4453`.

## Detalles que importan

- **Semántica.** El resultado siempre es para el jugador que mueve. `move_outcomes` da, para cada
  jugada legal, el resultado que obtiene quien la juega. `outcome` es el máximo de esos.
- **Posiciones terminales.** Pons rechaza posiciones inválidas o ya terminadas sin escribir nada
  en stdout, lo que colgaría al proceso que lo lee. `Position` valida toda secuencia y `Solver`
  resuelve las terminales sin consultar al binario (quien "mueve" tras un cuatro en línea perdió;
  tablero lleno es empate).
- **Modo débil vs. fuerte.** `Solver(weak=True)` devuelve solo el signo fuera del libro de
  aperturas y es cerca de 2x más rápido. `Solver(weak=False)` devuelve el puntaje exacto de Pons
  (cuántas fichas quedan al definirse la partida). `scores()` expone el puntaje crudo por columna,
  con `-1000` en columnas llenas.
- **Costo.** Un proceso `c4solver` vivo por `Solver`, con caché en memoria (se vacía al superar
  `cache_size`). Fuera del libro una consulta cuesta del orden de milisegundos. No es compartible
  entre procesos: cada worker de multiprocessing crea su propio `Solver`.
- **Licencia.** El solver es AGPL v3 (`third_party/connect4/LICENSE`). En la tesina hay que
  citar versión (commit), forma de compilación y libro usado; este README y `setup.sh` son la
  fuente de esos datos.
