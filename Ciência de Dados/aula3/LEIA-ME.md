# Aula 03 — NumPy

Apresentação em HTML/CSS/JavaScript, sem dependências externas — mesmo formato e
mesmos controles das aulas de Linguagem de Programação (o motor veio de lá,
adaptado para Python).

## Como abrir

Duplo clique em **`index.html`**. Funciona offline, em qualquer navegador moderno.

| Ação | Como |
|---|---|
| Avançar / voltar | botões, `→` `←`, `espaço`, `PageUp/PageDown` ou deslizar |
| Índice da aula | botão `☰` ou tecla `M` |
| Exportar em PDF | botão **PDF** ou tecla `P` |
| Tema claro/escuro | botão `◐` ou tecla `T` |
| Tela cheia | botão `⛶` ou tecla `F` |
| Ir a um slide | endereço terminado em `#25`, por exemplo |
| Sincronizar abas | automático — todas as abas do deck ficam no mesmo slide; tecla `S` desliga só na aba atual |

## A ideia da aula

Deck **direto**: 25 slides, uma ideia por slide, pouco texto e nenhuma discussão
de memória ou de implementação.

Quatro partes:

1. **Abertura (4 slides)** — o que é NumPy, para que serve (cada item com um
   exemplo de duas linhas) e como se usa.
2. **Doze exemplos**, quase todos no formato **"Sem NumPy" à esquerda × "Com
   NumPy" à direita**, com uma frase de fecho embaixo.
3. **Três combinações com gráfico** — o NumPy calcula, o Matplotlib desenha.
4. **No trabalho (1 slide)** — seis formas de usar NumPy no emprego, cada uma com
   a linha que a resolve, e um exemplo prático: o relatório de segunda-feira em
   quatro linhas. É o último slide do deck.

O aluno deve conseguir entender o slide **sem a narração** — a fala serve para
comentar, não para completar.

### Regra de densidade

O deck foi medido slide a slide e ajustado para leitura rápida:

| Limite | Valor |
|---|---|
| Palavras por slide (fora o código) | **35 em média**, nenhum acima de 65 |
| Frase de fecho (`.callout`) | até 2 linhas |
| Descrição de card (`<small>`) | até ~12 palavras |
| Etiqueta de topo (`.kicker`) | 3 a 6 palavras |
| Blocos por slide | 3 a 4 — título, conteúdo, uma frase |

Os três slides mais longos (**Onde aparece**, **Conferindo**, **Atividade**) são
listas de itens curtos, não parágrafos — dá para varrer com o olho.

Se for editar, o medidor está em `medir-densidade.py`: ele lista qualquer slide
que passe dos limites acima.

## O dataset

**`dados/taxis.csv`** — 6.433 corridas de táxi de Nova York, março de 2019
(o mesmo do notebook da aula 1; origem: `seaborn-data`).

As colunas usadas na aula: `distance` (milhas), `fare`, `tip`, `payment`,
`pickup` / `dropoff` (horários) e `passengers`.

Escolhido porque cada coluna responde a uma pergunta que a turma entende sem
explicação — e porque tem sujeira real: 51 corridas de distância zero, 44
pagamentos em branco e a gorjeta em dinheiro que dá sempre 0,00.

## Os 56 slides

| # | Slide | O que mostra |
|---|---|---|
| 1–4 | abertura | o que é · para que serve (com exemplo) · `import numpy as np` |
| 5–6 | o dado | as colunas do dataset · `read_csv` + `to_numpy()` |
| 8 | Converter | laço × `distancia * 1.60934` |
| 9 | O tempo | 153 ms × 2,6 ms em 10 milhões de valores |
| 10 | Somar | acumulador × `.sum()` — US$ 84.214,87 |
| 11 | Resumir | `.mean() .min() .max() .std()` · `np.median` |
| 12 | Filtrar | laço com `if` × `distancia[distancia > 10]` |
| 13 | Contar | contador × `(distancia > 10).sum()` — 394 |
| 14 | Proporção | `.sum()` conta · `.mean()` dá 6,1% |
| 15 | Combinar | `&` e `\|` com parênteses — 225 corridas |
| 16 | Rotular | `if/else` no laço × `np.where` |
| 17 | Juntar duas | `tarifa + gorjeta` |
| 18 | Dividir | `tarifa / distancia` → US$ 5,42 por milha |
| 19 | Porcentagem | `gorjeta / tarifa * 100` → 26,5% de quem deu |
| 20 | O dado sujo | 51 distâncias zero · `np.where` → `np.nan` · `nanmean` |
| 21 | A mais cara | `max`, `argmax`, `sort` — US$ 150 e 36,7 milhas |
| 23 | Inventar dados | `arange`, `zeros`, `default_rng(42)` |
| 21–23 | **os três gráficos** | ver a tabela abaixo |
| 31 | O padrão | coluna → NumPy → gráfico. O gráfico não faz conta |
| 32–40 | **a vitrine** | ver a tabela mais abaixo |
| 41–46 | **no trabalho** | ver a tabela mais abaixo |
| 47–48 | pedir à IA · conferir | o fecho da parte conceitual |
| 49–54 | questões | três, com o slide da resposta comentada |
| 55–57 | fechamento | atividade · três frases para guardar · tarefa |

