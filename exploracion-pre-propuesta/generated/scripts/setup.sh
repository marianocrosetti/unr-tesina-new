#!/usr/bin/env bash
# Idempotent setup: solver binary + opening book + python env.
# Works on macOS and on a fresh Ubuntu GPU box (needs: git, g++, make, curl, python3.11+).
set -euo pipefail
cd "$(dirname "$0")/.."

# 1. Pascal Pons' exact solver (AGPL) ----------------------------------------
if [ ! -d third_party/connect4/.git ]; then
  git clone -q https://github.com/PascalPons/connect4.git third_party/connect4
fi
( cd third_party/connect4 && make -s c4solver )
if [ ! -s third_party/connect4/7x6.book ]; then
  curl -sL -o third_party/connect4/7x6.book \
    https://github.com/PascalPons/connect4/releases/download/book/7x6.book
fi
printf '\n' | third_party/connect4/c4solver -a -b third_party/connect4/7x6.book 2>/dev/null | tail -1 \
  | grep -q -- "-2 -1 0 1 0 -1 -2" && echo "solver OK"

# 2. Python env (uv) -----------------------------------------------------------
if ! command -v uv >/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
uv sync -q
uv run python -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available(), 'mps', getattr(torch.backends,'mps',None) and torch.backends.mps.is_available())"
uv run python -m c4.solver
echo "setup done"
