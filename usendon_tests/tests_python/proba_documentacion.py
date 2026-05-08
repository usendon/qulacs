
# Para probar estes arquivos primeiro teño que cargar os módulos con:
# ml qmio/hpc gcc/12.3.0  gcccore/12.3.0 impi/2021.13.0 boost/1.85.0 cmake/3.27.6 nlohmann_json/3.11.3 python/3.9.9
# Despois activo o entorno virtual env con source env/bin/activate e instalo Qulacs con pip install qulacs.
# Despois executo o arquivo que corresponda en cada caso con python3 nome_arquivo.py e listo.

import qulacs
help(qulacs.QuantumCircuit.add_ECR_gate)