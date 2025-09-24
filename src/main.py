from mpi4py import MPI
import time, math, os
from utils import monte_carlo_pi

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Parametrização via env vars (fácil de escalar no SLURM)
TOTAL_SAMPLES = int(os.getenv("TOTAL_SAMPLES", "10000000"))  # 1e7 padrão
SEED_BASE      = int(os.getenv("SEED_BASE", "42"))

# Divisão de trabalho
chunk = TOTAL_SAMPLES // size
rem   = TOTAL_SAMPLES %  size
local_n = chunk + (1 if rank < rem else 0)

t0 = time.time()
local_inside = monte_carlo_pi(local_n, SEED_BASE + rank)
# Redução: soma dos pontos dentro do círculo
total_inside = comm.reduce(local_inside, op=MPI.SUM, root=0)
# Redução: soma total de amostras
total_samples = comm.reduce(local_n, op=MPI.SUM, root=0)
t1 = time.time()

if rank == 0:
    pi_est = 4.0 * (total_inside / float(total_samples))
    print(f"[MPI] procs={size} samples={total_samples} pi={pi_est:.8f} time={t1-t0:.4f}s")
    # Log simples para results/
    os.makedirs("results", exist_ok=True)
    with open("results/run_log.csv", "a", encoding="utf-8") as f:
        f.write(f"{size},{total_samples},{pi_est:.10f},{t1-t0:.6f}\n")
