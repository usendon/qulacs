#!/bin/bash
#SBATCH -J CUDA            # Job name
#SBATCH -o cuda/cuda_%j.out
#SBATCH -e cuda/cuda_%j.error
##SBATCH --gres=gpu:a100:1   # Request 1 GPU of 2 available on an average A100 node
#SBATCH --gres=gpu:1 # cambio temporal para ver se entra antes
#SBATCH -p viz
#SBATCH -c 16             # Cores per task requested
#SBATCH --time=03:00:00       # Run time (hh:mm:ss) 
#SBATCH --mem-per-cpu=3G    # Memory per core demandes (96 GB = 3GB * 32 cores)
#SBATCH --exclusive

##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

date

module --force purge

ml cesga/2020 cuda/11.5.0 cmake/3.23.1

module load gompi/2020.4.1_hwl

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_gcc_with_gpu.sh

WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/tests_random_tempos
cd $WORKDIR


nvcc -ccbin mpicxx -O2 -std=c++17 -I /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include proba_ECR_gate_host.cpp -o proba_ECR_gate_host -L /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib -lgpusim_static -lvqcsim_static -lcppsim_static -lcsim_static     -lcudart -lcublas -Xcompiler -fopenmp -D_USE_GPU


NQUBITS=20
N_REPS=400     # <-- número de repeticiones que quieras

echo "=== ECR gate: $N_REPS repeticiones con qubits aleatorios ==="
./proba_ECR_gate_host $NQUBITS $N_REPS




