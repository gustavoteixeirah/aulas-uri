# Seis aulas de Machine Learning

Especificação para montar as aulas. Cada aula vira uma pasta (`aula-ml-1` … `aula-ml-6`), com slides, caderno e o CSV em `dados/`. Este arquivo descreve o que entra em cada uma. O prompt para o agente que gera os slides fica para depois.

A turma já programa e já passou por pandas, limpeza e um projeto exploratório. Estas aulas não reabrem isso. Cada uma entrega uma regra do tipo: dado este objetivo, este é o modelo, e este é o jeito de medi-lo.

O MLflow entra na aula 2 e acompanha toda run até a aula 5. A aula 6 pega uma dessas runs e publica.

Stack do caderno: Python 3, pandas, scikit-learn, matplotlib, mlflow. Na aula 6, o serviço mínimo sobe com o próprio MLflow (`mlflow models serve`).

Toda figura e todo número na projeção saem do código rodado sobre o CSV da pasta. Nada de métrica decorada.

O CSV fica versionado em `dados/` para a aula rodar sem rede. O caderno também mostra a célula que baixa da origem, para a turma ver de onde o arquivo veio.

```python
import kagglehub
kagglehub.dataset_download("dono/nome-do-dataset")
```

| Aula | Dataset no Kaggle | Caso de uso | Modelo |
|---|---|---|---|
| 1 | Palmer Archipelago penguin data | Classificar a espécie a partir de medidas | Um classificador simples, com validação cruzada |
| 2 | Medical Cost Personal Datasets | Estimar um custo e ler o peso de cada fator | Regressão linear |
| 3 | Telco Customer Churn | Prever quem sai e escolher qual erro tolerar | Regressão logística |
| 4 | Diamonds | Prever um preço em que as categorias se cruzam | Floresta, comparada à reta |
| 5 | Bike Sharing Demand | Prever a demanda da próxima hora | Corte temporal e baseline sazonal |
| 6 | Mall Customer Segmentation | Agrupar sem coluna de resposta | K-means, e o deploy do modelo de churn |

---

## Aula 1 — Um modelo do começo ao fim

Pasta: `aula-ml-1`

### O que a aula ensina

A aula abre o que é aprender com dados: feature, alvo e a diferença entre acertar o que o modelo já viu e acertar um caso novo. Supervisionado e não supervisionado aparecem só o bastante para a turma saber em qual família está. O exemplo é o Palmer Archipelago penguin data, arquivo `penguins_size.csv`: medidas do bico, da asa e da massa entram, a espécie sai. O caso de uso é classificar um exemplar novo em uma de três categorias, com poucas colunas numéricas.

Numa tarde a turma percorre o ciclo inteiro. Prepara o mínimo, separa uma parte dos dados para prova, treina um classificador simples, prevê um pinguim que ficou de fora e mede o resultado com validação cruzada, para o número não depender de um único sorteio. No fim, cada etapa tem nome, e uma métrica tirada do próprio treino não conta como evidência.

A regra que fica: alvo categórico, problema pequeno, primeiro fecha o ciclo e só depois troca de algoritmo.

O classificador desta aula é uma regressão logística. Ela entra como o motor do ciclo. Coeficiente, limiar e matriz de confusão ficam para a aula 3.

### Dataset

- Página: https://www.kaggle.com/datasets/parulpandey/palmer-archipelago-antarctica-penguin-data
- Arquivo: `penguins_size.csv` (o simplificado, não o `penguins_lter.csv`)
- Cerca de 344 linhas
- Colunas: `species`, `island`, `culmen_length_mm`, `culmen_depth_mm`, `flipper_length_mm`, `body_mass_g`, `sex`
- Alvo: `species` (Adelie, Chinstrap, Gentoo)
- Features desta aula: as quatro medidas. Ilha e sexo ficam de fora, para o primeiro modelo caber num gráfico de duas variáveis
- Há linhas com medida ausente. O caderno descarta essas linhas e mostra quantas saíram. Imputação não é assunto desta aula

### Slides

