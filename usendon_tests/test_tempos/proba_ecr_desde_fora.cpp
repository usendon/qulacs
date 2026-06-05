#define _USE_MATH_DEFINES
#include <cmath>
#include <cppsim/state.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/gate_merge.hpp>
#include <cppsim/gate_matrix.hpp>
#include <cppsim/gate_general.hpp>
#include <cppsim/circuit.hpp>
#include <iostream>

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Uso: " << argv[0] << " nqubits q1 q2" << std::endl;
        return 1;
    }

    UINT nqubits = std::atoi(argv[1]);
    UINT qubit1 = std::atoi(argv[2]);
    UINT qubit2 = std::atoi(argv[3]);

    QuantumState state(nqubits); 
    //state.set_Haar_random_state(2023);
    int dim = 1 << nqubits;      

    QuantumCircuit circuit(nqubits);

    ComplexMatrix two_qubit_matrix(4,4);
    two_qubit_matrix <<
        0, 1, 0, 1.i,
        1, 0, -1.i, 0,
        0, 1.i, 0, 1,
        -1.i, 0, 1, 0;
    two_qubit_matrix /= sqrt(2.);

    auto two_qubit_gate = gate::DenseMatrix({qubit1,qubit2}, two_qubit_matrix);
    circuit.add_gate(two_qubit_gate);
    
    auto t_ini = std::chrono::high_resolution_clock::now();
    circuit.update_quantum_state(&state);
    auto t_fin = std::chrono::high_resolution_clock::now();

    double ns = std::chrono::duration<double, std::nano>(t_fin - t_ini).count();

    std::cout << std::fixed << ns << std::endl;
    

    return 0;
}
