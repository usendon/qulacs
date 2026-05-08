
import numpy as np
from qulacs.converter import (
    convert_QASM_to_qulacs_circuit,
    convert_qulacs_circuit_to_QASM,
)
from qulacs.gate import ECR


def test_ecr_qasm_roundtrip():
    qasm = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
ecr q[0],q[1];
""".strip()

    # QASM → circuito
    circuit = convert_QASM_to_qulacs_circuit(qasm.splitlines())

    # comprobar que la puerta es ECR
    gate = circuit.get_gate(0)
    assert np.allclose(gate.get_matrix(), ECR(0, 1).get_matrix())

    # circuito → QASM
    recovered_qasm = convert_qulacs_circuit_to_QASM(circuit)

    # volver a convertir
    circuit2 = convert_QASM_to_qulacs_circuit(recovered_qasm)

    # comprobar equivalencia
    assert np.allclose(
        circuit2.get_gate(0).get_matrix(),
        ECR(0, 1).get_matrix()
    )

    print("Test ECR correcto ✅")


if __name__ == "__main__":
    test_ecr_qasm_roundtrip()