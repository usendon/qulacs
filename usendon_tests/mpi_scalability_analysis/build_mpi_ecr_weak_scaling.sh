#!/bin/bash
#SBATCH --job-name=MPI
#SBATCH -o mpi_weak_scaling/mpi_weak_scaling_%j.out
#SBATCH -e mpi_weak_scaling/mpi_weak_scaling_%j.error
#SBATCH --time=00:30:00
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
proba_ECR_gate_mpi.cpp -o proba_ECR_gate_mpi \
-lcppsim_static -lcsim_static -lvqcsim_static \
-fopenmp -D_USE_MPI

EXECUTABLE="./proba_ECR_gate_mpi"

NQUBITS=34
N_REPS=10

echo "======================================"
echo "EJECUCIÓN MPI"
echo "Tasks SLURM: $SLURM_NTASKS"
echo "Qubits: $NQUBITS"
echo "Reps: $N_REPS"
echo "======================================"

srun --mpi=pmi2 -n $SLURM_NTASKS $EXECUTABLE $NQUBITS $N_REPS

