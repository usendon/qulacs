import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------- Helpers ----------
def rounded_box(ax, xy, w, h, text="", fc="#ffffff", ec="#000000",
                lw=1.5, fontsize=12, textcolor="black",
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
ax.text(0.5, 0.970, "Local vs global qubit operations",
        ha="center", va="center", fontsize=18)
ax.text(0.5, 0.940,
        "(two-qubit gates: q₀ and q₁ are the two target qubits; gate applied as G(q₀, q₁))",
        ha="center", va="center", fontsize=10, color="dimgray")

# ══════════════════════════════════════════════════════════════
# COLUMN CONSTANTS  (defined first so qubit row can align to them)
# ══════════════════════════════════════════════════════════════
col_w   = 0.210
col_gap = 0.040
total_w = 3 * col_w + 2 * col_gap
x1      = (1.0 - total_w) / 2   # left edge of col 1, centred on figure
x2      = x1 + col_w + col_gap
x3      = x2 + col_w + col_gap

# ══════════════════════════════════════════════════════════════
# TOP QUBIT ROW  — aligned so it spans exactly x1..x3+col_w
# ══════════════════════════════════════════════════════════════
y_top     = 0.862
qb_h      = 0.043

local_labels  = ["0", "...", "q₀", "...", "q₁", "m-1"]
global_labels = ["m", "...", "q₀", "...", "q₁", "...", "n-1"]
n_local  = len(local_labels)
n_global = len(global_labels)
n_total  = n_local + n_global

# Distribute qubit boxes evenly across [x1, x3+col_w]
row_w      = total_w                        # same total width as the three columns
group_gap  = 0.008                          # extra gap between local and global groups
# Each box gets equal pitch; solve: n_total*qb_w + (n_total-1)*qb_gap + group_gap = row_w
# We fix qb_w and derive qb_gap:
qb_w   = 0.033
slots  = n_total - 1  # number of inter-box gaps (one of which is replaced by group_gap)
# total gaps space = row_w - n_total*qb_w - group_gap  spread over (slots-1) regular gaps
qb_gap = (row_w - n_total * qb_w - group_gap) / (n_total - 1)

xs = []
for i in range(n_local):
    xs.append(x1 + i * (qb_w + qb_gap))
for i in range(n_global):
    # after last local box: add one extra group_gap on top of the normal qb_gap
    xs.append(x1 + n_local * (qb_w + qb_gap) + group_gap + i * (qb_w + qb_gap))

all_labels = local_labels + global_labels
for i, lab in enumerate(all_labels):
    ec = green if i < n_local else purple
    tc = green if i < n_local else purple
    fc = green_fill if i < n_local else purple_fill
    rounded_box(ax, (xs[i], y_top), qb_w, qb_h,
                text=lab, fc=fc, ec=ec, lw=1.2,
                fontsize=11, textcolor=tc, radius=0.006)

sep_x = (xs[n_local - 1] + qb_w + xs[n_local]) / 2
ax.plot([sep_x, sep_x], [y_top - 0.005, y_top + qb_h + 0.005],
        color="black", lw=1.5, linestyle="--")

line_y = y_top - 0.018
tick_h = 0.007
lx0  = xs[0]
lx1_q = sep_x          # local bracket extends to the separator
gx0  = sep_x           # global bracket starts from the separator
gx1  = xs[-1] + qb_w

for x0, x1_end, col, label in [
    (lx0-0.005, lx1_q-0.01, black,  "local  (0 ≤ q < m)"),
    (gx0+0.009, gx1+0.008,   black, "global  (m ≤ q < n)"),
]:
    ax.plot([x0, x1_end], [line_y, line_y], color=col, lw=1.4)
    ax.plot([x0, x0],     [line_y, line_y + tick_h], color=col, lw=1.4)
    ax.plot([x1_end, x1_end], [line_y, line_y + tick_h], color=col, lw=1.4)
    ax.text((x0 + x1_end) / 2, line_y - 0.012,
            label, ha="center", va="top", fontsize=11, color="black")

VGAP         = 0.026   # uniform gap between every pair of consecutive boxes
CASE_TITLE_Y = 0.790
# First box top edge = just below the case title
CONTENT_TOP  = CASE_TITLE_Y - 0.033

# ──────────────────────────────────────────────────────────────
# HELPER: draw a "process" box that contains a title line,
# an optional subtitle line, and an amplitude sub-box.
# Returns the bottom y of the outer box.
# ──────────────────────────────────────────────────────────────
def process_box(ax, bx, top_y, bw,
                title, title_fs, title_col, title_h,
                subtitle, subtitle_fs, subtitle_col, subtitle_h,
                amp_text, amp_w, amp_h,
                box_fc, box_ec, box_lw=1.3,
                inner_pad_top=0.010, inner_pad_bot=0.012, inner_pad_between=0.006):
    """
    Layout (top→bottom inside the box):
      inner_pad_top
      title_h
      inner_pad_between  (only if subtitle)
      subtitle_h         (only if subtitle)
      inner_pad_between
      amp_h
      inner_pad_bot
    """
    has_subtitle = bool(subtitle)
    total_h = (inner_pad_top + title_h
               + (inner_pad_between + subtitle_h if has_subtitle else 0)
               + inner_pad_between + amp_h
               + inner_pad_bot)
    box_y = top_y - total_h

    rounded_box(ax, (bx, box_y), bw, total_h,
                fc=box_fc, ec=box_ec, lw=box_lw)

    # title
    ty = box_y + total_h - inner_pad_top - title_h / 2
    ax.text(bx + bw/2, ty, title,
            ha="center", va="center", fontsize=title_fs, color=title_col)

    # subtitle
    if has_subtitle:
        sy = ty - title_h/2 - inner_pad_between - subtitle_h/2
        ax.text(bx + bw/2, sy, subtitle,
                ha="center", va="center", fontsize=subtitle_fs, color=subtitle_col)
        amp_top = sy - subtitle_h/2 - inner_pad_between
    else:
        amp_top = ty - title_h/2 - inner_pad_between

    # amplitude sub-box (centred horizontally)
    amp_x = bx + (bw - amp_w) / 2
    amp_y = amp_top - amp_h
    rounded_box(ax, (amp_x, amp_y), amp_w, amp_h,
                text=amp_text, fc="white", ec=box_ec, fontsize=12, radius=0.007)

    return box_y   # bottom of outer box

# ──────────────────────────────────────────────────────────────
# CASE 1 — both local
# Boxes (top→bottom): process-p (big, with 2×2 grid) | footer
# ──────────────────────────────────────────────────────────────
ax.text(x1 + col_w/2, CASE_TITLE_Y, "Case 1: both local",
        ha="center", va="center", fontsize=15, color=black)

# 2×2 grid dimensions
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

# title
ax.text(x1 + col_w/2,
        c1_main_y + c1_main_h - pad_top1 - title_h1/2,
        "Process p", ha="center", va="center", fontsize=16, color=green)
# subtitle
ax.text(x1 + col_w/2,
        c1_main_y + c1_main_h - pad_top1 - title_h1 - between1 - subtitle_h1/2,
        "all 4 amplitudes here\n(the bits at 0 or 1 are q₀ and q₁)",
        ha="center", va="center", fontsize=11, color=green)

# 2×2 grid centred horizontally, sitting above pad_bot1
grid_x = x1 + (col_w - grid_w) / 2
grid_y = c1_main_y + pad_bot1

amp_coords = [
    (grid_x,                    grid_y + amp_h + amp_vgap),
    (grid_x + amp_w + amp_hgap, grid_y + amp_h + amp_vgap),
    (grid_x,                    grid_y),
    (grid_x + amp_w + amp_hgap, grid_y),
]
for coord, lab in zip(amp_coords,
                      [r"$\alpha_{·0·0·}$", r"$\alpha_{·0·1·}$",
                       r"$\alpha_{·1·0·}$", r"$\alpha_{·1·1·}$"]):
    rounded_box(ax, coord, amp_w, amp_h,
                text=lab, fc="white", ec=green, fontsize=13, radius=0.007)

mid_x     = grid_x + amp_w + amp_hgap / 2
mid_y_top = grid_y + amp_h + amp_vgap + amp_h / 2
mid_y_bot = grid_y + amp_h / 2
mid_xl    = grid_x + amp_w / 2
mid_xr    = grid_x + amp_w + amp_hgap + amp_w / 2
ax.text(mid_x,  mid_y_top, "↔", fontsize=26, color=green, ha="center", va="center")
ax.text(mid_x,  mid_y_bot, "↔", fontsize=26, color=green, ha="center", va="center")
ax.text(mid_xl, grid_y + amp_h + amp_vgap/2, "↕", fontsize=26, color=green, ha="center", va="center")
ax.text(mid_xr, grid_y + amp_h + amp_vgap/2, "↕", fontsize=26, color=green, ha="center", va="center")

# footer — VGAP below the process box
c1_footer_h = 0.036
c1_footer_y = c1_main_y - VGAP - c1_footer_h
rounded_box(ax, (x1, c1_footer_y), col_w, c1_footer_h,
            text="No MPI communication",
            fc=green_fill, ec=green, lw=1.3, fontsize=12, textcolor=green)

# ──────────────────────────────────────────────────────────────
# CASE 2 — one local, one global
# Boxes (top→bottom): explanation | proc-p | MPI-bar | proc-p′ | footer
# ──────────────────────────────────────────────────────────────
ax.text(x2 + col_w/2, CASE_TITLE_Y, "Case 2: one local, one global",
        ha="center", va="center", fontsize=15, color=black)

amp2_w = 0.090
amp2_h = 0.066

# ── Box E: explanation (5 lines) ──
c2_E_h = 0.128
c2_E_y = CONTENT_TOP - c2_E_h
rounded_box(ax, (x2, c2_E_y), col_w, c2_E_h,
            fc=purple_fill, ec=purple, lw=1.3)
ax.text(x2 + col_w/2, c2_E_y + c2_E_h/2,
        "Partner p′ = flip the bit of the\n"
        "higher-index qubit in rank(p).\n"
        "This higher-index qubit can be q₀\n"
        "or q₁ and it corresponds to the\n"
        "global qubit, denoted as glob.",
        ha="center", va="center", fontsize=11, color=purple)

# ── Box D: Process p (glob=0) ──
# height = pad_top + title + between + subtitle + between + amp + pad_bot
c2_title_h    = 0.028
c2_subtitle_h = 0.024
c2_pad_top    = 0.010
c2_pad_bot    = 0.012
c2_between    = 0.008
c2_proc_h     = c2_pad_top + c2_title_h + c2_between + c2_subtitle_h + c2_between + amp2_h + c2_pad_bot

c2_D_top = c2_E_y - VGAP
c2_D_y   = c2_D_top - c2_proc_h
rounded_box(ax, (x2, c2_D_y), col_w, c2_proc_h,
            fc=green_fill, ec=green, lw=1.3)
ax.text(x2 + col_w/2,
        c2_D_y + c2_proc_h - c2_pad_top - c2_title_h/2,
        "Process p", ha="center", va="center", fontsize=15, color=green)
ax.text(x2 + col_w/2,
        c2_D_y + c2_proc_h - c2_pad_top - c2_title_h - c2_between - c2_subtitle_h/2,
        "glob bit = 0 in rank",
        ha="center", va="center", fontsize=10.5, color=green)
rounded_box(ax, (x2 + (col_w - amp2_w)/2,
                 c2_D_y + c2_pad_bot),
            amp2_w, amp2_h,
            text="$\\alpha_{·0·}$\n(glob=0)", fc="white", ec=green, fontsize=12)

# ── Box C: MPI exchange bar ──
c2_C_h   = 0.034
c2_C_top = c2_D_y - VGAP
c2_C_y   = c2_C_top - c2_C_h
rounded_box(ax, (x2, c2_C_y), col_w, c2_C_h,
            text="MPI exchange 1 (flip bit glob)",
            fc=purple_fill, ec=purple, lw=1.3, fontsize=11, textcolor=purple)

# ── Box B: Process p′ (glob=1) ──
c2_B_top = c2_C_y - VGAP
c2_B_y   = c2_B_top - c2_proc_h
rounded_box(ax, (x2, c2_B_y), col_w, c2_proc_h,
            fc=purple_fill, ec=purple, lw=1.3)
ax.text(x2 + col_w/2,
        c2_B_y + c2_proc_h - c2_pad_top - c2_title_h/2,
        "Process p′", ha="center", va="center", fontsize=15, color=purple)
ax.text(x2 + col_w/2,
        c2_B_y + c2_proc_h - c2_pad_top - c2_title_h - c2_between - c2_subtitle_h/2,
        "glob bit = 1 in rank",
        ha="center", va="center", fontsize=10.5, color=purple)
rounded_box(ax, (x2 + (col_w - amp2_w)/2,
                 c2_B_y + c2_pad_bot),
            amp2_w, amp2_h,
            text="$\\alpha_{·1·}$\n(glob=1)", fc="white", ec=purple, fontsize=12)

# ── Footer ──
c2_footer_h = 0.036
c2_footer_y = c2_B_y - VGAP - c2_footer_h
rounded_box(ax, (x2, c2_footer_y), col_w, c2_footer_h,
            text="1 MPI communication step",
            fc=purple_fill, ec=purple, lw=1.3, fontsize=12, textcolor=purple)

# ──────────────────────────────────────────────────────────────
# CASE 3 — both global
# Boxes (top→bottom): partner-info | proc-p | MPI-1 | proc-p′ | MPI-2 | proc-p″ | footer
# ──────────────────────────────────────────────────────────────
ax.text(x3 + col_w/2, CASE_TITLE_Y, "Case 3: both global",
        ha="center", va="center", fontsize=15, color=black)

amp3_w = 0.090
amp3_h = 0.056

# Process box sizes for case 3 (no subtitle, just title + amp)
c3_title_h = 0.028
c3_pad_top  = 0.010
c3_pad_bot  = 0.012
c3_between  = 0.008
c3_proc_h   = c3_pad_top + c3_title_h + c3_between + amp3_h + c3_pad_bot

c3_mpi_h    = 0.034
c3_footer_h = 0.036

# ── Box G: partner info ──
c3_G_h = 0.096
c3_G_y = CONTENT_TOP - c3_G_h
rounded_box(ax, (x3, c3_G_y), col_w, c3_G_h,
            fc=purple_fill, ec=purple, lw=1.3)
ax.text(x3 + col_w/2, c3_G_y + c3_G_h - 0.025,
        "Partner qubits in rank p",
        ha="center", va="center", fontsize=13, color=purple)
ax.text(x3 + col_w/2, c3_G_y + c3_G_h/2 - 0.010,
        "Partner p′:  flip bit q₀ in rank p\nPartner p′′: flip bits q₀ and q₁ in rank p",
        ha="center", va="center", fontsize=10.5, color=purple)

def draw_proc3(ax, bx, bw, top_y, title, amp_text,
               box_fc, box_ec,
               title_h, pad_top, pad_bot, between, amp_w, amp_h, proc_h):
    """Draw a case-3 process box (title + amp sub-box). Returns bottom y."""
    by = top_y - proc_h
    rounded_box(ax, (bx, by), bw, proc_h, fc=box_fc, ec=box_ec, lw=1.3)
    ax.text(bx + bw/2, by + proc_h - pad_top - title_h/2,
            title, ha="center", va="center", fontsize=15, color=box_ec)
    rounded_box(ax, (bx + (bw - amp_w)/2, by + pad_bot),
                amp_w, amp_h,
                text=amp_text, fc="white", ec=box_ec, fontsize=12, radius=0.007)
    return by

def draw_mpi3(ax, bx, bw, top_y, text, h):
    """Draw an MPI bar. Returns bottom y."""
    by = top_y - h
    rounded_box(ax, (bx, by), bw, h, text=text,
                fc=purple_fill, ec=purple, lw=1.3, fontsize=11, textcolor=purple)
    return by

# Build case 3 top-down
c3_F_bottom = draw_proc3(ax, x3, col_w, c3_G_y - VGAP,
    "Process p", r"$\alpha_{·0·0·},\alpha_{·0·1·}$",
    purple_fill, purple,
    c3_title_h, c3_pad_top, c3_pad_bot, c3_between, amp3_w, amp3_h, c3_proc_h)

c3_E_bottom = draw_mpi3(ax, x3, col_w, c3_F_bottom - VGAP,
    "MPI exchange 1  (flip bit q₀)", c3_mpi_h)

c3_D_bottom = draw_proc3(ax, x3, col_w, c3_E_bottom - VGAP,
    "Process p′*", r"$\alpha_{·1·0·}$",
    purple_fill, purple,
    c3_title_h, c3_pad_top, c3_pad_bot, c3_between, amp3_w, amp3_h, c3_proc_h)

c3_C_bottom = draw_mpi3(ax, x3, col_w, c3_D_bottom - VGAP,
    "MPI exchange 2  (flip bits q₀ and q₁)", c3_mpi_h)

c3_B_bottom = draw_proc3(ax, x3, col_w, c3_C_bottom - VGAP,
    "Process p′′", r"$\alpha_{·1·1·}$",
    purple_fill, purple,
    c3_title_h, c3_pad_top, c3_pad_bot, c3_between, amp3_w, amp3_h, c3_proc_h)

c3_footer_y = c3_B_bottom - VGAP - c3_footer_h
rounded_box(ax, (x3, c3_footer_y), col_w, c3_footer_h,
            text="2 MPI communication steps",
            fc=purple_fill, ec=purple, lw=1.3, fontsize=12, textcolor=purple)

# ══════════════════════════════════════════════════════════════
# LEGEND
# ══════════════════════════════════════════════════════════════
# place legend below the lowest footer of the three columns
lowest_y = min(c1_footer_y, c2_footer_y, c3_footer_y)
legend_line_y = lowest_y - 0.022
ax.plot([x1, x3 + col_w], [legend_line_y, legend_line_y], color="#cccccc", lw=1)

note_y = legend_line_y - 0.018
ax.text(x1, note_y,
        "Notation: the bits marked with · are the remaining bits. *q₀ is suppossed to be the higger qubit index for simplicity.",
        fontsize=11.5, va="center")

swatch_y   = note_y - 0.045
swatch_h   = 0.022
swatch_w   = 0.016
for fc, ec, label, lx in [
    (green_fill,  green,  "Local qubit / no comm.", x1),
    (purple_fill, purple, "Global qubit",           x1 + 0.30),
]:
    patch = FancyBboxPatch((lx, swatch_y), swatch_w, swatch_h,
                           boxstyle="round,pad=0.002,rounding_size=0.004",
                           linewidth=1.2, edgecolor=ec, facecolor=fc)
    ax.add_patch(patch)
    ax.text(lx + swatch_w + 0.010, swatch_y + swatch_h/2,
            label, fontsize=11.5, va="center")

# Expand ylim so bbox_inches="tight" includes the swatches
ax.set_ylim(swatch_y - 0.015, 1)

plt.savefig("local_vs_global_qubits_two-qubit_gate.png",
            dpi=300, bbox_inches="tight")
print("Saved.")