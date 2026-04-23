

#include <cstring>
#include <bitset>
#include <complex>
#include <iostream>
#include <vector>
using namespace std::complex_literals;
#include <algorithm>


#include "MPIutil.hpp"
#include "constant.hpp"
#include "update_ops.hpp"
#include "utility.hpp"
#include "csim/type.hpp"
#ifdef _OPENMP
#include <omp.h>
#endif

#ifdef _USE_SIMD
#ifdef _MSC_VER
#include <intrin.h>
#else
#include <x86intrin.h>
#endif
#endif


void ECR_gate(UINT target_qubit_index_0, UINT target_qubit_index_1,
    CTYPE* state, ITYPE dim) {
#ifdef _OPENMP
    OMPutil::get_inst().set_qulacs_num_threads(dim, 13);
#endif

#ifdef _USE_SIMD
    ECR_gate_parallel_simd(
        target_qubit_index_0, target_qubit_index_1, state, dim);
#elif defined(_USE_SVE)
    ECR_gate_parallel_sve(
        target_qubit_index_0, target_qubit_index_1, state, dim);
#else
    ECR_gate_parallel_unroll(
        target_qubit_index_0, target_qubit_index_1, state, dim);
#endif

#ifdef _OPENMP
    OMPutil::get_inst().reset_qulacs_num_threads();
#endif
}


void ECR_gate_parallel_unroll(UINT target_qubit_index_0,
    UINT target_qubit_index_1, CTYPE* state, ITYPE dim) {
    const ITYPE loop_dim = dim / 4;

    const ITYPE mask_0 = 1ULL << target_qubit_index_0;
    const ITYPE mask_1 = 1ULL << target_qubit_index_1;
    const ITYPE mask = mask_0 + mask_1;

    const UINT min_qubit_index =
        get_min_ui(target_qubit_index_0, target_qubit_index_1);
    const UINT max_qubit_index =
        get_max_ui(target_qubit_index_0, target_qubit_index_1);
    const ITYPE min_qubit_mask = 1ULL << min_qubit_index;
    const ITYPE max_qubit_mask = 1ULL << (max_qubit_index - 1);
    const ITYPE low_mask = min_qubit_mask - 1;
    const ITYPE mid_mask = (max_qubit_mask - 1) ^ low_mask;
    const ITYPE high_mask = ~(max_qubit_mask - 1);

    const double sqrt2inv = 1. / sqrt(2.);


#ifdef _OPENMP
#pragma omp parallel for
#endif
    for (ITYPE state_index = 0; state_index < loop_dim; ++state_index) {
        ITYPE basis_index_00 = (state_index & low_mask) +
                               ((state_index & mid_mask) << 1) +
                               ((state_index & high_mask) << 2);
        ITYPE basis_index_01 = basis_index_00 + mask_0;
        ITYPE basis_index_10 = basis_index_00 + mask_1;
        ITYPE basis_index_11 = basis_index_00 + mask;

        CTYPE v00 = state[basis_index_00];
        CTYPE v01 = state[basis_index_01];
        CTYPE v10 = state[basis_index_10];
        CTYPE v11 = state[basis_index_11];

        CTYPE new_v00 = sqrt2inv * (v01 + 1.i * v11);
        CTYPE new_v01 = sqrt2inv * (v00 - 1.i * v10);
        CTYPE new_v10 = sqrt2inv * (v11 + 1.i * v01);
        CTYPE new_v11 = sqrt2inv * (v10 - 1.i * v00);

        state[basis_index_00] = new_v00;
        state[basis_index_01] = new_v01;
        state[basis_index_10] = new_v10;
        state[basis_index_11] = new_v11;
    }

} 

