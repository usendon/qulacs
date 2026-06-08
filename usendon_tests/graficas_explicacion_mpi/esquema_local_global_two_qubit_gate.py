import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------- Helpers ----------
def rounded_box(ax, xy, w, h, text="", fc="#ffffff", ec="#000000",
                lw=1.5, fontsize=13, textcolor="black",
                weight="normal", radius=0.010):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.006,rounding_size={radius}",
        linewidth=lw, edgecolor=ec, facecolor=fc
    )
    ax.add_patch(patch)
    if text:
        ax.text(x + w/2, y + h/2, text,
                ha="center", va="center", fontsize=fontsize,
                color=textcolor, fontweight=weight)

# ---------- Figure ----------
fig, ax = plt.subplots(figsize=(18, 13), dpi=160)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

green       = "#2f7f66"
green_fill  = "#dff2ea"
purple      = "#8f5fc5"
purple_fill = "#f8f0ff"
black       = "black"

# ══════════════════════════════════════════════════════════════
# MAIN TITLE
# ══════════════════════════════════════════════════════════════
ax.text(0.5, 0.970, "Local vs global qubit operations for a two-qubit gate",
        ha="center", va="center", fontsize=18)

# ══════════════════════════════════════════════════════════════
# COLUMN CONSTANTS
# ══════════════════════════════════════════════════════════════
col_w   = 0.210
col_gap = 0.040
total_w = 3 * col_w + 2 * col_gap
x1      = (1.0 - total_w) / 2
x2      = x1 + col_w + col_gap
x3      = x2 + col_w + col_gap

# ══════════════════════════════════════════════════════════════
# TOP QUBIT ROW
# ══════════════════════════════════════════════════════════════
y_top     = 0.862
qb_h      = 0.043

local_labels  = ["0", "...", "q₀", "...", "q₁", "m-1"]
global_labels = ["m", "...", "q₀", "...", "q₁", "...", "n-1"]
n_local  = len(local_labels)
n_global = len(global_labels)
n_total  = n_local + n_global

row_w      = total_w
group_gap  = 0.008
qb_w   = 0.033
qb_gap = (row_w - n_total * qb_w - group_gap) / (n_total - 1)

xs = []
for i in range(n_local):
    xs.append(x1 + i * (qb_w + qb_gap))
for i in range(n_global):
    xs.append(x1 + n_local * (qb_w + qb_gap) + group_gap + i * (qb_w + qb_gap))

all_labels = local_labels + global_labels
for i, lab in enumerate(all_labels):
    ec = green if i < n_local else purple
    tc = black
    fc = green_fill if i < n_local else purple_fill
    rounded_box(ax, (xs[i], y_top), qb_w, qb_h,
                text=lab, fc=fc, ec=ec, lw=1.2,
                fontsize=13, textcolor=tc, radius=0.006)

sep_x = (xs[n_local - 1] + qb_w + xs[n_local]) / 2
ax.plot([sep_x, sep_x], [y_top - 0.005, y_top + qb_h + 0.005],
        color="black", lw=1.5, linestyle="--")

line_y = y_top - 0.018
tick_h = 0.007
lx0  = xs[0]
lx1_q = sep_x
gx0  = sep_x
gx1  = xs[-1] + qb_w

for x0, x1_end, col, label in [
    (lx0-0.005, lx1_q-0.01, black,  "local qubits  (0 ≤ q < m)"),
    (gx0+0.009, gx1+0.008,   black, "global qubits (m ≤ q < n)"),
]:
    ax.plot([x0, x1_end], [line_y, line_y], color=col, lw=1.4)
    ax.plot([x0, x0],     [line_y, line_y + tick_h], color=col, lw=1.4)
    ax.plot([x1_end, x1_end], [line_y, line_y + tick_h], color=col, lw=1.4)
    ax.text((x0 + x1_end) / 2, line_y - 0.012,
            label, ha="center", va="top", fontsize=13, color="black")

