#!/bin/bash
#SBATCH --job-name=MPI
#SBATCH -o mpi_2_nodos/mpi_2_nodos_%j.out
#SBATCH -e mpi_2_nodos/mpi_2_nodos_%j.error
#SBATCH --time=06-00:00:00
#SBATCH -N 2
#SBATCH -n 4
#SBATCH --mem=1000G
#SBATCH --exclusive 
##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL


date

module --force purge

ml qmio/hpc gcc/12.3.0 gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_mpicc.sh


WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/tests_random_tempos
cd $WORKDIR


mpicxx -O2 -I/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include -L/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib -Wl,-rpath,../../../lib/ \
           proba_ECR_gate_mpi.cpp -o proba_ECR_gate_mpi \
           -lcppsim_static -lcsim_static -lvqcsim_static  \
           -fopenmp -D_USE_MPI   

EXECUTABLE="./proba_ECR_gate_mpi"

NQUBITS=20
N_REPS=400     # <-- número de repeticiones que quieras

echo "=== ECR gate: $N_REPS repeticiones con qubits aleatorios ==="
srun --mpi=pmix -n 4 $EXECUTABLE $NQUBITS $N_REPS

