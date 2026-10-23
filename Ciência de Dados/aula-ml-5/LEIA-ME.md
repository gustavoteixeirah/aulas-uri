# Aula ML 05 — Séries temporais

Slides em `index.html`. Caderno em `aula-ml-5.ipynb`. Runs em `mlruns/`, experimento `aula-ml-5-bicicletas`.

```bash
export MLFLOW_ALLOW_FILE_STORE=true
python saidas.py
```

O `train.csv` traz os dias 1 a 19 de cada mês (10.886 horas). Treino é 2011 (5.422 horas). Teste é 2012 (5.464).

| run | RMSE |
|---|---|
| baseline, lag de 7 dias, 3.445 horas em que o par existe | 95 |
| reta com calendário, 2012 inteiro | 159 |
| a mesma reta, nas mesmas 3.445 horas | 162 |
| a mesma reta, com split aleatório | 111 |

A reta não ganha da semana anterior. O split aleatório fica mais bonito que o corte no tempo e ainda perde para a baseline. `casual` e `registered` somam `count` em todas as linhas e ficam fora do modelo.
