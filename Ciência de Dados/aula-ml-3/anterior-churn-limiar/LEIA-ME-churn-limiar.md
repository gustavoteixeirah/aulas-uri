# Aula ML 03 — Classificação (15/10, aula gravada)

Slides em `index.html` (21 slides). Três cadernos, rodados nesta ordem:

| caderno | o que faz |
|---|---|
| `01-treino.ipynb` | lê o CSV, limpa o mínimo, separa treino/teste estratificado, treina a regressão logística, mostra um cliente (score → probabilidade → classe), acurácia contra o chute "sempre fica". Gera `img/g-sigmoide.png`. |
| `02-mlflow.ipynb` | o mesmo treino, mais matriz de confusão, precisão, recall e F1, gravados na run `limiar-0.5`. |
| `03-comparar.ipynb` | v1 limiar 0,5 → v2 limiar 0,3 → v3 `class_weight="balanced"`, uma run cada. Lê as runs de volta e gera `img/g-evolucao.png`. |

Dados: `dados/WA_Fn-UseC_-Telco-Customer-Churn.csv`. Entradas: `tenure`, `MonthlyCharges`, `TotalCharges`, `Contract` (one-hot). As 11 linhas com `TotalCharges` vazio saem (7.043 → 7.032). Split 75/25, `stratify=y`, `random_state=0`.

MLflow: pasta `mlruns/`, experimento `churn`.

```bash
MLFLOW_ALLOW_FILE_STORE=true mlflow ui --backend-store-uri mlruns
```

Números do teste (1.758 clientes, 467 saíram):

| run | acurácia | precisão | recall | F1 |
|---|---|---|---|---|
| chutar sempre "fica" | 0,734 | — | 0 | — |
| v1-limiar-0.5 | 0,788 | 0,638 | 0,469 | 0,541 |
| v2-limiar-0.3 | 0,748 | 0,518 | 0,754 | 0,614 |
| v3-peso-balanceado | 0,719 | 0,483 | 0,814 | 0,606 |

Versão anterior (30/09): `index-anterior.html`, `aula-ml-3-anterior.ipynb`, `mlruns-anterior/` (experimento `aula-ml-3-churn`), `css/style-anterior.css`. O `saidas.py` e o `numeros.json` são dessa versão e não batem com os slides novos. O LEIA-ME antigo dizia que a run `logistica-balanceada` de lá alimenta `../aula-ml-6/modelos/churn`.
