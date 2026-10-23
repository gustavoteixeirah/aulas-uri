# Programação para Ciência de Dados — Plano das 18 Aulas
### Versão para turma com experiência prévia em programação

**Carga horária:** 60h · 4 créditos · 18 encontros de ~3h20
**Linguagem:** Python 3 · **Ambiente:** Google Colab (aulas 1–2) → Colab + local (aulas 3+)

---

## 1. Premissa que reorganiza tudo

A turma já programa. Isso muda três decisões estruturais:

1. **Fundamentos de linguagem em 2 aulas, não 4.** Não se ensina o que é uma variável ou um laço — ensina-se o que Python faz *diferente*: indentação como sintaxe, tipagem dinâmica, fatiamento, comprehensions, mutabilidade. Um bom programador absorve isso em duas sessões.
2. **As 2 aulas liberadas vão para o projeto.** A grade final dá **5 encontros de machine learning** e **6 de oficina** — os grupos escrevem em sala, com atendimento. Aquisição de dados (SQL, APIs, scraping) ficou de fora; ver a nota no mapa geral.
3. **A dificuldade da disciplina se desloca.** Para quem já programa, o desafio não é sintaxe — é abandonar o laço explícito em favor da vetorização, e é a parte estatística. Programador experiente escreve `for` sobre linhas de DataFrame por meses se ninguém o confrontar com um `%timeit`. Combata isso desde a aula 3.

---

## 2. Mapa geral

| Bloco | Aulas | Conteúdo |
|---|---|---|
| Introdução + Fundamentos | 1–2 | Panorama da área, o pipeline, datasets na prática |
| Manipulação e análise | 3–5 | NumPy, Pandas, limpeza e transformação |
| Um projeto de ponta a ponta | 6 | o trabalho inteiro demonstrado — última aula de conteúdo antes da Etapa 1 |
| **Oficina da Etapa 1** | **7–9** | **os grupos escrevem em sala · entrega em 25/09** |
| Machine Learning | 10–14 | estatística descritiva, validação, regressão, classificação, ajuste |
| **Oficina da Etapa 2** | **15–17** | **exploração → modelagem → escrita · entrega em 19/11** |
| Devolutiva | 18 | leitura dos trabalhos entregues e fechamento |

**11 aulas de conteúdo, 6 de oficina e 1 de devolutiva.** As oficinas não têm slides: os grupos
trabalham em sala e o professor circula. Duas consequências desta grade, assumidas:
**sai a prova prática** (a avaliação passa a ser projeto + listas) e **sai o bloco de aquisição
de dados** — SQL, APIs e scraping ficam fora do semestre, porque os grupos já terão escolhido
o dataset quando ele seria dado. A estatística descritiva, que era a aula 7, foi absorvida pela
abertura do bloco de ML, onde ela é pré-requisito imediato.

---

## 3. Avaliação

O semestre tem **duas notas**, e o projeto final responde pela maior parte das duas.
Pesos sugeridos — confirme no plano de ensino oficial:

| Nota 1 · até 25/09 | Peso |
|---|---|
| **Entrega 1 do projeto** — relatório SBC, seções 1 a 4 | 70% |
| Listas 1 e 2 — aulas 2 e 5 | 30% |

| Nota 2 · 01/10 a 19/11 | Peso |
|---|---|
| **Entrega 2 do projeto** — relatório completo | 70% |
| Listas 3 e 4 — aulas 12 e 14 | 30% |

> **Sem prova.** A prova prática que valia 35% da Nota 2 foi cortada quando as aulas 10 e 11
> viraram machine learning; os pontos foram para a Entrega 2. Com isso o projeto responde por
> **70% das duas notas** — o que aumenta o peso do acompanhamento nas oficinas e do combate
> à terceirização por IA. A antiga Lista 3, que caía na aula 7, sai junto com a aula.

**Não há apresentação.** O trabalho é avaliado pelo texto: um artigo no **template da SBC**,
acompanhado do notebook que produziu cada número dele.

**Projeto final — divulgue na aula 2.** Grupos de **até 3 pessoas**. Dataset público
(dados.gov.br, Brasil.io, IBGE/SIDRA, Base dos Dados, Kaggle) com mínimos duros — ≥ 2.000
registros, colunas de tipos variados e faltantes reais, conferidos com quatro linhas de pandas.
Três perguntas de negócio, limpeza + EDA + visualização + pelo menos um modelo, e uma seção
obrigatória de **limitações**.

