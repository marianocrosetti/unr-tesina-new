# Expertos ciegos (`generated/cegueras`)

Infraestructura para construir expertos de Connect 4 que juegan óptimo en una **variante del juego donde
solo cuentan algunos tipos de línea** (V, H, D1 = `\`, D2 = `/`), y para medir si sirven como fuentes de
datos para experimentos de trascendencia. Las partidas se juegan siempre con las reglas reales.

## Archivos

- `build_variants.py`: compila un binario del solver de Pons por subconjunto de líneas (`build/<VHD1D2>/c4solver`).
  La única función tocada es `Position::compute_winning_position` (un `#if` por dirección).
- `experts.py`: `Expert(mask, p_blind, tiebreak)`, `play_game`, caché en disco (`cache/`) de posiciones resueltas.
  Máscara: V=1, H=2, D1=4, D2=8; 15 = juego real. `blind_name(11) == "sin_D1"`.
- `gen.py <nombre> <masks> <n> [workers] [kmin,kmax]`: partidas en paralelo (`data/<nombre>.jsonl`). Env `TIEBREAK`.
- `roundrobin.py <n> [workers]`: fuerza relativa. Env `TIEBREAK`, `KRANGE`, `RR_OUT`, `ONLY_VS`.
- `holding.py <roundrobin.json>`: tasa de conservación del valor teórico contra el óptimo.
- `states.py <games> <out> <max> [workers] [masks]`: estados decidibles + política de cada variante.
- `report.py <states> <tag> [games.jsonl ...] [rr.json] [tiebreak=uniform|center|hash|perm]`: tablas A–E.
- `sanity_windows.py <states>`: error 0 cuando no queda ventana viva del tipo ciego.
- `bench_variants.py`, `bench_depth.py`: tiempos de resolución sin libro.

## Reproducir

```bash
uv run python build_variants.py
TIEBREAK=hash uv run python gen.py mix4h 11,7,13,14 1500 6 6,8
uv run python states.py data/mix4h.jsonl data/states_mix4h.jsonl 3000 6 11,7,13,14,3
uv run python report.py data/states_mix4h.jsonl v2 data/mix4h.jsonl tiebreak=hash
```
