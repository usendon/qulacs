#!/bin/bash
#SBATCH --job-name=test_gate
#SBATCH -o test_gate/test_gate_%j.out
#SBATCH -e test_gate/test_gate_%j.error
#SBATCH --time=1:00:00
#SBATCH -N 1
#SBATCH -n 4
#SBATCH --mem-per-cpu=64G
##SBATCH --mail-user=usendon@cesga.es
##SBATCH --mail-type=END,FAIL

uptime

module --force purge
ml qmio/hpc gcc/12.3.0 gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/
source script/build_gcc_with_memory_sanitizer.sh


WORKDIR=/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/tests
cd $WORKDIR

if [ ! -d googletest ]; then
    git clone https://github.com/google/googletest.git
    cd googletest
    mkdir build
    cd build
    cmake .. -DCMAKE_POSITION_INDEPENDENT_CODE=ON
    make
fi



# 3️⃣ Compilar tu test usando Google Test local
cd $WORKDIR

g++ -O2 -fsanitize=address -fno-omit-frame-pointer -I./googletest/googletest/include \
        -I/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/include \
        -L./googletest/build/lib \
        -L/mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/lib \
        -Wl,-rpath,../../../lib/ \
        /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/test/cppsim/test_gate.cpp \
        -o executable_test_gate -lcppsim_static -lcsim_static -lvqcsim_static -lgtest -lgtest_main -lpthread -fopenmp

# 4️⃣ Ejecutar el test
./executable_test_gate --gtest_filter=GateTest.ApplyTwoQubitGate
./executable_test_gate --gtest_filter=GateTest.DuplicateIndex


