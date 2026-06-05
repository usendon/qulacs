import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# =========================================================
# Helpers
# =========================================================

def rounded_box(
    ax,
    x,
    y,
    w,
    h,
    text="",
    fc="#eef7f3",
    ec="#4b9b7f",
    lw=1.5,
    fontsize=13,
    textcolor="#2b2b2b",
    radius=0.08,
    alpha=1.0,
    zorder=1
):

    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        linewidth=lw,
        edgecolor=ec,
        facecolor=fc,
        alpha=alpha,
        zorder=zorder
    )

    ax.add_patch(box)

    if text:
        ax.text(
            x + w / 2,
            y + h / 2,
            text,
            ha="center",
            va="center",
            fontsize=fontsize,
            color=textcolor,
            zorder=zorder + 1
        )

    return box


# =========================================================
# Figure
# =========================================================

fig, ax = plt.subplots(figsize=(13, 10))

ax.set_xlim(0, 14)
ax.set_ylim(0, 12)

ax.axis("off")


# =========================================================
# Colors
# =========================================================

local_edge = "#57a489"
local_fill = "#dff2ea"

global_edge = "#8f5fc5"
global_fill = "#f8f0ff"


# =========================================================
# Top qubit strip
# =========================================================

start_x = 1.2

w = 0.6
h = 0.6
gap = 0.18

y = 9.9

labels_local = ["0", "1", "⋯", "q", "⋯", "m-1"]
labels_global = ["m", "q", "⋯", "⋯", "⋯", "n-1"]


# =========================================================
# Local qubits
# =========================================================

for i, lab in enumerate(labels_local):

    x = start_x + i * (w + gap)

    rounded_box(
        ax,
        x,
        y,
        w,
        h,
        text=lab,
        fc=local_fill,
        ec=local_edge,
        fontsize=13,
        radius=0.07
    )


# =========================================================
# Separator
# =========================================================

sep_x = start_x + len(labels_local) * (w + gap) - gap / 2

ax.plot(
    [sep_x, sep_x],
    [9.7, 10.7],
    linestyle="--",
    color="gray"
)


# =========================================================
# Global qubits
# =========================================================

start_global = sep_x + 0.15

for i, lab in enumerate(labels_global):

    x = start_global + i * (w + gap)

    rounded_box(
        ax,
        x,
        y,
        w,
        h,
        text=lab,
        fc=global_fill,
        ec=global_edge,
        fontsize=13,
        radius=0.07
    )


# =========================================================
# Bounds and centers
# =========================================================

# Local region
local_left = start_x
local_right = sep_x

local_center = (local_left + local_right) / 2

# Global region
right_end = start_global + len(labels_global) * (w + gap) - gap

global_left = sep_x
global_right = right_end

global_center = (global_left + global_right) / 2

# Whole diagram center
center_x = (local_left + global_right) / 2


# =========================================================
# Main title
# =========================================================

ax.text(
    center_x,
    11.2,
    "Local vs global qubit operations for a single-qubit gate",
    fontsize=18,
    ha="center"
)

'''
ax.text(
    center_x,
    10.8,
    "(single-qubit gates: each gate couples exactly two amplitudes differing only in bit q)",
    fontsize=10,
    ha="center",
    color="dimgray"
)
'''


# =========================================================
# Local/global labels under top strip
# =========================================================

ax.plot(
    [local_left, local_right],
    [9.75, 9.75],
    color="gray",
    lw=1
)

ax.plot(
    [local_left, local_left],
    [9.7, 9.8],
    color="gray",
    lw=1
)

ax.plot(
    [local_right, local_right],
    [9.7, 9.8],
    color="gray",
    lw=1
)

ax.text(
    local_center,
    9.35,
    "local qubits (0 ≤ q < m)",
    ha="center",
    fontsize=13
)

ax.plot(
    [global_left, global_right],
    [9.75, 9.75],
    color="gray",
    lw=1
)

ax.plot(
    [global_right, global_right],
    [9.7, 9.8],
    color="gray",
    lw=1
)

ax.text(
    global_center,
    9.35,
    "global qubits (m ≤ q < n)",
    ha="center",
    fontsize=13
)


# =========================================================
# Left panel: local gate
# =========================================================

ax.text(
    local_center,
    8.6,
    "Gate on local qubit (q < m)",
    fontsize=15,
    ha="center"
)

local_box_w = 4.2
local_box_h = 4.5

local_box_x = local_center - local_box_w / 2

new_h = local_box_h * 0.73

y_new = 3.5 + (local_box_h - new_h)  # ajusta hacia abajo

rounded_box(
    ax,
    local_box_x,
    y_new,
    local_box_w,
    new_h,
    fc="#eef7f3",
    ec=local_edge,
    radius=0.18,
    lw=2
)


ax.text(
    local_center,
    7.5,
    "Process p",
    fontsize=15,
    ha="center",
    color="#2f7f66"
)

'''
ax.text(
    local_center,
    7.15,
    "owns 2ᵐ amplitudes",
    fontsize=13,
    ha="center",
    color="#2f7f66"
)
'''


# =========================================================
# Local amplitudes
# =========================================================

rounded_box(
    ax,
    local_center - 1.7,
    6.4,
    1.6,
    0.8,
    text=r"$\alpha_{...0...}$",
    fc="#f6fbf9",
    ec=local_edge,
    fontsize=18,
    radius=0.10
)