VGAP         = 0.026
CASE_TITLE_Y = 0.790
CONTENT_TOP  = 0.76

# ══════════════════════════════════════════════════════════════
# CASE 1 — both local
# ══════════════════════════════════════════════════════════════
ax.text(x1 + col_w/2, CASE_TITLE_Y, "Case 1: both local",
        ha="center", va="center", fontsize=15, color=black)

amp_w    = 0.075
amp_h    = 0.080
amp_hgap = 0.016
amp_vgap = 0.022
grid_w   = 2 * amp_w + amp_hgap
grid_h   = 2 * amp_h + amp_vgap

title_h1    = 0.030
subtitle_h1 = 0.044
pad_top1    = 0.012
pad_bot1    = 0.016
between1    = 0.010
c1_main_h   = pad_top1 + title_h1 + between1 + subtitle_h1 + between1 + grid_h + pad_bot1
c1_main_y   = CONTENT_TOP - c1_main_h

rounded_box(ax, (x1, c1_main_y), col_w, c1_main_h,
            fc=green_fill, ec=green, lw=1.3)

ax.text(x1 + col_w/2,
        c1_main_y + c1_main_h - pad_top1 - title_h1/2,
        "Process p", ha="center", va="center", fontsize=16, color=green)
ax.text(x1 + col_w/2,
        c1_main_y + c1_main_h - pad_top1 - title_h1 - between1 - subtitle_h1/2,
        "all 3 amplitudes here\n(the bits at 0 or 1 are q₀ and q₁)",
        ha="center", va="center", fontsize=13, color=green)

grid_x = x1 + (col_w - grid_w) / 2
top_y  = c1_main_y + pad_bot1 + amp_h + amp_vgap
bot_y  = c1_main_y + pad_bot1

amp_coords = [
    (grid_x,                          top_y),
    (grid_x + amp_w + amp_hgap,      top_y),
    (grid_x + (amp_w + amp_hgap)/2,  bot_y),
]

labels = [
    r"$\alpha_{...0...1...}$",
    r"$\alpha_{...1...1...}$",
    r"$\alpha_{...0...0...}$"
]

for coord, lab in zip(amp_coords, labels):
    rounded_box(ax, coord, amp_w, amp_h,
                text=lab, fc="#f6fbf9", ec=green,
                fontsize=15, radius=0.007)

def center(xy):
    x, y = xy
    return (x + amp_w/2, y + amp_h/2)

c_top_left  = center(amp_coords[0])
c_top_right = center(amp_coords[1])
c_bottom    = center(amp_coords[2])

ax.annotate("", xy=c_bottom, xytext=c_top_left,
            arrowprops=dict(arrowstyle="<->", color=green, lw=2, shrinkA=32, shrinkB=32))
ax.annotate("", xy=c_bottom, xytext=c_top_right,
            arrowprops=dict(arrowstyle="<->", color=green, lw=2, shrinkA=32, shrinkB=32))

# The bottom of Case 1's main box — Cases 2 & 3 will align their first process box to this
c1_main_bottom = c1_main_y

# ══════════════════════════════════════════════════════════════
# CASE 2 — one local, one global
# ══════════════════════════════════════════════════════════════
ax.text(x2 + col_w/2, CASE_TITLE_Y, "Case 2: one local, one global",
        ha="center", va="center", fontsize=15, color=black)

amp2_w = 0.090
amp2_h = 0.066

c2_title_h    = 0.028
c2_subtitle_h = 0.024
c2_pad_top    = 0.010
c2_pad_bot    = 0.012
c2_between    = 0.008
c2_proc_h     = c2_pad_top + c2_title_h + c2_between + c2_subtitle_h + c2_between + amp2_h + c2_pad_bot

# ── Box D: Process p (glob=0) — top aligned with Case 1's outer box top ──
c2_D_top = c1_main_y + c1_main_h   # = CONTENT_TOP, same top edge as Case 1's box
c2_D_y   = c2_D_top - c2_proc_h

