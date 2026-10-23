# Aula 04 — Pandas

Apresentação em HTML/CSS/JavaScript, sem dependências externas — mesmo formato,
mesmos controles e mesmo motor da aula 3.

## Como abrir

Duplo clique em **`index.html`**. Funciona offline, em qualquer navegador moderno.

| Ação | Como |
|---|---|
| Avançar / voltar | botões, `→` `←`, `espaço`, `PageUp/PageDown` ou deslizar |
| Índice da aula | botão `☰` ou tecla `M` |
| Exportar em PDF | botão **PDF** ou tecla `P` |
| Tema claro/escuro | botão `◐` ou tecla `T` |
| Tela cheia | botão `⛶` ou tecla `F` |
| Sincronizar abas | automático; tecla `S` desliga só na aba atual |

## A ideia da aula

**24 slides**, uma ideia por slide, pouco texto — o mesmo padrão da aula 3.

Todos os slides usam o mesmo dado, as 6.433 corridas de táxi, e **toda saída na
tela é a saída de verdade**: os blocos escuros foram gerados rodando os comandos
sobre o `dados/taxis.csv` desta pasta (`python saidas.py` reproduz e confere).

Cinco partes:

1. **Abertura (3)** — o que é e para que serve, com código no próprio slide.
2. **Entrada (6)** — o panorama das fontes e depois uma fonte por slide, sempre
   no mesmo formato: o dado como ele chega de um lado, a tabela que sai do outro.
3. **Na prática (9)** — um método por slide, sempre na mesma moldura: o comando,
   a saída real e uma frase de explicação.
4. **Quatro gráficos (5)** — nenhum deles sairia de uma lista: cruzar duas
   colunas, dividir cada linha pelo total, ter data no índice. Os dois últimos
   são o mesmo código em 31 e em 365 dias.
5. **Resumo (1)** — três verbos: visualizar, agrupar, destilar.

## Os 24 slides

| # | Slide | O que mostra |
|---|---|---|
| 1–3 | abertura | o que é · ler/olhar/agrupar |
| 4 | **Carregar** | as seis fontes numa tela — o panorama |
| 5 | CSV | o arquivo de texto do táxi × a tabela, com o índice que o Pandas põe |
| 6 | Excel | a planilha com A/B e linha 1 × o cabeçalho e a contagem do 0 |
| 7 | Banco de dados | `create_engine` + um `select` × a tabela pronta |
| 8 | JSON | a lista de objetos da API × uma linha por objeto |
| 9 | Na mão | o dicionário digitado × chave vira coluna |
| 10 | divisória | abre a seção **Na prática** |
| 11 | A tabela | `shape` e `head(3)` — 6.433 × 14 |
| 12 | **info** | tipos e quantos valores existem; o `payment` tem 6389 |
| 13 | **describe** | oito números por coluna: média 13,09, mediana 9,50 |
| 14 | Uma coluna | a **Series** — e o `to_numpy()`, que devolve só os números |
| 15 | Filtrar | `df[df["distance"] > 10]` arrasta a **linha inteira** — 394 corridas |
| 16 | Duas condições | máscara com `&` × `df.query("...")` — as mesmas 225 |
| 17 | **value_counts** | 4.577 cartão · 1.812 dinheiro · 44 em branco; e por que não serve para número contínuo |
| 18 | **groupby** | uma linha por categoria: dinheiro **0,00** × cartão **2,78** |
| 19 | divisória | abre a seção **Com gráficos** |
| 20–23 | os quatro gráficos | ver abaixo |
| 24 | **Resumo** | a tabela inteira de uma vez — visualizar · agrupar · destilar |


## Os quatro gráficos

Nenhum deles sairia de uma lista de números: um cruza duas colunas numa matriz,
outro divide cada linha pelo seu próprio total, os dois últimos têm data no
índice. As imagens estão em `img/`, geradas por `graficos.py` — que roda sobre os
CSV desta pasta e imprime os achados.

**O título de cada slide é a pergunta**, não o nome do método — o aluno lê a
pergunta, olha o desenho e já sabe o que está vendo. Na etiqueta de cima fica o
**nome do tipo de gráfico em português** e o método que o gerou.