rounded_box(
    ax,
    local_center + 0.3,
    6.4,
    1.6,
    0.8,
    text=r"$\alpha_{...1...}$",
    fc="#f6fbf9",
    ec=local_edge,
    fontsize=18,
    radius=0.10
)


# Arrow between amplitudes
ax.annotate(
    "",
    xy=(local_center + 0.25, 6.8),
    xytext=(local_center - 0.1, 6.8),
    arrowprops=dict(
        arrowstyle="<->",
        color=local_edge,
        lw=2
    )
)

ax.text(
    local_center,
    5.8,
    "both in same process\nbit q is a local index bit",
    fontsize=13,
    ha="center",
    color="#2f7f66"
)

rounded_box(
    ax,
    local_center - 1.0,
    5.0,
    2.0,
    0.55,
    text="gate acts locally",
    fc="#f6fbf9",
    ec=local_edge,
    fontsize=13,
    radius=0.08
)

'''
rounded_box(
    ax,
    local_center - 1.7,
    3.2,
    3.4,
    0.6,
    text="No MPI communication",
    fc="#e7f7ee",
    ec=local_edge,
    fontsize=12,
    radius=0.08
)
'''


# =========================================================
# Right panel: global gate
# =========================================================

ax.text(
    global_center,
    8.6,
    "Gate on global qubit (q ≥ m)",
    fontsize=15,
    ha="center"
)

global_box_w = 4.3
global_box_h = 2.2

global_box_x = global_center - global_box_w / 2


# =========================================================
# Top process
# =========================================================

rounded_box(
    ax,
    global_box_x,
    5.8,
    global_box_w,
    global_box_h,
    fc="#f2f1ff",
    ec=global_edge,
    radius=0.18,
    lw=2
)

ax.text(
    global_center,
    7.5,
    "Process p",
    fontsize=15,
    ha="center",
    color="#8f5fc5"
)

ax.text(
    global_center,
    7.15,
    "bit q = 0 in rank index",
    fontsize=13,
    ha="center",
    color="#8f5fc5"
)

rounded_box(
    ax,
    global_center - 1.55,
    6.05,
    3.1,
    0.65,
    text=r"$\alpha_{...0...}$",
    fc="#faf9ff",
    ec=global_edge,
    fontsize=16,
    radius=0.08
)


# =========================================================
# Bottom process
# =========================================================

rounded_box(
    ax,
    global_box_x,
    2.8,
    global_box_w,
    global_box_h,
    fc="#f2f1ff",
    ec=global_edge,
    radius=0.18,
    lw=2
)

ax.text(
    global_center,
    4.5,
    "Process p'",
    fontsize=15,
    ha="center",
    color="#8f5fc5"
)

ax.text(
    global_center,
    4.15,
    "bit q = 1 in rank index",
    fontsize=13,
    ha="center",
    color="#8f5fc5"
)

rounded_box(
    ax,
    global_center - 1.55,
    3.05,
    3.1,
    0.65,
    text=r"$\alpha_{...1...}$",
    fc="#faf9ff",
    ec=global_edge,
    fontsize=16,
    radius=0.08
)


# =========================================================
# Communication arrow
# =========================================================

ax.annotate(
    "",
    xy=(global_center, 6.0),
    xytext=(global_center, 4.8),
    arrowprops=dict(
        arrowstyle="<->",
        color=global_edge,
        lw=2
    ),
    zorder=1
)

rounded_box(
    ax,
    global_center - 0.95,
    5.2,
    1.9,
    0.4,
    text="MPI exchange",
    fc="#f2f1ff",
    ec=global_edge,
    fontsize=10,
    textcolor="#8f5fc5",
    radius=0.05,
    zorder=5
)

'''
ax.text(
    global_center,
    2.3,
    "p and p' are any two partner ranks\n(determined by bit q)",
    fontsize=13,
    ha="center",
    color="#3f3f3f"
)
'''

'''
rounded_box(
    ax,
    global_center - 1.6,
    1.5,
    3.2,
    0.55,
    text="MPI communication required",
    fc="#f2f1ff",
    ec=global_edge,
    fontsize=13,
    radius=0.08
)
'''


# =========================================================
# Footer / legend
# =========================================================
'''
ax.plot(
    [1.0, 11.2],
    [1.2, 1.2],
    color="gray",
    lw=0.8
)


ax.text(
    1.2,
    0.85,
    "Notation: the bits marked with · are the remaining bits.",
    fontsize=9,
    color="dimgray"
)
'''

rounded_box(
    ax,
    1.2,
    1.8,
    0.22,
    0.22,
    fc=local_fill,
    ec=local_edge,
    radius=0.03
)

ax.text(
    1.55,
    1.9,
    "Local qubit / no comm.",
    fontsize=10,
    va="center"
)

rounded_box(
    ax,
    4.3,
    1.8,
    0.22,
    0.22,
    fc=global_fill,
    ec=global_edge,
    radius=0.03
)

ax.text(
    4.65,
    1.9,
    "Global qubit",
    fontsize=10,
    va="center"
)


# =========================================================
# Save
# =========================================================

plt.tight_layout()

plt.savefig(
    "local_vs_global_qubits_single-qubit_gate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()