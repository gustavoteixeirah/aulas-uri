# Aula ML 06 — Deploy, e o que ficou de fora

Slides em `index.html`. O agrupamento roda em `aula-ml-6.ipynb`. O serviço não é célula: é o comando abaixo, no terminal, durante o slide do contrato.

O modelo em `modelos/churn` é a run `logistica-balanceada` da aula 3, corte 0,5, recall 0,801. Esta aula não retreina.

## Subir o serviço

Com o ambiente em que o MLflow está instalado ativo, para o `uvicorn` estar no `PATH`:

```bash
mlflow models serve -m modelos/churn -p 5001 --no-conda
```

O pedido completo, as 19 colunas, está em `pedido.json`. É a primeira linha do arquivo da aula 3: tenure 1, contrato mensal, cobrança 29,85.

```bash
curl -s -X POST http://127.0.0.1:5001/invocations \
  -H "Content-Type: application/json" \
  -d @pedido.json
```

Resposta obtida ao servir este artefato:

```json
{"predictions": [{"probabilidade_sai": 0.850764027564424, "sai": 1}]}
```

O mesmo pedido sem `MonthlyCharges` está em `pedido-incompleto.json`. A resposta recusa o contrato:

```text
Model is missing inputs ['MonthlyCharges'].
```

## O agrupamento

```bash
python saidas.py
```

200 clientes. O cotovelo dobra em k = 5 (a queda da inércia vai de 43 para 10). Os centros, em mil dólares de renda e score de gasto: meio (55, 50), alto/alto (87, 82), alto/baixo (88, 17), baixo/baixo (26, 21), baixo/alto (26, 79).
