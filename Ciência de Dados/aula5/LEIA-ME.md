# Aula 05 — Limpeza e transformação

Apresentação em HTML/CSS/JavaScript, sem dependências externas — mesmo formato,
mesmos controles e mesmo motor das aulas 3 e 4 — mais um **caderno de
acompanhamento** que segue os slides na mesma numeração.

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

O caderno abre com `jupyter lab aula05.ipynb`, usando a `.venv` desta pasta.

## O caderno anda junto com os slides

**Distribua o `aula05.ipynb` no começo da aula.** Ele acompanha a projeção na
mesma numeração: quando a tela mostrar `18 / 82` no rodapé, o aluno procura por
**`▸ Slide 18`** no caderno e roda a célula. O primeiro markdown traz um índice
recolhível de todos os slides, para quem chegar atrasado se achar.

Os slides que têm célula estão marcados com **`▸ caderno`** no canto superior
direito. Os que não têm — capa, divisórias, conceito puro — não confundem
ninguém, porque a numeração simplesmente pula.

**Como isso se mantém alinhado.** O fonte do caderno (`caderno-fonte.py`) não
escreve números, escreve chaves:

```python
## {{sentinela}} · A sentinela
```

E o slide correspondente carrega a mesma chave:

```html
<section class="slide" data-title="★ A sentinela" data-nb="sentinela" ...>
```

O `montar-caderno.py` lê o HTML, descobre em que posição cada chave caiu, troca
`{{sentinela}}` por `▸ Slide 18`, gera o índice e executa o caderno. **Inseriu um
slide no meio? Rode `python montar-caderno.py` e a numeração inteira se
reacomoda.** Ele também recusa a montagem se algum slide prometer célula que não
existe, ou se o caderno citar um slide que não existe.

```bash
python montar-caderno.py --so-checar   # confere o alinhamento, não grava nada
python montar-caderno.py               # monta, executa e grava o aula05.ipynb
```

## A ideia da aula

**82 slides** e **91 células de código**, 61 delas amarradas a um slide. É a aula
mais longa do semestre, e de propósito: limpeza é onde o aluno vai passar 80% da
vida profissional, e é o único assunto que não se aprende vendo — só fazendo.

O princípio que organiza tudo: **cada defeito aparece primeiro no dado real,
depois ganha o comando, e por último a decisão de negócio**. Nunca o contrário.
Nenhum slide apresenta um método antes de a turma ter visto o estrago que ele
conserta.

E, antes de tudo isso, **o método de descoberta**: os slides 7 a 10 não mostram
defeitos, mostram *como se procura* por eles. É a sequência que ensina o aluno a
achar sozinho, num arquivo que ele nunca viu.

**Toda saída na tela é a saída de verdade.** Os blocos escuros foram gerados
rodando os comandos sobre os arquivos de `dados/`. O `saidas.py` reproduz tudo e,
no fim, **confere com asserções os 20 números que os slides afirmam em negrito**.

### Os dez blocos

| bloco | slides | o que entrega |
|---|---|---|
| Abertura | 1–5 | o que é limpar, os 80%, os cinco datasets, os sete defeitos |
| **Diagnóstico** | 6–12 | **o método de descoberta em quatro passos**, o `raio_x`, as 27 grafias |
| **Faltantes** | 13–30 | o maior bloco: disfarces, sentinela, `dropna`, imputação, MNAR |
| Duplicatas | 31–35 | `duplicated`, o grão da tabela, a quase-duplicata, a falsa |
| Tipos | 36–41 | `astype` × `to_numeric`, dinheiro brasileiro, `category` |
| **Datas** | 42–49 | os três atos do `to_datetime`, o `.dt`, o fuso |
| Texto | 50–58 | espaço, acento, a função `chave`, `map`, `extract`, `zfill` |
| Derivadas | 59–64 | `assign`, `np.select`, o custo do `apply`, `cut` × `qcut` |
| **Outliers** | 65–72 | IQR, z-score, MAD, e os três tipos que pedem coisas diferentes |
| Fecho | 73–82 | `.loc`, a cópia, o pipeline, a auditoria, as dez regras |