#ifdef _USE_SIMD
void ECR_gate_parallel_simd(UINT target_qubit_index_0,
    UINT target_qubit_index_1, CTYPE* state, ITYPE dim) {
    const ITYPE loop_dim = dim / 4;

    const ITYPE mask_0 = 1ULL << target_qubit_index_0;
    const ITYPE mask_1 = 1ULL << target_qubit_index_1;
    const ITYPE mask = mask_0 + mask_1;

    const UINT min_qubit_index =
        get_min_ui(target_qubit_index_0, target_qubit_index_1);
    const UINT max_qubit_index =
        get_max_ui(target_qubit_index_0, target_qubit_index_1);
    const ITYPE min_qubit_mask = 1ULL << min_qubit_index;
    const ITYPE max_qubit_mask = 1ULL << (max_qubit_index - 1);
    const ITYPE low_mask = min_qubit_mask - 1;
    const ITYPE mid_mask = (max_qubit_mask - 1) ^ low_mask;
    const ITYPE high_mask = ~(max_qubit_mask - 1);
    const double sqrt2inv = 1. / sqrt(2.);

    if (min_qubit_index == 0) {
        ECR_gate_parallel_unroll(target_qubit_index_0,
    target_qubit_index_1, state, dim);
    } else {
    #ifdef _OPENMP
    #pragma omp parallel for
    #endif
        for (ITYPE state_index = 0; state_index < loop_dim; state_index+=2) {
            ITYPE basis_index_00 = (state_index & low_mask) +
                                ((state_index & mid_mask) << 1) +
                                ((state_index & high_mask) << 2);
            ITYPE basis_index_01 = basis_index_00 + mask_0;
            ITYPE basis_index_10 = basis_index_00 + mask_1;
            ITYPE basis_index_11 = basis_index_00 + mask;

            double* ptr00 = (double*)(state + basis_index_00);
            double* ptr01 = (double*)(state + basis_index_01);
            double* ptr10 = (double*)(state + basis_index_10);
            double* ptr11 = (double*)(state + basis_index_11);

            __m256d a_lo = _mm256_loadu_pd(ptr00); 
            __m256d a_hi = _mm256_loadu_pd(ptr01); 
            __m256d b_lo = _mm256_loadu_pd(ptr10); 
            __m256d b_hi = _mm256_loadu_pd(ptr11); 

            auto mul_by_i_256 = [](const __m256d& x) -> __m256d {
                __m256d swapped = _mm256_permute_pd(x, 0b0101); // swap Re <-> Im
                const __m256d sign = _mm256_set_pd(1.0, -1.0, 1.0, -1.0);
                return _mm256_mul_pd(swapped, sign);
            };

            __m256d i_b_hi = mul_by_i_256(b_hi);
            __m256d i_b_lo = mul_by_i_256(b_lo);
            __m256d i_a_hi = mul_by_i_256(a_hi);
            __m256d i_a_lo = mul_by_i_256(a_lo);

            __m256d tmp_new_v00 = _mm256_add_pd(a_hi, i_b_hi);
            __m256d tmp_new_v01 = _mm256_sub_pd(a_lo, i_b_lo);
            __m256d tmp_new_v10 = _mm256_add_pd(b_hi, i_a_hi);
            __m256d tmp_new_v11 = _mm256_sub_pd(b_lo, i_a_lo);

            __m256d svec = _mm256_set1_pd(sqrt2inv);
            tmp_new_v00 = _mm256_mul_pd(tmp_new_v00, svec);
            tmp_new_v01 = _mm256_mul_pd(tmp_new_v01, svec);
            tmp_new_v10 = _mm256_mul_pd(tmp_new_v10, svec);
            tmp_new_v11 = _mm256_mul_pd(tmp_new_v11, svec);

            _mm256_storeu_pd(ptr00, tmp_new_v00); 
            _mm256_storeu_pd(ptr01, tmp_new_v01); 
            _mm256_storeu_pd(ptr10, tmp_new_v10); 
            _mm256_storeu_pd(ptr11, tmp_new_v11); 
        }
    }
} 
#endif


#ifdef _USE_SVE

/////////////////////

#include <inttypes.h>  // para PRIu64 (portable)

static void print_svuint64(svuint64_t v) {
    uint64_t tmp[svcntd()];                // buffer temporal
    svst1(svptrue_b64(), tmp, v);          // volcar a memoria

    int n = svcntd();
    for (int i = 0; i < n; i++) {
        printf("%" PRIu64 " ", tmp[i]);    // impresión portable
    }
    printf("\n");
}