Cada slide diz, embaixo, **quais colunas entraram** no gráfico. Vale apontar: dois
dos quatro usam **uma coluna só** — a data. É o argumento de que `parse_dates` na
leitura paga dividendos o resto da análise inteira.

| # | A pergunta | O tipo | Colunas | O que só a tabela permite | A resposta |
|---|---|---|---|---|---|
| 20 | **Quando as pessoas pegam táxi?** | mapa de calor | `pickup` | `pivot_table` de dia × hora vira uma matriz 7 × 24 que o `imshow` desenha | pico **sexta, 17h** (84 corridas); madrugada só tem movimento no fim de semana |
| 21 | **Onde ainda se paga em dinheiro?** | barras empilhadas 100% | `pickup_borough`, `payment` | `unstack()` abre o pagamento em colunas e `div(axis=0)` divide cada linha pelo seu total | **Queens 41%** em dinheiro contra 27% de Manhattan |
| 22 | O movimento muda ao longo do mês? | gráfico de linhas | `pickup` | índice de data: `loc["2019-03"]`, `resample("D")` e `rolling(7)` | oscila com a semana e cede de leve: pico 14/03 (260), fundo 24/03 (149) |
| 23 | **E no ano inteiro?** | gráfico de linhas | `dia`, `corridas` | o mesmo `resample` e `rolling`, agora sobre 365 dias de um CSV já resumido | **84,6 milhões** de corridas: março é o topo, agosto o fundo, e cada mergulho é um feriado — o menor dia do ano é o **Natal** |

**O slide 21 é o melhor para discutir.** Manhattan tem 5.236 corridas e o Bronx
99 — em barra de contagem, o Bronx desapareceria. O `div(axis=0)` põe os quatro
na mesma régua, e aí a pergunta fica interessante: por que no Queens se paga
tanto em dinheiro? (De lá saem os aeroportos, e turista chega sem cartão local.)

**No slide 22, a linha fina é o serrote da semana** e a grossa é a tendência. Se
a turma perguntar de onde vem a linha grossa, é a média dos sete dias
anteriores — `rolling(7)`.

**O par 22 → 23 é o argumento do zoom.** O código do 23 é o mesmo do 22; só o
arquivo é maior. Vale dizer o número em voz alta: **84,6 milhões** de corridas
couberam em 365 linhas de 8 KB, porque o `resample` resumiu antes de desenhar. O
`dados/corridas-2019.csv` já vem pronto na pasta; quem quiser refazê-lo roda
`python baixa-ano-2019.py`, que lê os doze arquivos públicos do TLC de Nova York
pegando só duas colunas de cada um.

No 23, deixe a turma achar os feriados antes de contar: o mergulho de julho é o
dia 4, o de novembro é Thanksgiving, o de dezembro é o Natal — e março, a faixa
âmbar, é o mês que a aula inteira usou.

Para regerar: `python graficos.py` (precisa de pandas e matplotlib).

## Os números dos slides

Medidos com pandas 3.0 sobre o `dados/taxis.csv` desta pasta.

| Onde | Número |
|---|---|
| A tabela | 6.433 linhas × 14 colunas |
| Tarifa: média · mediana · máximo | 13,09 · 9,50 · 150,00 |
| Formas de pagamento | 4.577 cartão · 1.812 dinheiro · **44 em branco** |
| Gorjeta por pagamento | dinheiro **0,00** · cartão **2,78** |
| Tarifa mediana por bairro | Queens 21,00 · Bronx 16,00 · Brooklyn 12,50 · Manhattan 8,50 |
| Corridas acima de 10 milhas | 394 · tarifa média 46,53 |
| Valores distintos de distância | 1.079 — por isso `value_counts` não serve nela |
| Período | 28/02 a 31/03/2019 · pico 14/03 (260) · fundo 24/03 (149) |
| Hora mais movimentada | sexta, 17h — 84 corridas |
| Pagamento em dinheiro | Queens 41% · Brooklyn 31% · Manhattan 27% · Bronx 25% |
| Corridas por bairro | Manhattan 5.236 · Queens 649 · Brooklyn 380 · Bronx 99 |
| 2019 inteiro (slide 23) | 84.597.002 corridas em 365 dias |
| Mês mais forte · mais fraco | março 7.866.400 · agosto 6.073.089 |
| Menor dia do ano | 25/12 — 101.917 corridas |