## Os cinco datasets

| arquivo | linhas | origem | o que ele ensina |
|---|---|---|---|
| `vendas-sujas.csv` | 627 | gerado | **18 defeitos plantados** — o caso central da aula |
| `sensores.csv` | 1.081 | gerado | tempo, fuso, buraco na série e a linha que não existe |
| `rh.csv` | 222 | gerado | imputar por grupo, `cut`/`qcut`, o outlier legítimo |
| `titanic.csv` | 891 | real (aula 2) | faltante de verdade: 177 idades, 687 cabines, 2 portos |
| `taxis.csv` | 6.433 | real (aula 3) | o defeito em escala, e a duplicata que não é erro |

Os três gerados nascem de `gerar-dados.py` com **semente fixa** (`20260828`):
rodar de novo devolve byte a byte os mesmos arquivos, e os números dos slides não
mudam. O cabeçalho do script lista, um a um, os dezoito defeitos plantados e em
que slide cada um é usado.

## Os sete gráficos

Em `img/`, gerados por `graficos.py`. Cada um desenha **uma decisão de limpeza**,
não um dado.

| # | slide | o que mostra | o achado |
|---|---|---|---|
| g1 | 19 | mapa de faltantes do Titanic | **três padrões diferentes** na mesma tabela: salpicado, quase-tudo, duas linhas |
| g2 | 23 | média × mediana em duas distribuições | `skew` 0,39 e 7,16 — só na segunda a escolha muda o resultado |
| g3 | 28 | imputação: original × geral × por grupo | a mediana geral cria **um pico artificial**; a do grupo, cinco menores |
| g4 | 25 | o vazio de 3h15 do sensor | o `ffill` congela a estufa; o `interpolate` liga as pontas |
| g5 | 69 | os pedidos em escala log | quatro losangos verdes: **as vendas corporativas que o IQR apagaria** |
| g6 | 63 | `cut` × `qcut` sobre o mesmo salário | 183·3·**0**·2 contra 47·47·47·47 |
| g7 | 49 | temperatura por hora, UTC × Brasília | o pico às 18h que na verdade é às 15h |

**O g5 é o gráfico da aula.** Se sobrar tempo para um só, é esse: a nuvem roxa, a
linha vermelha do IQR, e os quatro diamantes verdes muito à direita — que são
30,7% do faturamento e que qualquer regra automática jogaria fora.

## Os três slides que sustentam a aula

**46 — "112 datas trocadas de mês".** O melhor slide do deck, e ele nasceu de um
bug real encontrado ao preparar a aula. A sequência é um teatro em três atos: o
palpite automático perde 534 datas de 600 (mas **avisa**); o `format="mixed"` com
`dayfirst=True` perde só 12 e parece resolver; e então o `max` mostra dezembro
num arquivo que vai até agosto. O `dayfirst` foi aplicado também às datas em ISO,
e 112 delas trocaram de mês — sem erro, sem aviso, sem `NaT`.

> Pergunte antes de virar o slide 45: *"o período vai de janeiro a dezembro. Está
> certo?"*. Alguém vai notar. Se ninguém notar, esse é o próprio recado.

**69 e 70 — a venda corporativa.** Quatro pedidos em seiscentos, 30,7% do
faturamento, todos fora do limite do IQR. Pergunte: *"removo?"*. A turma vai
dizer que sim. Aí mostre a coluna `obs`: *"venda corporativa - contrato anual"*.
A frase de fecho é a lição da aula inteira: **remover outlier sem olhar o que ele
é não é limpeza, é apagar o maior cliente da empresa.**

**29 — a flag `_faltava`.** Quem não tem idade registrada no Titanic sobreviveu
menos: 29,4% contra 40,6%. A ausência carregava informação sobre a pessoa. É o
slide que transforma "faltante é um problema a resolver" em "faltante é um dado a
investigar".

