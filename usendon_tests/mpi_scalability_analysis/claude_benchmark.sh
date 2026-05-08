#!/bin/bash
#SBATCH --job-name=MPI
#SBATCH -o benchmark/benchmark_%j.out
#SBATCH -e benchmark/benchmark_%j.error
#SBATCH --time=22:00:00
#SBATCH -N 16     # <-- esto cambia: 1, 2, 4, 8, 16, 32, 64
#SBATCH -n 16       # <-- esto cambia igual que -N
#SBATCH --mem=1000G     # usa toda la RAM disponible por nodo
#SBATCH --exclusive

echo "Nodos asignados: $SLURM_JOB_NUM_NODES"
echo "Tasks totales: $SLURM_NTASKS"
echo "Nodos: $SLURM_NODELIST"

uptime

module --force purge
ml qmio/hpc gcc/12.3.0 gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

export OMP_PROC_BIND=true
export OMP_PLACES=cores
export I_MPI_DEBUG=0

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/
source script/build_mpicc.sh

WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/mpi_scalability_analysis
cd $WORKDIR

# compilación
mpicxx -O2 \
-I/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include \
-L/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib \
-Wl,-rpath,/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib \
claude_benchmark.cpp -o claude_benchmark \
-lcppsim_static -lcsim_static -lvqcsim_static \
-fopenmp -D_USE_MPI

RESULTS="$WORKDIR/resultados_ecr_borrado_openmp_externos.csv"
EXEC="$WORKDIR/claude_benchmark"

# Cabecera CSV
echo "nqubits,nprocs,m,q1,q2,tipo,mean_time_s,stddev_s" > $RESULTS

# ─────────────────────────────────────────────
# FUNCIÓN DE AYUDA
# Ejecuta el benchmark para un par (q1, q2) con N nodos
# Uso: run_benchmark <nodos> <nqubits> <q1> <q2>
# ─────────────────────────────────────────────
run_benchmark() {
    local nodos=$1
    local nqubits=$2
    local q1=$3
    local q2=$4

    srun --nodes=$nodos \
         --ntasks=$nodos \
         --ntasks-per-node=1 \
         $EXEC $nqubits $q1 $q2 >> $RESULTS
}

# ═════════════════════════════════════════════
# STRONG SCALING — n fijo = 30, variamos nodos
# La frontera m = nqubits - log2(nprocs) cambia
# con cada configuración de nodos
# ═════════════════════════════════════════════

echo "# === STRONG SCALING (n=30) ===" >> $RESULTS

# ── 1 nodo: m=30, todos los qubits son locales ──
# Solo caso LL posible
echo "# 1 nodo (m=30): solo LL" >> $RESULTS
run_benchmark 1 30  0  1     # LL: par más local

# ── 2 nodos: m=29, globales=[29] ──
# LL y LG posibles (GG no: solo 1 global)
echo "# 2 nodos (m=29): LL y LG" >> $RESULTS
run_benchmark 2 30  0  1     # LL
run_benchmark 2 30  0 29     # LG: más local con único global

# ── 4 nodos: m=28, globales=[28,29] ──
echo "# 4 nodos (m=28): LL, LG y GG" >> $RESULTS
run_benchmark 4 30  0  1     # LL
run_benchmark 4 30  0 28     # LG: más local con primer global
run_benchmark 4 30 28 29     # GG: únicos dos globales

# ── 8 nodos: m=27, globales=[27,28,29] ──
echo "# 8 nodos (m=27): LL, LG y GG" >> $RESULTS
run_benchmark 8 30  0  1     # LL
run_benchmark 8 30  0 27     # LG: más local con primer global
run_benchmark 8 30 27 28     # GG: primeros dos globales

# ── 16 nodos: m=26, globales=[26,27,28,29] ──
echo "# 16 nodos (m=26): LL, LG y GG" >> $RESULTS
run_benchmark 16 30  0  1    # LL
run_benchmark 16 30  0 26    # LG: más local con primer global
run_benchmark 16 30 26 27    # GG: primeros dos globales

# ═════════════════════════════════════════════
# WEAK SCALING — 30 qubits por proceso
# Aumentamos 1 qubit al doblar nodos
# La frontera m se mantiene siempre en 30
# ═════════════════════════════════════════════

echo "# === WEAK SCALING (30 qubits/proceso) ===" >> $RESULTS

# ── 1 nodo: n=30, m=30 ──
echo "# Weak: 1 nodo n=30 (m=30)" >> $RESULTS
run_benchmark 1 30  0  1

# ── 2 nodos: n=31, m=30, globales=[30] ──
echo "# Weak: 2 nodos n=31 (m=30)" >> $RESULTS
run_benchmark 2 31  0  1
run_benchmark 2 31  0 30    # LG

# ── 4 nodos: n=32, m=30, globales=[30,31] ──
echo "# Weak: 4 nodos n=32 (m=30)" >> $RESULTS
run_benchmark 4 32  0  1
run_benchmark 4 32  0 30    # LG
run_benchmark 4 32 30 31    # GG

# ── 8 nodos: n=33, m=30, globales=[30,31,32] ──
echo "# Weak: 8 nodos n=33 (m=30)" >> $RESULTS
run_benchmark 8 33  0  1
run_benchmark 8 33  0 30    # LG
run_benchmark 8 33 30 31    # GG

# ── 16 nodos: n=34, m=30, globales=[30,31,32,33] ──
echo "# Weak: 16 nodos n=34 (m=30)" >> $RESULTS
run_benchmark 16 34  0  1
run_benchmark 16 34  0 30   # LG
run_benchmark 16 34 30 31   # GG

echo "Benchmark completado. Resultados en $RESULTS"