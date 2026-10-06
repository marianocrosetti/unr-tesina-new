#!/usr/bin/env bash
# Descarga, compila y verifica el solver exacto de Connect 4 de Pascal Pons (AGPL v3).
#
# Deja todo en solver/third_party/connect4/ (gitignored):
#   - el código fuente clonado, fijado al commit $COMMIT
#   - el binario c4solver compilado
#   - el libro de aperturas 7x6.book (~33 MB), bajado de las releases del repo
#
# Es idempotente: se puede correr las veces que haga falta. Requiere: git, g++, make, curl.
# Por defecto clona por SSH; en una máquina sin claves usar: C4_REPO_URL=https://github.com/PascalPons/connect4.git ./setup.sh
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DIR="$HERE/third_party/connect4"
COMMIT="d6ba50d8aaf2308c769d9bf2abd42d90f34baf41"   # último commit de master al 2026-09 ("Add Solver::analyze")
REPO="${C4_REPO_URL:-git@github.com:PascalPons/connect4.git}"
BOOK_URL="https://github.com/PascalPons/connect4/releases/download/book/7x6.book"

for tool in git g++ make curl; do
  command -v "$tool" >/dev/null || { echo "setup.sh: falta '$tool' en el PATH" >&2; exit 1; }
done

# 1. Fuente -------------------------------------------------------------------
if [ ! -d "$DIR/.git" ]; then
  echo "[1/4] Clonando $REPO"
  git clone -q "$REPO" "$DIR"
else
  echo "[1/4] Fuente ya clonado"
fi
if [ "$(git -C "$DIR" rev-parse HEAD)" != "$COMMIT" ]; then
  git -C "$DIR" fetch -q origin
  git -C "$DIR" checkout -q "$COMMIT"
fi
echo "      commit: $(git -C "$DIR" rev-parse --short HEAD)"

# 2. Binario ------------------------------------------------------------------
echo "[2/4] Compilando c4solver"
make -s -C "$DIR" c4solver

# 3. Libro de aperturas -------------------------------------------------------
if [ ! -s "$DIR/7x6.book" ]; then
  echo "[3/4] Bajando 7x6.book"
  curl -fL --progress-bar -o "$DIR/7x6.book" "$BOOK_URL"
else
  echo "[3/4] Libro ya presente"
fi

# 4. Verificación -------------------------------------------------------------
# Posición vacía en modo fuerte: el primer jugador gana solo por la columna central.
expected="-2 -1 0 1 0 -1 -2"
got="$(printf '\n' | "$DIR/c4solver" -a -b "$DIR/7x6.book" 2>/dev/null | tail -1 | xargs)"
if [ "$got" = "$expected" ]; then
  echo "[4/4] Verificación OK: posición vacía -> $got"
else
  echo "[4/4] Verificación FALLÓ: esperaba '$expected', obtuve '$got'" >&2
  exit 1
fi
