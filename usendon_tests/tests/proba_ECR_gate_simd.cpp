
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
    //state.set_Haar_random_state(2023); // para poñer como vector inicial un estado aleatorio de Haar.

    // Así podo especificar todos os elementos do vector inicial
    CPPCTYPE* vec = state.data_cpp();

    vec[0] = CPPCTYPE(-0.0239903 , 0.144622);
    vec[1] = CPPCTYPE(-0.00401427 , -0.0171282);
    vec[2] = CPPCTYPE(-0.0509344 , -0.0931894);
    vec[3] = CPPCTYPE(0.0942017 , 0.0334697);
    vec[4] = CPPCTYPE(0.00389566 , 0.0359732);
    vec[5] = CPPCTYPE(0.0317816 , 0.0237135);
    vec[6] = CPPCTYPE(-0.0761535 , 0.0282523);
    vec[7] = CPPCTYPE(-0.209643 , -0.0322976);
    vec[8] = CPPCTYPE(0.113173 , 0.0119846);
    vec[9] = CPPCTYPE(0.0573167 , -0.0457254);
    vec[10] = CPPCTYPE(0.126863 , 0.0424623);
    vec[11] = CPPCTYPE(0.10592 , -0.0468664);
    vec[12] = CPPCTYPE(0.141958 , -0.030211);
    vec[13] = CPPCTYPE(0.0642105 , 0.0287049);
    vec[14] = CPPCTYPE(-0.0539603 , -0.0407605);
    vec[15] = CPPCTYPE(-0.0814553 , -0.11139);
    vec[16] = CPPCTYPE(-0.129028 , -0.0108608);
    vec[17] = CPPCTYPE(-0.010776 , 0.0108481);
    vec[18] = CPPCTYPE(0.0507035 , -0.0279671);
    vec[19] = CPPCTYPE(0.111726 , 0.0762989);
    vec[20] = CPPCTYPE(-0.0424525 , -0.0595222);
    vec[21] = CPPCTYPE(0.0556081 , 0.0345132);
    vec[22] = CPPCTYPE(0.0206992 , 0.00899229);
    vec[23] = CPPCTYPE(0.134876 , 0.0203263);
    vec[24] = CPPCTYPE(-0.0281452 , -0.0314024);
    vec[25] = CPPCTYPE(-0.09522 , -0.0217526);
    vec[26] = CPPCTYPE(0.0217783 , 0.0542609);
    vec[27] = CPPCTYPE(-0.0786687 , 0.0100896);
    vec[28] = CPPCTYPE(0.0726186 , 0.0800035);
    vec[29] = CPPCTYPE(0.0169768 , -0.034094);
    vec[30] = CPPCTYPE(0.138159 , 0.0400033);
    vec[31] = CPPCTYPE(-0.0366473 , -0.0475544);
    vec[32] = CPPCTYPE(-0.0590559 , -0.0645557);
    vec[33] = CPPCTYPE(0.0868682 , 0.0178351);
    vec[34] = CPPCTYPE(-0.0289358 , -0.0471506);
    vec[35] = CPPCTYPE(-0.0472883 , -0.00227706);
    vec[36] = CPPCTYPE(0.0638405 , -0.119844);
    vec[37] = CPPCTYPE(-0.0162377 , -0.0790561);
    vec[38] = CPPCTYPE(0.0762699 , -0.00709372);
    vec[39] = CPPCTYPE(-0.0468353 , -0.050761);
    vec[40] = CPPCTYPE(0.0668368 , 0.0363636);
    vec[41] = CPPCTYPE(-0.00331747 , -0.0152093);
    vec[42] = CPPCTYPE(-0.022155 , 0.0170532);
    vec[43] = CPPCTYPE(0.0874242 , -0.0502526);
    vec[44] = CPPCTYPE(0.101514 , 0.067997);
    vec[45] = CPPCTYPE(-0.0361666 , 0.0248417);
    vec[46] = CPPCTYPE(-0.0296069 , -0.0241413);
    vec[47] = CPPCTYPE(-0.0274658 , -0.0264882);
    vec[48] = CPPCTYPE(-0.0448873 , 0.043009);
    vec[49] = CPPCTYPE(0.0540248 , -0.0330731);
    vec[50] = CPPCTYPE(0.0571312 , -0.00783799);
    vec[51] = CPPCTYPE(-0.025517 , -0.050137);
    vec[52] = CPPCTYPE(0.0123634 , -0.133242);
    vec[53] = CPPCTYPE(-0.088242 , -0.0672474);
    vec[54] = CPPCTYPE(-0.0766582 , 0.046552);
    vec[55] = CPPCTYPE(-0.08697 , 0.0262972);
    vec[56] = CPPCTYPE(0.110922 , 0.037186);
    vec[57] = CPPCTYPE(-0.0165145 , 0.0871179);
    vec[58] = CPPCTYPE(-0.09951 , -0.0734493);
    vec[59] = CPPCTYPE(0.0562272 , -0.0167369);
    vec[60] = CPPCTYPE(0.0309211 , -0.0636219);
    vec[61] = CPPCTYPE(-0.115497 , 0.0621198);
    vec[62] = CPPCTYPE(0.0423681 , -0.00467829);
    vec[63] = CPPCTYPE(0.0761215 , -0.0378748);
    vec[64] = CPPCTYPE(-0.0641262 , 0.0199242);
    vec[65] = CPPCTYPE(-0.0541151 , -0.00267501);
    vec[66] = CPPCTYPE(0.0436277 , 0.078372);
    vec[67] = CPPCTYPE(-0.104796 , 0.0612408);
    vec[68] = CPPCTYPE(-0.0923222 , 0.0698335);
    vec[69] = CPPCTYPE(-0.0295236 , 0.00467548);
    vec[70] = CPPCTYPE(-0.0651859 , -0.060538);
    vec[71] = CPPCTYPE(0.0564171 , -0.0765304);
    vec[72] = CPPCTYPE(0.0498052 , -0.203021);
    vec[73] = CPPCTYPE(0.0374912 , -0.0136563);
    vec[74] = CPPCTYPE(-0.0422553 , -0.00810695);
    vec[75] = CPPCTYPE(-0.00932414 , 0.000915806);
    vec[76] = CPPCTYPE(-0.0590152 , -0.0840712);
    vec[77] = CPPCTYPE(-0.0495172 , 0.0704125);
    vec[78] = CPPCTYPE(-0.0975659 , 0.0756314);
    vec[79] = CPPCTYPE(0.129424 , -0.104327);
    vec[80] = CPPCTYPE(0.0125445 , -0.0491555);
    vec[81] = CPPCTYPE(0.0570453 , -0.129286);
    vec[82] = CPPCTYPE(0.0531294 , -0.0119314);
    vec[83] = CPPCTYPE(-0.00400889 , 0.0105336);
    vec[84] = CPPCTYPE(-0.0698975 , 0.0583326);
    vec[85] = CPPCTYPE(-0.0259579 , -0.0470549);
    vec[86] = CPPCTYPE(-0.0735613 , -0.00195274);
    vec[87] = CPPCTYPE(-0.0114799 , 0.0206761);
    vec[88] = CPPCTYPE(-0.0140706 , -0.083835);
    vec[89] = CPPCTYPE(0.108014 , 0.0330946);
    vec[90] = CPPCTYPE(0.0345696 , 0.0354597);
    vec[91] = CPPCTYPE(0.0166945 , 0.0149269);
    vec[92] = CPPCTYPE(0.0772134 , -0.0207269);
    vec[93] = CPPCTYPE(0.0113856 , -0.0554246);
    vec[94] = CPPCTYPE(-0.0686969 , -0.0067513);
    vec[95] = CPPCTYPE(0.0128492 , 0.0749997);
    vec[96] = CPPCTYPE(0.0458814 , -0.0511303);
    vec[97] = CPPCTYPE(0.0436769 , -0.0653899);
    vec[98] = CPPCTYPE(-0.1108 , 0.00516352);
    vec[99] = CPPCTYPE(-0.0322901 , 0.0440148);
    vec[100] = CPPCTYPE(0.0654613 , 0.0453045);
    vec[101] = CPPCTYPE(0.068514 , 0.0455072);
    vec[102] = CPPCTYPE(-0.0722089 , -0.0573174);
    vec[103] = CPPCTYPE(-0.0530112 , 0.0454159);
    vec[104] = CPPCTYPE(0.0160013 , -0.0580065);
    vec[105] = CPPCTYPE(-0.00736293 , -0.0398361);
    vec[106] = CPPCTYPE(-0.0248993 , 0.0126353);
    vec[107] = CPPCTYPE(0.0541834 , -0.0543067);
    vec[108] = CPPCTYPE(-0.0169747 , -0.0270327);
    vec[109] = CPPCTYPE(0.117076 , 0.0722945);
    vec[110] = CPPCTYPE(-0.0197192 , 0.092428);
    vec[111] = CPPCTYPE(0.0459396 , 0.0465174);
    vec[112] = CPPCTYPE(0.0170933 , -0.0563172);
    vec[113] = CPPCTYPE(0.0356619 , 0.0339489);
    vec[114] = CPPCTYPE(0.0729558 , 0.0458179);
    vec[115] = CPPCTYPE(-0.0924216 , 0.0387678);
    vec[116] = CPPCTYPE(0.145186 , 0.0354272);
    vec[117] = CPPCTYPE(-0.0604164 , 0.0155511);
    vec[118] = CPPCTYPE(-0.00835696 , -0.0206924);
    vec[119] = CPPCTYPE(0.0033367 , -0.10328);
    vec[120] = CPPCTYPE(0.124349 , 0.0139058);
    vec[121] = CPPCTYPE(-0.0237065 , -0.0084021);
    vec[122] = CPPCTYPE(0.00281162 , -0.0255157);
    vec[123] = CPPCTYPE(-0.0383445 , -0.0373354);
    vec[124] = CPPCTYPE(0.060912 , -0.0250355);
    vec[125] = CPPCTYPE(0.0365664 , 0.0254484);
    vec[126] = CPPCTYPE(-0.0768532 , 0.0333156);
    vec[127] = CPPCTYPE(-0.043443 , 0.0530398);


    int dim = 1 << nqubits;      
    
    std::cout << "\n--- Vector inicial ---" << std::endl;
        for (size_t i = 0; i < dim; i++) {           
            std::cout << "I|" << i << "> : " << vec[i].real()
                          << " + " << vec[i].imag() << "i" << std::endl;
        }
    

    QuantumCircuit circuit(nqubits);
    circuit.add_ECR_gate(qubit1,qubit2);

    circuit.update_quantum_state(&state);

    int local_dim = dim / mpisize;  // amplitudes por rank
  
    // Imprimo o vector de estado final
    CPPCTYPE* ref_vec = state.data_cpp();
    std::cout << "\n--- Vector de estado (single cpu) ---" << std::endl;
    for (size_t i = 0; i < dim; i++) {
        std::cout << "F|" << i << "> : " << ref_vec[i].real()
                    << " + " << ref_vec[i].imag() << "i" << std::endl;
    }
    
    return 0;
}
