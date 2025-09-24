Aqui está um **README.md** completinho (em PT-BR), pronto pra colar na raiz do projeto.

---

# Projeto HPC — Estimativa de π com Monte Carlo (MPI)

Monte Carlo paralelo para estimar π usando **mpi4py** (CPU/MPI).
Serve como baseline simples para medir **escalabilidade forte** e **fraca** em ambientes locais e em cluster (ex.: **Santos Dumont/SLURM**).

## 📂 Estrutura

```
projeto-hpc/
├─ README.md
├─ env/
│  └─ requirements.txt
├─ src/
│  ├─ main.py            # versão MPI (paralelo)
│  ├─ main_serial.py     # fallback sem MPI (serial)
│  └─ utils.py
├─ scripts/
│  ├─ build.sh           # setup (Linux/WSL/macOS)
│  ├─ run_local.sh       # roda local (MPI se houver, senão serial)
│  ├─ build_windows.bat  # setup (Windows)
│  ├─ run_local_windows.bat
│  ├─ run_serial_windows.bat
│  ├─ profile.sh         # matriz de testes local
│  └─ job_cpu.slurm      # submissão no SLURM (Santos Dumont)
├─ results/              # logs .out/.err e run_log.csv
└─ report/               # anexos e relatório
```

## ✅ Requisitos

* **Python 3.10+**
* **NumPy** e **mpi4py** (instalados pelos scripts)
* Para rodar MPI:

  * **Linux/WSL/macOS:** OpenMPI ou MPICH no PATH (`mpirun/mpiexec`)
  * **Windows:** Microsoft MPI (MS-MPI) no PATH (`mpiexec`)

> Se estiver no **Windows + Git Bash** e o comando `python` abrir a Microsoft Store, desative os *App execution aliases* (Configurações → Apps → *Aliases de execução do aplicativo* → desligue **python.exe** e **python3.exe**) e/ou instale Python do python.org marcando **Add to PATH**.

## 🚀 Como rodar

### Windows (rápido, sem MPI)

```bat
scripts\build_windows.bat
scripts\run_serial_windows.bat
```

Isso cria `.venv`, instala dependências e roda a versão **serial**.
Gera `results\run_log.csv` com `procs,total_samples,pi,time_sec`.

### Windows (com MPI)

Instale o **MS-MPI**, depois:

```bat
scripts\build_windows.bat
scripts\run_local_windows.bat
```

Roda com `mpiexec -n 4`.

### Linux/WSL/macOS

> Dica: se os `.sh` vierem com EOL do Windows, rode `dos2unix scripts/*.sh`.

```bash
bash scripts/build.sh
bash scripts/run_local.sh
```

O `run_local.sh` tenta usar MPI; se não achar `mpiexec`, roda a versão **serial**.

## ⚙️ Parâmetros

* `TOTAL_SAMPLES` (env var): número total de amostras (default: `1e7` local, `1e8` no SLURM).
* `SEED_BASE` (env var): base para semente (default: `42`).

Exemplo:

```bash
TOTAL_SAMPLES=50000000 bash scripts/run_local.sh
```

## 🧪 Experimentos sugeridos

### Escalabilidade forte (problema fixo)

* Fixe `TOTAL_SAMPLES = 1e8`
* Varie processos: `p ∈ {1,2,4,8,16,32}`
* Métricas: `tempo`, `speedup = T(1)/T(p)`, `eficiência = speedup/p`

### Escalabilidade fraca (trabalho por processo \~ constante)

* Fixe `samples_per_proc = 1e7`
* Rode com `TOTAL_SAMPLES = p * samples_per_proc`

**Coleta:** todos os runs gravam linha em `results/run_log.csv`:

```
procs,total_samples,pi,time_sec
```

## 🖥️ Execução no Santos Dumont (SLURM)

1. Ajuste módulos (exemplo):

   ```bash
   module load python/3.10 openmpi
   ```
2. Crie a venv e instale deps (uma vez por job dir):

   ```bash
   bash scripts/build.sh
   ```
3. Edite recursos em `scripts/job_cpu.slurm` (tempo, ntasks, mem).
4. Submeta:

   ```bash
   sbatch scripts/job_cpu.slurm
   ```
5. Acompanhe:

   ```bash
   squeue -u $USER
   tail -f results/*.out
   ```

> **Boas práticas SD:** use diretórios de trabalho apropriados (ex.: `/scratch`), evite cargas pesadas no nó de login, e mantenha logs na pasta `results/`.

## 🧩 Como funciona (resumo técnico)

* **Divisão de carga:** cada rank recebe `⌊N/p⌋` amostras; os primeiros `N mod p` recebem +1.
* **Cálculo local:** sorteia pontos (x,y) uniformes em `[0,1]²` e conta `x²+y² ≤ 1`.
* **Redução:** `MPI.Reduce` soma `inside` e `n_amostras`; rank 0 computa `π ≈ 4 * inside / total`.
* **Determinismo:** `seed = SEED_BASE + rank`.

## 🧰 Troubleshooting

* **`python3: command not found` no Git Bash (Windows):** edite scripts para usar fallback `python` / `py -3` (já preparado) e ative venv com `source .venv/Scripts/activate`.
* **`mpiexec: command not found`:** instale OpenMPI/MPICH (Linux/WSL) ou MS-MPI (Windows) ou rode a versão **serial** (`src/main_serial.py`).
* **Permissão/EOL em `.sh` no Windows:**
  `dos2unix scripts/*.sh && chmod +x scripts/*.sh`

## 📝 .gitignore sugerido

```
.venv/
__pycache__/
*.pyc
results/*.out
results/*.err
results/run_log.csv
.vscode/
.idea/
.DS_Store
Thumbs.db
```

## 📑 Licença

Este projeto é acadêmico/educacional. Adapte a licença conforme sua necessidade (MIT, BSD, etc.).

---

Se quiser, eu também preparo um **modelo de relatório** (Markdown/LaTeX) e um script para **plotar speedup/eficiência** a partir do `results/run_log.csv`.