Entrega em duas etapas: **25/09** (seções 1 a 4, Nota 1) e **19/11** (relatório completo, Nota 2).
A segunda entrega inclui as seções da primeira **revisadas** — erro apontado e não corrigido conta
duas vezes contra.

Para esta turma, exija também: `requirements.txt`, repositório Git com histórico real e o teste de
reprodutibilidade (clonar → instalar → *Run All* → os números do PDF batem com os do notebook).
Eles têm condição de entregar isso, e é o que separa um notebook de um artefato profissional.

**Defesa contra cópia de IA — sem arguição oral.** Toda conclusão precisa apontar o número que a
sustenta, e todo número precisa existir numa célula que roda. Texto genérico, sem os dados do grupo,
aparece na primeira leitura.

**Política de IA generativa — anuncie na aula 1.** Sugestão: liberada para dúvidas e explicação de código, uso obrigatoriamente declarado no projeto. Sem prova, o controle passa a ser o acompanhamento nas oficinas — você vê o trabalho nascer, e trabalho terceirizado não sobrevive a três aulas de atendimento. Com uma turma que programa, presumir que não usarão é ingenuidade.

---

## 4. As 18 aulas

### Aula 1 — Introdução, fundamentos de Python e primeiro projeto
*(notebook pronto em anexo; roteiro minuto a minuto na seção 5)*

Panorama da área. **O pipeline de ciência de dados como espinha dorsal da aula** — as 7 etapas, sua natureza cíclica, a distribuição real do tempo e o modo típico de falha de cada uma. Python idiomático em ritmo acelerado: sintaxe, tipos, controle de fluxo, listas/dicionários/tuplas/sets, fatiamento, comprehensions, funções, armadilhas. Encerra percorrendo o pipeline inteiro num projeto real — previsão de tarifa de táxi a partir de 6.400 corridas de Nova York — com cada seção nomeada pela etapa correspondente.

O pipeline é o mapa que dá sentido às outras 17 aulas: cada uma aprofunda uma etapa. Apresentá-lo no primeiro dia faz com que a turma sempre saiba onde está.

### Aula 2 — Datasets: de onde vêm e o que há dentro
- **De onde vem o dado:** onde os datasets vivem, Kaggle por dentro, o que checar antes de baixar
- **O Titanic no notebook, ao vivo:** carregar, medir, cruzar, desenhar — do arquivo bruto a cinco achados, sem nenhum modelo
- Taxa e o `n` · a média que mente · o vazio que é informação · a coluna escondida dentro do nome · imputação e seu custo
- **Encerrar apresentando o projeto final** (20 slides próprios, para postar no AVA)
- **Entrega:** Lista 1 — repetir a análise do Titanic em outro dataset

> A aula não ensina sintaxe de Python. A turma escreve código com ajuda de IA; o que se ensina
> é o raciocínio sobre o dado. O ferramental de linguagem que estava aqui saiu do plano.

### Aula 3 — NumPy
- `ndarray`: dtype, shape, contiguidade em memória, por que é rápido
- **Vetorização vs laço, medido com `%timeit` ao vivo.** Esta é a aula que muda o hábito da turma.
- Fatiamento em N dimensões, indexação booleana, *fancy indexing*
- *Broadcasting* — a regra e seus erros clássicos
- Agregações e o significado de `axis`
- View vs cópia (a versão NumPy do aliasing de referências)
- **Exercício:** processar 10 milhões de valores nas duas formas e comparar

### Aula 4 — Pandas: fundamentos
- `Series`, `DataFrame`, e o índice como conceito de primeira classe
- `read_csv` e os parâmetros que salvam o dia: `sep`, `encoding`, `parse_dates`, `na_values`, `dtype`, `usecols`, `chunksize`
- Inspeção: `info`, `describe`, `dtypes`, `value_counts`, `nunique`
- Seleção: `[]` vs `.loc` vs `.iloc` — a distinção que gera mais bug na carreira de todo mundo
- Indexação booleana, `query`, `isin`, `between`
- `SettingWithCopyWarning`: o que é, por que aparece, como resolver

