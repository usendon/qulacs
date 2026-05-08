
#include <iostream>
#include <cppsim/state_gpu.hpp>
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

    QuantumStateGpu state(nqubits);
    state.set_Haar_random_state(2023);
    CPPCTYPE* vec = state.duplicate_data_cpp();

    int dim = 1 << nqubits;      
    
    std::cout << "\n--- Vector inicial ---" << std::endl;
        for (size_t i = 0; i < dim; i++) {           
            std::cout << "I|" << i << "> : " << vec[i].real()
                          << " + " << vec[i].imag() << "i" << std::endl;
        }
    
    QuantumCircuit circuit(nqubits);
    circuit.add_ECR_gate(qubit1,qubit2);
    circuit.update_quantum_state(&state);

  
    // Imprimo o vector de estado final
    CPPCTYPE* ref_vec = state.duplicate_data_cpp();
    std::cout << "\n--- Vector de estado ---" << std::endl;
    for (size_t i = 0; i < dim; i++) {
        std::cout << "F|" << i << "> : " << ref_vec[i].real()
                    << " + " << ref_vec[i].imag() << "i" << std::endl;
    }
    
    return 0;
}