1. **Capa.** Nome da aula e a pergunta: dada a medida de um bico, qual é a espécie.
2. **O que é aprender aqui.** O modelo ajusta uma regra nos exemplos e essa regra tem de valer para um exemplo que ele não usou no ajuste. Acertar a tabela de treino, sozinho, não é o objetivo.
3. **As duas famílias.** Supervisionado: existe coluna de resposta. Não supervisionado: não existe, e o trabalho vira agrupamento. A aula 6 volta nesta segunda família. Hoje é a primeira.
4. **Vocabulário mínimo.** Feature, alvo, treino, teste, generalização. Um diagrama de cinco caixas: pergunta, dados, separação, treino, prova. Esse diagrama volta no fechamento, com o que a turma acabou de fazer em cada caixa.
5. **O arquivo.** De onde veio (Kaggle, Palmer Station), o que é uma linha (um pinguim), as três espécies, as quatro medidas. Uma tabela com as primeiras linhas, saída real.
6. **O que tem dentro.** Contagem por espécie, um gráfico de dispersão bico × asa colorido pela espécie, e a contagem de linhas com medida ausente. A separação visual já antecipa que o problema é tratável.
7. **A separação.** Uma parte ajusta, a outra só entra na hora de medir. `train_test_split` com `stratify` na espécie, para as três classes aparecerem dos dois lados. Semente fixa, para a aula repetir.
8. **O modelo e uma predição.** A regressão logística treinada nas quatro medidas. Em seguida uma linha concreta, escolhida do teste, com as medidas na tela e a espécie prevista ao lado da espécie real.
9. **A métrica de uma separação só.** Acurácia no teste dessa semente. No slide seguinte, a mesma conta com outra semente, para a turma ver o número mexer. Daí a necessidade da validação cruzada.
10. **Validação cruzada.** A ideia do k-fold em um desenho: o dado se parte em k pedaços, cada pedaço é prova uma vez, a métrica é a média. `cross_val_score` com 5 folds, estratificado. Na tela: os cinco números e a média.
11. **O ciclo com nome.** O diagrama do slide 4, agora preenchido com o que rodou: arquivo, descarte das linhas incompletas, split, logística, uma predição, média dos cinco folds.
12. **A regra.** Alvo categórico e problema pequeno: feche o ciclo com um classificador simples e valide em mais de uma partição. Trocar de algoritmo é assunto das aulas seguintes.

### Caderno

Células na mesma ordem dos slides que têm código. Slides de conceito (2, 3, 4, 12) não ganham célula.

```python
import kagglehub
kagglehub.dataset_download(
    "parulpandey/palmer-archipelago-antarctica-penguin-data"
)
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

pinguins = pd.read_csv("dados/penguins_size.csv")
medidas = [
    "culmen_length_mm",
    "culmen_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]
pinguins = pinguins.dropna(subset=medidas + ["species"])

X = pinguins[medidas]
y = pinguins["species"]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=0
)

modelo = Pipeline([
    ("escala", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])
modelo.fit(X_treino, y_treino)

# uma linha do teste, mostrada na projeção
previsto = modelo.predict(X_teste.iloc[[0]])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
notas = cross_val_score(modelo, X, y, cv=cv, scoring="accuracy")
```

A escala entra dentro do pipeline para o hábito nascer cedo. A aula não explica o vazamento ainda. Isso é a aula 2, com a demonstração de calcular a escala antes do split.

---

## Aula 2 — Regressão linear, e o MLflow daqui pra frente

Pasta: `aula-ml-2`

### O que a aula ensina

O alvo passa a ser um número. O dataset é o Medical Cost Personal Datasets, arquivo `insurance.csv`: idade, IMC, filhos, fumante, região e o custo do plano. O caso de uso é estimar esse custo e dizer quanto cada fator pesa.

A média entra como baseline. A regressão linear é o modelo, porque o coeficiente do fumante e o da idade são a resposta que se quer ler. MAE, RMSE e R² entram cada uma com o que deixa passar. O split entra com calma: treino e teste, por que avaliar no treino infla o resultado, e o vazamento de calcular a escala antes de separar. Variáveis categóricas viram colunas numéricas, o numérico entra na mesma escala, e esse preparo mora dentro de um pipeline, para o teste repetir o caminho do treino.

Cada tentativa, a média e a regressão, com e sem o preparo dentro do pipeline, é registrada no MLflow: parâmetros, métrica e o artefato do modelo. Daqui até a aula 5, rodar um modelo inclui logar a run. A comparação deixa de ser print solto no notebook.

A regra que fica: prever um número e explicar o efeito de cada variável, comece pela reta e compare com a média.

O resíduo ainda guarda estrutura, em especial onde fumante e IMC se cruzam. A aula mostra esse resíduo e para. O modelo que trata cruzamento é a aula 4, em outro dataset, para a regra não ficar presa a este arquivo.

### Dataset

- Página: https://www.kaggle.com/datasets/mirichoi0218/insurance
- Arquivo: `insurance.csv`
- 1.338 linhas, 7 colunas: `age`, `sex`, `bmi`, `children`, `smoker`, `region`, `charges`
- Alvo: `charges`
- Nenhuma coluna é identificador. Todas podem entrar no modelo, depois de codificar `sex`, `smoker` e `region`

### Slides

