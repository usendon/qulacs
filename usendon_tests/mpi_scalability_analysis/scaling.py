import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv("resultados_ecr.csv", comment="#")
df.columns = df.columns.str.strip()

# Separar strong y weak por columna m
strong = df[df["m"] != 30].copy()
weak   = df[df["m"] == 30].drop_duplicates(subset=["nqubits","nprocs","q1","q2"]).copy()

COLORS  = {"LL": "#2196F3", "LG": "#FF9800", "GG": "#F44336"}
MARKERS = {"LL": "o",       "LG": "s",        "GG": "^"}

# Pares representativos fijos por tipo:
# LL: (0,1)  → existe en 1,2,4,8,16 nodos
# LG: (0, primer global de cada config) → q1=0, q2=m (que varía)
# GG: (m, m+1) → los dos primeros globales de cada config
# Para LG y GG usamos el par donde q1=0,q2=m y q1=m,q2=m+1 respectivamente
# que equivale a filtrar por q1==0 para LG y q1==q2-1 para GG

def get_representative(df_tipo, tipo):
    if tipo == "LL":
        return df_tipo[(df_tipo["q1"] == 0) & (df_tipo["q2"] == 1)]
    elif tipo == "LG":
        # q1=0, q2=m (primer global)
        return df_tipo[(df_tipo["q1"] == 0) & (df_tipo["q2"] == df_tipo["m"])]
    elif tipo == "GG":
        # q1=m, q2=m+1 (dos primeros globales)
        return df_tipo[(df_tipo["q1"] == df_tipo["m"]) & (df_tipo["q2"] == df_tipo["m"] + 1)]

# ─────────────────────────────────────────────
# FIGURA 1: STRONG SCALING
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Strong Scaling (n=30 fijo) — Puerta ECR", fontsize=13, fontweight="bold")

for tipo in ["LL", "LG", "GG"]:
    subset = strong[strong["tipo"] == tipo]
    rep = get_representative(subset, tipo).sort_values("nprocs")

    if rep.empty:
        continue

    ax.plot(rep["nprocs"], rep["mean_time_s"],
            marker=MARKERS[tipo], color=COLORS[tipo],
            label=tipo, linewidth=2)

# Línea ideal basada en LL
ll_rep = get_representative(strong[strong["tipo"] == "LL"], "LL").sort_values("nprocs")
if not ll_rep.empty:
    nprocs = ll_rep["nprocs"].tolist()
    t0 = ll_rep["mean_time_s"].iloc[0]
    ideal = [t0 / (n / nprocs[0]) for n in nprocs]
    ax.plot(nprocs, ideal, "k--", linewidth=1, label="Ideal (LL)", alpha=0.5)

ax.set_xlabel("Número de procesos (nprocs)")
ax.set_ylabel("Tiempo medio (s)")
ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}"))
ax.legend(title="Tipo de par", fontsize=10)
ax.grid(True, which="both", linestyle="--", alpha=0.4)
ax.annotate("Par representativo:\nLL=(0,1)  LG=(0,m)  GG=(m,m+1)",
            xy=(0.02, 0.04), xycoords="axes fraction", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("strong_scaling.png", dpi=150, bbox_inches="tight")
plt.close()
print("Guardado: strong_scaling.png")

# ─────────────────────────────────────────────
# FIGURA 2: WEAK SCALING
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Weak Scaling (30 qubits/proceso) — Puerta ECR", fontsize=13, fontweight="bold")

for tipo in ["LL", "LG", "GG"]:
    subset = weak[weak["tipo"] == tipo]
    rep = get_representative(subset, tipo).sort_values("nprocs")

    if rep.empty:
        continue

    ax.plot(rep["nprocs"], rep["mean_time_s"],
            marker=MARKERS[tipo], color=COLORS[tipo],
            label=tipo, linewidth=2)

# Línea ideal: tiempo constante del primer punto de cada tipo
for tipo in ["LL", "LG", "GG"]:
    subset = weak[weak["tipo"] == tipo]
    rep = get_representative(subset, tipo).sort_values("nprocs")
    if rep.empty:
        continue
    t0 = rep["mean_time_s"].iloc[0]
    nprocs = rep["nprocs"].tolist()
    ax.hlines(t0, xmin=nprocs[0], xmax=nprocs[-1],
              colors=COLORS[tipo], linestyles="--", linewidth=1, alpha=0.5)

ax.set_xlabel("Número de procesos (nprocs)")
ax.set_ylabel("Tiempo medio (s)")
ax.set_xscale("log", base=2)
ax.set_yscale("log")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}"))
ax.legend(title="Tipo de par", fontsize=10)
ax.grid(True, which="both", linestyle="--", alpha=0.4)
ax.annotate("Par representativo:\nLL=(0,1)  LG=(0,m)  GG=(m,m+1)\n(línea discontinua = ideal)",
            xy=(0.02, 0.04), xycoords="axes fraction", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("weak_scaling.png", dpi=150, bbox_inches="tight")
plt.close()
print("Guardado: weak_scaling.png")

print("\nHecho.")