## Condução

- **A aula não cabe em um encontro se você tentar dar tudo.** Ela foi montada
  para ter folga de corte. Veja a lista abaixo.
- **Os slides 7 a 10 são o coração pedagógico da aula.** Eles respondem à
  pergunta que o aluno faz calado: *"como você soube que essa coluna estava
  errada?"*. Passo 1, o `dtypes` acusa o sintoma. Passo 2, o `unique()` mostra a
  cara do dado. Passo 3, o `to_numeric(errors="coerce")` conta os culpados — e o
  contraste entre `qtd` (16 tortos, exceção) e `valor` (495, o formato é outro) é
  o que ensina a diferença entre consertar e converter. Passo 4, o `describe()`
  denuncia o `-999` e o prazo de 365 dias, que **nenhum tipo acusaria**.
- **O bloco de faltantes (13–30) é metade da aula e merece ser.** É onde a turma
  mais tropeça e onde a decisão de negócio aparece com mais clareza.
- **Distribua o caderno antes de começar** e diga a regra em voz alta: *"o
  número no rodapé do slide é o número da seção no caderno"*. Depois disso, cada
  slide marcado com `▸ caderno` é um convite para a turma rodar junto.
- **Peça para rodarem antes de você mostrar a saída.** Nos slides 8, 9 e 10 isso
  funciona especialmente bem: eles descobrem o `-999` antes de você contar.
- **O slide 15 (`NaN != NaN`) leva vinte segundos** e evita uma hora de
  sofrimento no laboratório. Não corte.
- **O slide 40 (`category`) tem um número que impressiona:** 422,9 MB contra
  5,7 MB. Vale dizer em voz alta.
- **O slide 62 (`apply`)** é o único de desempenho. Diga o número — quatro mil
  vezes — e siga.
- **Se a turma perguntar do `SettingWithCopyWarning`** (slide 74): ele foi
  removido no pandas 3, porque o *Copy-on-Write* virou padrão. Quem aprendeu em
  tutorial antigo vai procurar por ele e não achar.

### Se faltar tempo

Saem sem prejuízo, nesta ordem: **57** (`extract`), **64** (`pipe`), **52** (o
espaço invisível), **41** (`category` com ordem), **72** (quando o outlier é o
assunto), **78** (gravar).

**Nunca corte:** 9, 10, 16, 18, 21, 23, 27, 29, 46, 55, 69, 70.

### Nomes de variáveis: uma regra da casa

Tudo aqui é lido em voz alta na frente de uma turma. Dois nomes foram trocados
por isso:

| era | virou | por quê |
|---|---|---|
| `cru` | `bruto` | falado, a sílaba puxa risada — e "dado bruto" é o termo técnico melhor |
| `tit` | `titanic` | abreviação com outro sentido em inglês |

A regra, para quem for editar: **leia o nome em voz alta antes de escrevê-lo.**
Os nomes dos 32 clientes, dos produtos e das cidades já passaram por essa
varredura; se você trocar o dataset, refaça.

### O que ficou de fora, de propósito

`merge`, `concat`, `groupby` com `agg` de múltiplas funções, `pivot_table` e
`melt` — todos são da **aula 6**. Aqui o `groupby` aparece só como ferramenta de
imputação (`transform`), sem slide de apresentação: se alguém perguntar, diga que
é o assunto da próxima aula.

## O caderno da aula

`aula05.ipynb` — **91 células de código, todas executadas**, com as saídas
gravadas. A estrutura é a dos slides: uma seção por slide marcado, com uma frase
de contexto e o código. **O texto longo fica nos slides, que você narra; o
caderno guarda o que se executa** — foi assim que os dois ficaram concisos sem
perder nada.

Depois do slide 78 vem o **apêndice**, que não corresponde a slide nenhum:

| # | assunto |
|---|---|
| A.1 | `interpolate(method="time")` e o `limit=` na grade regular |
| A.2 | a árvore de decisão do faltante, em tabela |
| A.3 | `convert_dtypes` — útil como sugestão, nunca como decisão |
| A.4 | `contains` e o `NaN`: o que mudou entre `object` e `str` no pandas 3 |
| A.5 | validar e-mail e telefone com `fullmatch` |
| A.6 | Titanic: a tabela pronta em oito linhas encadeadas |
| A.7 | táxis: seis perguntas que o `isna()` não responde |
| A.8 | a coluna derivada que denuncia — a velocidade impossível |

**O A.7 é o melhor achado do caderno:** nos táxis,
`total ≠ tarifa + gorjeta + pedágio` em **6.411 das 6.433 corridas**. A diferença
assume meia dúzia de valores fixos — são as taxas de Nova York, e a coluna que
explicaria a conta simplesmente não veio no arquivo. *Um analista apressado
"corrigiria" 6.411 linhas. O certo era perguntar.*

Mande a turma rodar o apêndice em casa: é onde a aula vira método.

## O exercício — Lista 2

`exercicio-aula05.ipynb` + `dados/clinica-suja.csv`.

Uma clínica com quatro unidades, 814 linhas de agendamento, **as mesmas doenças
do `vendas-sujas` em outra roupa**. O aluno não consegue copiar o código da aula,
mas todo defeito daqui ele já viu.

Onze questões, 14 pontos normalizados para 10 (sobra folga: dá para errar uma
questão inteira e ainda tirar dez). Cada questão tem uma célula de código **e uma
célula "Justifique:"** — e a justificativa vale mais.

O que o arquivo esconde, para você conferir a correção:

| defeito | onde | quanto |
|---|---|---|
| linhas idênticas | todas as colunas | 23 |
| quase-duplicatas | grafia do paciente | 11 → sobram **780 agendamentos únicos** |
| sentinela de data | `nascimento` = `01/01/1900` | 51 |
| sentinela numérica | `dias_ate_retorno` = `-1` | 364 (é "não marcou retorno") |
| grafias | `convenio` 21 → 5 · `especialidade` 17 → 5 · `unidade` 12 → 4 · `status` 9 → 4 | |
| datas | três formatos + 14 impossíveis; `format="mixed"` corrompe **150** | |
| duração impossível | `duracao_min` = 0, 480, 999 | 12 |
| **outlier legítimo** | 6 cirurgias, com a explicação na `obs` | R$ 11.934 a 27.300 |
| **outlier de digitação** | 5 consultas com um zero a mais, sem `obs` | R$ 1.466 a 3.921 |
| **outlier impossível** | valor negativo | 4 |
| faltantes em `valor_consulta` | | 60 (7,7%) |

Os três tipos de outlier estão plantados separadamente **de propósito**: a
questão 10 pede exatamente essa classificação, e ela só é possível lendo a
coluna `obs`.

## Verificar que nada quebrou

```bash
python gerar-dados.py              # refaz os quatro CSV (semente fixa)
python graficos.py                 # refaz os sete gráficos de img/
python montar-caderno.py           # remonta e executa o aula05.ipynb
python montar-caderno.py --so-checar   # só confere o alinhamento slides ↔ caderno
python saidas.py                   # roda os exemplos e confere os 20 números
python medir-densidade.py          # aponta slides com texto demais
```

O `saidas.py` e o `montar-caderno.py` **leem a numeração do próprio
`index.html`**, pelo atributo `data-nb`. Nenhum número de slide está escrito à
mão em lugar nenhum — mexer no deck não desalinha nada.

O `saidas.py` termina com um placar. Se algum número dos slides deixar de bater —
outra versão do pandas, outro CSV — ele aparece ali antes de aparecer na aula.

**Sobre a densidade:** o `medir-densidade.py` acusa cerca de vinte slides acima
do limite de 55 palavras. Quase todos são slides de **tabela** ou de **cards**,
onde o texto é estruturado e não corrido — a leitura de relance continua
funcionando. Os poucos de texto corrido já passaram por uma rodada de corte.

