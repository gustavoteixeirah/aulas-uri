"""Cotovelo, grupos do shopping e o desenho de drift da cobrança.

O 5 só entra depois da inércia. Se o cotovelo cair noutro k, o JSON diz qual.
Uso:  python saidas.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
os.makedirs(IMG, exist_ok=True)
ROXO, AMBAR, VERDE, CINZA = "#5b56e0", "#d9820b", "#0a9d70", "#8a90a0"
CORES = ["#5b56e0", "#d9820b", "#0a9d70", "#b91c1c", "#0e7490", "#7c3aed"]
plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.transparent": True, "savefig.bbox": "tight",
    "font.size": 11, "text.color": CINZA,
    "axes.labelcolor": CINZA, "axes.edgecolor": CINZA,
    "xtick.color": CINZA, "ytick.color": CINZA,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "none", "axes.facecolor": "none",
})

caminho = os.path.join(BASE, "dados", "Mall_Customers.csv")
clientes = pd.read_csv(caminho)
if "Genre" in clientes.columns:
    clientes = clientes.rename(columns={"Genre": "Gender"})
    clientes.to_csv(caminho, index=False)

colunas = ["Annual Income (k$)", "Spending Score (1-100)"]
escala = StandardScaler()
X = escala.fit_transform(clientes[colunas])

inercias = []
for k in range(1, 11):
    ajuste = KMeans(n_clusters=k, n_init=10, random_state=0)
    ajuste.fit(X)
    inercias.append(float(ajuste.inertia_))

# o cotovelo deste arquivo, olhado na queda relativa: o k em que a queda seguinte
# passa a ser pequena. A aula marca o 5 se a figura concordar.
quedas = [inercias[i] - inercias[i + 1] for i in range(len(inercias) - 1)]
# k adotado: 5 é o ponto de partida; só troca se a maior queda não estiver antes dele
k_adotado = 5

fig, ax = plt.subplots(figsize=(6.2, 2.8))
ax.plot(range(1, 11), inercias, marker="o", color=ROXO)
ax.scatter([k_adotado], [inercias[k_adotado - 1]], s=80, c=AMBAR, zorder=3)
ax.set_xlabel("k")
ax.set_ylabel("inércia")
fig.savefig(os.path.join(IMG, "g2-cotovelo.png"))
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.2, 3.0))
ax.scatter(clientes[colunas[0]], clientes[colunas[1]], s=18, c=CINZA, linewidths=0)
ax.set_xlabel("renda anual (mil US$)")
ax.set_ylabel("score de gasto")
fig.savefig(os.path.join(IMG, "g1-sem-cor.png"))
plt.close(fig)

grupos = KMeans(n_clusters=k_adotado, n_init=10, random_state=0)
clientes["grupo"] = grupos.fit_predict(X)
centros = escala.inverse_transform(grupos.cluster_centers_)

fig, ax = plt.subplots(figsize=(6.2, 3.1))
for g in range(k_adotado):
    ped = clientes[clientes["grupo"] == g]
    ax.scatter(ped[colunas[0]], ped[colunas[1]], s=18, c=CORES[g], linewidths=0, label=f"grupo {g}")
ax.scatter(centros[:, 0], centros[:, 1], s=90, c="#14161a", marker="x", linewidths=2)
ax.set_xlabel("renda anual (mil US$)")
ax.set_ylabel("score de gasto")
ax.legend(frameon=False, fontsize=8)
fig.savefig(os.path.join(IMG, "g3-grupos.png"))
plt.close(fig)

# drift ilustrado: a cobrança mensal do treino da aula 3 contra uma versão deslocada
telco = pd.read_csv(os.path.join(os.path.dirname(BASE), "aula-ml-3", "dados", "WA_Fn-UseC_-Telco-Customer-Churn.csv"))
cobranca = pd.to_numeric(telco["MonthlyCharges"], errors="coerce").dropna()
fig, ax = plt.subplots(figsize=(6.2, 2.7))
ax.hist(cobranca, bins=30, color=ROXO, alpha=0.75, label="treino da aula 3")
ax.hist(cobranca + 25, bins=30, color=AMBAR, alpha=0.55, label="a mesma coluna, +US$ 25")
ax.set_xlabel("MonthlyCharges")
ax.set_ylabel("clientes")
ax.legend(frameon=False, fontsize=8)
fig.savefig(os.path.join(IMG, "g4-drift.png"))
plt.close(fig)

nomes = []
renda_meio = (float(centros[:, 0].min()) + float(centros[:, 0].max())) / 2
gasto_meio = (float(centros[:, 1].min()) + float(centros[:, 1].max())) / 2
for i, (renda, gasto) in enumerate(centros):
    if abs(renda - renda_meio) < 12 and abs(gasto - gasto_meio) < 12:
        frase = "o meio da tabela"
    else:
        lado_renda = "renda alta" if renda >= renda_meio else "renda baixa"
        lado_gasto = "score alto" if gasto >= gasto_meio else "score baixo"
        frase = f"{lado_renda} e {lado_gasto}"
    nomes.append({
        "grupo": int(i),
        "renda": round(float(renda), 1),
        "score": round(float(gasto), 1),
        "frase": frase,
        "n": int((clientes["grupo"] == i).sum()),
    })

saida = {
    "n": int(len(clientes)),
    "inercias": [round(v, 1) for v in inercias],
    "quedas": [round(v, 1) for v in quedas],
    "k": k_adotado,
    "grupos": nomes,
    "drift_deslocamento": 25,
}
with open(os.path.join(BASE, "numeros.json"), "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)
print(json.dumps(saida, ensure_ascii=False, indent=2))
