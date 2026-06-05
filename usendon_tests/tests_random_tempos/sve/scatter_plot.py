import re
import matplotlib.pyplot as plt

def extraer_datos(archivo):
    tiempos = []
    pares = []

    patron = re.compile(r"qubits \((\d+),(\d+)\).*tiempo:\s*([\d.]+)\s*us")

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                q1 = int(m.group(1))
                q2 = int(m.group(2))
                t = float(m.group(3))

                pares.append((q1, q2))
                tiempos.append(t)

    return pares, tiempos


def distancia(q1, q2):
    return abs(q1 - q2)


def main():
    archivo = "sve_430854.out"

    pares, tiempos = extraer_datos(archivo)

    # 🔥 aquí está la parte que te faltaba
    distancias = [distancia(q1, q2) for (q1, q2) in pares]

    plt.figure(figsize=(10, 6))

    plt.scatter(distancias, tiempos, alpha=0.6, s=15)

    plt.xlabel("Distancia entre qubits")
    plt.ylabel("Tiempo (us)")
    plt.title("Tiempo de ejecución vs distancia entre qubits")
    plt.grid(True)

    plt.savefig("scatter_plot_tiempo_distancia.png",
                dpi=160, bbox_inches="tight", facecolor="white")

    plt.close()
    print("Saved: scatter_plot_tiempo_distancia.png")


if __name__ == "__main__":
    main()