1. **Capa.** Prever o custo e dizer o peso de cada fator.
2. **Quando o alvo é um número.** Regressão, ao lado da classificação da aula passada. A espécie era uma categoria. O custo é uma grandeza.
3. **O arquivo.** Origem, uma linha = um beneficiário, as sete colunas, `charges` como alvo. Primeiras linhas e `describe` de `charges`.
4. **A média, antes de qualquer reta.** Prever a média do treino para todo mundo. MAE e RMSE dessa previsão constante. Esse par de números é o piso: a reta precisa ganhar dele.
5. **Uma variável.** Custo contra idade, a reta ajustada por cima dos pontos, separados por fumante só no gráfico, para o olho ver dois grupos. O coeficiente da idade em frase: a cada ano a mais, o custo sobe este tanto, no modelo de uma variável.
6. **Várias variáveis.** O que um coeficiente diz quando as outras ficam paradas. Tabela dos coeficientes do modelo completo, com `smoker` em destaque. A aula lê dois ou três em voz alta e não transforma a tabela num desfile.
7. **Três métricas.** MAE na unidade do custo. RMSE, que pune mais o erro grande. R², a fração da variação que a reta acompanha, e o aviso de que R² alto não é, sozinho, um modelo certo.
8. **Treino e teste.** A mesma reta medida nos dois. O número do treino mais bonito que o do teste. Um slide só com essa comparação.
9. **Vazamento.** Duas contas lado a lado. Escala calculada no arquivo inteiro, antes do split. Escala calculada só no treino, dentro do pipeline. As duas métricas de teste na tela. O pipeline é a forma que impede a primeira conta.
10. **O pipeline.** `ColumnTransformer`: escala nas numéricas, one-hot nas categóricas, regressão linear no fim. O desenho do fluxo cabe num slide. O teste passa pelo mesmo objeto, sem refit.
11. **MLflow.** O que é uma run: parâmetros, métricas, artefato. O experimento desta aula. Quatro runs no mínimo: média, reta de uma variável, reta completa com vazamento, reta completa no pipeline. A interface aberta no projetor, ordenada por RMSE de teste.
12. **A regra.** Prever um número e citar o efeito: regressão linear, contra a média, medida no teste, com o preparo dentro do pipeline e a run registrada. O gráfico de resíduo fica no último slide como ponte: onde o erro ainda desenha um padrão, a reta não é o fim da história.

### Caderno

Sobe o tracking local na pasta da aula (`mlruns/`) e deixa o `mlflow ui` de pé antes do bloco 11.

```python
import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mlflow.set_experiment("aula-ml-2-custo")

custos = pd.read_csv("dados/insurance.csv")
alvo = "charges"
numericas = ["age", "bmi", "children"]
categoricas = ["sex", "smoker", "region"]

X = custos[numericas + categoricas]
y = custos[alvo]
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=0
)

def metricas(y_verdadeiro, y_previsto):
    return {
        "mae": mean_absolute_error(y_verdadeiro, y_previsto),
        "rmse": float(np.sqrt(mean_squared_error(y_verdadeiro, y_previsto))),
        "r2": r2_score(y_verdadeiro, y_previsto),
    }

with mlflow.start_run(run_name="media"):
    previsao = np.full_like(y_teste, fill_value=y_treino.mean(), dtype=float)
    mlflow.log_metrics({f"teste_{k}": v for k, v in metricas(y_teste, previsao).items()})

preparo = ColumnTransformer([
    ("num", StandardScaler(), numericas),
    ("cat", OneHotEncoder(drop="first"), categoricas),
])
reta = Pipeline([
    ("preparo", preparo),
    ("modelo", LinearRegression()),
])

with mlflow.start_run(run_name="reta-pipeline"):
    reta.fit(X_treino, y_treino)
    previsao = reta.predict(X_teste)
    mlflow.log_metrics({f"teste_{k}": v for k, v in metricas(y_teste, previsao).items()})
    mlflow.sklearn.log_model(reta, name="modelo")
```

A run com vazamento repete o ajuste calculando média e desvio no `X` inteiro, antes do split, e loga com `run_name="reta-com-vazamento"`. Os coeficientes saem de `reta.named_steps["modelo"].coef_` alinhados aos nomes do `OneHotEncoder`.

---

## Aula 3 — Classificação

Pasta: `aula-ml-3`

### O que a aula ensina

O alvo vira sim ou não. O dataset é o Telco Customer Churn: para cada cliente, serviços, contrato, cobrança e a coluna `Churn`. O caso de uso é prever quem cancela, sabendo que errar os dois lados custa coisas diferentes.