rounded_box(ax, (x2, c2_D_y), col_w, c2_proc_h,
            fc=green_fill, ec=green, lw=1.3)
ax.text(x2 + col_w/2,
        c2_D_y + c2_proc_h - c2_pad_top - c2_title_h/2,
        "Process p", ha="center", va="center", fontsize=16, color=green)
ax.text(x2 + col_w/2,
        c2_D_y + c2_proc_h - c2_pad_top - c2_title_h - c2_between - c2_subtitle_h/2,
        f"bit $(q_1 - m)$ = 0 in rank",
        ha="center", va="center", fontsize=13, color=green)
rounded_box(ax, (x2 + (col_w - amp2_w)/2,
                 c2_D_y + c2_pad_bot),
            amp2_w, amp2_h,
            text="$\\alpha_{...0...}$", fc="#eef7f3", ec=green, fontsize=15)

# ── Box C: MPI exchange bar ──
c2_C_h   = 0.034
c2_C_top = c2_D_y - VGAP
c2_C_y   = c2_C_top - c2_C_h
rounded_box(ax, (x2, c2_C_y), col_w, c2_C_h,
            text=f"MPI exchange (flip bit $(q_1-m)$)",
            fc=purple_fill, ec=purple, lw=1.3, fontsize=13, textcolor=purple)

arrow_x = x2 + col_w/2
ax.annotate(
    "",
    xy=(arrow_x, c2_C_y + c2_C_h + 0.023),
    xytext=(arrow_x, c2_C_y - 0.023),
    arrowprops=dict(arrowstyle="<->", color=purple, lw=2),
    zorder=0
)

# ── Box B: Process p′ (glob=1) ──
c2_B_top = c2_C_y - VGAP
c2_B_y   = c2_B_top - c2_proc_h

rounded_box(ax, (x2, c2_B_y), col_w, c2_proc_h,
            fc=purple_fill, ec=purple, lw=1.3)
ax.text(x2 + col_w/2,
        c2_B_y + c2_proc_h - c2_pad_top - c2_title_h/2,
        "Process p′", ha="center", va="center", fontsize=16, color=purple)
ax.text(x2 + col_w/2,
        c2_B_y + c2_proc_h - c2_pad_top - c2_title_h - c2_between - c2_subtitle_h/2,
        f"bit $(q_1-m)$ = 1 in rank",
        ha="center", va="center", fontsize=13, color=purple)
rounded_box(ax, (x2 + (col_w - amp2_w)/2,
                 c2_B_y + c2_pad_bot),
            amp2_w, amp2_h,
            text="$\\alpha_{...1...}$", fc="#faf9ff", ec=purple, fontsize=15)

# ══════════════════════════════════════════════════════════════
# CASE 3 — both global
# ══════════════════════════════════════════════════════════════
ax.text(x3 + col_w/2, CASE_TITLE_Y,
        "Case 3: both global",
        ha="center", va="center",
        fontsize=15, color=black)

amp3_w = 0.090
amp3_h = 0.056

c3_title_h = 0.028
c3_pad_top  = 0.010
c3_pad_bot  = 0.012
c3_between  = 0.008
c3_proc_h   = c3_pad_top + c3_title_h + c3_between + amp3_h + c3_pad_bot
c3_mpi_h    = 0.034


def draw_proc3(ax, bx, bw, top_y, title, amp_text,
               box_fc, box_ec,
               title_h, pad_top, pad_bot, between,
               amp_w, amp_h, proc_h):
    by = top_y - proc_h
    rounded_box(ax, (bx, by), bw, proc_h,
                fc=box_fc, ec=box_ec, lw=1.3)
    ax.text(bx + bw/2,
            by + proc_h - pad_top - title_h/2,
            title,
            ha="center", va="center",
            fontsize=15, color=box_ec)
    rounded_box(ax,
                (bx + (bw - amp_w)/2, by + pad_bot),
                amp_w, amp_h,
                text=amp_text,
                fc="#faf9ff",
                ec=box_ec,
                fontsize=15,
                radius=0.007)
    return by


