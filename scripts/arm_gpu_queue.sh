#!/usr/bin/env bash
# Waits for the data upload + any running generation to finish, then runs the GPU queue. Safe to re-run (one instance).
cd "$(dirname "$0")/.."
if [ -z "${FORCE:-}" ]; then
  pgrep -f "^bash scripts/gpu_queue.sh" >/dev/null && { echo "already running"; exit 0; }
  ps -eo args | grep -q "^arm_gpu_queue_wait" && { echo "already armed"; exit 0; }
fi
nohup bash -c 'exec -a arm_gpu_queue_wait bash -c "until [ \$(ls data/*.npz 2>/dev/null | grep -v _x4 | wc -l) -ge 26 ] && ! pgrep -x rsync >/dev/null && ! ps -eo args | grep -q \"^python3 -m c4.generate\"; do sleep 30; done; PY=python3 WORKERS=${WORKERS:-10} bash scripts/gpu_queue.sh"' > overnight/gpu_queue.log 2>&1 < /dev/null &
disown; echo "armed (WORKERS=${WORKERS:-10})"
