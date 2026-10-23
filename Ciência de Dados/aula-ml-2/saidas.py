"""Números e figuras da aula 2, e as quatro runs no MLflow.

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
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
os.makedirs(IMG, exist_ok=True)

ROXO, AMBAR, VERDE, CINZA = "#5b56e0", "#d9820b", "#0a9d70", "#8a90a0"
plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.transparent": True, "savefig.bbox": "tight",
    "font.size": 11, "text.color": CINZA,
    "axes.labelcolor": CINZA, "axes.edgecolor": CINZA,
    "xtick.color": CINZA, "ytick.color": CINZA,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "none", "axes.facecolor": "none",
})

mlflow.set_tracking_uri(os.path.join(BASE, "mlruns"))
mlflow.set_experiment("aula-ml-2-custo")

custos = pd.read_csv(os.path.join(BASE, "dados", "insurance.csv"))
alvo = "charges"
numericas = ["age", "bmi", "children"]
categoricas = ["sex", "smoker", "region"]
X = custos[numericas + categoricas]
y = custos[alvo]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)


def metricas(y_verdadeiro, y_previsto):
    return {
        "mae": float(mean_absolute_error(y_verdadeiro, y_previsto)),
        "rmse": float(np.sqrt(mean_squared_error(y_verdadeiro, y_previsto))),
        "r2": float(r2_score(y_verdadeiro, y_previsto)),
    }


def logar(nome, y_prev_teste, params, y_prev_treino=None, modelo=None):
    with mlflow.start_run(run_name=nome):
        mlflow.log_params(params)
        testes = metricas(y_te, y_prev_teste)
        mlflow.log_metrics({f"teste_{k}": v for k, v in testes.items()})
        if y_prev_treino is not None:
            treinos = metricas(y_tr, y_prev_treino)
            mlflow.log_metrics({f"treino_{k}": v for k, v in treinos.items()})
        if modelo is not None:
            mlflow.sklearn.log_model(modelo, name="modelo")
        return testes


# 1 — média
prev_media = np.full(len(y_te), fill_value=float(y_tr.mean()))
m_media = logar("media", prev_media, {"modelo": "media-do-treino"})

# 2 — reta de uma variável, sem escala, para o coeficiente ser dólares por ano
reta_idade = LinearRegression().fit(X_tr[["age"]], y_tr)
m_idade = logar(
    "reta-idade",
    reta_idade.predict(X_te[["age"]]),
    {"modelo": "linear", "features": "age"},
    y_prev_treino=reta_idade.predict(X_tr[["age"]]),
)
coef_idade = float(reta_idade.coef_[0])

# 3 — vazamento: escala e one-hot ajustados no arquivo inteiro, antes do split
esc_vaz = StandardScaler().fit(X[numericas])
oh_vaz = OneHotEncoder(drop="first", sparse_output=False).fit(X[categoricas])


def transformar_vaz(frame):
    num = esc_vaz.transform(frame[numericas])
    cat = oh_vaz.transform(frame[categoricas])
    return np.hstack([num, cat])


reta_vaz = LinearRegression().fit(transformar_vaz(X_tr), y_tr)
m_vaz = logar(
    "reta-com-vazamento",
    reta_vaz.predict(transformar_vaz(X_te)),
    {"modelo": "linear", "preparo": "antes-do-split"},
)

# 4 — pipeline: o teste repete o caminho do treino
preparo = ColumnTransformer([
    ("num", StandardScaler(), numericas),
    ("cat", OneHotEncoder(drop="first", sparse_output=False), categoricas),
])
reta = Pipeline([
    ("preparo", preparo),
    ("modelo", LinearRegression()),
])
reta.fit(X_tr, y_tr)
prev_te = reta.predict(X_te)
prev_tr = reta.predict(X_tr)
m_pipe = logar(
    "reta-pipeline",
    prev_te,
    {"modelo": "linear", "preparo": "pipeline"},
    y_prev_treino=prev_tr,
    modelo=reta,
)
m_pipe_treino = metricas(y_tr, prev_tr)

nomes = list(reta.named_steps["preparo"].get_feature_names_out())
coefs = reta.named_steps["modelo"].coef_
escala = reta.named_steps["preparo"].named_transformers_["num"].scale_
# coeficiente em dólares por unidade original da coluna numérica
por_unidade = {}
for nome, coef in zip(nomes, coefs):
    if nome.startswith("num__"):
        coluna = nome.split("__", 1)[1]
        por_unidade[coluna] = float(coef / escala[numericas.index(coluna)])
    else:
        por_unidade[nome.split("__", 1)[1]] = float(coef)

# gráfico: custo × idade, reta de uma variável, cor por fumante
fig, ax = plt.subplots(figsize=(6.4, 3.2))
for valor, cor, rotulo in (("no", ROXO, "não fuma"), ("yes", AMBAR, "fuma")):
    ped = custos[custos["smoker"] == valor]
    ax.scatter(ped["age"], ped["charges"], s=10, c=cor, alpha=0.75, linewidths=0, label=rotulo)
idade_linha = np.linspace(custos["age"].min(), custos["age"].max(), 40)
ax.plot(idade_linha, reta_idade.predict(idade_linha.reshape(-1, 1)), color=VERDE, lw=2)
ax.set_xlabel("idade")
ax.set_ylabel("custo")
ax.legend(frameon=False, fontsize=9)
fig.savefig(os.path.join(IMG, "g1-idade.png"))
plt.close(fig)

# resíduo do pipeline contra o IMC, cor por fumante
residuo = y_te.to_numpy() - prev_te
fig, ax = plt.subplots(figsize=(6.4, 3.0))
for valor, cor, rotulo in (("no", ROXO, "não fuma"), ("yes", AMBAR, "fuma")):
    mask = X_te["smoker"].to_numpy() == valor
    ax.scatter(X_te["bmi"].to_numpy()[mask], residuo[mask], s=12, c=cor, alpha=0.8, linewidths=0, label=rotulo)
ax.axhline(0, color=CINZA, lw=1)
ax.set_xlabel("IMC")
ax.set_ylabel("resíduo no teste")
ax.legend(frameon=False, fontsize=9)
fig.savefig(os.path.join(IMG, "g2-residuo.png"))
plt.close(fig)

saida = {
    "n": int(len(custos)),
    "describe_charges": {k: float(v) for k, v in y.describe()[["min", "mean", "50%", "max"]].items()},
    "media_treino": float(y_tr.mean()),
    "coef_idade_uma_variavel": coef_idade,
    "coeficientes_por_unidade": por_unidade,
    "media": m_media,
    "reta_idade": m_idade,
    "vazamento": m_vaz,
    "pipeline_teste": m_pipe,
    "pipeline_treino": m_pipe_treino,
    "primeiras": custos.head(3).to_dict(orient="records"),
}
with open(os.path.join(BASE, "numeros.json"), "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)
print(json.dumps(saida, ensure_ascii=False, indent=2))
