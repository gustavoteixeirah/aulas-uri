# Aula 02 · Ciência de Dados

A aula tem **três artefatos**, na ordem em que são usados:

1. **`exercicios-aula01-resolucao.ipynb`** — o gabarito da lista da aula 1, para corrigir
   em sala. Cada célula roda sozinha, então dá para pular direto para qualquer exercício.
2. **`aula02.ipynb`** — o notebook da aula. É onde a aula acontece: o Titanic aberto,
   cruzado e desenhado, do arquivo bruto a cinco achados. **Sem aula de linguagem** —
   nenhum bloco sobre sintaxe de Python.
3. **`index.html`** — os 20 slides do **projeto final**, para apresentar no fim da aula e
   postar no AVA depois.

E, para os alunos levarem: **`../exercicios/lista1-outro-dataset.pdf`** — a Lista 1, que
manda repetir a análise do Titanic num dataset com outros tipos de coluna.

> O deck **completo** da aula 2 (45 slides, com os blocos sobre de onde vem o dado e o
> Titanic) continua em **`index-aula-completa.html`** e no `aula2-slides.pdf`. Ele não é
> apresentado — serve de material de consulta e de fonte para os slides do trabalho.

## Como abrir

Slides: duplo clique em **`index.html`**. Funciona offline, em qualquer navegador moderno.

Notebook:

```bash
python -m venv .venv && source .venv/bin/activate
pip install pandas matplotlib seaborn jupyter
jupyter lab aula02.ipynb
```

## Controles dos slides

| Ação | Como |
|---|---|
| Avançar | botão **Avançar**, `→`, `espaço`, `Enter`, `PageDown` ou deslizar para a esquerda |
| Voltar | botão **Voltar**, `←`, `Backspace`, `PageUp` ou deslizar para a direita |
| Índice da aula | botão `☰` ou tecla `M` |
| Tema claro/escuro | botão `◐` ou tecla `T` (o tema fica salvo) |
| Exportar em PDF | botão **PDF** ou tecla `P` |
| Tela cheia | botão `⛶` ou tecla `F` |
| Primeiro / último slide | `Home` / `End` |
| Ir direto a um slide | endereço terminado em `#22`, por exemplo |

Pela linha de comando:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --no-pdf-header-footer --print-to-pdf=aula2-slides.pdf \
  "file:///caminho/para/aula2/index.html"