## Os números da aula

Medidos com pandas 3.0.5 sobre os arquivos de `dados/`.

| onde | número |
|---|---|
| `uf` no arquivo bruto | **27 grafias** para 10 estados |
| não viram número (slide 9) | `qtd` **16 de 627** · `valor` **495 de 627** |
| o que o `describe` denuncia | `avaliacao` min **−999** · `entrega_dias` max **365** |
| faltantes reconhecidos | 624 sem `na_values` · **677** com |
| a sentinela `-999` | média da avaliação: **−120,88** → 3,59 sem ela |
| `dropna()` sem argumento | 891 → **183 linhas** (79% da tabela) |
| Titanic | `Age` 177 (19,9%) · `Cabin` 687 (77,1%) · `Embarked` 2 |
| idade faltante × sobrevivência | **29,4% contra 40,6%** |
| desvio da idade | 14,53 → 13,02 (geral) → 13,30 (por grupo) |
| `skew` do salário | **7,16** — média 11.821, mediana 7.870 |
| duplicatas | 627 → 609 (idênticas) → **600** (quase-duplicatas) |
| falsas duplicatas nos táxis | **935** — 15% do arquivo |
| `format="mixed"` | **112 datas** trocadas de mês; a faixa pega só 30 |
| memória: `str` × `category` | 422,9 MB → **5,7 MB** (6 milhões de linhas) |
| `apply(axis=1)` × vetorizado | 195,8 ms × **0,05 ms** |
| `cut(4)` no salário | **183 · 3 · 0 · 2** — contra 47·47·47·47 do `qcut` |
| vendas corporativas | 4 pedidos = **30,7% do faturamento** |
| "quanto vendemos?" | **1.662.243** com tudo · **703.001** removendo pelo IQR |
| fuso do sensor | pico às **18h** lendo UTC · **15h** em Brasília |
| a conta dos táxis | `total ≠ fare+tip+tolls` em **6.411 de 6.433** |

## Arquivos

```
aula5/
├── index.html                 os 82 slides
├── aula05.ipynb               o caderno de acompanhamento (gerado — não edite)
├── caderno-fonte.py           o fonte do caderno, em chaves {{...}} — edite AQUI
├── montar-caderno.py          resolve as chaves, gera o índice e executa
├── exercicio-aula05.ipynb     a Lista 2, com o enunciado das 11 questões
├── LEIA-ME.md                 este arquivo
├── gerar-dados.py             monta os quatro CSV sujos (semente 20260828)
├── graficos.py                gera os sete gráficos de img/
├── saidas.py                  reproduz os slides e confere os 20 números
├── medir-densidade.py         aponta slides com texto demais
├── dados/
│   ├── vendas-sujas.csv       627 pedidos · 18 defeitos plantados
│   ├── sensores.csv           1.081 leituras em UTC · buracos e sentinelas
│   ├── rh.csv                 222 pessoas · grafias, faltantes e diretoria
│   ├── clinica-suja.csv       814 agendamentos · o dataset do exercício
│   ├── titanic.csv            891 passageiros (real, da aula 2)
│   └── taxis.csv              6.433 corridas (real, da aula 3)
├── img/                       os sete gráficos, fundo transparente
├── css/style.css              estilo, tema claro/escuro, impressão
├── js/
│   ├── highlight.js           realce de sintaxe — Python
│   ├── slides.js              navegação, índice, tema, PDF
│   └── sync.js                sincroniza o slide entre abas
└── .venv/                     pandas 3.0.5 · numpy · matplotlib · jupyterlab
```

O `dados/vendas-limpas.csv` aparece quando o caderno é executado até a parte 11 —
é a saída do pipeline, e pode ser apagado à vontade.

## Plano B

Tudo funciona offline: o deck não busca nada na rede, os gráficos já são imagens,
e os seis CSV estão na pasta. Antes da aula, exporte o PDF com a tecla `P` — uma página por
slide, 4:3, sempre no tema claro — e leve no pendrive.