Quem sai é minoria, cerca de um em cada quatro, então um modelo que responde "fica" para todo mundo já acerta a maior parte e não serve para nada. Regressão logística, a leitura em probabilidade e o limiar que transforma probabilidade em decisão. Matriz de confusão, precisão, recall e F1. O que muda ao pesar a classe minoritária ou ao mexer no limiar. A turma escolhe a métrica pelo custo do erro.

Cada limiar e cada peso de classe vira uma run, no mesmo experimento, para a diferença aparecer na tabela do MLflow.

A regra que fica: alvo sim ou não, classes desbalanceadas, escolha a métrica pelo custo do erro e use regressão logística.

O pipeline e o split são os da aula 2. A aula reaproveita o desenho e troca o modelo e as métricas.

### Dataset

- Página: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- Arquivo: `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- 7.043 linhas, 21 colunas
- Alvo: `Churn` (`Yes` / `No`)
- `customerID` não entra no modelo
- `TotalCharges` vem como texto e tem células vazias. A conversão para número e o preenchimento acontecem dentro do pipeline, não num `fillna` solto antes do split
- Features: as demais. São muitas categóricas (`Contract`, `InternetService`, `PaymentMethod`, e os serviços sim/não). O one-hot da aula 2 resolve

### Slides

1. **Capa.** Quem cancela no mês que vem, e qual erro a operadora aguenta.
2. **Sim ou não.** A espécie da aula 1 tinha três classes e o interesse era acertar. Aqui são duas classes e os erros não são simétricos: deixar escapar quem vai sair, e incomodar quem ia ficar.
3. **O arquivo.** Uma linha = um cliente. O que há de serviço, contrato e cobrança. `Churn` como alvo. `customerID` riscado na lista de colunas.
4. **A acurácia que mente.** A proporção de `Churn == No` na tela. Um classificador constante que prevê "fica" para todos, com a acurácia dessa regra. Esse número é o baseline. Qualquer modelo tem de ser lido contra ele, e a acurácia sozinha não distingue os dois.
5. **Probabilidade.** A logística devolve um número entre 0 e 1. Não é a classe. Um histograma das probabilidades no teste, com a massa de quem ficou e de quem saiu em cores diferentes.
6. **Limiar.** A classe nasce quando a probabilidade passa de um corte. O corte 0,5 é uma escolha, não uma lei. Três cortes (0,3, 0,5, 0,7) com a quantidade de alertas que cada um dispara.
7. **Matriz de confusão.** As quatro casas, com os nomes em frase: acertou quem fica, acertou quem sai, alertou à toa, deixou passar. Uma matriz desenhada para o corte 0,5, números reais.
8. **Precisão, recall, F1.** Precisão: dos alertas, quantos saíram de fato. Recall: de quem saiu, quantos o alerta pegou. F1 como meio-termo quando ninguém declarou o custo. A aula não apresenta curva ROC. O limiar já carrega a decisão.
9. **Peso da classe.** `class_weight="balanced"` numa run ao lado da run sem peso, mesmo corte. O recall de quem sai sobe, a precisão cai. As duas linhas na mesma tabela.
10. **MLflow.** Um experimento `aula-ml-3-churn`. Runs: constante "fica", logística no corte 0,5, logística nos cortes 0,3 e 0,7, logística com peso balanceado. Colunas: precisão, recall e F1 da classe que sai, mais a acurácia, para a acurácia aparecer alta numa run que a turma já descartou.
11. **A escolha.** A turma declara um custo, por exemplo "deixar passar quem sai custa mais do que um contato inútil", e aponta a run que obedece a esse custo. A regra fecha o slide: a métrica se escolhe antes de comemorar o número.

### Caderno

```python
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

mlflow.set_experiment("aula-ml-3-churn")

clientes = pd.read_csv("dados/WA_Fn-UseC_-Telco-Customer-Churn.csv")
clientes["TotalCharges"] = pd.to_numeric(clientes["TotalCharges"], errors="coerce")
y = (clientes["Churn"] == "Yes").astype(int)
X = clientes.drop(columns=["customerID", "Churn"])

numericas = ["tenure", "MonthlyCharges", "TotalCharges"]
categoricas = [c for c in X.columns if c not in numericas]