////////////////////

static inline svfloat64_t mul_by_i(svbool_t pg, svfloat64_t x) {
    svuint64_t tbl_idx = svindex_u64(0, 1);   
    std::cout << "tbl_idx" << std::endl;
    print_svuint64(tbl_idx);
    tbl_idx = sveor_z(pg, tbl_idx, svdup_u64(1));
    std::cout << "tbl_idx con OR bit a bit" << std::endl;
    print_svuint64(tbl_idx);

    svfloat64_t swapped = svtbl_f64(x, tbl_idx);

    svbool_t odd = svcmpne(pg, svand_z(pg, tbl_idx, svdup_u64(1)), svdup_u64(0));
    std::cout << "tbl_idx con AND" << std::endl;
    print_svuint64(svand_z(pg, tbl_idx, svdup_u64(1)));

    svfloat64_t sign = svsel(odd, svdup_f64(-1.0), svdup_f64(1.0));

    return svmul_x(pg, swapped, sign);
}

//////////////////////////

static void print_svfloat64(svfloat64_t v) {
    double tmp[svcntd()];              // tamaño dinámico del vector
    svst1(svptrue_b64(), tmp, v);      // copiar a memoria

    int n = svcntd();
    for (int i = 0; i < n; i++) {
        printf("%f ", tmp[i]);
    }
    printf("\n");
}

/////////////////////////


void ECR_gate_parallel_sve(UINT target_qubit_index_0,
                           UINT target_qubit_index_1,
                           CTYPE* state, ITYPE dim) {
    const ITYPE loop_dim = dim / 4;
    const ITYPE mask_0 = 1ULL << target_qubit_index_0;
    const ITYPE mask_1 = 1ULL << target_qubit_index_1;
    const ITYPE mask = mask_0 + mask_1;

    const UINT min_qubit_index = get_min_ui(target_qubit_index_0, target_qubit_index_1);
    const UINT max_qubit_index = get_max_ui(target_qubit_index_0, target_qubit_index_1);

    const ITYPE min_qubit_mask = 1ULL << min_qubit_index;
    const ITYPE max_qubit_mask = 1ULL << (max_qubit_index - 1);
    const ITYPE low_mask  = min_qubit_mask - 1;
    const ITYPE mid_mask  = (max_qubit_mask - 1) ^ low_mask;
    const ITYPE high_mask = ~(max_qubit_mask - 1);
    const double sqrt2inv = 1. / sqrt(2.);

    // # of complex128 numbers in an SVE register
    ITYPE VL = svcntd() / 2;


    if ((dim > VL) && (min_qubit_mask >= VL)) {

    #ifdef _OPENMP
    #pragma omp parallel for
    #endif
        for (ITYPE state_index = 0; state_index < loop_dim; state_index+=VL) {

            ITYPE basis_index_00 = (state_index & low_mask) +
                                ((state_index & mid_mask) << 1) +
                                ((state_index & high_mask) << 2);
            ITYPE basis_index_01 = basis_index_00 + mask_0;
            ITYPE basis_index_10 = basis_index_00 + mask_1;
            ITYPE basis_index_11 = basis_index_00 + mask;


            svfloat64_t input00 = svld1(svptrue_b64(), (double*)&state[basis_index_00]);
            std::cout << "input00" << std::endl;
            print_svfloat64(input00);
            svfloat64_t input01 = svld1(svptrue_b64(), (double*)&state[basis_index_01]);
            svfloat64_t input10 = svld1(svptrue_b64(), (double*)&state[basis_index_10]);
            svfloat64_t input11 = svld1(svptrue_b64(), (double*)&state[basis_index_11]);


            svfloat64_t i_00 = mul_by_i(svptrue_b64(),  input00);
            svfloat64_t i_10 = mul_by_i(svptrue_b64(),  input10);
            svfloat64_t i_11 = mul_by_i(svptrue_b64(),  input11);
            svfloat64_t i_01 = mul_by_i(svptrue_b64(),  input01);


            svfloat64_t output00 = svadd_x(svptrue_b64(), input01, i_11); 
            svfloat64_t output01 = svsub_x(svptrue_b64(), input00, i_10); 
            svfloat64_t output10 = svadd_x(svptrue_b64(), input11, i_01); 
            svfloat64_t output11 = svsub_x(svptrue_b64(), input10, i_00); 


            svfloat64_t sv_factor = svdup_f64(sqrt2inv);

            output00 = svmul_x(svptrue_b64(), output00, sv_factor);
            output01 = svmul_x(svptrue_b64(), output01, sv_factor);
            output10 = svmul_x(svptrue_b64(), output10, sv_factor);
            output11 = svmul_x(svptrue_b64(), output11, sv_factor);

            svst1(svptrue_b64(), (double *)&state[basis_index_00], output00);
            svst1(svptrue_b64(), (double *)&state[basis_index_01], output01);
            svst1(svptrue_b64(), (double *)&state[basis_index_10], output10);
            svst1(svptrue_b64(), (double *)&state[basis_index_11], output11);

            
        }
    }

    else {
        ECR_gate_parallel_unroll(target_qubit_index_0, target_qubit_index_1, state, dim);
    }

}