## As três combinações com gráfico

Todas seguem a mesma regra: **o NumPy reduz milhares de números a poucos, e o
gráfico só recebe o resultado**. As imagens estão em `img/` e são geradas por
`graficos.py`.

| # | Slide | NumPy | O achado |
|---|---|---|---|
| 1 | Histograma | `np.histogram` | 2.125 corridas entre 1 e 2 milhas |
| 2 | Por hora | `np.bincount` | pico às 18h (417) · fundo às 5h (51) |
| 3 | Média por hora | máscara `hora == h` + `.mean()` | 5h é o horário mais caro (US$ 16,77) |

Para **regerar os gráficos** (outras cores, outro recorte):

```bash
python graficos.py     # precisa de numpy, pandas, matplotlib e seaborn
```

Ele salva seis PNGs em `img/`; o deck usa três (`g1`, `g2`, `g3`). Os outros —
a reta do `polyfit`, a gorjeta por forma de pagamento e a curva acumulada —
continuam sendo gerados, caso você queira reativar aqueles slides.

## Os números dos slides

Medidos, não estimados: Python 3.12 com NumPy 2.5 e o `taxis.csv` de `dados/`.

| Onde | Número |
|---|---|
| 10 M de valores × 1.1, laço × NumPy | 153 ms × 2,6 ms |
| Distância: média · mediana · máximo | 3,02 · 1,64 · 36,7 milhas |
| Tarifa: média · mediana · máximo | 13,09 · 9,50 · 150 dólares |
| Faturamento do mês | US$ 84.214,87 |
| Corridas acima de 10 milhas | 394 · 6,1% (225 delas com gorjeta) |
| Gorjeta | 64% deram · mediana de 26,5% da tarifa |
| Sujeira conhecida | 51 distâncias zero · 44 pagamentos em branco |

Se rodar diferente na sua máquina, **use os seus números**.

## Condução

- **O slide 9 (O tempo) é o argumento da aula.** Vale rodar `%timeit` ao vivo no
  Colab antes de mostrá-lo, e deixar a turma chutar a diferença.
- **O bloco de gráficos e a vitrine são o fecho natural** — se a aula atrasar,
  corte exemplos (18, 19, 22 ou 23) e slides da vitrine (34, 38, 40), nunca os
  gráficos nem os dois últimos slides sobre pedir e conferir.
- **A vitrine se conduz rápido**: 30 a 60 segundos por slide, sem explicar a
  função. O objetivo é que eles saiam sabendo que **existe** — o "como" eles vão
  pedir à IA na semana seguinte.
- **Nunca corte 12, 13 e 14** (filtrar, contar, proporção): é o que eles vão usar
  todo dia a partir da aula 4.
- **Plano B:** o deck é offline, o `taxis.csv` está na pasta e os gráficos já são
  imagens — nada depende de rede nem de execução ao vivo.

## Arquivos

```
aula3/
├── index.html            os 25 slides
├── aula3-slides.pdf      exportação (uma página por slide, 4:3)
├── graficos.py           gera os seis gráficos (g1…g6)   ← rode para refazer
├── dados/taxis.csv       6.433 corridas de NYC, março de 2019
├── img/                  os três gráficos usados, fundo transparente
├── css/style.css         estilo, tema claro/escuro, animações e impressão
└── js/
    ├── highlight.js      realce de sintaxe — Python
    ├── questoes.js       banco de questões (sem uso: a âncora saiu do HTML)
    ├── quiz.js           gera os slides de questão
    ├── slides.js         navegação, índice, tema, PDF
    └── sync.js           sincroniza o slide entre abas
```

## Diferenças em relação ao código das aulas de LP

- `js/highlight.js`: reescrito para **Python** — `#` é comentário, palavras-chave
  do Python, docstrings.
- `css/style.css`: acrescentados, no fim do arquivo, `.fig` (a figura elástica dos
  slides de gráfico), `.bars` (as barras de tempo), `.placas` (o número em
  destaque), `.hist`, `.eixos` e as células `.cel.off` / `.cel.ok` / `.cel.bool`.
- O motor de **execução passo a passo** (`trace.js` / `tracos.js`) não é usado aqui.