preparo = ColumnTransformer([
    ("num", Pipeline([
        ("nulos", SimpleImputer(strategy="median")),
        ("escala", StandardScaler()),
    ]), numericas),
    ("cat", Pipeline([
        ("nulos", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]), categoricas),
])

def avaliar(y_verdadeiro, probabilidade, corte):
    classe = (probabilidade >= corte).astype(int)
    return {
        "acuracia": accuracy_score(y_verdadeiro, classe),
        "precisao_sai": precision_score(y_verdadeiro, classe, zero_division=0),
        "recall_sai": recall_score(y_verdadeiro, classe, zero_division=0),
        "f1_sai": f1_score(y_verdadeiro, classe, zero_division=0),
    }

# logística no pipeline; logar um start_run por corte e outro com class_weight="balanced"
```

A conversão de `TotalCharges` antes do split é leitura de tipo, não estatística do alvo. A mediana que preenche o vazio fica no `SimpleImputer`, dentro do pipeline, ajustada só no treino.

A run constante prevê a classe 0 para todo o teste e entra no mesmo experimento, para o slide 4 e o slide 10 usarem o mesmo número.

---

## Aula 4 — Árvores, florestas e a comparação

Pasta: `aula-ml-4`

### O que a aula ensina

Quando a relação não é uma reta e as categorias interagem, entram a árvore de decisão, que dá para desenhar, a floresta aleatória e uma visão prática de gradient boosting, sem a álgebra. O KNN fecha o menu como o modelo que decide pela vizinhança.

O dataset é o Diamonds: quilate, corte, cor, clareza e o preço. O caso de uso continua sendo prever um número, mas corte, cor e clareza se cruzam com o quilate, e a relação deixa de ser uma reta. No mesmo split, a regressão linear, a árvore e a floresta aleatória entram como runs, com boosting e KNN no mesmo experimento. Importância de variável por permutação, mais honesta do que a conta interna da árvore.

A floresta leva quando o objetivo é errar menos. A reta fica quando o objetivo é citar o coeficiente. A escolha do algoritmo é a leitura dessa tabela: quem ganhou no teste, com qual erro, e o que mudou de um parâmetro para o outro.

A regra que fica: o alvo ser um número não decide o modelo. Decide a forma da relação.

### Dataset

- Página: https://www.kaggle.com/datasets/shivam2503/diamonds
- Arquivo: `diamonds.csv`
- Cerca de 54 mil linhas
- Colunas: `carat`, `cut`, `color`, `clarity`, `depth`, `table`, `price`, `x`, `y`, `z`
- Alvo: `price`
- `x`, `y`, `z` são as dimensões em milímetros. Entram no modelo. Linhas com dimensão 0 saem antes do split, com a contagem anunciada. São defeito de medida, não outlier de preço
- `cut`, `color` e `clarity` são categóricas ordenadas. No primeiro modelo entram como one-hot, igual à aula 2, para a comparação não misturar "mudei o algoritmo" com "mudei a codificação"

### Slides

1. **Capa.** O mesmo tipo de alvo da aula 2, um preço, e um modelo diferente.
2. **Onde a reta quebra.** Preço contra quilate. A nuvem curva. Um segundo gráfico, o mesmo quilate partido pelos níveis de `cut` ou `clarity`, para o cruzamento aparecer sem frase abstrata.
3. **O arquivo.** Origem, uma linha = um diamante, o alvo `price`, as categorias de corte, cor e clareza numa legenda curta (o que cada letra significa).
4. **A reta, de novo.** O pipeline da aula 2 neste arquivo. RMSE de teste logado. Serve de referência, não de campeão antecipado.
5. **A árvore.** Uma árvore de profundidade 3, desenhada, com o corte do primeiro nó legível. A ideia: perguntas sim/não sobre uma feature, e uma média de preço em cada folha. Em seguida a mesma árvore sem o teto de profundidade, e o RMSE de treino muito abaixo do de teste. Overfitting com número, não com definição solta.
6. **A floresta.** Muitas árvores, cada uma num recorte dos dados, a previsão é a média. Dois parâmetros na tela e nada mais: número de árvores e profundidade máxima. A run da floresta ao lado da run da árvore funda e da run da reta.
7. **Boosting, em um slide.** As árvores entram em sequência, cada uma olhando o erro da anterior. Uma run de `GradientBoostingRegressor` com parâmetros default, no mesmo split. Sem derivada, sem diagrama de resíduo em série.
8. **KNN.** A previsão é a média dos k vizinhos mais próximos, depois da escala. Uma run com k declarado. O slide diz quando ele cabe: pouco dado, relação local, custo de prever aceitável. Neste arquivo ele é o contraste, não o favorito esperado.
9. **A tabela.** As runs no MLflow: reta, árvore rasa, árvore funda, floresta, boosting, KNN. RMSE e MAE de teste. A árvore funda também mostra o RMSE de treino, para o overfitting ficar na mesma linha.
10. **Permutação.** No teste, embaralhar uma coluna e medir quanto o RMSE piora. Barras para a floresta. A conta interna da árvore (`feature_importances_`) aparece ao lado, numa frase: ela favorece a coluna que a árvore usou para partir, e a permutação mede o efeito na previsão.
11. **A regra.** Preço com categoria cruzada e curva: floresta ou boosting, medidos no mesmo teste da reta. Coeficiente legível: a reta, sabendo o erro que ela deixa na mesa.

### Caderno

```python
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor, plot_tree

mlflow.set_experiment("aula-ml-4-diamonds")

pedras = pd.read_csv("dados/diamonds.csv")
pedras = pedras[(pedras["x"] > 0) & (pedras["y"] > 0) & (pedras["z"] > 0)]

alvo = "price"
numericas = ["carat", "depth", "table", "x", "y", "z"]
categoricas = ["cut", "color", "clarity"]
```

Um único `train_test_split` com `random_state=0`. Cada modelo é um pipeline com o mesmo `ColumnTransformer` da aula 2 e um estimador diferente. Cada um abre `mlflow.start_run`. A árvore desenhada usa `max_depth=3` e `plot_tree` numa figura salva em `img/`. A importância por permutação roda no teste, no pipeline da floresta, com `n_repeats` pequeno o bastante para a aula não esperar minutos. O arquivo tem dezenas de milhares de linhas. A floresta e o boosting usam parâmetros contidos (`n_estimators` na casa das dezenas ou poucas centenas, `n_jobs=-1`) para o bloco caber no horário.

---

## Aula 5 — Séries temporais

Pasta: `aula-ml-5`

### O que a aula ensina

A linha tem data, e sortear o teste usa o futuro para prever o passado. O dataset é o Bike Sharing Demand, arquivo `train.csv`: hora, calendário, clima e a quantidade de aluguéis. O caso de uso é prever a demanda de uma hora que ainda não aconteceu.

`casual` e `registered` ficam de fora, porque somam o alvo. O teste é um período posterior ao treino. Antes do modelo, a previsão ingênua: repetir a mesma hora da semana anterior, também como run. Só então um modelo simples com calendário e clima, avaliado só nesse futuro. Uma run com split aleatório entra de propósito, para a métrica inflada aparecer do lado da outra.

As runs deixam visível o que o corte temporal faz com a métrica.

A regra que fica: se a linha tem data e o alvo é o próximo período, o corte é no tempo, e a baseline sazonal vem antes do algoritmo.

O modelo com calendário é uma regressão linear, de propósito. A aula não apresenta um algoritmo novo. O assunto novo é o corte e a baseline. Árvore no mesmo corte temporal pode entrar como uma run extra, se sobrar tempo, reusando a floresta da aula 4. Não é o centro.

### Dataset

- Página: https://www.kaggle.com/competitions/bike-sharing-demand
- Arquivo: `train.csv` da competição
- Colunas: `datetime`, `season`, `holiday`, `workingday`, `weather`, `temp`, `atemp`, `humidity`, `windspeed`, `casual`, `registered`, `count`
- Alvo: `count`
- `casual + registered = count`. As duas primeiras não entram como feature. Um slide mostra a soma batendo com `count` numa amostra de linhas, para o vazamento ser uma conta, não um aviso
- O `train.csv` desta competição traz os dias 1 a 19 de cada mês, não o mês inteiro. O slide do arquivo diz isso. O corte temporal e a baseline usam o timestamp que existe, sem completar os dias 20–31
- `atemp` é a temperatura sentida, colada em `temp`. O modelo usa `temp` e deixa `atemp` de fora, para não duplicar a mesma informação. Uma frase no slide das features, sem aula de correlação

### Slides

1. **Capa.** Quantas bicicletas saem na próxima hora.
2. **O que muda por causa da data.** Um desenho de uma série, um bloco no passado e um bloco no futuro. Ao lado, o mesmo desenho com pontos sorteados nos dois blocos: o teste contém horas que estão no meio do treino. Essa segunda figura é a armadilha.
3. **O arquivo.** Origem, uma linha = uma hora, o recorte dos dias 1 a 19, `count` como alvo. Série desenhada de um mês, para a sazonalidade do dia aparecer antes de qualquer modelo.
4. **A coluna que é o alvo disfarçado.** Três linhas na tela: `casual`, `registered`, a soma, `count`. As duas primeiras riscadas da lista de features.
5. **O corte.** Treino = ano de 2011. Teste = ano de 2012. Os dois só com os dias que o arquivo tem. Tamanho de cada lado na tela. Nenhum `train_test_split` neste caminho.
6. **O que se repete.** Hora do dia e dia da semana: duas agregações da média de `count` no treino. O gráfico da hora é o argumento da baseline.
7. **A previsão ingênua.** Para cada hora do teste, a previsão é o `count` da mesma hora, sete dias antes, quando essa hora existe no arquivo. MAE e RMSE só nas horas em que o lag existe. Run `baseline-semana`.
8. **O modelo com calendário.** Features: hora, dia da semana, mês, `season`, `holiday`, `workingday`, `weather`, `temp`, `humidity`, `windspeed`. Regressão linear no pipeline, ajustada só em 2011, medida em 2012. Run `reta-calendario`.
9. **O split aleatório, de propósito.** O mesmo modelo, agora com `train_test_split` embaralhado, métrica no pedaço sorteado. Run `reta-split-aleatorio`. As três runs lado a lado. A do split aleatório fica melhor, e o slide diz por quê: o teste viu horas vizinhas às do treino.
10. **A regra.** Alvo no próximo período: ordene pelo tempo, corte no tempo, comece pela repetição da semana anterior, e desconfie de métrica que veio de linha sorteada.

### Caderno

```python
mlflow.set_experiment("aula-ml-5-bicicletas")

horas = pd.read_csv("dados/train.csv", parse_dates=["datetime"])
horas = horas.sort_values("datetime")
assert (horas["casual"] + horas["registered"] == horas["count"]).all()

horas["hora"] = horas["datetime"].dt.hour
horas["dia_semana"] = horas["datetime"].dt.dayofweek
horas["mes"] = horas["datetime"].dt.month

treino = horas[horas["datetime"].dt.year == 2011]
teste = horas[horas["datetime"].dt.year == 2012]

features = [
    "hora", "dia_semana", "mes", "season", "holiday",
    "workingday", "weather", "temp", "humidity", "windspeed",
]
```

A baseline faz o merge do teste com o próprio arquivo deslocado em sete dias, pela chave do timestamp, e ignora as horas sem par. O modelo de calendário trata hora, dia da semana, mês, `season` e `weather` como categóricas no one-hot. `temp`, `humidity` e `windspeed` entram na escala. Tudo dentro do pipeline, ajustado em `treino`.

A run do split aleatório usa o arquivo inteiro, o mesmo pipeline e `random_state=0`, e loga as métricas com o prefixo deixando claro que o teste não é 2012.

---

## Aula 6 — Deploy, e o que ficou de fora

Pasta: `aula-ml-6`

### O que a aula ensina

Duas pontas que as aulas anteriores deixaram abertas.

A primeira é publicar. Um modelo já registrado, o de churn da aula 3, sobe como serviço. O MLflow serve o artefato da run escolhida. A turma vê o contrato: quais campos entram, o que volta, um pedido real com a probabilidade de saída. Em seguida, o que acontece depois da publicação: o dado novo se afasta do treino, a métrica que foi logada deixa de descrever o mundo, e o retreino volta a ser parte do trabalho. Drift entra como conceito operacional, com um exemplo em cima das cobranças do próprio churn, não como plataforma de monitoramento.

A segunda ponta é o caso sem coluna de resposta. O dataset é o Mall Customer Segmentation: renda e score de gasto, sem alvo. O caso de uso é separar grupos de clientes para uma ação diferente em cada grupo. O modelo é o k-means. O número de grupos sai do cotovelo, olhado no gráfico, e a turma nomeia os grupos pela posição deles, não por um rótulo que o arquivo não tem.

A regra que fica, em duas linhas: sem alvo, o trabalho é agrupar. Com alvo e um modelo já escolhido, o passo seguinte é servir a predição.

O notebook deixa de ser o lugar onde a predição acontece. O serviço é que recebe o pedido.

### Dataset do agrupamento

- Página: https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python
- Arquivo: `Mall_Customers.csv`
- 200 linhas
- Colunas: `CustomerID`, `Gender`, `Age`, `Annual Income (k$)`, `Spending Score (1-100)`
- Não há alvo. `CustomerID` não entra no algoritmo
- O primeiro ajuste usa só renda anual e score de gasto, para o gráfico ser de duas dimensões e os grupos aparecerem a olho. Idade e gênero ficam para um segundo ajuste, opcional, se der tempo. O centro da aula é o caso de duas colunas

### O modelo que sobe

A run `logística` da aula 3, a do corte que a turma tiver escolhido naquele dia. O caderno desta aula aponta para o `run_id` guardado, ou para o nome da run, dentro do `mlruns` da aula 3. Se as pastas estiverem separadas, copiar o artefato registrado para `aula-ml-6/modelos/churn` antes da aula, e o slide diz que aquele diretório é a run promovida. A aula não retreina o churn. Ela publica o que já foi medido.

### Slides

1. **Capa.** Duas perguntas: como isso responde um pedido fora do notebook, e o que fazer quando não existe coluna de resposta.
2. **O que já está registrado.** Print da UI do MLflow da aula 3, com a run escolhida, a métrica que justificou a escolha e o artefato. A promoção é apontar para essa run, não ajustar de novo.
3. **O contrato.** A lista dos campos que o pipeline da aula 3 espera, com um exemplo de JSON de um cliente. A resposta: a probabilidade de `Churn` e a classe no limiar que foi logado com a run. O limiar viaja com o modelo, anotado como parâmetro da run, para o serviço não inventar 0,5 na hora.
4. **O serviço.** O comando que sobe o artefato. Um pedido `curl` na tela, e a resposta de verdade logo abaixo. O slide seguinte mostra o mesmo pedido com um campo faltando, e o erro que volta, para o contrato não ser só o caso feliz.
5. **Depois de publicar.** Drift: a distribuição de `MonthlyCharges` do treino contra uma versão deslocada, desenhada por cima. A métrica logada descreve o arquivo da aula 3. Quando o arquivo novo se afasta, a run antiga não é mais a evidência. Retreino é repetir o ciclo das aulas 2 e 3 e registrar outra run, não editar o serviço à mão.
6. **Sem alvo.** A família anunciada na aula 1. Uma linha do shopping não diz a qual grupo o cliente "deveria" pertencer. O trabalho é formar os grupos.
7. **O arquivo do shopping.** 200 clientes, renda e score. O gráfico de dispersão sem cor nenhuma, antes do algoritmo.
8. **K-means.** Cada ponto fica no grupo do centro mais próximo. Os centros se movem até estabilizar. k é escolha de quem analisa. Inércia para k de 1 a 10, o cotovelo na tela, e o k adotado marcado.
9. **Os grupos com nome.** O mesmo gráfico, agora colorido, centros desenhados. Cada grupo ganha uma frase a partir da posição: renda alta e score alto, renda alta e score baixo, e o que mais o cotovelo tiver separado. A frase é leitura do centro, e o slide diz isso.
10. **As duas regras.** Sem coluna de resposta: k-means, k pelo cotovelo, grupo nomeado pelo centro. Com modelo já medido: a run vira serviço, o contrato é explícito, e o retreino acontece quando o dado novo deixa de parecer o da run.

### Caderno e o serviço

O agrupamento roda no caderno.

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

clientes = pd.read_csv("dados/Mall_Customers.csv")
colunas = ["Annual Income (k$)", "Spending Score (1-100)"]
X = StandardScaler().fit_transform(clientes[colunas])

inercias = []
for k in range(1, 11):
    ajuste = KMeans(n_clusters=k, n_init=10, random_state=0)
    ajuste.fit(X)
    inercias.append(ajuste.inertia_)

grupos = KMeans(n_clusters=5, n_init=10, random_state=0)
clientes["grupo"] = grupos.fit_predict(X)
```

O 5 do `n_clusters` é o ponto de partida clássico deste arquivo. O caderno só fixa esse número depois de a inércia estar desenhada. Se o cotovelo da execução cair noutro k, o slide usa o k que a figura mostrar. O código acima é o esqueleto, não um número blindado contra a figura.

A escala aqui pode ficar fora do pipeline: não há teste. O slide diz a diferença em uma frase. Na aula 2 a escala ia para dentro do pipeline porque existia um teste que não podia vazar. Aqui o arquivo inteiro é o material do agrupamento.

O serviço não é célula de notebook. É um comando, documentado no `LEIA-ME` da pasta, executado no terminal durante o slide 4:

```bash
mlflow models serve -m modelos/churn -p 5001 --no-conda
```

```bash
curl -s -X POST http://127.0.0.1:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["tenure", "MonthlyCharges"], "data": [[12, 70.5]]}}'
```

O JSON completo, com todas as colunas do pipeline, fica no caderno e no slide 3. O trecho acima só marca o formato. A resposta projetada é a que esse comando devolver na aula, colada no slide só depois de rodar.

---

## O que as seis aulas deixam na mão da turma

| Objetivo | O que fazer | Onde viu |
|---|---|---|
| Classificar em poucas categorias e fechar o ciclo | Classificador simples e validação cruzada | Pinguins, aula 1 |
| Prever um número e citar o efeito de cada fator | Regressão linear contra a média, pipeline, run no MLflow | Custo do plano, aula 2 |
| Prever um sim ou não, com um erro mais caro que o outro | Regressão logística, limiar, precisão e recall da classe que importa | Churn, aula 3 |
| Prever um número quando as categorias se cruzam e a curva não é reta | Comparar reta, árvore e floresta no mesmo teste | Diamantes, aula 4 |
| Prever o próximo período | Corte no tempo e baseline sazonal antes do modelo | Bicicletas, aula 5 |
| Separar grupos sem coluna de resposta | K-means e cotovelo | Shopping, aula 6 |
| Usar um modelo já medido fora do notebook | Run do MLflow servida, com contrato | Churn publicado, aula 6 |
