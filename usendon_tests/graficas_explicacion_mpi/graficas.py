
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import rcParams

# --------------------------------------------------
# Estilo similar a la segunda figura
# --------------------------------------------------
rcParams["font.family"] = "serif"
rcParams["mathtext.fontset"] = "cm"
rcParams["font.size"] = 11

fig, ax = plt.subplots(figsize=(8, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis("off")

# Colores pastel similares a la Fig. 2
GREEN_BG = "#dcefd3"
GREEN_BOX = "#bfe3b3"

PURPLE_BG = "#e6e0f5"
PURPLE_BOX = "#cfc4ee"

EDGE_GREEN = "#8dbb85"
EDGE_PURPLE = "#9b8bd0"

# --------------------------------------------------
# Función para dibujar workers
# --------------------------------------------------
def worker(ax, x, y, color, edge, title, amps):
    box = FancyBboxPatch(
        (x, y),
        1.4,
        1.35,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=1.2,
        edgecolor=edge,
        facecolor=color,
    )
    ax.add_patch(box)

    ax.text(
        x + 0.7,
        y + 1.1,
        title,
        ha="center",
        va="center",
        fontsize=10,
    )

    ax.text(
        x + 0.7,
        y + 0.45,
        amps,
        ha="center",
        va="center",
        fontsize=11,
    )


# --------------------------------------------------
# Contenedor Process 0
# --------------------------------------------------
proc0 = FancyBboxPatch(
    (1.2, 0.8),
    2.3,
    10.0,
    boxstyle="round,pad=0.04,rounding_size=0.18",
    linewidth=1.2,
    edgecolor=EDGE_GREEN,
    facecolor=GREEN_BG,
)
ax.add_patch(proc0)

ax.text(
    2.35,
    10.4,
    "Process 0",
    fontsize=16,
    ha="center",
)

# --------------------------------------------------
# Contenedor Process 1
# --------------------------------------------------
proc1 = FancyBboxPatch(
    (6.0, 0.8),
    2.3,
    10.0,
    boxstyle="round,pad=0.04,rounding_size=0.18",
    linewidth=1.2,
    edgecolor=EDGE_PURPLE,
    facecolor=PURPLE_BG,
)
ax.add_patch(proc1)

ax.text(
    7.15,
    10.4,
    "Process 1",
    fontsize=16,
    ha="center",
)

# --------------------------------------------------
# Workers proceso 0
# --------------------------------------------------
worker(ax, 1.45, 8.4, GREEN_BOX, EDGE_GREEN,
       "Worker 0",
       r"$\alpha_{00000}$" "\n" r"$\vdots$" "\n" r"$\alpha_{00011}$")

worker(ax, 1.45, 6.0, GREEN_BOX, EDGE_GREEN,
       "Worker 1",
       r"$\alpha_{00100}$" "\n" r"$\vdots$" "\n" r"$\alpha_{00111}$")

worker(ax, 1.45, 3.6, GREEN_BOX, EDGE_GREEN,
       "Worker 2",
       r"$\alpha_{01000}$" "\n" r"$\vdots$" "\n" r"$\alpha_{01011}$")

worker(ax, 1.45, 1.2, GREEN_BOX, EDGE_GREEN,
       "Worker 3",
       r"$\alpha_{01100}$" "\n" r"$\vdots$" "\n" r"$\alpha_{01111}$")

# --------------------------------------------------
# Workers proceso 1
# --------------------------------------------------
worker(ax, 6.25, 8.4, PURPLE_BOX, EDGE_PURPLE,
       "Worker 0",
       r"$\alpha_{10000}$" "\n" r"$\vdots$" "\n" r"$\alpha_{10011}$")

worker(ax, 6.25, 6.0, PURPLE_BOX, EDGE_PURPLE,
       "Worker 1",
       r"$\alpha_{10100}$" "\n" r"$\vdots$" "\n" r"$\alpha_{10111}$")

worker(ax, 6.25, 3.6, PURPLE_BOX, EDGE_PURPLE,
       "Worker 2",
       r"$\alpha_{11000}$" "\n" r"$\vdots$" "\n" r"$\alpha_{11011}$")

worker(ax, 6.25, 1.2, PURPLE_BOX, EDGE_PURPLE,
       "Worker 3",
       r"$\alpha_{11100}$" "\n" r"$\vdots$" "\n" r"$\alpha_{11111}$")

# --------------------------------------------------
# Flechas de comunicación
# --------------------------------------------------
ax.annotate(
    "",
    xy=(6.5, 9.35),
    xytext=(3.45, 9.35),
    arrowprops=dict(
        arrowstyle="->",
        lw=1.2,
        color="gray"
    )
)

ax.annotate(
    "",
    xy=(6.5, 7.0),
    xytext=(3.45, 9.35),
    arrowprops=dict(
        arrowstyle="->",
        lw=1.2,
        color="gray"
    )
)

plt.tight_layout()
plt.savefig(
    "process_workers_styled.pdf",
    bbox_inches="tight"
)
plt.savefig(
    "process_workers_styled.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()