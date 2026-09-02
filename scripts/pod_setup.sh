#!/usr/bin/env bash
# One-time setup on a RunPod pytorch pod (torch preinstalled system-wide). Run from the repo root.
set -euo pipefail
cd "$(dirname "$0")/.."
apt-get install -y -qq g++ make >/dev/null 2>&1 || true
[ -d third_party/connect4/.git ] || git clone -q https://github.com/PascalPons/connect4.git third_party/connect4
( cd third_party/connect4 && make -s c4solver )
[ -s third_party/connect4/7x6.book ] || curl -sL -o third_party/connect4/7x6.book https://github.com/PascalPons/connect4/releases/download/book/7x6.book
pip install -q numpy tqdm matplotlib pandas
python3 -c "import torch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
python3 -m c4.solver
