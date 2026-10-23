"""Roda o ciclo da aula 1 e grava os números e as figuras dos slides.

Toda métrica projetada sai daqui, sobre dados/penguins_size.csv.
Uso:  python saidas.py
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(BASE, "dados", "penguins_size.csv")
IMG = os.path.join(BASE, "img")
os.makedirs(IMG, exist_ok=True)

ROXO, AMBAR, VERDE, CINZA = "#5b56e0", "#d9820b", "#0a9d70", "#8a90a0"
CORES = {"Adelie": ROXO, "Chinstrap": AMBAR, "Gentoo": VERDE}

plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.transparent": True, "savefig.bbox": "tight",
    "font.size": 11, "text.color": CINZA,
    "axes.labelcolor": CINZA, "axes.edgecolor": CINZA,
    "xtick.color": CINZA, "ytick.color": CINZA,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "none", "axes.facecolor": "none",
})

MEDIDAS = [
    "culmen_length_mm",
    "culmen_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]


def modelo():
    return Pipeline([
        ("escala", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])


def acuracia(semente):
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=semente
    )
    m = modelo()
    m.fit(X_tr, y_tr)
    return float((m.predict(X_te) == y_te).mean()), len(X_te)


bruto = pd.read_csv(DADOS)
n_bruto = int(len(bruto))
incompletas = int(bruto[MEDIDAS + ["species"]].isna().any(axis=1).sum())
pinguins = bruto.dropna(subset=MEDIDAS + ["species"]).copy()
n = int(len(pinguins))

X = pinguins[MEDIDAS]
y = pinguins["species"]
contagem = {k: int(v) for k, v in y.value_counts().items()}

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=0
)
clf = modelo()
clf.fit(X_tr, y_tr)
linha = X_te.iloc[0]
verdadeiro = str(y_te.iloc[0])
previsto = str(clf.predict(X_te.iloc[[0]])[0])
acc0, n_teste = acuracia(0)
acc1, _ = acuracia(1)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
notas = cross_val_score(modelo(), X, y, cv=cv, scoring="accuracy")

# dispersão bico × asa
fig, ax = plt.subplots(figsize=(6.4, 3.15))
for especie, cor in CORES.items():
    pedaco = pinguins[pinguins["species"] == especie]
    ax.scatter(
        pedaco["culmen_length_mm"], pedaco["flipper_length_mm"],
        s=18, c=cor, label=especie, alpha=0.9, linewidths=0,
    )
ax.set_xlabel("comprimento do bico (mm)")
ax.set_ylabel("asa (mm)")
ax.legend(frameon=False, fontsize=9)
fig.savefig(os.path.join(IMG, "g1-bico-asa.png"))
plt.close(fig)

# as cinco notas da validação cruzada
fig, ax = plt.subplots(figsize=(6.4, 2.4))
ax.bar([f"parte {i}" for i in range(1, 6)], notas, color=ROXO, width=0.62)
ax.axhline(notas.mean(), color=AMBAR, lw=1.4)
ax.set_ylim(0.9, 1.005)
ax.set_ylabel("acurácia")
fig.savefig(os.path.join(IMG, "g2-folds.png"))
plt.close(fig)

primeiras = bruto[MEDIDAS + ["species"]].head(4)

saida = {
    "n_bruto": n_bruto,
    "incompletas": incompletas,
    "n": n,
    "contagem": contagem,
    "n_treino": int(len(X_tr)),
    "n_teste": int(n_teste),
    "linha": {c: float(linha[c]) for c in MEDIDAS},
    "verdadeiro": verdadeiro,
    "previsto": previsto,
    "acc0": acc0,
    "acc1": acc1,
    "notas": [float(x) for x in notas],
    "media": float(notas.mean()),
    "primeiras": primeiras.astype(object).where(primeiras.notna(), None).to_dict(orient="records"),
}
caminho = os.path.join(BASE, "numeros.json")
with open(caminho, "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)

assert n_bruto == 344
assert incompletas > 0
assert previsto in contagem
assert 0.9 < saida["media"] <= 1.0
print(json.dumps(saida, ensure_ascii=False, indent=2))
