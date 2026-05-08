#!/bin/bash
#SBATCH --job-name=ECR_desde_fora
#SBATCH -o ECR_desde_fora/ECR_desde_fora_%j.out
#SBATCH -e ECR_desde_fora/ECR_desde_fora_%j.error
#SBATCH --time=05-00:00:00
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem-per-cpu 64G
#SBATCH --exclusive 
##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

uptime

module --force purge

ml qmio/hpc gcc/12.3.0  gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_gcc.sh

WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/tests
cd $WORKDIR

g++ -O2 -I /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include -L /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib proba_ecr_desde_fora.cpp -o proba_ecr_desde_fora -lvqcsim_static -lcppsim_static -lcsim_static -fopenmp

EXECUTABLE="./proba_ecr_desde_fora"

NQUBITS=7

for ((i=3; i<4; i++)); do
    for ((j=6; j<7; j++)); do
        if [ $i -ne $j ]; then
            echo "=== ECR gate en qubits $i $j ==="
            $EXECUTABLE $NQUBITS $i $j 
        fi
    done
done
