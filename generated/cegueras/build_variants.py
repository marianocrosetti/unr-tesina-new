"""Compila una variante del solver de Pons por cada subconjunto de tipos de línea que cuentan.

Máscara de bits C4_LINES: V=1, H=2, D1=4 (diagonal \\, col+1 fila-1), D2=8 (diagonal /, col+1 fila+1). 15 = juego real.
La única función que define qué es "ganar" en el solver es Position::compute_winning_position;
se la envuelve en #if por dirección. Todo lo demás (negamax, orden de jugadas, TT) queda igual.
"""
import re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[1] / "solver" / "third_party" / "connect4"
BUILD = HERE / "build"
NAMES = {1: "V", 2: "H", 4: "D1", 8: "D2"}

def variant_name(mask):
    return "".join(n for b, n in NAMES.items() if mask & b) or "none"

def patch(text):
    def guard(block_comment, bit):
        # envuelve desde el comentario de la dirección hasta la línea en blanco siguiente
        pat = re.compile(r"(\n    //\s*" + block_comment + r"[^\n]*\n)(.*?)(\n\n)", re.S)
        m = pat.search(text)
        assert m, block_comment
        return text[:m.start()] + f"\n#if C4_LINES & {bit}" + m.group(1) + m.group(2) + "\n#endif" + m.group(3) + text[m.end():]
    text = text.replace("position_t r = (position << 1) & (position << 2) & (position << 3);",
                        "position_t r = 0, p = 0; (void)p;\n#if C4_LINES & 1\n    r = (position << 1) & (position << 2) & (position << 3);\n#endif")
    text = text.replace("    position_t p = (position << (HEIGHT + 1))", "    p = (position << (HEIGHT + 1))")
    text = guard("horizontal", 2)
    text = guard("diagonal 1", 4)
    text = guard("diagonal 2", 8)
    assert "#ifndef C4_LINES" not in text
    text = text.replace("namespace GameSolver {", "#ifndef C4_LINES\n#define C4_LINES 15\n#endif\nnamespace GameSolver {", 1)
    return text

def build(mask):
    name = variant_name(mask)
    d = BUILD / name
    d.mkdir(parents=True, exist_ok=True)
    for f in ["Solver.cpp", "Solver.hpp", "MoveSorter.hpp", "OpeningBook.hpp", "TranspositionTable.hpp", "main.cpp"]:
        shutil.copy(SRC / f, d / f)
    (d / "Position.hpp").write_text(patch((SRC / "Position.hpp").read_text()))
    cmd = ["g++", "--std=c++11", "-O3", "-DNDEBUG", f"-DC4_LINES={mask}", "-o", str(d / "c4solver"), str(d / "main.cpp"), str(d / "Solver.cpp")]
    subprocess.run(cmd, check=True)
    return name

if __name__ == "__main__":
    masks = [int(m) for m in sys.argv[1:]] or list(range(1, 16))
    for m in masks:
        print(f"mask {m:2d} -> {build(m)}")
