#!/bin/bash
#SBATCH --job-name=simd
#SBATCH -o simd/simd_%j.out
#SBATCH -e simd/simd_%j.error
#SBATCH --time=06-00:00:00
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=1000G
#SBATCH --exclusive 
##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

uptime

module --force purge

ml qmio/hpc gcc/12.3.0 gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_gcc.sh


WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/tests
cd $WORKDIR

g++ -O2 -I/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include -L/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib -Wl,-rpath,../../../lib/ \
           proba_ECR_gate_simd.cpp -o proba_ECR_gate_simd \
           -lcppsim_static -lcsim_static -lvqcsim_static  \
           -fopenmp -D_USE_SIMD

           
EXECUTABLE="./proba_ECR_gate_simd"

NQUBITS=7


for ((i=0; i<1; i++)); do
    for ((j=6; j<7; j++)); do
        if [ $i -ne $j ]; then
            echo "=== ECR gate en qubits $i $j ==="
            srun $EXECUTABLE $NQUBITS $i $j 
        fi
    done
done



