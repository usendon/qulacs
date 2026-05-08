import re

input_file = "mpi_1_nodo_423630.out"
output_file = "output.txt"

# Regex para detectar:
# 1. Cabecera de bloque ECR
ecr_pattern = re.compile(r"^=== ECR gate en qubits \d+ \d+ ===")

# 2. Líneas de estado F|n>
f_pattern = re.compile(r"^F\|(\d+)> : (.+)")

blocks = []
current_block = None

with open(input_file, "r") as f:
    for line in f:
        line = line.strip()

        # Detectar inicio de bloque válido
        if ecr_pattern.match(line):
            if current_block:
                blocks.append(current_block)
            current_block = {
                "header": line,
                "states": {}
            }
            continue

        # Ignorar TODO lo demás si no estamos en bloque válido
        if current_block is None:
            continue

        # Detectar líneas F|>
        match = f_pattern.match(line)
        if match:
            index = int(match.group(1))
            value = match.group(2)
            current_block["states"][index] = value

# Guardar último bloque
if current_block:
    blocks.append(current_block)

# Escribir salida ordenada
with open(output_file, "w") as out:
    for block in blocks:
        out.write(block["header"] + "\n\n")
        out.write("--- Vector de estado (multi-cpu) ---\n\n")

        for i in sorted(block["states"].keys()):
            out.write(f"F|{i}> : {block['states'][i]}\n")

        out.write("\n\n")