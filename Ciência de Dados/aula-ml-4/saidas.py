"""Cinco modelos no mesmo split dos diamantes, mais a permutação e o Diamante 157.

Parâmetros contidos de propósito: a floresta e o boosting cabem no horário.
Uso:  python saidas.py
"""
import json
import os

os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor, plot_tree

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
os.makedirs(IMG, exist_ok=True)
ROXO, AMBAR, VERDE, CINZA, AZUL, VERMELHO = "#5b56e0", "#d9820b", "#0a9d70", "#8a90a0", "#2563eb", "#dc2626"

plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 160,
    "savefig.transparent": True,
    "savefig.bbox": "tight",
    "font.size": 10,
    "text.color": CINZA,
    "axes.labelcolor": CINZA,
    "axes.edgecolor": CINZA,
    "xtick.color": CINZA,
    "ytick.color": CINZA,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "none",
    "axes.facecolor": "none",
})

mlflow.set_tracking_uri(os.path.join(BASE, "mlruns"))
mlflow.set_experiment("aula-ml-4-diamonds")

bruto = pd.read_csv(os.path.join(BASE, "dados", "diamonds.csv"))
n_bruto = int(len(bruto))
pedras = bruto[(bruto["x"] > 0) & (bruto["y"] > 0) & (bruto["z"] > 0)].copy()
n_zero = n_bruto - int(len(pedras))

alvo = "price"
numericas = ["carat", "depth", "table", "x", "y", "z"]
categoricas = ["cut", "color", "clarity"]
X = pedras[numericas + categoricas]
y = pedras[alvo]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)


def preparo():
    return ColumnTransformer([
        ("num", StandardScaler(), numericas),
        ("cat", OneHotEncoder(drop="first", sparse_output=False), categoricas),
    ])


def rmse(a, b):
    return float(np.sqrt(mean_squared_error(a, b)))


def mae(a, b):
    return float(mean_absolute_error(a, b))


estimadores = {
    "reta": LinearRegression(),
    "arvore-rasa": DecisionTreeRegressor(max_depth=3, random_state=0),
    "arvore-funda": DecisionTreeRegressor(random_state=0),
    "floresta": RandomForestRegressor(
        n_estimators=80, max_depth=16, n_jobs=-1, random_state=0
    ),
    "boosting": GradientBoostingRegressor(
        n_estimators=80, max_depth=3, random_state=0
    ),
    "knn": KNeighborsRegressor(n_neighbors=15),
}

nomes_apresentacao = {
    "reta": "Regressão linear (reta)",
    "arvore-rasa": "Árvore rasa (prof. 3)",
    "arvore-funda": "Árvore funda (sem teto)",
    "floresta": "Floresta (80 árvores)",
    "boosting": "Boosting (80 árvores)",
    "knn": "KNN (k=15)",
}

cores_modelos = [
    "#8a90a0",  # reta
    "#d9820b",  # arvore rasa
    "#dc2626",  # arvore funda
    "#0a9d70",  # floresta (campeã)
    "#5b56e0",  # boosting
    "#2563eb",  # knn
]

resultados = {}
modelos = {}
for nome, est in estimadores.items():
    pipe = Pipeline([("preparo", preparo()), ("modelo", est)])
    pipe.fit(X_tr, y_tr)
    prev_te = pipe.predict(X_te)
    prev_tr = pipe.predict(X_tr)
    notas = {
        "teste_rmse": rmse(y_te, prev_te),
        "teste_mae": mae(y_te, prev_te),
        "treino_rmse": rmse(y_tr, prev_tr),
    }
    with mlflow.start_run(run_name=nome):
        mlflow.log_params({"modelo": nome})
        mlflow.log_metrics(notas)
    resultados[nome] = notas
    modelos[nome] = pipe
    print(f"{nome:15s}: { {k: round(v) for k, v in notas.items()} }", flush=True)

# 1. Gráfico de dispersão Preço contra Quilate (g1-quilate.png)
fig, ax = plt.subplots(figsize=(6.4, 3.2))
amostra = pedras.sample(4000, random_state=0)
for corte, cor in zip(
    ["Fair", "Good", "Very Good", "Premium", "Ideal"],
    ["#8a90a0", "#d9820b", "#5b56e0", "#0a9d70", "#14161a"],
):
    ped = amostra[amostra["cut"] == corte]
    ax.scatter(ped["carat"], ped["price"], s=6, c=cor, alpha=0.55, linewidths=0, label=corte)
ax.set_xlabel("quilate")
ax.set_ylabel("preço (US$)")
ax.legend(frameon=False, fontsize=8, markerscale=2)
fig.savefig(os.path.join(IMG, "g1-quilate.png"))
plt.close(fig)

