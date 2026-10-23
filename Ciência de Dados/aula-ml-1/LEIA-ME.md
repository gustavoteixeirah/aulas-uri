# Aula ML 01 — Introdução à Machine Learning

Slides em HTML, no mesmo motor das aulas anteriores. São **22 slides** (capa + 23). O caderno segue as seções (sem ▸ Slide nas células); a coluna de número no intro do notebook liga cada seção ao slide HTML. Slides com **▸ caderno** têm seção correspondente em `aula-ml-1.ipynb`.

Abertura conceitual (slides 2–7): o que é ML, o que é um modelo, o modelo na prática (spam), tipos de ML, generalização e o ciclo. O slide **8** é o cronograma (6 aulas + 2 trabalhos). O caso dos pinguins começa no slide 9 (objetivo no 11).

## Mapa do miolo (dados → ciclo → prova)

| # | Título | caderno |
|---|---|---|
| 8 | Cronograma | — |
| 9 | Dataset | arquivo |
| 10 | Exploração | dentro |
| 11 | Objetivo | — |
| 12 | Pré-processamento | preprocessamento |
| 13 | Treino, validação e teste | separacao |
| 14 | Modelos de ML | — |
| 15 | O score do modelo | — |
| 16 | Por que a resposta é Adelie | — |
| 17 | Por que escalar | — |
| 18 | Treinar o modelo | treino |
| 19 | Uma predição no teste | predicao |
| 20 | Acurácia no teste | metrica |
| 21 | Ciclo preenchido | — |
| 22 | Rodem o notebook local | — |

Fluxo de código no ciclo: preprocess → split → (conceito logística) → fit → predict → accuracy → CV.

## Como abrir

Duplo clique em `index.html`.

| Ação | Como |
|---|---|
| Avançar / voltar | `→` `←`, espaço, ou os botões |
| Índice | `M` |
| PDF | `P` |
| Tema | `T` |
| Tela cheia | `F` |

O caderno abre com `jupyter lab aula-ml-1.ipynb`, a partir desta pasta, para o `dados/penguins_size.csv` resolver.

```bash
python saidas.py
```

Roda o ciclo de novo e regrava `img/` e `numeros.json`. Os números dos slides estão conferidos contra essa saída: 344 linhas, 2 incompletas, 85/86 na semente 0, 84/86 na semente 1, acurácia no teste ~0,988.

A primeira linha de `X_teste`, com a semente 0, o modelo erra (Adelie previsto como Chinstrap). O slide 19 usa um erro de propósito: uma predição no teste mostra o contrato; a métrica é a conta nos 86.