#endif  // _USE_SVE


#ifdef _USE_MPI

void ECR_gate_mpi(UINT target_qubit_index_0, UINT target_qubit_index_1,
    CTYPE* state, ITYPE dim, UINT inner_qc) {
    // ordeo os qubits de xeito que o de maior índice se almacene en left_qubit e o de menor índice en right_qubit.
    UINT left_qubit, right_qubit;
    if (target_qubit_index_0 > target_qubit_index_1) {
        left_qubit = target_qubit_index_0;
        right_qubit = target_qubit_index_1;
    } else {
        left_qubit = target_qubit_index_1;
        right_qubit = target_qubit_index_0;
    }

    if (left_qubit < inner_qc) { // os dous qubits son internos ao proceso
        // Non ten sentido aplicar MPI, uso a función ECR_gate que xa teño definida e fago os cálculos nunha única CPU.
        ECR_gate(target_qubit_index_0, target_qubit_index_1, state, dim);

    } else if (right_qubit < inner_qc) {  // one target is outer
        /* Neste caso un dos qubits é interno (está dentro do propio proceso) e o outro é externo. 
        Precísase unha comunicación entre procesos. */

        MPIutil& m = MPIutil::get_inst();
        const UINT rank = m.get_rank(); // obtén o rank de cada proceso
        ITYPE dim_work = dim; // inicialízase a dim_work como a dim de cada proceso
        ITYPE num_work = 1; // inicialízase o número de traballos por proceso a 1
        /* old_si vai facer unha copia do fragmento de state de cada proceso. Isto é necesario porque en
        _ECR_gate_mpi_local_global vanse modificar directamente os valores de si, e para seguir calculando
        son necesarios os seus valores iniciais*/
        ITYPE rw;
        
        /* O seguinte é equivalente a malloc e mempcy. CTYPE é std::complex<double> (definido noutros arquivos,
        por exemplo en util_common.h).
        */
        std::vector<CTYPE> old_si_buf(state, state + dim);
        CTYPE* old_si = old_si_buf.data();

        std::vector<CTYPE> t_buf;
        CTYPE* t;
        /* Para definir t teño que distinguir entre se o índice do target_qubit_index_0 é máis grande ou máis pequeno
        que o do target_qubit_index_1. Se target_qubit_index_0 < target_qubit_index_1 para calcular cada unha das
        compoñentes finais do vector de estado úsanse tanto as amplitudes iniciais do propio proceso como as do proceso
        par (aquel co que se comunica). No caso de que target_qubit_index_0 > target_qubit_index_1 para calcular unha 
        amplitude final úsanse só as amplitudes do proceso par, as do propio proceso non se usan. Debido a isto, os procesos
        precisan todas as amplitudes dos seus procesos pares, non se pode dividir cada proceso en varios traballos (por
        que senón o si (state) sería só de cada traballo e non tería todas as amplitudes necesarias para o cálculo).
        t vaise usar para almacenar temporalmente as amplitudes do proceso par e poder facer cálculos con elas na función
        _ECR_gate_mpi_local_global.
        */
        if (target_qubit_index_0 < target_qubit_index_1) {
            t = m.get_workarea(&dim_work, &num_work); /* t neste caso é un punteiro a un bloque de memoria (zona de traballo)
            que devolve get_workarea. Esta función vai axustar automaticamente num_work e dim_work segundo o descrito no
            ficheiro MPIutil.cpp, de xeito que agora o valor de num_work pode ser 1 ou distinto de 1 e dim_work axustarase de
            xeito que num_work*dim_work = dim (dimensión en cada proceso). A dimensión total do vector de estado será num_work*dim_work*mpi_size.
            */
        } else {
            t_buf.resize(dim);
            t = t_buf.data();
            // t neste caso inicialízase como unha reserva de memoria que permita almacenar o 
            // fragmento do vector de estado correspondente a un proceso completo.
        } 

        /* Cada proceso contén as amplitudes dos qubits internos e o valor dos qubits externos está codificado no número de rank. left_qubit por 
        definición é o qubit de maior índice, polo tanto neste caso corresponderase co qubit externo.
        O proceso par a un dado é aquel que ten invertido o left_qubit. */
        const ITYPE tgt_rank_bit = 1 << (left_qubit - inner_qc); /* crease unha máscara de bits que marque a 1 a posición do left_qubit (ignorando os
        qubits internos). inner_qc é o número de qubits internos correspondente e calcúlase como "const UINT inner_qc = n - log_nodes;", onde n é o
        número total de qubits do sistema.
        */
        const int pair_rank = rank ^ tgt_rank_bit; // calcúlase o proceso par (pair_rank) a un proceso (rank) determinado invertindo o valor do left_qubit.
        
        /* Agora fago un bucle que percorra para cada proceso todos os traballos (works). Para cada un dos traballos hai que facer o envío e recibo de
        datos correspondente e chamar á función que aplica a matriz (_ECR_gate_mpi_local_global).*/
        for (ITYPE w = 0; w < num_work; ++w) {
            CTYPE* si;
            if (num_work > 1) { /* No caso de que o número de traballos por proceso sexa maior que 1 entre o rank e o pair_rank xa non se compartirán todas as
                amplitudes do vector de estado. Hai que asegurarse entón de que se comunican os work que toca e para iso hai que escoller con coidado a onde
                se apunta co si dun dos procesos. */
                if (rank < (UINT)pair_rank) {
                    si = state + w*dim_work; // os si dun dos procesos involucrados na comunicación (hai varios si porque hai varios works) poden escollerse de 
                    //forma que apunten á primeira posición do seu vector de estado correspondente. 
                    rw = w;
                } else {
                    /* Os si do outro proceso (aquel co que se comunican os que entran no if anterior) teñen que escollerse con máis coidado para asegurarnos de
                    que estamos comunicando os bloques de amplitudes que se necesitan.
                    */

                    ITYPE ideal_global_index_work = ((ITYPE)rank*num_work + w) * dim_work; /* ideal_global_index_work vai almacenar o enteiro que corresponde á posición global 
                    (posición respecto ao vector de estado completo) na que estou. Almacena a posición global correspondente ao primeiro valor do work w
                    no que me atopo. É a posición "ideal", é dicir, só é a posición global real se os works se comunican por orde (o worker 0 dun proceso co worker 0 do outro, o worker 1 co 1...).
                    */
                    ITYPE my_target_index = ideal_global_index_work ^ ((1ULL << target_qubit_index_0) + (1ULL << target_qubit_index_1)); /* my_target_index vai calcular
                    a posición global que se obtén ao invertir os dous qubits sobre os que se aplica a porta. Marca a primeira posición do bloque par co que quero
                    comunicar o bloque actual.
                    */

                    si = state + (my_target_index%dim); /* my_target_index%dim devolve o resto de dividir my_target_index entre dim e isto representa a posición do 
                    my_target_index referida ao proceso concreto no que estou (posición local). state apunta á primeira posición do vector de estado local ao 
                    proceso no que me atope.
                    */
                   rw = (ITYPE)(my_target_index%dim)/dim_work;
                }
            } else { /* se o número de traballos por proceso é un entón o vector de estado de cada traballo é igual ao vector de estado de cada proceso.
                O rank e o pair_rank vanse comunicar e compartir todos os elementos dos seus vectores de estado.
                */
                si = state;
            }
            
            m.m_DC_sendrecv(si, t, dim_work, pair_rank); // fago o sendrecv enviando o que hai en si e recibindo en t entre o rank e o pair_rank. Vaise enviando
            // a información en bloques de tamaño dim_work (que se corresponde coa dimensión do proceso só se num_work = 1).
      
            _ECR_gate_mpi_local_global(rw, rank, target_qubit_index_0, target_qubit_index_1, left_qubit, right_qubit, old_si, si, t, dim, dim_work, num_work);
            // por último chámase á función que vai permitir aplicar a porta.

        }


    } else {  // both targets are outer
        // Os dous qubits son externos ao proceso MPI. Precísanse entón dúas comunicacións.
        MPIutil& m = MPIutil::get_inst();
        const UINT rank = m.get_rank();
        ITYPE dim_work = dim;
        ITYPE num_work = 0;
        const UINT tgt0_rank_bit = 1 << (target_qubit_index_0 - inner_qc);  
        const UINT tgt1_rank_bit = 1 << (target_qubit_index_1 - inner_qc);  
        const UINT tgt_rank_bit = tgt0_rank_bit + tgt1_rank_bit; 
        const int pair_rank = rank ^ tgt0_rank_bit;  // calcúlase o proceso par (pair_rank) a un proceso (rank) determinado invertindo o valor do target_qubit_index_0.
        const int pair_rank1 = rank ^ tgt_rank_bit;  /* calcúlase o proceso par (pair_rank1) a un proceso (rank) determinado invertindo o valor tanto do target_qubit_index_0
        como do target_qubit_index_1.
        */
        CTYPE* tmp = m.get_workarea(
            &dim_work, &num_work); 
        (void)tmp;            
        std::vector<CTYPE> t1_buf(dim_work);
        std::vector<CTYPE> t2_buf(dim_work);
        CTYPE* t1 = t1_buf.data();
        CTYPE* t2 = t2_buf.data();
        CTYPE* si = state;
        
        bool is_lower_rank = !(rank & tgt0_rank_bit); // devolve True se o target_qubit_index_0 está a 0 no rank.
        for (ITYPE i = 0; i < num_work; ++i) {
            m.m_DC_sendrecv(si, t1, dim_work, pair_rank);
            m.m_DC_sendrecv(si, t2, dim_work, pair_rank1);
            _ECR_gate_mpi_external(t1, t2, si, dim_work, is_lower_rank);
            si += dim_work;
        }

    }
}