# 2. Desenho da árvore rasa (g2-arvore.png)
rasa = modelos["arvore-rasa"]
nomes_features = list(rasa.named_steps["preparo"].get_feature_names_out())
fig, ax = plt.subplots(figsize=(11, 4.2))
plot_tree(
    rasa.named_steps["modelo"],
    feature_names=nomes_features,
    filled=False,
    impurity=False,
    fontsize=7,
    ax=ax,
    max_depth=3,
)
fig.savefig(os.path.join(IMG, "g2-arvore.png"))
plt.close(fig)

# Primeira pergunta em unidades originais
indice_primeira = int(rasa.named_steps["modelo"].tree_.feature[0])
primeira_nome = nomes_features[indice_primeira]
limiar_primeira = float(rasa.named_steps["modelo"].tree_.threshold[0])
if primeira_nome.startswith("num__"):
    coluna = primeira_nome.split("__", 1)[1]
    escala = rasa.named_steps["preparo"].named_transformers_["num"]
    i_num = numericas.index(coluna)
    limiar_primeira = float(limiar_primeira * escala.scale_[i_num] + escala.mean_[i_num])
    primeira_nome = coluna

# 3. Gráfico de Comparação de Modelos (g-comparacao.png)
labels = [nomes_apresentacao[k] for k in estimadores.keys()]
teste_rmse_vals = [resultados[k]["teste_rmse"] for k in estimadores.keys()]
treino_rmse_vals = [resultados[k]["treino_rmse"] for k in estimadores.keys()]
teste_mae_vals = [resultados[k]["teste_mae"] for k in estimadores.keys()]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)

# Painel 1: RMSE no teste (campeão = menor barra)
bars1 = ax1.barh(labels, teste_rmse_vals, color=cores_modelos)
for bar, val in zip(bars1, teste_rmse_vals):
    ax1.text(val + 15, bar.get_y() + bar.get_height() / 2, f"{round(val):,}".replace(",", "."), va="center", fontsize=9, fontweight="bold")
ax1.set_title("RMSE no teste (US$ · menor é melhor)", fontsize=11, pad=10)
ax1.set_xlim(0, 1650)
ax1.invert_yaxis()

# Painel 2: Treino vs Teste (evidência do overfitting da árvore funda)
y_pos = np.arange(len(labels))
h = 0.35
ax2.barh(y_pos - h/2, treino_rmse_vals, height=h, label="Treino", color="#94a3b8")
ax2.barh(y_pos + h/2, teste_rmse_vals, height=h, label="Teste", color="#3b82f6")
for y_idx, (tr, te) in enumerate(zip(treino_rmse_vals, teste_rmse_vals)):
    if labels[y_idx].startswith("Árvore funda"):
        ax2.text(tr + 15, y_idx - h/2, f"treino: {round(tr)}!", va="center", fontsize=8.5, color="#dc2626", fontweight="bold")
ax2.set_title("Treino vs Teste (Overfitting)", fontsize=11, pad=10)
ax2.set_xlim(0, 1650)
ax2.legend(frameon=False, fontsize=9)

plt.tight_layout()
fig.savefig(os.path.join(IMG, "g-comparacao.png"), dpi=160, bbox_inches="tight")
plt.close(fig)

# 4. Permutação no teste para a Floresta (g3-permutacao.png)
print("Calculando permutação no teste da floresta…", flush=True)
perm = permutation_importance(
    modelos["floresta"],
    X_te,
    y_te,
    n_repeats=3,
    random_state=0,
    scoring="neg_root_mean_squared_error",
    n_jobs=-1,
)
ordem = np.argsort(perm.importances_mean)[::-1]
fig, ax = plt.subplots(figsize=(6.4, 3.2))
ax.barh(
    [X.columns[i] for i in ordem][::-1],
    perm.importances_mean[ordem][::-1],
    color=ROXO,
)
ax.set_xlabel("quanto o RMSE piora ao embaralhar a coluna (US$)")
fig.savefig(os.path.join(IMG, "g3-permutacao.png"))
plt.close(fig)

interna = modelos["arvore-funda"].named_steps["modelo"].feature_importances_
nomes_arv = modelos["arvore-funda"].named_steps["preparo"].get_feature_names_out()
top_interna = sorted(zip(nomes_arv, interna), key=lambda t: -t[1])[:4]

# 5. O Diamante 157 concreto passo a passo
pedra_idx = 157
pedra = X_te.iloc[[pedra_idx]]
y_real = float(y_te.iloc[pedra_idx])
prep_global = modelos["reta"].named_steps["preparo"]
pedra_trans = prep_global.transform(pedra)[0]

