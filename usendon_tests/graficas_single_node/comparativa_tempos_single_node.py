import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── datos ──────────────────────────────────────────────────────────────────────
data = {
    "ECR_gate_parallel_unroll": {
        "Intel Xeon":     5_895_827,
        "Fujitsu A64FX":  4_909_630,
        "NVIDIA A100 GPU": None,
    },
    "ECR_gate_parallel_simd": {
        "Intel Xeon":      978_578,
        "Fujitsu A64FX":   None,
        "NVIDIA A100 GPU": None,
    },
    "ECR_gate_parallel_sve": {
        "Intel Xeon":     None,
        "Fujitsu A64FX":  1_810_022,
        "NVIDIA A100 GPU": None,
    },
    "ECR_gate_gpu": {
        "Intel Xeon":     None,
        "Fujitsu A64FX":  None,
        "NVIDIA A100 GPU": 27_814,
    },
}

hardware   = ["Intel Xeon", "Fujitsu A64FX", "NVIDIA A100 GPU"]
functions  = list(data.keys())

# ── paleta ────────────────────────────────────────────────────────────────────
colors  = ["#0ca0ba", "#2f7f66", "#8f5fc5",  "#ff1fa9"]
markers = ["o", "s", "^", "D"]

# ══════════════════════════════════════════════════════════════════════════════
# Gráfico 2 — Barras agrupadas: eje x = hardware, leyenda = función
# ══════════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(10, 5))

n_hw   = len(hardware)
n_fn   = len(functions)
width  = 0.18
offsets = np.linspace(-(n_fn - 1) / 2 * width, (n_fn - 1) / 2 * width, n_fn)
x = np.arange(n_hw)

# calcula cuántas funciones tienen dato real para cada hardware
hw_fns = {hw: [f for f in functions if data[f].get(hw) is not None] for hw in hardware}

already_labeled = set()

for i, (fname, color) in enumerate(zip(functions, colors)):
    for j, hw in enumerate(hardware):
        val = data[fname].get(hw)
        if val is None:
            continue
        local_fns = hw_fns[hw]
        n_local = len(local_fns)
        local_offsets = np.linspace(-(n_local - 1) / 2 * width, (n_local - 1) / 2 * width, n_local)
        local_i = local_fns.index(fname)
        ax2.bar(x[j] + local_offsets[local_i], val, width,
                label=fname if fname not in already_labeled else "_nolegend_",
                color=color, zorder=3)
        already_labeled.add(fname)

ax2.set_xticks(x)
ax2.set_xticklabels(hardware, fontsize=10)
ax2.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
ax2.set_ylabel("Tempo de execución medio (ns)", fontsize=11)
ax2.set_xlabel("Hardware", fontsize=11)
ax2.legend(fontsize=9, title_fontsize=9, loc="upper right")
ax2.grid(axis="y", color="#e1e0d9", linewidth=0.8, zorder=0)
ax2.set_axisbelow(True)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig2.tight_layout()
fig2.savefig("ecr_bar_chart.png", dpi=150)
print("Guardado: ecr_bar_chart.png")

plt.show()