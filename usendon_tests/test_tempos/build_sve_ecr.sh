#!/bin/bash
#SBATCH -p a64
#SBATCH --job-name=SVE
#SBATCH -o sve/sve_%j.out
#SBATCH -e sve/sve_%j.error
#SBATCH --time=03-00:00:00
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=3G
#SBATCH --exclusive 
##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

date

module --force purge

source /etc/profile

ml gnu12/12.2.0  openmpi4/4.1.4 boost/1.80.0 cmake/3.24.2 

cd ../..

set -eux

GCC_COMMAND=${C_COMPILER:-"gcc"}
GXX_COMMAND=${CXX_COMPILER:-"g++"}

USE_TEST=${USE_TEST:-"No"}
USE_GPU=${USE_GPU:-"No"}
USE_MPI=${USE_MPI:-"No"}
COVERAGE=${COVERAGE:-"No"}

CMAKE_OPS="-D CMAKE_C_COMPILER=$GCC_COMMAND -D CMAKE_CXX_COMPILER=$GXX_COMMAND -D CMAKE_BUILD_TYPE=Release"
CMAKE_OPS="${CMAKE_OPS} -D USE_MPI=${USE_MPI} -D USE_GPU=${USE_GPU}"
CMAKE_OPS="${CMAKE_OPS} -D USE_TEST=${USE_TEST} -D COVERAGE=${COVERAGE}"
CMAKE_OPS="${CMAKE_OPS} -D USE_PYTHON=OFF"

mkdir -p ./build_arm
cd ./build_arm
if [ "${QULACS_OPT_FLAGS:-"__UNSET__"}" = "__UNSET__" ]; then
  cmake -G "Unix Makefiles" ${CMAKE_OPS} ..
else
  cmake -G "Unix Makefiles" ${CMAKE_OPS} -D OPT_FLAGS="${QULACS_OPT_FLAGS}" ..
fi
make -j $(nproc)
cd ../

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/test_tempos

g++ -O2 -I../../include -I/opt/cesga/qmio/hpc/software/Compiler/gcccore/12.3.0/nlohmann_json/3.11.3/include/ -L../../lib  proba_ECR_gate_sve.cpp -o proba_ECR_gate_sve -lvqcsim_static -lcppsim_static -lcsim_static -fopenmp -D_USE_SVE  -Wl,-rpath,/opt/cesga/qmio/hpc/software/Compiler/gcccore/12.3.0/nlohmann_json/3.11.3/include/

EXECUTABLE="./proba_ECR_gate_sve"

NQUBITS=20


TOTAL=0
COUNT=0

for ((i=2; i<NQUBITS; i++)); do
    for ((j=2; j<NQUBITS; j++)); do
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

echo "Número de medidas: $COUNT" 

echo "=============================="
echo "MEDIA FINAL: $MEDIA ns"
echo "=============================="

