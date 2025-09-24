#!/usr/bin/env bash
set -e
# Rodadas para matriz de experimentos local
for p in 1 2 4 8; do
  TOTAL_SAMPLES=8000000 mpirun -np $p python3 -m mpi4py src/main.py
done
