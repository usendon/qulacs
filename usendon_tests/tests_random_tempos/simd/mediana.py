import re
import statistics

def extraer_tiempos(archivo):
    tiempos = []

    # expresión para capturar el número antes de "us"
    patron = re.compile(r"tiempo:\s*([\d.]+)\s*us")

    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            match = patron.search(linea)
            if match:
                tiempos.append(float(match.group(1)))

    return tiempos


def main():
    archivo = "simd_430738.out"  # cambia esto por tu archivo

    tiempos = extraer_tiempos(archivo)

    if not tiempos:
        print("No se encontraron tiempos en el archivo.")
        return

    mediana = statistics.median(tiempos)

    print(f"Número de muestras: {len(tiempos)}")
    print(f"Mediana de tiempos: {mediana:.2f} us")


if __name__ == "__main__":
    main()