#!/bin/bash
#SBATCH -p a64
#SBATCH --job-name=MPI
#SBATCH -o benchmark_a64/benchmark_%j.out
#SBATCH -e benchmark_a64/benchmark_%j.error
#SBATCH --time=22:00:00
#SBATCH -N 16     # <-- esto cambia: 1, 2, 4, 8, 16, 32, 64
#SBATCH -n 16       # <-- esto cambia igual que -N
#SBATCH --mem=28G     # usa toda la RAM disponible por nodo
#SBATCH --exclusive


date

echo "Nodos asignados: $SLURM_JOB_NUM_NODES"
echo "Tasks totales: $SLURM_NTASKS"
echo "Nodos: $SLURM_NODELIST"

module --force purge

source /etc/profile

ml gnu12/12.2.0  openmpi4/4.1.4 boost/1.80.0 cmake/3.24.2 

export OMP_NUM_THREADS=1
export OMP_PROC_BIND=true
export OMP_PLACES=cores
export I_MPI_DEBUG=0

cd ../..

set -eux

GCC_COMMAND=${C_COMPILER:-"mpicc"}
GXX_COMMAND=${CXX_COMPILER:-"mpicxx"}

USE_TEST=${USE_TEST:-"No"}
USE_GPU=${USE_GPU:-"No"}
USE_MPI=${USE_MPI:-"Yes"}
COVERAGE=${COVERAGE:-"No"}

CMAKE_OPS="-D CMAKE_C_COMPILER=$GCC_COMMAND -D CMAKE_CXX_COMPILER=$GXX_COMMAND -D CMAKE_BUILD_TYPE=Release"
CMAKE_OPS="${CMAKE_OPS} -D USE_MPI=${USE_MPI} -D USE_GPU=${USE_GPU}"
CMAKE_OPS="${CMAKE_OPS} -D USE_TEST=${USE_TEST} -D COVERAGE=${COVERAGE}"
CMAKE_OPS="${CMAKE_OPS} -DUSE_PYTHON=OFF \
-DBUILD_PYTHON=OFF \
-DENABLE_PYTHON=OFF \
-DCMAKE_DISABLE_FIND_PACKAGE_Python3=ON \
-DCMAKE_DISABLE_FIND_PACKAGE_PythonInterp=ON"

mkdir -p ./build_arm
cd ./build_arm
if [ "${QULACS_OPT_FLAGS:-"__UNSET__"}" = "__UNSET__" ]; then
  cmake -G "Unix Makefiles" ${CMAKE_OPS} ..
else
  cmake -G "Unix Makefiles" ${CMAKE_OPS} -D OPT_FLAGS="${QULACS_OPT_FLAGS}" ..
fi
make -j $(nproc)
cd ../



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

RESULTS="$WORKDIR/resultados_ecr_a64.csv"
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

    mpirun \
        --bind-to core \
        --map-by node \
        -np $nodos \
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