## Condução

- **O slide 18 (`groupby`) é o centro da aula.** Pergunte antes de virar: "quem
  dá mais gorjeta, quem paga em dinheiro ou no cartão?". A saída na tela responde.
- **A seção Na prática tem uma moldura só, do 11 ao 18:** o comando em cima, a
  saída real embaixo, uma frase de fecho. Nada de tabela desenhada à mão — é o que
  o Python devolveu. Rodar `python saidas.py` reproduz tudo, na ordem dos slides.
- **O `describe` (13) responde uma pergunta que sempre aparece:** "não existe um
  comando que mostre tudo?". Existe, e é este.
- **O slide 4 (`Carregar`) leva trinta segundos.** Não é lista para memorizar: o
  recado é que a fonte muda a primeira linha e mais nada — o CSV desta aula, a
  planilha que o chefe manda e o banco da empresa entram todos como DataFrame.
- **Os slides 5 a 9 provam isso na tela.** Todos têm a mesma moldura: à esquerda
  o dado como ele chega, à direita a tabela que sai. De 6 a 9 a tabela de saída é
  **sempre a mesma** — duas lojas e dois valores. Vale dizer isso em voz alta na
  virada do 8 para o 9: fonte diferente, resultado idêntico.
- **O slide 6 (`Excel`) é o que gera pergunta:** a linha 1 da planilha vira
  cabeçalho e a numeração recomeça no 0. Quem vem de planilha tropeça nisso.
- **O slide 17 (`value_counts`) tem uma pergunta pronta:** "e se eu contar a
  distância?". O `nunique` ao lado responde — 1.079 valores diferentes, uma
  contagem inútil. Contar é para categoria.
- **Se faltar tempo**, os que saem sem prejuízo são 7 (`Banco de dados`) e 16
  (duas condições). Nunca corte 4, 5, 12, 17 e 18.
- **O que ficou de fora de propósito:** `.loc` × `.iloc` e o
  `SettingWithCopyWarning`. Os dois pedem o conceito de índice e de cópia, que
  rendem mais na aula 5, quando a turma já estiver mexendo em dado sujo.
- **Também ficaram para a aula 5:** `agg` com o `n`, coluna derivada, `nlargest`
  e `isna().sum()`. Os gráficos usam `pivot_table`, `unstack`, `.dt`, `resample` e
  `rolling` sem slide de apresentação — o comando está na tela, então explique em
  uma frase quando chegar lá: são os métodos que a aula 5 detalha.
- **O slide 24 fecha o arco do slide 3.** Lá a promessa era "ler, olhar, agrupar";
  aqui os dois primeiros viram um só, **visualizar**, e entra o **destilar** — o
  que a seção de gráficos entregou. Se sobrar tempo, volte ao 3 e compare.
- **"Destilar" é a palavra honesta:** quem desenha é o Matplotlib. O Pandas reduz
  milhões de linhas aos poucos números que cabem num gráfico — o slide 23 é a
  prova, 84,6 milhões viraram 365 pontos.
- **Se um número sair diferente** de um slide, rode `python saidas.py` e compare:
  o script lê o mesmo CSV e imprime comando por comando.
- **Plano B:** tudo offline — o deck, os gráficos (já são imagens) e o CSV.

## Arquivos

```
aula4/
├── index.html            os 24 slides
├── aula4-slides.pdf      exportação (uma página por slide, 4:3)
├── graficos.py           gera os quatro gráficos de img/
├── baixa-ano-2019.py     monta o corridas-2019.csv a partir do TLC de NY
├── saidas.py             roda os exemplos e imprime a saída de cada slide
├── medir-densidade.py    aponta slides com texto demais
├── dados/
│   ├── taxis.csv         as mesmas 6.433 corridas da aula 3
│   └── corridas-2019.csv  365 dias de 2019 — 84,6 milhões de corridas resumidas
├── img/                  os quatro gráficos, fundo transparente
├── css/style.css         estilo, tema claro/escuro, impressão
└── js/
    ├── highlight.js      realce de sintaxe — Python
    ├── slides.js         navegação, índice, tema, PDF
    └── sync.js           sincroniza o slide entre abas
```
