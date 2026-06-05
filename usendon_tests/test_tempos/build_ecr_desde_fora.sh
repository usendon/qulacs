#!/bin/bash
#SBATCH --job-name=ecr_desde_fora
#SBATCH -o ecr_desde_fora/ecr_desde_fora_%j.out
#SBATCH -e ecr_desde_fora/ecr_desde_fora_%j.error
#SBATCH --time=03-00:00:00
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=1000G
#SBATCH --exclusive 
##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

date

module --force purge

ml qmio/hpc gcc/12.3.0  gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_gcc.sh

WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/test_tempos
cd $WORKDIR

g++ -O2 -I /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include -L /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib proba_ecr_desde_fora.cpp -o proba_ecr_desde_fora -lvqcsim_static -lcppsim_static -lcsim_static -fopenmp

EXECUTABLE="./proba_ecr_desde_fora"

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