```

## Estrutura

```
aula2/
├── aula02.ipynb          o notebook da aula — 12 seções, 33 células, 10 gráficos
├── exercicios-aula01-resolucao.ipynb   gabarito da lista da aula 1
├── index.html            os 20 slides do projeto final — o que se apresenta e se posta
├── index-aula-completa.html   o deck de 45 slides, para consulta
├── projeto-final-slides.pdf   exportação do deck do trabalho
├── css/style.css         estilo, tema claro/escuro e animações
├── js/slides.js          navegação, índice, realce de sintaxe (Python)
├── demo.py               a mesma demonstração em script — plano B, se o Jupyter falhar
├── dados/titanic.csv     o train.csv da competição Titanic (Kaggle) · CC0
├── titanic.png           figura do Titanic (usada no deck completo)
└── aula2-slides.pdf      exportação, para o plano B
```

## Conteúdo dos slides do projeto final

| Slides | Assunto |
|---|---|
| 1–4 | capa · o trabalho em uma frase · as duas entregas · os três artefatos |
| **01 · Escolher o dataset** (5–12) | onde procurar · como escolher (assunto que interessa) e os proibidos · os mínimos com exemplo de cada um · as quatro linhas que conferem · **dois exemplos rodados de verdade** · a conferência item por item |
| **02 · Escrever o relatório** (13–19) | pergunta de negócio · a estrutura das 7 seções · limitações · critérios por etapa · cronograma · os cinco jeitos de se dar mal |
| 20 | o que fazer nesta semana |

Os dois slides de exemplo (10 e 11) mostram **saída real**: os dados abertos da Câmara
(7.889 deputados, CSV com `sep=";"`) e os táxis de Nova York que vêm com o seaborn.
O código, a saída e o gráfico foram gerados rodando — nada foi escrito à mão. As figuras
são `ex-deputados.png` e `ex-taxis.png`; para atualizá-las, rode o código do próprio slide.

Ficaram de fora, de propósito: LGPD, tabela de licenças, as 8 perguntas de triagem e a
armadilha do dataset limpo demais. O deck é sobre **fazer o trabalho**, não sobre teoria
de dados — esse material continua no `index-aula-completa.html`.

## O notebook

| § | O que mostra | Slides |
|---|---|---|
| 1 | abrir o arquivo · `shape` e `info` — tamanho e faltantes | 19–22 |
| 2 | o que cada coluna quer dizer | 17–18 |
| 3 | **quem sobreviveu?** · o pictograma das 891 pessoas, barras por sexo e classe, e o mapa de calor sexo × classe | 23–24 |
| 4 | criança tinha mais chance? · histograma e faixas etárias | 26 |
| 5 | o preço do bilhete · média × mediana, boxplot por classe, dispersão idade × tarifa | 25 |
| 6 | o que está escondido dentro do nome · o título social e o "Master" | 26 |
| 7 | sozinho ou com a família? · e a família Sage, sete pessoas, nenhuma sobrevivente | 27 |
| 8 | **a coluna 77% vazia que era ouro** · e o deck do navio, extraído da letra da cabine | 28 |
| 9 | e as 177 idades que faltam? · três saídas, uma escolhida | 29 |
| 10 | o painel — tudo em quatro gráficos | 30–31 |
| 11 | **e você, teria sobrevivido?** · a turma testa os próprios dados | — |
| 12 | confira o seu dataset candidato com as mesmas quatro linhas | 8–12 |

Tudo o que aparece nos slides é **saída real** do notebook — nada foi inventado para
caber no slide. As células marcadas com ✋ **Sua vez** são pausas: a turma escreve.

O notebook usa `pandas`, `matplotlib` e `seaborn` — os três precisam estar instalados,
porque quase toda seção termina em gráfico. São **dez** ao todo. Testado em pandas 2.x
e 3.x.

A paleta é fixa e significa alguma coisa: **verde** = sobreviveu, **vermelho** = morreu,
**azul** = uma taxa. Barras de uma mesma série têm sempre a mesma cor.

## Roteiro sugerido (~3h20)

| Tempo | O quê | Como conduzir |
|---|---|---|
| 0:00–0:40 | **Correção da lista da aula 1** | `exercicios-aula01-resolucao.ipynb`. Pare no exercício 10 (as armadilhas) — é o que mais gera discussão. |
| 0:40–1:35 | **Notebook § 1–6** | Projete o Jupyter, não o slide. O pictograma das 891 pessoas abre o § 3; o mapa de calor é o primeiro "uau" da aula. |
| 1:35–1:50 | **Intervalo** | |
| 1:50–2:40 | **Notebook § 7–11** | O § 8 (`Cabin`) é o momento da aula. Faça a pergunta **antes** de rodar a célula. Termine no § 11: cada um calcula a própria chance. |
| 2:40–3:10 | **Slides do projeto final** | Os 20 slides. Leia junto as duas entregas (slide 3), os mínimos do dataset (11) e os critérios (17). |
| 3:10–3:20 | **Lista 1 e fechamento** | Distribua a `lista1-outro-dataset.pdf`, mostre o § 12 (conferir o dataset candidato) e recolha dúvidas. |

**Notas de condução**

- **O momento da aula é o § 8** (`Cabin`, 77% vazia). Faça a pergunta — "jogar essa
  coluna fora?" — e deixe a turma responder *antes* de rodar a célula que mostra
  0,300 contra 0,667. Quem disse "joga fora" acabou de aprender por que não.
- **A coluna `pessoas` ao lado de toda taxa** parece óbvia e não é. Vale insistir: é a
  regra que mais aparece nos erros do projeto final.
- **O § 11 fecha a aula rindo** — cada aluno calcula a chance de sobreviver com os
  próprios dados. Deixe a turma brincar dois minutos; é o que fixa a ideia de que uma
  taxa é sempre a taxa *de um grupo*.
- **Os § 4 e § 5 são os mais fáceis de acelerar** se o tempo apertar. Não pule o § 6
  (o título dentro do nome) nem o § 8 (`Cabin`): são os dois que a turma leva para casa.
- **Não corra o bloco 03.** Se estiver atrasado, corte do § 1 do notebook. O trabalho
  precisa ser explicado com calma: ele responde pelas duas notas do semestre.
- **O slide 12 proíbe o Titanic no projeto.** Diga isso explicitamente ao terminar o
  notebook, senão metade da turma propõe o Titanic na aula 3.
- **Plano B:** o `aula2-slides.pdf`, o `demo.py` e o `titanic.csv` num pendrive. O
  `demo.py` roda a mesma demonstração sem Jupyter; só o tour pelo Kaggle depende de rede.

## Cronograma do semestre

O documento `../cronograma-semestre.pdf` (fonte em `.html`, ao lado) expande o slide 18
para os 18 encontros: tema de cada aula, marcos do projeto, listas, prova e as duas
entregas. **Seis encontros são oficina** — aulas 8–9 para a Etapa 1 e 15–18 para a
Etapa 2 —, e o conteúdo que ocupava esses seis encontros foi realocado para as aulas
6, 7, 10, 12, 13 e 14. O mapa dessa realocação está na última página do cronograma.

## Material do aluno

- `aula02.ipynb` e `dados/titanic.csv` — para rodar, quebrar e modificar
- `projeto-final-slides.pdf` — os slides do trabalho, para postar no AVA
- `../exercicios/lista1-outro-dataset.pdf` — a Lista 1, entrega até o início da aula 3
- `../trabalho/projeto-final.pdf` — o enunciado completo do projeto
- `../cheatsheet/cheatsheet.pdf` — referência de Python
