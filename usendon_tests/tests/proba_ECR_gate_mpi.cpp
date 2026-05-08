
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
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &mpirank);
    MPI_Comm_size(MPI_COMM_WORLD, &mpisize);
	const UINT global_nqubits = (UINT)std::log2(mpisize); 

  
    QuantumState state(nqubits, 1); // use multi_cpu if possible
    state.set_Haar_random_state(2023);

    CPPCTYPE* vec = state.data_cpp();

    // Asignar un valor (por ejemplo 1 + 0i)
    /* if (mpirank == 0) {
        vec[0] = CPPCTYPE(1. / sqrt(2.), 1. / sqrt(2.));
    } */  

    ITYPE global_dim = 1 << nqubits;
    ITYPE local_dim = (1 << nqubits)/mpisize;    
    
    CPPCTYPE* ref_vec = state.data_cpp();

    // Para imprimir só os elementos distintos de cero do vector inicial
    /* for (size_t i = 0; i < local_dim; i++) {    
        if (vec[i].real() != 0 && vec[i].imag() != 0) {
            std::cout << "I|" << i + mpirank*local_dim << "> : " << vec[i].real() << " + " << vec[i].imag() << "i" << std::endl;
        }
    }  */ 

    QuantumCircuit circuit(nqubits);
    circuit.add_ECR_gate(qubit1, qubit2);
    circuit.update_quantum_state(&state);
    CPPCTYPE* local_vec = state.data_cpp();
        
    // Imprimo só as compoñentes distintas de cero do vector final
    /* std::cout << "------------------------------------------" << "\n";
    for (ITYPE i = 0; i < local_dim; i++) {    
        if (local_vec[i].real() != 0 && local_vec[i].imag() != 0) {
            std::cout << "F|" << i + (ITYPE)mpirank * local_dim << "> : " 
                    << local_vec[i].real() << " + " << local_vec[i].imag() << "i" << std::endl;
        }
    } */

    // Imprimo todo o vector final
    std::cout << "------------------------------------------" << "\n";
    for (size_t i = 0; i < local_dim; i++) {    
        std::cout << "F|" << i + mpirank*local_dim << "> : " << local_vec[i].real() << " + " << local_vec[i].imag() << "i" << std::endl;

    }   

    MPI_Finalize();
    return 0;
}
