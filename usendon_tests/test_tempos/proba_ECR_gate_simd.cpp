
#include <iostream>
#include <cppsim/state.hpp>
#include <cppsim/circuit.hpp>
#include <cppsim/observable.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/gate_merge.hpp>

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Uso: " << argv[0] << " nqubits q1 q2" << std::endl;
        return 1;
    }

    int nqubits = std::atoi(argv[1]);
    int qubit1 = std::atoi(argv[2]);
    int qubit2 = std::atoi(argv[3]);
    int mpirank, mpisize;



    QuantumState state(nqubits); // use single cpu. Por defecto inicialízase ao |00...0>.
    state.set_Haar_random_state(2023); // para poñer como vector inicial un estado aleatorio de Haar.


    int dim = 1 << nqubits;      
    


    QuantumCircuit circuit(nqubits);
    circuit.add_ECR_gate(qubit1,qubit2);


    auto t_ini = std::chrono::high_resolution_clock::now();
    circuit.update_quantum_state(&state);
    auto t_fin = std::chrono::high_resolution_clock::now();

    double ns = std::chrono::duration<double, std::nano>(t_fin - t_ini).count();

    std::cout << std::fixed << ns << std::endl;
    
    return 0;
}