def draw_mpi3(ax, bx, bw, top_y, text, h):
    by = top_y - h
    rounded_box(ax, (bx, by), bw, h,
                text=text,
                fc=purple_fill,
                ec=purple,
                lw=1.3,
                fontsize=13,
                textcolor=purple)
    return by


# Start Case 3 at the same level as Case 2's first process box
start_y = c2_D_top

c3_F_bottom = draw_proc3(
    ax, x3, col_w,
    start_y,
    "Process p′",
    r"$\alpha_{...0...1...}$",
    purple_fill, purple,
    c3_title_h, c3_pad_top, c3_pad_bot,
    c3_between, amp3_w, amp3_h, c3_proc_h
)

c3_E_bottom = draw_mpi3(
    ax, x3, col_w,
    c3_F_bottom - VGAP,
    f"MPI exchange 1  (flip bit $(q_0-m)$)",
    c3_mpi_h
)

arrow_x = x3 + col_w/2

ax.annotate(
    "",
    xy=(arrow_x, c3_E_bottom + 0.057),   # arriba del MPI
    xytext=(arrow_x, c3_E_bottom - 0.023),  # abajo del MPI
    arrowprops=dict(
        arrowstyle="<->",
        color=purple,
        lw=2
    ),
    zorder=0
)

c3_D_bottom = draw_proc3(
    ax, x3, col_w,
    c3_E_bottom - VGAP,
    "Process p",
    r"$\alpha_{...0...0...}$",
    purple_fill, purple,
    c3_title_h, c3_pad_top, c3_pad_bot,
    c3_between, amp3_w, amp3_h, c3_proc_h
)

c3_C_bottom = draw_mpi3(
    ax, x3, col_w,
    c3_D_bottom - VGAP,
    f"MPI exchange 2 \n (flip bits $(q_0-m)$ and $(q_1-m)$)",
    c3_mpi_h
)

arrow_x = x3 + col_w/2

ax.annotate(
    "",
    xy=(arrow_x, c3_C_bottom + 0.057),   # arriba del MPI
    xytext=(arrow_x, c3_C_bottom - 0.023),  # abajo del MPI
    arrowprops=dict(
        arrowstyle="<->",
        color=purple,
        lw=2
    ),
    zorder=0
)

c3_B_bottom = draw_proc3(
    ax, x3, col_w,
    c3_C_bottom - VGAP,
    "Process p′′",
    r"$\alpha_{...1...1...}$",
    purple_fill, purple,
    c3_title_h, c3_pad_top, c3_pad_bot,
    c3_between, amp3_w, amp3_h, c3_proc_h
)

# ══════════════════════════════════════════════════════════════
# LEGEND (bottom)
# ══════════════════════════════════════════════════════════════
leg_y  = 0.17
leg_h  = 0.008
leg_w  = leg_h * (13 / 18)

rounded_box(ax, (0.14, leg_y), leg_w, leg_h, fc=green_fill, ec=green, lw=1.2, radius=0.0)
ax.text(0.12 + leg_w + 0.028, leg_y + leg_h/2,
        "  Local qubit / no comm.", ha="left", va="center", fontsize=13)

rounded_box(ax, (0.35, leg_y), leg_w, leg_h, fc=purple_fill, ec=purple, lw=1.2, radius=0.0)
ax.text(0.35 + leg_w + 0.008, leg_y + leg_h/2,
        "  Global qubit", ha="left", va="center", fontsize=13)
plt.tight_layout()
plt.savefig("local_vs_global_qubits_two-qubit_gate.png",
            dpi=160, bbox_inches="tight", facecolor="white")
plt.close()
print("Saved.")