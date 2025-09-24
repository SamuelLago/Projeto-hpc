#!/usr/bin/env bash
set -e
source .venv/bin/activate
export TOTAL_SAMPLES=${TOTAL_SAMPLES:-2000000}  # 2e6 p/ teste rápido
mpirun -np 4 python3 -m mpi4py src/main.py
