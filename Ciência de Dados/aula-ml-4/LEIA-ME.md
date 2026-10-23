# Aula ML 04 — Árvores, florestas e a comparação (22/10)

Slides em `index.html` (21 slides): capa, da reta da aula 2 para hoje, o dataset, onde a reta quebra (`img/g1-quilate.png`), e 3 slides por algoritmo (a ideia, a fórmula matemática, e o diamante 157 passo a passo). Comparação geral das runs (`img/g-comparacao.png`), importância por permutação (`img/g3-permutacao.png`) e fecho.

Apostila completa para leitura e estudo: `apostila-aula-4.pdf`, gerada de `apostila-aula-4.html` (Chrome headless, imprimir em PDF).

Caderno interativo: `aula-ml-4.ipynb`, com 20 células didáticas com todo o fluxo, treino dos seis modelos, visualização da árvore de decisão rasa, diagnóstico do overfitting, análise do diamante 157 e teste de permutação.

Caso de uso: Diamonds (`dados/diamonds.csv`, fonte: https://www.kaggle.com/datasets/shivam2503/diamonds). Preço de venda no atacado internacional a partir do peso em quilates, corte, cor, clareza e dimensões tridimensionais (x, y, z). As 20 pedras com dimensão zero saem antes do split (53.940 → 53.920). Split 75/25 fixo com `random_state=0` (40.440 treino / 13.480 teste). Todos os estimadores usam o mesmo preparo numérico (escala padronizada) e categórico (one-hot) num pipeline do scikit-learn.

Cada modelo vira uma run no MLflow (pasta `mlruns/`, experimento `aula-ml-4-diamonds`).

```bash
# Executar o script de treino e geração dos artefatos
python saidas.py

# Subir a interface visual do MLflow
MLFLOW_ALLOW_FILE_STORE=true mlflow ui --backend-store-uri mlruns
```

Números do teste (13.480 diamantes avaliados):

| modelo | hiperparâmetros | RMSE Teste (US$) | MAE Teste (US$) | RMSE Treino (US$) | diagnóstico |
|---|---|---|---|---|---|
| árvore rasa | `max_depth=3` | 1.430 | 812 | 1.411 | underfitting (perde da reta) |
| regressão linear (reta) | padrão | 1.142 | 738 | 1.122 | baseline de referência linear |
| KNN | `n_neighbors=15` | 896 | 450 | 822 | pesado para produção |
| gradient boosting | `n_estimators=80, max_depth=3` | 891 | 461 | 872 | rápido e equilibrado |
| árvore funda | sem teto (`max_depth=None`) | 821 | 384 | **9** | overfitting severo |
| **floresta (random forest)** | `n_estimators=80, max_depth=16` | **624** | **302** | 367 | **campeã absoluta** |

## O Diamante 157 do Teste (exemplo concreto)
- **Pedra:** 2,01 quilates, corte *Ideal*, cor *G*, pureza *SI2*, x=8,13 mm, y=8,10 mm, z=5,01 mm.
- **Preço Real de Mercado:** **US$ 18.259**
- **Regressão Linear:** prevê US$ 14.081 (erro de −US$ 4.178 pela incapacidade de modelar a valorização exponencial dos diamantes de 2 quilates).
- **Árvore Rasa (prof. 3):** prevê US$ 14.898 (média das 1.560 pedras grandes que caíram na folha 14).
- **Árvore Funda:** memoriza pedras quase idênticas no treino e prevê US$ 18.181 (treino RMSE 9!).
- **KNN (k=15):** encontra 15 pedras no treino entre 2,00 e 2,05 quilates e prevê a média de US$ 15.277.
- **Gradient Boosting:** soma correções sequenciais de 80 árvores rasas a partir da média global e prevê US$ 15.461.
- **Floresta Aleatória (Random Forest):** a média dos votos independentes das 80 árvores converge para **US$ 16.131**, reduzindo o erro pela metade em relação à reta e vencendo no teste geral.