### Aula 5 — Limpeza e transformação
- Dados faltantes: `isna`, `dropna`, `fillna`; imputação por média, mediana, forward-fill — e a decisão de negócio por trás de cada uma
- Duplicatas, conversão de tipos, `astype`, `category`
- Datas: `to_datetime`, o acessador `.dt`, fusos
- Texto: acessador `.str`, regex, normalização (acentos, caixa, espaços)
- Colunas derivadas: `assign`, `apply`, `map`, `np.where`, `pd.cut`
- Outliers: IQR, z-score, e quando *não* remover
- **Exercício:** dataset propositalmente sujo, preparado por você
- **Entrega:** Lista 2

### Aula 6 — Um projeto de ponta a ponta *(04/09)*
*Última aula de conteúdo antes da Etapa 1. Material pronto em `aula6-projeto/`.*

- Um projeto real percorrido nas 7 seções do relatório, com o peso de cada uma ao lado
- Dataset Olist — 95.824 pedidos de e-commerce brasileiro, 7 tabelas
- Agregação e cruzamento de tabelas aparecem **embutidos**, como meio: o funil de preparação
  (99.441 → 95.824) e a chave de avaliação que repete
- Modelagem demonstrada: baseline, split temporal, matriz de confusão, e **vazamento de dados**
- Fecha com a régua de avaliação, o teste de reprodutibilidade e o calendário até 25/09
- **Tarefa da semana:** escolher o dataset e as três perguntas

> **O conteúdo de agregação** (`groupby`, `agg`, `transform`, `merge`, `pivot_table`,
> séries temporais e Matplotlib) tem material completo pronto em `aula6/` — 87 slides com
> saídas reais e verificadas. Ele **não vira aula**: fica como referência para os grupos
> consultarem durante as oficinas, e é de lá que sai a resposta quando alguém travar
> num cruzamento de tabelas.

### Aulas 7 a 9 — Oficina da Etapa 1 *(11/09, 18/09, 25/09)*
*Sem slides. Os grupos trabalham em sala e você circula.*

- **Aula 7 (11/09) — o dataset.** Cada grupo roda as quatro linhas (`shape`, `dtypes`,
  `nunique`, `isna`) na frente de você e você aprova, ou não, o dataset e as três perguntas.
  Quem chega sem dataset perde a aula — avise na aula 6.
- **Aula 8 (18/09) — seções 1 a 3.** Escrita em sala, atendimento grupo a grupo. Mini-clínicas
  por demanda: leitura do arquivo, dicionário de dados, unidade de observação.
- **Aula 9 (25/09) — seção 4 e fechamento.** A limpeza justificada, o template SBC na prática,
  **revisão cruzada** (cada grupo lê o relatório de outro) e o **teste de reprodutibilidade**
  (clonar o repositório do colega e rodar).
- **Entrega 1 — 25/09, no fim do dia da aula 9.** Vale a Nota 1.

---

### Aula 10 — Estatística descritiva e o que é "aprender" com dados *(01/10)*
*Abre o bloco de ML. A primeira metade é o que era a antiga aula 7 — e é pré-requisito real
para ler qualquer métrica de modelo.*

- Tendência central e por que a média engana em distribuição assimétrica
- Dispersão: variância, desvio padrão, IQR; distribuições e assimetria
- Correlação: Pearson × Spearman; o quarteto de Anscombe (mostrar, não descrever)
- **Correlação ≠ causalidade**, com exemplos de erro real; paradoxo de Simpson
- Então: aprendizado supervisionado × não supervisionado, classificação × regressão
- Features, target, generalização — por que "decorar" não é aprender
- A API do scikit-learn: `fit`/`predict`/`transform`

### Aula 11 — Validação, e o erro que infla tudo *(08/10)*
- `train_test_split`; por que nunca avaliar no treino
- Overfitting × underfitting; viés × variância
- KNN como primeiro modelo, por ser geometricamente intuitivo
- **Validação cruzada** k-fold e estratificada
- **Vazamento de dados** — o erro mais comum e mais caro da área. Demonstre ao vivo: normalizar
  antes do split e ver a métrica inflar. `Pipeline` como defesa estrutural
- Split temporal: quando os dados têm data, sortear linhas é trapaça
- **Checkpoint 2 do projeto:** EDA feita, as 3 perguntas com respostas preliminares

