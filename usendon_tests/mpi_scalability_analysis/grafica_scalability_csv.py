import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Estilo sin LaTeX externo ──────────────────────────────────────────────────
plt.rcParams.update({
    'text.usetex'           : False,
    'font.family'           : 'DejaVu Serif',
    'font.size'             : 13,
    'mathtext.fontset'      : 'dejavuserif',
    'axes.spines.top'       : True,
    'axes.spines.right'     : True,
    'axes.linewidth'        : 0.9,
    'xtick.direction'       : 'out',
    'ytick.direction'       : 'out',
    'xtick.major.width'     : 0.9,
    'ytick.major.width'     : 0.9,
    'xtick.major.size'      : 4,
    'ytick.major.size'      : 4,
    'legend.frameon'        : False,
    'legend.fontsize'       : 11,
    'figure.dpi'            : 150,
    'savefig.bbox'          : 'tight',
    'savefig.dpi'           : 300,
})

#C = {'LL': "#3BF6E6", 'LG': '#10B981', 'GG': '#F59E0B'}
C = {'LL': "darkcyan", 'LG': 'slateblue', 'GG':'darkorange'}
MARKERS = {'LL': 'o', 'LG': 's', 'GG': '^'}
MS = 7
LW = 1.8

df = pd.read_csv("scalability_with_threads.csv", na_values='-')
x  = df['Numero de nodos']

# ── Strong Scaling ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.5))

ax.plot(x, df['SC 0 1'],   color=C['LL'], marker=MARKERS['LL'], ms=MS, lw=LW, label='LL [0,1]')
ax.plot(x, df['SC 0 m'],   color=C['LG'], marker=MARKERS['LG'], ms=MS, lw=LW, label='LG [0,m]')
ax.plot(x, df['SC m m+1'], color=C['GG'], marker=MARKERS['GG'], ms=MS, lw=LW, label='GG [m,m+1]')

ax.set_xlabel('Number of nodes')
ax.set_ylabel('Time (s)')
#ax.set_title('Strong Scaling', fontstyle='italic', pad=10)
ax.legend(loc='best')
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.tight_layout()
plt.savefig("strong_scaling_con_threads.pdf")
plt.savefig("strong_scaling_con_threads.png")
plt.close()

# ── Weak Scaling ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.5))

ax.plot(x, df['WS 0 1'],   color=C['LL'], marker=MARKERS['LL'], ms=MS, lw=LW, label='LL [0,1]')
ax.plot(x, df['WS 0 m'],   color=C['LG'], marker=MARKERS['LG'], ms=MS, lw=LW, label='LG [0,m]')
ax.plot(x, df['WS m m+1'], color=C['GG'], marker=MARKERS['GG'], ms=MS, lw=LW, label='GG [m,m+1]')

ax.set_xlabel('Number of nodes')
ax.set_ylabel('Time (s)')
#ax.set_title('Weak Scaling', fontstyle='italic', pad=28)  # pad mayor para dejar sitio al eje superior
ax.legend(loc='best')
ax.xaxis.set_major_locator(ticker.FixedLocator(x))        # fija ticks en los nodos reales

# ── Eje superior con número de qubits ────────────────────────────────────────
# En weak scaling: nodos 1,2,4,8,16 → qubits 30,31,32,33,34
nodos   = df['Numero de nodos'].values
import numpy as np
qubits = 30 + np.log2(nodos).astype(int)   # weak scaling: +1 qubit por cada x2 nodos

ax2 = ax.twiny()                          # comparte eje Y, nuevo eje X arriba
ax2.set_xlim(ax.get_xlim())              # mismo rango que el eje inferior
ax2.set_xticks(nodos)
ax2.set_xticklabels(qubits)
ax2.set_xlabel('Number of qubits', labelpad=8)

plt.tight_layout()
plt.savefig("weak_scaling_con_threads.pdf")
plt.savefig("weak_scaling_con_threads.png")
plt.close()

# ── Speedup ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.5))

ax.plot(x, df['Speedup 0 1'],   color=C['LL'], marker=MARKERS['LL'], ms=MS, lw=LW, label='LL [0,1]')
ax.plot(x, df['Speedup 0 m'],   color=C['LG'], marker=MARKERS['LG'], ms=MS, lw=LW, label='LG [0,m]')
ax.plot(x, df['Speedup m m+1'], color=C['GG'], marker=MARKERS['GG'], ms=MS, lw=LW, label='GG [m,m+1]')

ax.plot(x, df['Ideal 0 1'],   color=C['LL'], lw=LW, ls='--', alpha=0.45, label='Ideal LL [0,1]')
ax.plot(x, df['Ideal 0 m'],   color=C['LG'], lw=LW, ls='--', alpha=0.45, label='Ideal LG [0,m]')
ax.plot(x, df['Ideal m m+1'], color=C['GG'], lw=LW, ls='--', alpha=0.45, label='Ideal GG [m,m+1]')

ax.set_xlabel('Number of nodes')
ax.set_ylabel('Speedup')
#ax.set_title('Speedup', fontstyle='italic', pad=10)
ax.legend(ncol=2, loc='upper left', handlelength=2.2, columnspacing=1.2)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

plt.tight_layout()
plt.savefig("speedup_con_threads.pdf")
plt.savefig("speedup_con_threads.png")
plt.close()

print("Figuras guardadas correctamente.")