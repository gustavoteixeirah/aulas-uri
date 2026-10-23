# Aula ML 03 — Algoritmos de classificação (15/10, aula gravada)

Slides em `index.html` (16 slides): capa, aula 1 → aula 2 → hoje, o dataset, e 3 slides por algoritmo (a ideia, a fórmula, o cliente 157 passo a passo). A comparação dos quatro fica no caderno `aula-ml-3.ipynb`.

Apostila (no lugar da aula gravada): `apostila-aula-3.pdf`, gerada de `apostila-aula-3.html` (Chrome headless, imprimir em PDF).

Caso de uso: Telco Customer Churn (`dados/WA_Fn-UseC_-Telco-Customer-Churn.csv`, fonte: https://www.kaggle.com/datasets/blastchar/telco-customer-churn, dados de exemplo da IBM), quem vai cancelar. Entradas: `tenure`, `MonthlyCharges`, `TotalCharges`, `Contract` (one-hot). As 11 linhas com `TotalCharges` vazio saem (7.043 → 7.032). Split 75/25, `stratify=y`, `random_state=0`. Os 4 algoritmos usam o mesmo preparo (escala nas numéricas, one-hot no contrato) num pipeline.

O caderno treina e compara: chute "sempre fica", regressão logística, KNN (k=5), Naive Bayes (GaussianNB), árvore de decisão (max_depth=4). Gera `img/g-comparacao.png` e mostra o cliente 157 do teste nos 4 modelos. Cada modelo vira uma run no MLflow (pasta `mlruns/`, experimento `classificadores`).

```bash
MLFLOW_ALLOW_FILE_STORE=true mlflow ui --backend-store-uri mlruns
```

Números do teste (1.758 clientes, 467 saíram):

| algoritmo | acurácia | precisão | recall | F1 |
|---|---|---|---|---|
| sempre fica | 0,734 | 0 | 0 | 0 |
| regressão logística | 0,788 | 0,638 | 0,469 | 0,541 |
| KNN | 0,790 | 0,629 | 0,507 | 0,562 |
| Naive Bayes | 0,664 | 0,432 | 0,833 | 0,569 |
| árvore | 0,786 | 0,625 | 0,486 | 0,547 |

## Versões anteriores (guardadas, não apagadas)

- 15/10, versão de 13 slides com a comparação nos slides: `index-v13.html` (usa `img/g-comparacao.png`).

- 14/10, aula de uma logística só (limiar, peso da classe): `index-churn-limiar.html`, cadernos em `anterior-churn-limiar/`, runs em `mlruns-churn-limiar/` (experimento `churn`). Os cadernos dessa pasta leem `dados/` e gravam em `img/` e `mlruns/`: para rodar de novo, copie de volta para a pasta da aula. O deck usa `img/g-sigmoide.png` e `img/g-evolucao.png`.
- 30/09: `index-anterior.html`, `aula-ml-3-anterior.ipynb`, `mlruns-anterior/` (experimento `aula-ml-3-churn`), `css/style-anterior.css`. O `saidas.py` e o `numeros.json` são dessa versão e não batem com os slides atuais. O LEIA-ME antigo dizia que a run `logistica-balanceada` de lá alimenta `../aula-ml-6/modelos/churn`.