### Aula 12 — Regressão *(15/10)*
- Regressão linear simples e múltipla; interpretação de coeficientes
- Mínimos quadrados: a intuição geométrica, sem álgebra pesada
- Métricas: MAE, RMSE, R² — o que cada uma esconde
- Pré-processamento: `StandardScaler`, `OneHotEncoder`, `Pipeline`
- Regularização: Ridge e Lasso, e por que existem
- Árvores de regressão e Random Forest — visão prática
- **Entrega:** Lista 3

### Aula 13 — Classificação *(22/10)*
*A aula mais densa do bloco. Chegue com o material fechado.*

- Regressão logística: por que é classificação apesar do nome; leitura em probabilidade
- Árvore de decisão, Random Forest, Gradient Boosting
- **Matriz de confusão**; acurácia, precisão, recall, F1 — e o *trade-off* como decisão de negócio
- Por que acurácia engana em base desbalanceada (o classificador de fraude que acerta 99%)
- Curva ROC, AUC, ajuste de limiar
- Classes desbalanceadas: `class_weight`, reamostragem
- *A aula 6 já mostrou tudo isso funcionando no Olist — retome aquele exemplo.*

### Aula 14 — Ajuste, não supervisionado e produção *(29/10)*
- `GridSearchCV` e `RandomizedSearchCV`; curvas de aprendizado; seleção de features
- Importância de variáveis por permutação — e por que ela é mais honesta que a interna
- **Não supervisionado:** k-means e a escolha de k (cotovelo, silhueta), PCA e variância
  explicada, detecção de anomalias — em panorama
- **Do notebook à realidade:** serialização de modelos, panorama de MLOps, *drift*
- **Entrega:** Lista 4 · **Checkpoint 3 do projeto:** modelo rodando, com baseline e métrica

---

### Aulas 15 a 17 — Oficina da Etapa 2 *(05/11, 12/11, 19/11)*
*Sem slides. Uma etapa do trabalho por encontro.*

- **Aula 15 (05/11) — exploração.** A EDA que *responde às três perguntas*, não a que enfeita.
  Escolha do modelo e definição do baseline de cada grupo.
- **Aula 16 (12/11) — modelagem.** Treino, métrica e validação no dataset de cada grupo.
  Clínica de vazamento. Leitura crítica: métrica boa demais quase sempre é erro.
- **Aula 17 (19/11) — escrita e entrega.** Conclusões que respondem às perguntas, a seção de
  limitações, figuras com legenda, referências no padrão SBC. Revisão cruzada e teste de
  reprodutibilidade entre grupos.
- **Entrega 2 — 19/11, no fim do dia da aula 17.** Vale a Nota 2.

### Aula 18 — Devolutiva *(26/11)*
*Depois da entrega. É a aula que fecha o semestre.*

- Leitura comentada dos trabalhos: os achados que valeram a pena e os erros que se repetiram
- Os três ou quatro trabalhos mais fortes, mostrados com autorização do grupo — é o melhor
  material de referência que a turma vai ter
- O que cada erro recorrente teria custado num contexto profissional
- Trilha de estudo: o que vem depois desta disciplina

---

## 5. Aula 1 — roteiro minuto a minuto

**Objetivo:** ao sair, todo aluno terá escrito Python idiomático e construído um modelo preditivo que ele consegue explicar linha por linha.

