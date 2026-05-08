#!/bin/bash
#SBATCH --job-name=MPI
#SBATCH -o benchmark/benchmark_%j.out
#SBATCH -e benchmark/benchmark_%j.error
#SBATCH --time=22:00:00
#SBATCH -N 16     
#SBATCH -n 16       
#SBATCH --mem=1000G     # usa toda la RAM disponible por nodo
#SBATCH --exclusive

echo "Nodos asignados: $SLURM_JOB_NUM_NODES"
echo "Tasks totales: $SLURM_NTASKS"
echo "Nodos: $SLURM_NODELIST"

uptime

module --force purge
ml qmio/hpc gcc/12.3.0 gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

export OMP_NUM_THREADS=1
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
    srun "$EXEC" $nqubits $q1 $q2 
}


# ═════════════════════════════════════════════
# STRONG SCALING — n fijo = 30, variamos nodos
# La frontera m = nqubits - log2(nprocs) cambia
# con cada configuración de nodos
# ═════════════════════════════════════════════

echo "# === STRONG SCALING (n=30) ===" >> $RESULTS

# ── 16 nodos: m=26, globales=[26,27,28,29] ──
echo "# 16 nodos (m=26): LL, LG y GG" >> $RESULTS
run_benchmark 16 30  0  1    # LL
run_benchmark 16 30  0 13    # LL
run_benchmark 16 30 24 25    # LL: límite local
run_benchmark 16 30  0 26    # LG: más local con primer global
run_benchmark 16 30 13 26    # LG: mitad local con primer global
run_benchmark 16 30 25 26    # LG: límite local con primer global
run_benchmark 16 30 25 29    # LG: límite local con último global
run_benchmark 16 30 26 27    # GG: primeros dos globales
run_benchmark 16 30 26 29    # GG: primer y último global
run_benchmark 16 30 28 29    # GG: últimos dos globales

# ═════════════════════════════════════════════
# WEAK SCALING — 30 qubits por proceso
# Aumentamos 1 qubit al doblar nodos
# La frontera m se mantiene siempre en 30
# ═════════════════════════════════════════════

echo "# === WEAK SCALING (30 qubits/proceso) ===" >> $RESULTS

# ── 16 nodos: n=34, m=30, globales=[30,31,32,33] ──
echo "# Weak: 16 nodos n=34 (m=30)" >> $RESULTS
run_benchmark 16 34  0  1
run_benchmark 16 34  0 15
run_benchmark 16 34 28 29   # LL
run_benchmark 16 34  0 30   # LG
run_benchmark 16 34 15 30   # LG
run_benchmark 16 34 29 30   # LG
run_benchmark 16 34 29 33   # LG
run_benchmark 16 34 30 31   # GG
run_benchmark 16 34 30 33   # GG
run_benchmark 16 34 32 33   # GG

echo "Benchmark completado. Resultados en $RESULTS"