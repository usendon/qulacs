#!/usr/bin/env python3
"""
Lee archivos de salida de ejecuciones MPI de Qulacs,
extrae el número de tasks y el tiempo, y genera una gráfica
con el tiempo y el speedup.

Uso:
    python plot_mpi.py archivo1.txt archivo2.txt ...
  o bien:
    python plot_mpi.py *.txt
"""

import sys
import re
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def parse_file(filepath):
    """
    Extrae tasks y tiempo de un archivo de salida MPI.
    Busca la última línea con el patrón: <int> <float>
    que aparece tras el bloque de ejecución.
    """
    pattern = re.compile(r"^\s*(\d+)\s+([\d.]+)\s*$")
    tasks = None
    tiempo = None

    with open(filepath, "r", errors="replace") as f:
        for line in f:
            m = pattern.match(line)
            if m:
                tasks = int(m.group(1))
                tiempo = float(m.group(2))

    return tasks, tiempo


def main():
    if len(sys.argv) < 2:
        print("Uso: python plot_mpi.py archivo1 archivo2 ...")
        sys.exit(1)

    archivos = sys.argv[1:]
    datos = []

    for filepath in archivos:
        if not os.path.isfile(filepath):
            print(f"[AVISO] No encontrado: {filepath}")
            continue
        tasks, tiempo = parse_file(filepath)
        if tasks is None or tiempo is None:
            print(f"[AVISO] No se encontraron datos en: {filepath}")
            continue
        datos.append((tasks, tiempo))
        print(f"  {os.path.basename(filepath):30s}  tasks={tasks:4d}  tiempo={tiempo:.4f}s")

    if not datos:
        print("No se pudieron extraer datos de ningún archivo.")
        sys.exit(1)

    # Ordenar por número de tasks
    datos.sort(key=lambda x: x[0])
    tasks_arr = np.array([d[0] for d in datos])
    tiempo_arr = np.array([d[1] for d in datos])

    # Speedup: T(1 task) / T(N tasks)
    # Si no hay ejecución con 1 task, usamos la de menor número de tasks como referencia
    t_ref = tiempo_arr[0]
    tasks_ref = tasks_arr[0]
    speedup_arr = t_ref / tiempo_arr

    # Speedup ideal basado en el número de tasks relativos al de referencia
    speedup_ideal = tasks_arr / tasks_ref

    # ── Figura ──────────────────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 9), sharex=True)
    fig.suptitle("Rendimiento MPI – Qulacs (1 task/nodo)", fontsize=15, fontweight="bold", y=0.98)

    color_tiempo  = "#2563EB"   # azul
    color_speedup = "#16A34A"   # verde
    color_ideal   = "#9CA3AF"   # gris

    # ── Panel superior: Tiempo ───────────────────────────────────────────────
    ax1.plot(tasks_arr, tiempo_arr, "o-", color=color_tiempo,
             linewidth=2, markersize=7, label="Tiempo medido")
    for x, y in zip(tasks_arr, tiempo_arr):
        ax1.annotate(f"{y:.2f}s", (x, y),
                     textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=8, color=color_tiempo)
    ax1.set_ylabel("Tiempo (s)", fontsize=11)
    ax1.set_title("Tiempo de ejecución", fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(fontsize=9)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # ── Panel inferior: Speedup ──────────────────────────────────────────────
    ax2.plot(tasks_arr, speedup_ideal, "--", color=color_ideal,
             linewidth=1.5, label=f"Speedup ideal (ref. {tasks_ref} nodo/s)")
    ax2.plot(tasks_arr, speedup_arr, "s-", color=color_speedup,
             linewidth=2, markersize=7, label="Speedup real")
    for x, y in zip(tasks_arr, speedup_arr):
        ax2.annotate(f"{y:.2f}×", (x, y),
                     textcoords="offset points", xytext=(0, 8),
                     ha="center", fontsize=8, color=color_speedup)
    ax2.set_xlabel("Número de nodos MPI", fontsize=11)
    ax2.set_ylabel("Speedup", fontsize=11)
    ax2.set_title("Speedup", fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(fontsize=9)
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Eje X: marcas en los valores de nodos disponibles
    ax2.set_xticks(tasks_arr)
    ax2.set_xticklabels([str(t) for t in tasks_arr])

    plt.tight_layout()
    output_png = "mpi_rendimiento.png"
    plt.savefig(output_png, dpi=150, bbox_inches="tight")
    print(f"\nGráfica guardada en: {output_png}")
    plt.show()


if __name__ == "__main__":
    main()