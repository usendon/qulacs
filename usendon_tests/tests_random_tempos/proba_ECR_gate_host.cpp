
#include <iostream>
#include <cppsim/state_gpu.hpp>
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

    // Estado inicial aleatorio
    QuantumStateGpu estado_inicial(nqubits);
    estado_inicial.set_Haar_random_state(2023);



    // Generador aleatorio y vector de tiempos  <-- añadir aquí
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(0, nqubits - 1);
    std::vector<double> tiempos;
    tiempos.reserve(N);

    for (int rep = 0; rep < N; rep++) {
        // Restaurar estado inicial antes de cada aplicación

        QuantumStateGpu estado_rep(nqubits);
        estado_rep.load(&estado_inicial);
        // Escoger qubits aleatorios
        int q1 = dist(rng);
        int q2;
        do { q2 = dist(rng); } while (q2 == q1);

        // Medir tiempo
        QuantumCircuit circuit(nqubits);
        circuit.add_ECR_gate(q1, q2);

        auto t_ini = std::chrono::high_resolution_clock::now();
        circuit.update_quantum_state(&estado_rep);
        auto t_fin = std::chrono::high_resolution_clock::now();

        double us = std::chrono::duration<double, std::micro>(t_fin - t_ini).count();
        tiempos.push_back(us);

        std::cout << "Rep " << rep << " | qubits (" << q1 << "," << q2
                  << ") | tiempo: " << us << " us" << std::endl;
    }

    // Media de tiempos
    double media = std::accumulate(tiempos.begin(), tiempos.end(), 0.0) / N;
    std::cout << "\n--- Media de tiempos (" << N << " repeticiones): "
              << media << " us ---" << std::endl;

    return 0;
}