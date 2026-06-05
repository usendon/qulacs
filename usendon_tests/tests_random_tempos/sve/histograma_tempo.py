import re
import matplotlib.pyplot as plt
import seaborn as sns

def extraer_tiempos(archivo):
    tiempos = []
    patron = re.compile(r"tiempo:\s*([\d.]+)\s*us")

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            match = patron.search(linea)
            if match:
                tiempos.append(float(match.group(1)))

    return tiempos


def main():
    archivo = "sve_430854.out"  # cambia esto

    tiempos = extraer_tiempos(archivo)

    if not tiempos:
        print("No se encontraron tiempos.")
        return

    plt.figure(figsize=(10, 6))

    # Histograma normalizado (PDF empírica)
    plt.hist(tiempos, bins=40, density=True, alpha=0.5, label="Histograma")

    # KDE (suavizado de la distribución)
    sns.kdeplot(tiempos, linewidth=2, label="Densidad (KDE)")

    plt.title("Distribución de tiempos de ejecución")
    plt.xlabel("Tiempo (us)")
    plt.ylabel("Densidad de probabilidad")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig("histograma_tempo_sve.png",
            dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved.")


if __name__ == "__main__":
    main()