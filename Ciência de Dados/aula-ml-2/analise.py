"""Gráficos da análise do consumo de cerveja, antes da regressão.

Uso: python analise.py
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
os.makedirs(IMG, exist_ok=True)

ROXO, AMBAR, CINZA = "#5b56e0", "#d9820b", "#8a90a0"
plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.transparent": True, "savefig.bbox": "tight",
    "font.size": 11, "text.color": CINZA,
    "axes.labelcolor": CINZA, "axes.edgecolor": CINZA,
    "xtick.color": CINZA, "ytick.color": CINZA,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "none", "axes.facecolor": "none",
})

bruto = pd.read_csv(os.path.join(BASE, "dados", "Consumo_cerveja.csv"))
dias = bruto.dropna(how="all").copy()
for coluna in [
    "Temperatura Media (C)",
    "Temperatura Minima (C)",
    "Temperatura Maxima (C)",
    "Precipitacao (mm)",
]:
    dias[coluna] = (
        dias[coluna].astype(str).str.replace(",", ".", regex=False).astype(float)
    )
consumo = "Consumo de cerveja (litros)"
dias[consumo] = dias[consumo].astype(float)

pares = [
    ("temp. média", "Temperatura Media (C)"),
    ("temp. mínima", "Temperatura Minima (C)"),
    ("temp. máxima", "Temperatura Maxima (C)"),
    ("precipitação", "Precipitacao (mm)"),
    ("fim de semana", "Final de Semana"),
]
correlacao = pd.Series(
    {rotulo: dias[coluna].corr(dias[consumo]) for rotulo, coluna in pares}
)

fig, ax = plt.subplots(figsize=(6.6, 2.7))
cores = [ROXO if valor >= 0 else AMBAR for valor in correlacao]
ax.barh(correlacao.index[::-1], correlacao.values[::-1], color=cores[::-1])
ax.set_xlabel("correlação com o consumo")
ax.set_xlim(-0.2, 1)
fig.savefig(os.path.join(IMG, "g-corr.png"))
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.6, 2.7))
ax.scatter(
    dias["Temperatura Maxima (C)"],
    dias[consumo],
    s=12,
    c=ROXO,
    alpha=0.75,
    linewidths=0,
)
ax.set_xlabel("temperatura máxima (°C)")
ax.set_ylabel("consumo (litros)")
fig.savefig(os.path.join(IMG, "g-temp.png"))
plt.close(fig)

medias = dias.groupby("Final de Semana")[consumo].mean()
fig, ax = plt.subplots(figsize=(6.6, 2.7))
ax.bar(
    ["dia de semana", "fim de semana"],
    [medias.loc[0.0], medias.loc[1.0]],
    color=[CINZA, ROXO],
)
ax.set_ylabel("consumo médio (litros)")
fig.savefig(os.path.join(IMG, "g-fds.png"))
plt.close(fig)

print("linhas_brutas", len(bruto))
print("linhas_vazias", int(bruto.isna().all(axis=1).sum()))
print("dias", len(dias))
print(correlacao.round(3).to_string())
print("media_semana", round(float(medias.loc[0.0]), 2))
print("media_fds", round(float(medias.loc[1.0]), 2))
