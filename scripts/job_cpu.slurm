#!/bin/bash
#SBATCH --job-name=proj_montecarlo
#SBATCH --output=results/%x_%j.out
#SBATCH --error=results/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
# Ajuste módulos do SD aqui, ex.:
# module load python/3.10 openmpi
# source .venv/bin/activate

echo "Iniciando em $(date)"
export TOTAL_SAMPLES=${TOTAL_SAMPLES:-100000000}   # 1e8 p/ cluster
srun python3 -m mpi4py src/main.py
