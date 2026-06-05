#!/bin/bash
#SBATCH -J CUDA            # Job name
#SBATCH -o cuda/cuda_%j.out
#SBATCH -e cuda/cuda_%j.error
#SBATCH --gres=gpu:a100:1   # Request 1 GPU of 2 available on an average A100 node
#SBATCH -c 32           # Cores per task requested
#SBATCH --time=04:00:00       # Run time (hh:mm:ss) 
#SBATCH --mem=24G    # Memory per core demandes (96 GB = 3GB * 32 cores)
#SBATCH --exclusive

##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

date

echo "a100"

module --force purge

ml cesga/2020 cuda/11.5.0 cmake/3.23.1

module load gompi/2020.4.1_hwl

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_gcc_with_gpu.sh
echo "Exit code del build: $?"

WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/test_tempos
cd $WORKDIR


nvcc -ccbin mpicxx -O2 -std=c++17 -I /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include proba_ECR_gate_host.cpp -o proba_ECR_gate_host -L /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib -lgpusim_static -lvqcsim_static -lcppsim_static -lcsim_static     -lcudart -lcublas -Xcompiler -fopenmp -D_USE_GPU

EXECUTABLE="./proba_ECR_gate_host"

NQUBITS=20

TOTAL=0
COUNT=0

for ((i=0; i<NQUBITS; i++)); do
    for ((j=0; j<NQUBITS; j++)); do
        if [ $i -ne $j ]; then
            echo "=== ECR gate en qubits $i $j ==="

            out=$($EXECUTABLE $NQUBITS $i $j)

            t=$out   # ya es el número directamente

            echo "tiempo = $t"

            TOTAL=$(echo "$TOTAL + $t" | bc)
            COUNT=$((COUNT + 1))
 
        fi
    done
done

MEDIA=$(echo "scale=6; $TOTAL / $COUNT" | bc)

echo "=============================="
echo "MEDIA FINAL: $MEDIA ns"
echo "=============================="

