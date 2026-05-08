#!/bin/sh

ml load qmio/hpc gcc/12.3.0  gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/

source script/build_gcc.sh

cd /mnt/netapp1/Store_CESGA/home/cesga/usendon/qulacs_fork/qulacs/usendon_tests/tests

g++ -O2 -I ../../include -L ../../lib proba_dm_ECR_gate.cpp -o proba_dm -lvqcsim_static -lcppsim_static -lcsim_static -fopenmp -lmpi

./proba_dm

# Para executar este arquivo o que teño que facer é abrir un compute con:
# compute -c 4 (4 é o número de núcleos que quero)
# E despois executalo neste compute con:
# source build_dm_ecr.sh