
import numpy as np
import re
import matplotlib.pyplot as plt

def main():
    archivo = "sve_430854.out"

    patron = re.compile(r"qubits \((\d+),(\d+)\).*tiempo:\s*([\d.]+)\s*us")

    matriz = np.zeros((20, 20))
    conteo = np.zeros((20, 20))

    with open(archivo, "r") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                i = int(m.group(1))
                j = int(m.group(2))
                t = float(m.group(3))

                matriz[i, j] += t
                conteo[i, j] += 1

    # media por celda
    with np.errstate(divide='ignore', invalid='ignore'):
        heatmap = np.divide(matriz, conteo)
        heatmap[conteo == 0] = np.nan

    plt.figure(figsize=(6,5))
    plt.imshow(heatmap, origin="lower")
    plt.colorbar(label="Tiempo medio (us)")
    plt.title("Heatmap de tiempos por par de qubits")
    plt.xlabel("Qubit j")
    plt.ylabel("Qubit i")

    plt.savefig("heatmap_tempo_sve.png",
            dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved.")


if __name__ == "__main__":
    main()