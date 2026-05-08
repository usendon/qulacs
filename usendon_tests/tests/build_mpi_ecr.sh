#!/bin/bash
#SBATCH --job-name=MPI
#SBATCH -o mpi/mpi_1_nodo_%j.out
#SBATCH -e mpi/mpi_1_nodo_%j.error
#SBATCH --time=06-00:00:00
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem=1000G
#SBATCH --exclusive 
##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

uptime

module --force purge

ml qmio/hpc gcc/12.3.0 gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_mpicc.sh

WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/tests
cd $WORKDIR

mpicxx -O2 -I/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include -L/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib -Wl,-rpath,../../../lib/ \
           proba_ECR_gate_mpi.cpp -o proba_ECR_gate_mpi \
           -lcppsim_static -lcsim_static -lvqcsim_static  \
           -fopenmp -D_USE_MPI   

EXECUTABLE="./proba_ECR_gate_mpi"

NQUBITS=7

for ((i=0; i<1; i++)); do
    for ((j=6; j<7; j++)); do
        if [ $i -ne $j ]; then
            echo "=== ECR gate en qubits $i $j ==="
            srun --mpi=pmix $EXECUTABLE $NQUBITS $i $j 

        fi
    done
done




#mpicxx -O2 -o benchmark_ecr claude_benchmark.cpp -I/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include -L/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib -lcppsim_static -lcsim_static -lvqcsim_static -fopenmp -D_USE_MPI  