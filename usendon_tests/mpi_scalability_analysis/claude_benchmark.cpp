#include <iostream>
#include <cstdlib>
#include <cmath>
#include <mpi.h>
#include <cppsim/state.hpp>
#include <cppsim/circuit.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/gate_merge.hpp>

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Uso: " << argv[0] << " nqubits q1 q2" << std::endl;
        return 1;
    }

    int nqubits = std::atoi(argv[1]);
    int qubit1  = std::atoi(argv[2]);
    int qubit2  = std::atoi(argv[3]);

    MPI_Init(&argc, &argv);
    int mpirank, mpisize;
    MPI_Comm_rank(MPI_COMM_WORLD, &mpirank);
    MPI_Comm_size(MPI_COMM_WORLD, &mpisize);

    // Número de qubits globales y frontera local/global
    int p = (mpisize > 1) ? (int)std::log2(mpisize) : 0;
    int m = nqubits - p; // frontera: qubits 0..m-1 son locales, m..n-1 son globales

    // Determinar tipo de par
    std::string tipo;
    bool q1_global = (qubit1 >= m);
    bool q2_global = (qubit2 >= m);
    if (!q1_global && !q2_global)      tipo = "LL";
    else if (q1_global && q2_global)   tipo = "GG";
    else                               tipo = "LG";

    const int N_RUNS = 6;
    double times[N_RUNS];

    for (int run = 0; run < N_RUNS; run++) {
        // Reinicializar estado en cada iteración
        QuantumState state(nqubits, 1);
        state.set_Haar_random_state(2023 + run);

        QuantumCircuit circuit(nqubits);
        circuit.add_ECR_gate(qubit1, qubit2);

        // Sincronizar todos los procesos antes de medir
        MPI_Barrier(MPI_COMM_WORLD);
        double t_start = MPI_Wtime();

        circuit.update_quantum_state(&state);

        MPI_Barrier(MPI_COMM_WORLD);
        double t_end = MPI_Wtime();

        times[run] = t_end - t_start;
    }

    // Solo rank 0 reporta; descarta la primera ejecución (warm-up)
    if (mpirank == 0) {
        double sum = 0.0;
        for (int i = 1; i < N_RUNS; i++) sum += times[i];
        double mean = sum / (N_RUNS - 1);

        // Calcular desviación estándar
        double sq_sum = 0.0;
        for (int i = 1; i < N_RUNS; i++) sq_sum += (times[i] - mean) * (times[i] - mean);
        double stddev = std::sqrt(sq_sum / (N_RUNS - 1));

        // Formato CSV: nqubits, nprocs, m, q1, q2, tipo, mean_time, stddev
        std::cout << nqubits << ","
                  << mpisize << ","
                  << m       << ","
                  << qubit1  << ","
                  << qubit2  << ","
                  << tipo    << ","
                  << mean    << ","
                  << stddev
                  << std::endl;
    }

    MPI_Finalize();
    return 0;
}