/* Vou definir unha función que concatena o valor dos dous qubits sobre os que se aplica a porta. Os qubits están ordeados: primeiro vai o left_qubit, que é o de
maior índice e despois o right_qubit, que é o de menor índice.*/
static inline ITYPE combine_qubit_bits(ITYPE N, const UINT right_qubit, const UINT left_qubit) {
    ITYPE r_bit = (N >> right_qubit) & 1; // extrae o valor do right_qubit
    ITYPE l_bit = (N >> left_qubit) & 1; // extrae o valor do left_qubit
    ITYPE value = (l_bit << 1) | r_bit; // concatena o valor dos dous qubits, primeiro left_qubit e despois right_qubit.
    return value;
}

static const double sqrt2inv = 1. / sqrt(2.);

void _ECR_gate_mpi_local_global(ITYPE rw, UINT rank, UINT target_qubit_index_0, UINT target_qubit_index_1, UINT left_qubit, UINT right_qubit, const CTYPE* old_si, CTYPE* si, CTYPE* t, ITYPE dim, ITYPE dim_work, ITYPE num_work) {
    /* Para aplicar a matriz divido en dous casos. Para target_qubit_index_0 < target_qubit_index_1 úsanse tanto as amplitudes do propio proceso como as do proceso par
    e num_work pode ser 1 ou distinto de 1. Para target_qubit_index_0 > target_qubit_index_1 úsanse só as amplitudes do proceso par pero non as do propio proceso e está
    establecido que num_work = 1.*/
    if (target_qubit_index_0 < target_qubit_index_1) {
            for (ITYPE j = 0; j < dim_work; j++) { // fago un bucle que percorra todos os valores dentro dun work
                ITYPE global_position = j + dim*(ITYPE)rank + dim_work*rw; // calculo a posición global da posición do vector de estado na que me atopo.
                ITYPE bitflip_0 = global_position ^ (1ULL << target_qubit_index_0); // calculo a posición global resultante de invertir o qubit dado por target_qubit_index_0
                ITYPE bitflip_0_1 = global_position ^ ((1ULL << target_qubit_index_0) + (1ULL << target_qubit_index_1)); // calculo a posición global resultante de invertir o
                // qubit dado por target_qubit_index_0 e target_qubit_index_1
                ITYPE si_target_index = bitflip_0%dim; // Os índices de old_si son locais respecto ao proceso porque old_si é unha copia do state completo de cada proceso. 
                ITYPE t_target_index = (bitflip_0_1%dim)%dim_work; /* teño que convertir a posición global calculada a unha posición local respecto ao traballo no que me atope.
                t ten índices locais a cada work porque no sendrecv envíanse todos os elementos dun work, pero non todos os do proceso.
                */
                /* Para cada unha das catro combinacións posibles de valores entre right_qubit e left_qubit aplícase unha fórmula diferente. Utilizo a función combine_qubit_bits
                para saber que combinación hai en cada caso e aplicar a fórmula que corresponda. */

                ITYPE cb = combine_qubit_bits(global_position, target_qubit_index_0, target_qubit_index_1);
                int sign = (cb % 2 == 0) ? 1 : -1;
                si[j] = sqrt2inv * old_si[si_target_index] + sign * sqrt2inv * 1i * t[t_target_index];
            }
    } else {
            for (ITYPE j = 0; j < dim; j++) { 
                ITYPE global_position = j + dim*(ITYPE)rank; // aquí non hai que ter en conta dim_work porque agora hai só un work entón dim_work = dim.
                ITYPE bitflip_0 = global_position ^ (1ULL << target_qubit_index_0); 
                ITYPE bitflip_0_1 = global_position ^ ((1ULL << target_qubit_index_0) + (1ULL << target_qubit_index_1)); 
                ITYPE target_index_bitflip_0 = bitflip_0%dim;
                ITYPE target_index_bitflip_0_1 = bitflip_0_1%dim;
                // Neste caso os índices de t son locais ao proceso. Só hai un work por proceso.

                ITYPE cb = combine_qubit_bits(global_position, target_qubit_index_1, target_qubit_index_0);
                int sign = (cb % 2 == 0) ? 1 : -1; // se o resultado da división enteira (sen decimais) de cb/2 é cero
                // o signo é positivo e se é 1
                si[j] = sqrt2inv * t[target_index_bitflip_0] + sign * sqrt2inv * 1i * t[target_index_bitflip_0_1];
            }
    }
}

void _ECR_gate_mpi_external(
    CTYPE* t1, CTYPE* t2, CTYPE* si, ITYPE dim, bool is_lower_rank) {
    #pragma omp parallel for
        for (ITYPE i = 0; i < dim; ++i) {
            // hai dúas fórmulas diferentes dependendo de se o target_qubit_index_0 está a 0 ou a 1 no rank
            if (is_lower_rank) {
                si[i] = (t1[i] + t2[i] * 1i) * sqrt2inv;
            } else {
                si[i] = (t1[i] - t2[i] * 1i) * sqrt2inv;
            }
        }
}

#endif