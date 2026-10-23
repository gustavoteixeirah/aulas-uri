"""Números, figuras e runs da aula 3. Também grava o modelo promovido.

O custo declarado na aula: deixar passar quem sai pesa mais do que um contato
inútil. A run promovida é a de maior recall da classe que sai, entre o corte
0,3 e a logística com peso balanceado. O artefato vai para
../aula-ml-6/modelos/churn, para a aula 6 publicar sem retreinar.

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
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

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

mlflow.set_tracking_uri(os.path.join(BASE, "mlruns"))
mlflow.set_experiment("aula-ml-3-churn")

clientes = pd.read_csv(os.path.join(BASE, "dados", "WA_Fn-UseC_-Telco-Customer-Churn.csv"))
clientes["TotalCharges"] = pd.to_numeric(clientes["TotalCharges"], errors="coerce")
y = (clientes["Churn"] == "Yes").astype(int)
X = clientes.drop(columns=["customerID", "Churn"])
numericas = ["tenure", "MonthlyCharges", "TotalCharges"]
categoricas = [c for c in X.columns if c not in numericas]
for c in categoricas:
    X[c] = X[c].astype(str)

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=0
)


def preparo():
    return ColumnTransformer([
        ("num", Pipeline([
            ("nulos", SimpleImputer(strategy="median")),
            ("escala", StandardScaler()),
        ]), numericas),
        ("cat", Pipeline([
            ("nulos", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]), categoricas),
    ])


def avaliar(y_verdadeiro, probabilidade, corte):
    classe = (probabilidade >= corte).astype(int)
    return {
        "acuracia": float(accuracy_score(y_verdadeiro, classe)),
        "precisao_sai": float(precision_score(y_verdadeiro, classe, zero_division=0)),
        "recall_sai": float(recall_score(y_verdadeiro, classe, zero_division=0)),
        "f1_sai": float(f1_score(y_verdadeiro, classe, zero_division=0)),
        "alertas": int(classe.sum()),
    }


def logar(nome, notas, params):
    with mlflow.start_run(run_name=nome):
        mlflow.log_params(params)
        mlflow.log_metrics({k: v for k, v in notas.items()})
    return notas


fica = float((y == 0).mean())
constante = np.zeros(len(y_te))
m_const = avaliar(y_te, constante, 0.5)
logar("constante-fica", m_const, {"modelo": "constante", "classe": 0})

modelo = Pipeline([
    ("preparo", preparo()),
    ("clf", LogisticRegression(max_iter=1000)),
])
modelo.fit(X_tr, y_tr)
prob = modelo.predict_proba(X_te)[:, 1]

cortes = {}
for corte in (0.3, 0.5, 0.7):
    notas = avaliar(y_te, prob, corte)
    logar(f"logistica-corte-{corte}", notas, {"modelo": "logistica", "corte": corte, "class_weight": "none"})
    cortes[str(corte)] = notas

balanceada = Pipeline([
    ("preparo", preparo()),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
balanceada.fit(X_tr, y_tr)
prob_b = balanceada.predict_proba(X_te)[:, 1]
m_bal = avaliar(y_te, prob_b, 0.5)
logar("logistica-balanceada", m_bal, {"modelo": "logistica", "corte": 0.5, "class_weight": "balanced"})

# custo da aula: deixar passar quem sai pesa mais. Promove o maior recall.
candidatos = {
    "logistica-corte-0.3": (cortes["0.3"], modelo, 0.3),
    "logistica-balanceada": (m_bal, balanceada, 0.5),
}
nome_promo, (notas_promo, modelo_promo, corte_promo) = max(
    candidatos.items(), key=lambda kv: kv[1][0]["recall_sai"]
)

class ServicoChurn(mlflow.pyfunc.PythonModel):
    def __init__(self, pipeline, corte):
        self.pipeline = pipeline
        self.corte = corte

    def predict(self, context, model_input, params=None):
        tabela = pd.DataFrame(model_input)
        probabilidade = self.pipeline.predict_proba(tabela)[:, 1]
        return pd.DataFrame({
            "probabilidade_sai": probabilidade,
            "sai": (probabilidade >= self.corte).astype(int),
        })


destino = os.path.join(os.path.dirname(BASE), "aula-ml-6", "modelos", "churn")
if os.path.isdir(destino):
    import shutil
    shutil.rmtree(destino)
os.makedirs(os.path.dirname(destino), exist_ok=True)
mlflow.pyfunc.save_model(
    path=destino,
    python_model=ServicoChurn(modelo_promo, corte_promo),
    input_example=X_tr.head(2),
)
with open(os.path.join(destino, "contrato.json"), "w", encoding="utf-8") as f:
    json.dump({
        "run": nome_promo,
        "corte": corte_promo,
        "colunas": list(X.columns),
        "metricas": notas_promo,
        "custo": "deixar passar quem sai pesa mais do que um contato inútil",
    }, f, ensure_ascii=False, indent=2)

cm = confusion_matrix(y_te, (prob >= 0.5).astype(int))
# linhas: real fica, real sai; colunas: previsto fica, previsto sai
fig, ax = plt.subplots(figsize=(6.2, 2.8))
ficou = prob[y_te.to_numpy() == 0]
saiu = prob[y_te.to_numpy() == 1]
bins = np.linspace(0, 1, 21)
ax.hist(ficou, bins=bins, color=ROXO, alpha=0.75, label="ficou")
ax.hist(saiu, bins=bins, color=AMBAR, alpha=0.75, label="saiu")
ax.set_xlabel("probabilidade de sair")
ax.set_ylabel("clientes no teste")
ax.legend(frameon=False)
fig.savefig(os.path.join(IMG, "g1-prob.png"))
plt.close(fig)

saida = {
    "n": int(len(clientes)),
    "churn_yes": int((y == 1).sum()),
    "churn_no": int((y == 0).sum()),
    "proporcao_fica": fica,
    "nulos_total": int(clientes["TotalCharges"].isna().sum()),
    "n_teste": int(len(y_te)),
    "constante": m_const,
    "cortes": cortes,
    "balanceada": m_bal,
    "matriz_05": cm.tolist(),
    "promovida": {"run": nome_promo, "corte": corte_promo, "metricas": notas_promo},
}
with open(os.path.join(BASE, "numeros.json"), "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)
print(json.dumps(saida, ensure_ascii=False, indent=2))
