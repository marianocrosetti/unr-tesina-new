#!/usr/bin/env bash
# Helpers to run the experiment on a rented GPU box over SSH.
#   REMOTE=ubuntu@1.2.3.4 ./scripts/remote.sh push      # rsync code (no data/runs/.venv) to ~/chess
#   REMOTE=ubuntu@1.2.3.4 ./scripts/remote.sh setup     # build solver, book, uv env on the box
#   REMOTE=ubuntu@1.2.3.4 ./scripts/remote.sh grid      # start scripts/run_grid.sh inside tmux (survives disconnect)
#   REMOTE=ubuntu@1.2.3.4 ./scripts/remote.sh status    # tail the grid log
#   REMOTE=ubuntu@1.2.3.4 ./scripts/remote.sh pull      # fetch results/ and runs/*/log.jsonl + final.pt back
set -euo pipefail
cd "$(dirname "$0")/.."
: "${REMOTE:?set REMOTE=user@host}"
RDIR=${RDIR:-chess}
SSH="ssh -o StrictHostKeyChecking=accept-new $REMOTE"

case "${1:-}" in
  push)
    rsync -az --delete -e "ssh -o StrictHostKeyChecking=accept-new" \
      --exclude .venv --exclude data --exclude runs --exclude results --exclude third_party --exclude .git \
      ./ "$REMOTE:$RDIR/" ;;
  setup)
    $SSH "sudo apt-get install -y -qq g++ make tmux rsync >/dev/null 2>&1 || true; cd $RDIR && bash scripts/setup.sh" ;;
  grid)
    $SSH "cd $RDIR && tmux new-session -d -s grid \"env ${GRID_ENV:-} bash scripts/run_grid.sh > grid.log 2>&1\" && echo started" ;;
  status)
    $SSH "cd $RDIR && tail -n ${N:-30} grid.log; ls results/*/seed*/states.json 2>/dev/null | wc -l" ;;
  pull)
    mkdir -p results runs
    rsync -az -e "ssh -o StrictHostKeyChecking=accept-new" "$REMOTE:$RDIR/results/" results/
    rsync -az -e "ssh -o StrictHostKeyChecking=accept-new" --include '*/' --include 'log.jsonl' --include 'config.json' --include 'final.pt' --exclude '*' \
      "$REMOTE:$RDIR/runs/" runs/ ;;
  *) echo "usage: REMOTE=user@host $0 {push|setup|grid|status|pull}"; exit 1 ;;
esac
