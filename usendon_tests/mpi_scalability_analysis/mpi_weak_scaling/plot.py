
#!/usr/bin/env python3
"""
Lee archivos .out de ejecuciones MPI de Qulacs (weak scaling),
extrae nodos, qubits y tiempo, y genera una gráfica como la del paper
(tiempo vs número de nodos, con qubits en eje X superior).

Uso:
    python plot_weak_scaling.py archivo1.out archivo2.out ...
  o bien:
    python plot_weak_scaling.py *.out
"""

import sys
import re
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def parse_file(filepath):
    """
    Extrae tasks, qubits y tiempo de un archivo .out de Qulacs MPI.
    Busca:
      - "Tasks SLURM: X"
      - "Qubits: X"
      - última línea con patrón "<int> <float>"
    """
    tasks   = None
    qubits  = None
    tiempo  = None

    pat_tasks  = re.compile(r"Tasks SLURM:\s*(\d+)")
    pat_qubits = re.compile(r"Qubits:\s*(\d+)")
    pat_result = re.compile(r"^\s*(\d+)\s+([\d.]+)\s*$")

    with open(filepath, "r", errors="replace") as f:
        for line in f:
            m = pat_tasks.search(line)
            if m:
                tasks = int(m.group(1))
            m = pat_qubits.search(line)
            if m:
                qubits = int(m.group(1))
            m = pat_result.match(line)
            if m:
                tiempo = float(m.group(2))

    return tasks, qubits, tiempo


def main():
    if len(sys.argv) < 2:
        print("Uso: python plot_weak_scaling.py archivo1.out archivo2.out ...")
        sys.exit(1)

    archivos = sys.argv[1:]
    datos = []

    for filepath in archivos:
        if not os.path.isfile(filepath):
            print(f"[AVISO] No encontrado: {filepath}")
            continue
        tasks, qubits, tiempo = parse_file(filepath)
        if None in (tasks, qubits, tiempo):
            print(f"[AVISO] Datos incompletos en: {filepath}  "
                  f"(tasks={tasks}, qubits={qubits}, tiempo={tiempo})")
            continue
        datos.append((tasks, qubits, tiempo))
        print(f"  {os.path.basename(filepath):35s}  nodos={tasks:3d}  "
              f"qubits={qubits:2d}  tiempo={tiempo:.4f}s")

    if not datos:
        print("No se pudieron extraer datos de ningún archivo.")
        sys.exit(1)

    # Ordenar por número de nodos
    datos.sort(key=lambda x: x[0])
    nodos_arr  = np.array([d[0] for d in datos])
    qubits_arr = np.array([d[1] for d in datos])
    tiempo_arr = np.array([d[2] for d in datos])

    # ── Figura ──────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(8, 5))

    color = "#2563EB"

    ax.plot(nodos_arr, tiempo_arr, "o-", color=color,
            linewidth=2, markersize=7, label="mpiQulacs")

    for x, y in zip(nodos_arr, tiempo_arr):
        ax.annotate(f"{y:.2f}s", (x, y),
                    textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=8, color=color)

    # Línea de referencia horizontal (tiempo ideal = constante)
    ax.axhline(tiempo_arr[0], color="gray", linestyle="--",
               linewidth=1.2, label="Ideal (tiempo constante)")

    # Eje X inferior: número de nodos
    ax.set_xlabel("Number of nodes", fontsize=11)
    ax.set_ylabel("Execution time [second]\n(lower is better)", fontsize=11)
    ax.set_title("Weak scaling (30 qubits per node)", fontsize=12, fontweight="bold")
    ax.set_xticks(nodos_arr)
    ax.set_xticklabels([str(n) for n in nodos_arr])
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(fontsize=9)
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    # Eje X superior: número de qubits
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(nodos_arr)
    ax2.set_xticklabels([str(q) for q in qubits_arr])
    ax2.set_xlabel("Number of qubits", fontsize=11)

    plt.tight_layout()
    output_png = "weak_scaling.png"
    plt.savefig(output_png, dpi=150, bbox_inches="tight")
    print(f"\nGráfica guardada en: {output_png}")
    plt.show()


if __name__ == "__main__":
    main()