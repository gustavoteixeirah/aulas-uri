# Aula ML 02 — Regressão linear, e o MLflow daqui pra frente

Slides em `index.html`. O caderno é `aula-ml-2.ipynb`. As quatro runs ficam em `mlruns/`, experimento `aula-ml-2-custo`.

```bash
export MLFLOW_ALLOW_FILE_STORE=true   # MLflow 3 exige isto para a pasta mlruns/
python saidas.py
mlflow ui --backend-store-uri mlruns
```

O `saidas.py` regrava figuras, `numeros.json` e as runs. Números que os slides afirmam, nesta semente (`random_state=0`):

| run | RMSE de teste |
|---|---|
| media | 12.549 |
| reta-idade | 11.745 |
| reta-com-vazamento | 5.669 |
| reta-pipeline | 5.669 |

A escala calculada antes do split não muda o RMSE da reta: a regressão linear absorve essa transformação. O slide 9 diz isso. O pipeline continua sendo o procedimento, porque o número não denuncia o vazamento.

O coeficiente falado em dólares por ano é o coeficiente da coluna padronizada dividido pelo desvio que o `StandardScaler` aprendeu no treino.