| Tempo | Bloco | Como conduzir |
|---|---|---|
| 0:00–0:15 | Abertura | Sua apresentação. Trajetória prática pesa mais que credencial nesta turma. |
| 0:15–0:35 | Diagnóstico | Enquete: quais linguagens já usaram? quem já mexeu com SQL, Excel, estatística? o que esperam da disciplina? **Anote os números** — o resto do semestre se calibra por isso. Com turma que programa, pergunte especificamente sobre estatística: é lá que estará a lacuna. |
| 0:35–0:50 | Panorama da área | O que faz um cientista de dados, papéis adjacentes (analista, engenheiro de dados, engenheiro de ML), mercado. Por que Python, com comparação honesta a R, SQL e Scala. |
| 0:50–1:12 | **O pipeline** | Projete o diagrama. Percorra as 7 etapas, depois desmonte a ilusão de linearidade: mostre os retornos, a distribuição real do tempo (60–80% nas etapas 2–4) e a tabela de falhas típicas. **Este é o bloco que estrutura o semestre inteiro** — não o comprima se atrasar; corte do panorama. |
| 1:12–1:20 | Setup do Colab | Rápido. Célula, execução, estado entre células, *restart and run all*. Todos executam `print("olá")`. |
| 1:20–1:35 | **Intervalo** | |
| 1:35–2:40 | **Parte 1 do notebook** | Python para quem já programa. Ritmo rápido — eles acompanham. Pare de verdade em quatro pontos: **fatiamento** (reaparece em NumPy e Pandas), **comprehensions** (idioma central), **desempacotamento**, e a tabela de **armadilhas** no final. O bug do default mutável merece os 3 minutos que leva para demonstrar. |
| 2:40–3:12 | **Parte 3 do notebook** | O projeto do táxi, com o diagrama ainda projetado ao lado. **Anuncie a etapa antes de cada seção** — "agora estamos na etapa 4, preparação". A repetição é o que fixa o mapa. Conduza como investigação: faça a pergunta, deixe-os prever, então execute. |
| 3:12–3:20 | Fechamento | Plano de ensino, avaliação, política de IA generativa, tarefa. |

**Notas de condução**

- **Deixe o diagrama projetado durante o projeto inteiro.** O ganho não está em explicar o pipeline uma vez, está em percorrê-lo com ele à vista. Quando a etapa 3 revelar as corridas com distância zero e isso obrigar a mexer na etapa 4, aponte para a seta de retorno no diagrama. É a diferença entre a turma memorizar sete caixas e entender que o processo é cíclico.
- **Não corra a Parte 1 até o fim se a turma engajar.** Se faltar tempo, corte funções (seção 1.5) — eles já sabem o conceito e a sintaxe se pega sozinho. Nunca corte a Parte 3: o projeto é o que dá concretude ao pipeline e o que vende a disciplina.
- **O contraste da etapa 5 é o momento pedagógico da aula.** Doze linhas de laço e dicionário viram um `groupby`. Para quem já programa, esse é o argumento que realmente convence — deixe-os ver as duas versões lado a lado antes de comentar.
- **A gorjeta em dinheiro dá exatamente zero.** Não deixe passar como curiosidade. Pergunte à turma: essas pessoas não dão gorjeta, ou o sistema não registra? Ninguém consegue decidir com os dados disponíveis. É a primeira lição de ceticismo sobre a origem do dado — e é exatamente a falha característica da etapa 2 na tabela.
- **Encerre pela última seção da etapa 7 (limitações).** É o que transforma um exercício técnico em postura profissional, e é o que você vai cobrar no projeto final.
- **Plano B:** Colab depende de rede. Leve o notebook exportado em HTML, o dataset em CSV e o diagrama em PNG no pendrive.

**Material:** notebook `aula01_fundamentos_e_projeto.ipynb` · diagrama `pipeline_ciencia_de_dados.png` (e `.svg`, editável) · plano de ensino

---

## 6. Notas para você, vindo de engenharia de backend

- **Deixe SOLID na porta — mas só do notebook.** Análise exploratória é rascunho; arquitetura ali vira cerimônia. O que vale insistir desde já: nomes descritivos, funções puras para transformações reutilizáveis, e reprodutibilidade — que é o "funciona na minha máquina" desta área. Na aula 14, quando o assunto vira produção, e nas oficinas, quando eles montam o repositório, seu repertório de engenharia passa a ser exatamente o diferencial da disciplina.
- **Vetorização é o antipadrão a combater.** O reflexo de iterar linha a linha é forte em quem já programa. Meça na frente deles na aula 3; um `%timeit` com 100× de diferença encerra a discussão de forma que nenhum argumento encerra.
- **Tipos existem, mas mudam de papel.** Em Pandas o tipo é propriedade do dado, não contrato de interface. O reflexo a instalar não é `mypy` — é `df.dtypes` e `df.info()` como primeiro comando diante de qualquer dataset.
- **`SettingWithCopyWarning` é aliasing de referência.** Você já entende o problema; use a analogia com cópia de referência em Java, funciona bem com esta turma.
- **A dificuldade real virá da aula 7.** Programador experiente aprende Pandas rápido e estatística devagar. Não confunda fluência sintática com competência analítica — nem na turma, nem na avaliação.
