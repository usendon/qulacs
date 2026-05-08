#include <iostream>
#include <cppsim/state.hpp>
#include <cppsim/circuit.hpp>
#include <cppsim/observable.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/gate_merge.hpp>
#include <vector>
#include <random>
#include <cmath>
#include <mpi.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cerr << "Uso: " << argv[0] << " nqubits N_repeticiones" << std::endl;
        return 1;
    }
    int nqubits = std::atoi(argv[1]); 
    int N       = std::atoi(argv[2]);

    MPI_Init(&argc, &argv);
    int mpirank, mpisize;
    MPI_Comm_rank(MPI_COMM_WORLD, &mpirank);
    MPI_Comm_size(MPI_COMM_WORLD, &mpisize);

    int use_mpi = (mpisize > 1) ? 1 : 0;

    if (mpirank == 0) { printf(">>> Creando state\n"); fflush(stdout); }
    QuantumState estado(nqubits, use_mpi);

    //if (mpirank == 0) { printf(">>> Llamando set_Haar_random_state\n"); fflush(stdout); }
    //estado.set_Haar_random_state(2023);

    // RNG con mismo seed en todos los procesos → mismos qubits en cada rep
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, nqubits - 1);

    if (mpirank == 0) { printf(">>> Entrando al loop\n"); fflush(stdout); }

    MPI_Barrier(MPI_COMM_WORLD);
    double t_ini = MPI_Wtime();

    for (int rep = 0; rep < N; rep++) {
        int q1 = dist(rng);
        int q2;
        do { q2 = dist(rng); } while (q2 == q1);

        QuantumCircuit circuit(nqubits);
        circuit.add_ECR_gate(q1, q2);
        circuit.update_quantum_state(&estado);

        if (mpirank == 0 && rep % 2 == 0) {
            printf(">>> rep %d completada\n", rep);
            fflush(stdout);
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double t_fin = MPI_Wtime();

    double tiempo_local  = t_fin - t_ini;
    double tiempo_global = 0.0;
    MPI_Reduce(&tiempo_local, &tiempo_global, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    if (mpirank == 0) {
        std::cout << mpisize << " " << tiempo_global << std::endl;
    }

    MPI_Finalize();
    return 0;
}