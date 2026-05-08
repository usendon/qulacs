
#include <iostream>
#include <cppsim/state.hpp>
#include <cppsim/circuit.hpp>
#include <cppsim/observable.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/gate_merge.hpp>
#include <chrono>
#include <vector>
#include <random>
#include <numeric>


int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cerr << "Uso: " << argv[0] << " nqubits N_repeticiones" << std::endl;
        return 1;
    }

    int nqubits = std::atoi(argv[1]); 
    int N       = std::atoi(argv[2]);
    int dim     = 1 << nqubits;

    int mpirank, mpisize;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &mpirank);
    MPI_Comm_size(MPI_COMM_WORLD, &mpisize);

    // Estado inicial aleatorio
    QuantumState state(nqubits, 1); // use multi_cpu if possible
    state.set_Haar_random_state(2023);

    // Guardar copia del estado inicial
    QuantumState estado_inicial(nqubits, 1);
    estado_inicial.load(&state);

    // Generador aleatorio y vector de tiempos  <-- añadir aquí
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, nqubits - 1);
    std::vector<double> tiempos;
    tiempos.reserve(N);

    for (int rep = 0; rep < N; rep++) {
        QuantumState estado_rep(nqubits, 1);
        estado_rep.load(&estado_inicial);

        int q1 = dist(rng);
        int q2;
        do { q2 = dist(rng); } while (q2 == q1);

        QuantumCircuit circuit(nqubits);
        circuit.add_ECR_gate(q1, q2);

        MPI_Barrier(MPI_COMM_WORLD);  // sincronizar antes de medir
        double t_ini = MPI_Wtime();
        circuit.update_quantum_state(&estado_rep);
        double t_fin = MPI_Wtime();

        double us = (t_fin - t_ini) * 1e6;  // MPI_Wtime devuelve segundos

        if (mpirank == 0) {
            tiempos.push_back(us);
            std::cout << "Rep " << rep << " | qubits (" << q1 << "," << q2
                    << ") | tiempo: " << us << " us" << std::endl;
        }
    }

    if (mpirank == 0) {
        double media = std::accumulate(tiempos.begin(), tiempos.end(), 0.0) / N;
        std::cout << "\n--- Media de tiempos (" << N << " repeticiones): "
                << media << " us ---" << std::endl;
    }
    MPI_Finalize();
    return 0;
}