# Reta
reg = modelos["reta"].named_steps["modelo"]
pred_reta = float(modelos["reta"].predict(pedra)[0])
pesos_reta = [
    {"feature": fn, "valor_padronizado": float(xt), "peso": float(w), "contribuicao": float(xt * w)}
    for fn, w, xt in zip(nomes_features, reg.coef_, pedra_trans)
]
pesos_reta = sorted(pesos_reta, key=lambda x: abs(x["contribuicao"]), reverse=True)

# Árvore rasa: caminho nós
tree_rasa = modelos["arvore-rasa"].named_steps["modelo"].tree_
node = 0
caminho_arvore = []
while tree_rasa.children_left[node] != tree_rasa.children_right[node]:
    f_idx = tree_rasa.feature[node]
    f_nome = nomes_features[f_idx]
    thresh = float(tree_rasa.threshold[node])
    val = float(pedra_trans[f_idx])
    decisao = val <= thresh
    caminho_arvore.append({
        "no": node,
        "feature": f_nome,
        "limiar": thresh,
        "valor": val,
        "resposta_sim": decisao,
    })
    node = tree_rasa.children_left[node] if decisao else tree_rasa.children_right[node]
pred_rasa = float(tree_rasa.value[node][0][0])
amostras_folha_rasa = int(tree_rasa.n_node_samples[node])

# Floresta
rf_mod = modelos["floresta"].named_steps["modelo"]
rf_trans = modelos["floresta"].named_steps["preparo"].transform(pedra)
pred_floresta = float(modelos["floresta"].predict(pedra)[0])
arv_preds = [float(t.predict(rf_trans)[0]) for t in rf_mod.estimators_]

# Boosting
pred_boosting = float(modelos["boosting"].predict(pedra)[0])

# KNN
knn_mod = modelos["knn"].named_steps["modelo"]
knn_prep = modelos["knn"].named_steps["preparo"]
pedra_knn_trans = knn_prep.transform(pedra)
dists, indices = knn_mod.kneighbors(pedra_knn_trans)
vizinhos = []
for d, idx in zip(dists[0][:5], indices[0][:5]):
    viz = X_tr.iloc[idx].to_dict()
    viz["distancia"] = float(d)
    viz["preco"] = float(y_tr.iloc[idx])
    vizinhos.append(viz)
pred_knn = float(modelos["knn"].predict(pedra)[0])

diamante_157 = {
    "posicao_teste": pedra_idx,
    "dados": pedra.iloc[0].to_dict(),
    "preco_real": y_real,
    "reta": {
        "previsao": pred_reta,
        "erro": pred_reta - y_real,
        "intercepto": float(reg.intercept_),
        "top_contribuicoes": pesos_reta[:6],
    },
    "arvore_rasa": {
        "previsao": pred_rasa,
        "erro": pred_rasa - y_real,
        "folha": node,
        "amostras_folha": amostras_folha_rasa,
        "caminho": caminho_arvore,
    },
    "arvore_funda": {
        "previsao": float(modelos["arvore-funda"].predict(pedra)[0]),
        "erro": float(modelos["arvore-funda"].predict(pedra)[0]) - y_real,
    },
    "floresta": {
        "previsao": pred_floresta,
        "erro": pred_floresta - y_real,
        "min_arvore": min(arv_preds),
        "max_arvore": max(arv_preds),
        "primeiras_5": arv_preds[:5],
    },
    "boosting": {
        "previsao": pred_boosting,
        "erro": pred_boosting - y_real,
    },
    "knn": {
        "previsao": pred_knn,
        "erro": pred_knn - y_real,
        "top5_vizinhos": vizinhos,
    },
}

saida = {
    "n_bruto": n_bruto,
    "n_zero": int(n_zero),
    "n": int(len(pedras)),
    "n_treino": int(len(X_tr)),
    "n_teste": int(len(X_te)),
    "cortes": sorted(pedras["cut"].unique().tolist()),
    "cores": sorted(pedras["color"].unique().tolist()),
    "clarezas": sorted(pedras["clarity"].unique().tolist()),
    "resultados": resultados,
    "primeira_pergunta": {"feature": primeira_nome, "limiar": limiar_primeira},
    "permutacao": [
        {"coluna": X.columns[i], "rmse_piora": float(perm.importances_mean[i])}
        for i in ordem
    ],
    "importancia_interna_top": [
        {"feature": n, "peso": float(p)} for n, p in top_interna
    ],
    "diamante_157": diamante_157,
}

def converter_para_json(obj):
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


with open(os.path.join(BASE, "numeros.json"), "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2, default=converter_para_json)

print("\nExecução concluída com sucesso! numeros.json e imagens atualizados.")
