#!/bin/bash
#SBATCH --job-name=OpenMP
#SBATCH -o benchmark/benchmark_%j.out
#SBATCH -e benchmark/benchmark_%j.error
#SBATCH --time=22:00:00

#SBATCH -N 1
#SBATCH -n 1

# pide suficientes CPUs para el máximo nº de threads
#SBATCH --cpus-per-task=64

#SBATCH --mem=1000G
#SBATCH --exclusive

echo "Nodo: $SLURM_NODELIST"
echo "CPUs disponibles: $SLURM_CPUS_PER_TASK"

uptime

module --force purge
ml qmio/hpc gcc/12.3.0 gcccore/12.3.0 impi/2021.13.0 \
   boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

export OMP_PROC_BIND=true
export OMP_PLACES=cores

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

RESULTS="$WORKDIR/resultados_openmp_scaling.csv"
EXEC="$WORKDIR/claude_benchmark"

echo "nqubits,threads,q1,q2,tipo,mean_time_s,stddev_s" > $RESULTS

# ─────────────────────────────────────────────
# FUNCIÓN
# Uso:
# run_openmp <threads> <nqubits> <q1> <q2>
# ─────────────────────────────────────────────

run_openmp() {

    local threads=$1
    local nqubits=$2
    local q1=$3
    local q2=$4

    export OMP_NUM_THREADS=$threads

    echo "===================================="
    echo "Threads: $threads"
    echo "===================================="

    srun --nodes=1 \
         --ntasks=1 \
         --cpus-per-task=$threads \
         $EXEC $nqubits $q1 $q2 >> $RESULTS
}

# ═════════════════════════════════════════════
# OPENMP SCALING
# ═════════════════════════════════════════════

echo "# === OPENMP SCALING ===" >> $RESULTS

NQUBITS=30

for t in 1 2 4 8 16 32 64
do
    echo "# Threads = $t" >> $RESULTS

    # LL
    run_openmp $t $NQUBITS 0 1

    # puedes añadir más casos:
    # run_openmp $t $NQUBITS 0 28
    # run_openmp $t $NQUBITS 28 29
done

echo "Benchmark completado."
echo "Resultados en $RESULTS"