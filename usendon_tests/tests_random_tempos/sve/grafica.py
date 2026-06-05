import re
import matplotlib.pyplot as plt

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
    archivo = "sve_430854.out"  # cambia esto por tu archivo

    tiempos = extraer_tiempos(archivo)

    if not tiempos:
        print("No se encontraron tiempos en el archivo.")
        return

    # eje x = número de repetición
    x = list(range(len(tiempos)))

    plt.figure(figsize=(12, 5))
    plt.plot(x, tiempos, linewidth=1)

    plt.title("Tiempos por repetición (ECR gate)")
    plt.xlabel("Repetición")
    plt.ylabel("Tiempo (us)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("grafica_tempo_sve_por_repeticion.png",
            dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved.")


if __name__ == "__main__":
    main()