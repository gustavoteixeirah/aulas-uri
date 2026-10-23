"""Corte temporal, baseline de sete dias e a run de propósito com split aleatório.

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
from sklearn.metrics import mean_absolute_error, mean_squared_error
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
mlflow.set_experiment("aula-ml-5-bicicletas")

horas = pd.read_csv(os.path.join(BASE, "dados", "train.csv"), parse_dates=["datetime"])
horas = horas.sort_values("datetime")
assert (horas["casual"] + horas["registered"] == horas["count"]).all()

horas["hora"] = horas["datetime"].dt.hour
horas["dia_semana"] = horas["datetime"].dt.dayofweek
horas["mes"] = horas["datetime"].dt.month

treino = horas[horas["datetime"].dt.year == 2011].copy()
teste = horas[horas["datetime"].dt.year == 2012].copy()

cat = ["hora", "dia_semana", "mes", "season", "weather"]
num = ["temp", "humidity", "windspeed"]
binarias = ["holiday", "workingday"]
features = cat + num + binarias


def modelo():
    return Pipeline([
        ("preparo", ColumnTransformer([
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat),
            ("num", StandardScaler(), num),
            ("bin", "passthrough", binarias),
        ])),
        ("reta", LinearRegression()),
    ])


def erros(y, prev):
    return {
        "mae": float(mean_absolute_error(y, prev)),
        "rmse": float(np.sqrt(mean_squared_error(y, prev))),
    }


# baseline: a mesma hora, sete dias antes, quando existe
teste = teste.copy()
teste["chave"] = teste["datetime"] - pd.Timedelta(days=7)
base = horas[["datetime", "count"]].rename(columns={"datetime": "chave", "count": "lag"})
junto = teste.merge(base, on="chave", how="left")
com_par = junto.dropna(subset=["lag"])
m_base = erros(com_par["count"], com_par["lag"])
with mlflow.start_run(run_name="baseline-semana"):
    mlflow.log_params({"modelo": "lag-7-dias", "teste": "2012"})
    mlflow.log_metrics({f"teste_{k}": v for k, v in m_base.items()})
    mlflow.log_metric("horas_com_par", int(len(com_par)))

reta = modelo()
reta.fit(treino[features], treino["count"])
prev = reta.predict(teste[features])
m_reta = erros(teste["count"], prev)
m_reta_mesmo_recorte = erros(com_par["count"], reta.predict(com_par[features]))
with mlflow.start_run(run_name="reta-calendario"):
    mlflow.log_params({"modelo": "linear", "corte": "2011-2012"})
    mlflow.log_metrics({f"teste_{k}": v for k, v in m_reta.items()})
    mlflow.log_metrics({f"mesmo_recorte_{k}": v for k, v in m_reta_mesmo_recorte.items()})

X_tr, X_te, y_tr, y_te = train_test_split(
    horas[features], horas["count"], test_size=0.25, random_state=0
)
aleatorio = modelo()
aleatorio.fit(X_tr, y_tr)
m_alea = erros(y_te, aleatorio.predict(X_te))
with mlflow.start_run(run_name="reta-split-aleatorio"):
    mlflow.log_params({"modelo": "linear", "corte": "sorteado", "teste": "nao-e-2012"})
    mlflow.log_metrics({f"teste_sorteado_{k}": v for k, v in m_alea.items()})

# um mês, para a sazonalidade do dia aparecer
janeiro = treino[(treino["datetime"].dt.year == 2011) & (treino["datetime"].dt.month == 1)]
fig, ax = plt.subplots(figsize=(6.6, 2.6))
ax.plot(janeiro["datetime"], janeiro["count"], color=ROXO, lw=1)
ax.set_ylabel("aluguéis")
fig.autofmt_xdate()
fig.savefig(os.path.join(IMG, "g1-janeiro.png"))
plt.close(fig)

por_hora = treino.groupby("hora")["count"].mean()
fig, ax = plt.subplots(figsize=(6.4, 2.6))
ax.bar(por_hora.index, por_hora.values, color=ROXO, width=0.8)
ax.set_xlabel("hora do dia · treino de 2011")
ax.set_ylabel("média de aluguéis")
fig.savefig(os.path.join(IMG, "g2-hora.png"))
plt.close(fig)

por_dia = treino.groupby("dia_semana")["count"].mean()
saida = {
    "n": int(len(horas)),
    "dias": sorted(int(d) for d in horas["datetime"].dt.day.unique()),
    "n_2011": int(len(treino)),
    "n_2012": int(len(teste)),
    "horas_com_lag": int(len(com_par)),
    "baseline": m_base,
    "reta": m_reta,
    "reta_mesmo_recorte": m_reta_mesmo_recorte,
    "aleatorio": m_alea,
    "media_por_hora": {str(int(k)): float(v) for k, v in por_hora.items()},
    "media_por_dia": {str(int(k)): float(v) for k, v in por_dia.items()},
    "amostra_vazamento": horas[["casual", "registered", "count"]].head(3).astype(int).to_dict(orient="records"),
}
with open(os.path.join(BASE, "numeros.json"), "w", encoding="utf-8") as f:
    json.dump(saida, f, ensure_ascii=False, indent=2)
print(json.dumps({k: saida[k] for k in ("n", "dias", "n_2011", "n_2012", "horas_com_lag", "baseline", "reta", "aleatorio", "amostra_vazamento")}, ensure_ascii=False, indent=2))
