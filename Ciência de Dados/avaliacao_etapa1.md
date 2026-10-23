# Avaliação da Etapa 1 — julgamento para validar

Notas sobre 10, pela checklist combinada. Cada linha é um critério, com a leitura que gerou o ponto. Item pela metade vale metade.

Isto é rascunho para você validar, não a nota fechada.

Dois avisos antes da tabela:

- Nesta pasta, o único `projeto.ipynb` está no ZIP da Steam. Nos outros dez grupos a reprodutibilidade ficou em zero porque não há notebook para abrir e rodar. Se o notebook foi entregue em outro lugar, esses 1,0 pontos sobem.
- O título e o resumo do modelo da SBC ficaram no trabalho de Gustavo Santos, Leonardo Pavão e Kaue da Rosa. O desconto está no critério de formato desse grupo. O trabalho do Cauê (com Orion Zancan e Lucas Machado) tem título próprio no documento. Não descontei título nele.

| Grupo | Nota |
|---|---|
| Lucas Hotto, Marcelo Brum, Vinícius Strzelecki | 9,0 |
| Maicon Amélio, Maykom Mikael, Deivid Oliveira | 8,5 |
| Naiane Teixeira | 8,5 |
| Leonardo Nascimento, Marlon Rodrigues, Igor Bless | 8,5 |
| Nicolas Justen, Vitor Back, Lucas Bolzan | 8,25 |
| Amanda Dias, Priscila Batista | 7,5 |
| Camila Santos, Flávia Figueiró, Isabela Cadore | 7,25 |
| Helena Machado, Guilherme Machado | 7,0 |
| Bernardo Novaczinski, Rodrigo Cibulski | 7,0 |
| Gustavo Santos, Leonardo Pavão, Kaue da Rosa | 5,25 |
| Orion Zancan, Lucas Machado, Cauê Voese | 4,25 |

---

## Lucas Hotto, Marcelo Brum, Vinícius Strzelecki

Popularidade e aprovação de jogos na Steam. Única entrega com notebook e com o arquivo que explica como rodar.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Há três, e as duas primeiras dependem do catálogo. |
| Sujeito e recorte | 0,25 | Gênero, preço e ano recortam as duas primeiras. A terceira é “é possível prever”, e o slide trata o modelo como meio, não como pergunta. |
| A resposta muda uma decisão | 0,25 | A introdução fala em escolher referências para um jogo novo. As perguntas não dizem que decisão muda se o número vier. |
| As perguntas definem o trabalho | 0,5 | Seleção de colunas, variáveis derivadas e o alvo seguem as três perguntas. |
| Origem encontrável | 0,5 | Nome, autor e URL do Kaggle. |
| Licença nomeada | 0,5 | MIT, como na página. |
| Dicionário e unidade de observação | 0,5 | Uma linha é um AppID. A tabela agrupa as variáveis e diz para que servem. |
| Mínimos do dataset | 0,5 | A tabela 2 confere cada mínimo, com o número e o veredito. |
| Entendimento da estrutura e da qualidade | 0,5 | 125.855 linhas, 40 colunas, tipos, distintos, ausências e o defeito do cabeçalho. |
| Defeitos interpretados | 0,5 | Cabeçalho que desloca as colunas, lançamento futuro, zero de preço que pode ser gratuito, zero de nota que pode ser ausência. |
| Cada limpeza tem razão | 1,0 | Recorte na data de acesso, categorias ausentes preservadas, colunas fora das perguntas retiradas. A razão está ao lado do gesto. |
| Descarte declara a assunção | 1,0 | O jogo futuro sai porque ainda não acumulou público. O preço zero fica porque pode ser gratuito. Ausência vira “Não informado”, não uma categoria inventada. |
| Variáveis criadas servem às perguntas | 0,5 | Ano, taxa de aprovação, gratuito, gênero principal e faixa de donos estão na tabela com o uso. |
| Dataset em condição de ser analisado | 0,5 | 125.854 linhas depois do recorte, alvo definido, e o vazamento de usar a própria taxa como preditor já está marcado. |
| Outra pessoa roda o notebook | 0,25 | O notebook está no ZIP e o LEIA-ME diz como colocar o `games.csv`. O CSV não veio, e o texto ainda aponta `C:\Users\lucas\Downloads\...`. Não executei o Run All. |
| Números do PDF saem do código | 0,25 | O LEIA-ME afirma que saem. Sem o CSV, não conferi célula por célula. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,5 | O próprio LEIA-ME registra 5 páginas. Resumo, referências e as quatro seções estão lá. |
| Figuras, citações e redação | 0,5 | Figuras 1 e 2 com legenda e fonte. O texto se lê como relatório. |
| **Total** | **9,0** | |

---

## Maicon Amélio, Maykom Mikael, Deivid Oliveira

Análise de Dados de Anúncios do Airbnb em San Francisco.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Preço, demanda por avaliações e reputação do anfitrião, todas neste recorte de anúncios. |
| Sujeito e recorte | 0,5 | Bairro, tipo de acomodação e anúncios comparáveis. Não é “analisar o Airbnb”. |
| A resposta muda uma decisão | 0,5 | Precificar um anúncio novo, escolher localização e sustentar preço premium. |
| As perguntas definem o trabalho | 0,5 | A preparação cita as três ao remover coluna e ao criar variável. |
| Origem encontrável | 0,25 | O nome “San Francisco Airbnb Listings” e o Kaggle aparecem. A referência não traz a URL da página. |
| Licença nomeada | 0,5 | CC0: Public Domain, como na página. |
| Dicionário e unidade de observação | 0,5 | Uma linha é um anúncio. As variáveis das perguntas estão nomeadas e explicadas. Não é um dicionário das 106. |
| Mínimos do dataset | 0,5 | 8.111 linhas, 106 colunas, preço contínuo, bairro com 37 valores, datas de 2008 a 2019, textos, ausência na faixa, preço como alvo. |
| Entendimento da estrutura e da qualidade | 0,5 | Shape, duplicatas, tipos, distintos, tabela de ausências entre 5% e 50%, amplitude das datas. |
| Defeitos interpretados | 0,5 | Preço veio como texto. Ausência de review é comum. Coluna 100% vazia não informa. |
| Cada limpeza tem razão | 1,0 | Monetário para número, booleanos padronizados, colunas vazias e esparsas fora porque não respondem às perguntas, preço ≤ 0 vira ausente. |
| Descarte declara a assunção | 1,0 | Outlier de preço fica, porque preço alto pode ser anúncio legítimo e a pergunta 1 é sobre preço alto. 583 casos só ganham uma marca. |
| Variáveis criadas servem às perguntas | 0,5 | Contagem de comodidades, preço por hóspede, tempo de anfitrião, dias desde a última avaliação, tem avaliação. |
| Dataset em condição de ser analisado | 0,5 | 8.111 linhas mantidas, 92 colunas depois dos cortes, arquivo `listings_clean.csv`. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,25 | As seções e o resumo estão certos. O PDF tem 7 páginas, acima do teto de 6. |
| Figuras, citações e redação | 0,5 | Tabelas com legenda, referência ao final, texto de relatório. |
| **Total** | **8,5** | |

---

## Naiane Teixeira

Devoluções, Descontos e Estoque: uma Análise Exploratória de Dados de Vendas em uma Boutique de Moda.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Devolução, desconto por categoria e a combinação dos dois, na base da boutique. |
| Sujeito e recorte | 0,5 | Produto, categoria, características nomeadas. O próprio texto recusa média solta e “aplicar modelo”. |
| A resposta muda uma decisão | 0,5 | Sinalizar risco antes da venda, rever a política de desconto, comprar menos de uma categoria. |
| As perguntas definem o trabalho | 0,5 | Cada tratamento da seção 4 aponta para P1, P2 ou P3. |
| Origem encontrável | 0,5 | Nome, autor no Kaggle e URL. |
| Licença nomeada | 0,5 | Apache License 2.0. |
| Dicionário e unidade de observação | 0,5 | Uma linha é um produto, não uma venda nem um dia. A tabela traz tipo, nulos e distintos de cada variável. |
| Mínimos do dataset | 0,25 | Volume, tipos, data de treze meses, sujeira em `size` e `customer_rating`, alvo `is_returned`. Não há coluna de texto livre, e o trabalho registra isso em vez de forçar. Um mínimo falhou. |
| Entendimento da estrutura e da qualidade | 0,5 | A tabela 1 e o texto cobrem tamanho, tipos, vazios, distintos e a checagem de preço contra o desconto. |
| Defeitos interpretados | 0,5 | `return_reason` vazio é estrutural, porque só o produto devolvido tem motivo. `size` vazio é falha de coleta. A distinção está escrita. |
| Cada limpeza tem razão | 1,0 | Tamanho vira “não informado” porque a ausência pode ser causa da devolução. Nota vazia não vira zero. Motivo vazio vira “não devolvido”. |
| Descarte declara a assunção | 1,0 | Nenhuma linha sai. O texto diz que os vazios têm significado e que exclusão esconderia a pergunta. |
| Variáveis criadas servem às perguntas | 0,5 | Mês da compra cruza com a coleção. `markdown_flag` separa “houve desconto” de “quanto”. |
| Dataset em condição de ser analisado | 0,25 | A seção 4 está no futuro: “serão mantidos”, “será revisitada”. A razão está pronta. O dataframe preparado não está mostrado. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. Os números do texto são específicos, mas não deu para bater com célula. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,5 | 5 páginas, resumo, referências e as quatro seções. |
| Figuras, citações e redação | 0,5 | Figuras 1 e 2 referidas, citações, leitura de relatório. |
| **Total** | **8,5** | |

---

## Leonardo Nascimento, Marlon Rodrigues, Igor Bless

Análise Exploratória de Dados de Corridas da Uber.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Motivo de cancelamento, tempo de chegada e corrida incompleta, no recorte 17h–19h. |
| Sujeito e recorte | 0,5 | Horário de pico, status da corrida, motivo. |
| A resposta muda uma decisão | 0,5 | Qual motivo priorizar, qual situação de chegada atender primeiro, qual grupo de corrida incompleta vem na frente. |
| As perguntas definem o trabalho | 0,5 | A preparação cria o marcador de horário e diz qual variável responde cada pergunta. |
| Origem encontrável | 0,5 | Autor, nome e URL do Kaggle. |
| Licença nomeada | 0,5 | CC BY-SA 4.0. |
| Dicionário e unidade de observação | 0,5 | Uma linha é uma solicitação de corrida. Variável, descrição e tipo. |
| Mínimos do dataset | 0,25 | 150.000 linhas e 21 colunas, várias categóricas com mais de 5 valores, numéricas contínuas. O período é 2024, no limite de doze meses. Os vazios citados passam de 50%. Não há coluna de texto livre clara: motivo e local são categorias fechadas. |
| Entendimento da estrutura e da qualidade | 0,5 | Tipos, ausências com contagem, distintos, status e o Booking ID repetido. Há um número solto: 148.770 na fonte e 150.000 no arquivo. |
| Defeitos interpretados | 0,5 | Ausência de motivo não é erro quando a corrida não foi cancelada. ID repetido não é, sozinho, duplicata exata. |
| Cada limpeza tem razão | 1,0 | Aspas no ID saem porque não significam nada. Data vira tempo para filtrar 17h–19h. Vazio operacional não vira zero. |
| Descarte declara a assunção | 1,0 | Os 1.233 registros de ID repetido ficam, porque excluir poderia apagar corrida distinta. A assunção está dita. |
| Variáveis criadas servem às perguntas | 0,5 | Marcador de horário de pico, e a taxa de incompletas no lugar da contagem absoluta. |
| Dataset em condição de ser analisado | 0,5 | O conjunto preparado preserva o arquivo e fica utilizável. Não há uma contagem final de linhas depois da preparação. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,5 | Resumo, referências e seções 1 a 4. É DOCX. Não contei página impressa. |
| Figuras, citações e redação | 0,25 | A referência existe e o texto argumenta. Não há figura com legenda. |
| **Total** | **8,5** | |

---

## Nicolas Justen, Vitor Back, Lucas Bolzan

Projeto de Análise de Dataset “European Soccer Database”.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Mando, favorito pela cotação e distância entre campeão e vice, nas partidas. |
| Sujeito e recorte | 0,5 | Temporada 2015/2016 na primeira. 2008/2009 a 2015/2016 na terceira. Liga e equipe nomeadas. |
| A resposta muda uma decisão | 0,25 | Dá para comparar mando, favoritismo e equilíbrio. O texto não diz que decisão alguém tomaria com a resposta. |
| As perguntas definem o trabalho | 0,5 | Cada filtro e cada variável derivada está amarrado a uma pergunta. |
| Origem encontrável | 0,5 | Hugo Mathien, Kaggle, URL, período da base. |
| Licença nomeada | 0,25 | Copiaram o que a página diz: “Database: Open Database, Contents: © Original Authors”. Isso nomeia a origem, e não é uma licença aberta clara. O slide pedia outra base quando a licença não está declarada. |
| Dicionário e unidade de observação | 0,5 | Uma linha é uma partida. Tabela com tipo e descrição. |
| Mínimos do dataset | 0,5 | 25.979 partidas, 14 colunas de conteúdo, oito temporadas, cotações com 13,04% de ausência, nomes de equipe, gols e data. |
| Entendimento da estrutura e da qualidade | 0,5 | A tabela 2 traz partidas, colunas, temporadas, ligas, datas inválidas, ausência e os seis nomes iguais com IDs diferentes. |
| Defeitos interpretados | 0,5 | Cotação ausente impede achar o favorito. Nome igual com ID diferente não é o mesmo time. |
| Cada limpeza tem razão | 1,0 | Partida sem cotação sai só da pergunta 2. Empate como menor cotação sai porque não há favorito único. Mínimo de 10 jogos em casa e fora evita média de amostra minúscula. |
| Descarte declara a assunção | 1,0 | O filtro não é da base inteira. Cada exclusão diz o que a pergunta passaria a comparar. |
| Variáveis criadas servem às perguntas | 0,5 | Pontos por mando, favorito pela cotação, vitória do favorito, diferença entre primeiro e segundo. |
| Dataset em condição de ser analisado | 0,5 | A seleção analítica está descrita. Os filtros são por pergunta, não um arquivo único já cortado. Ainda assim dá para analisar. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,5 | Resumo, referências e as quatro seções. É DOCX. O texto é curto. Não vi estourar o teto. |
| Figuras, citações e redação | 0,25 | Citação e tabelas. Não há figura. A redação é de relatório. |
| **Total** | **8,25** | |

---

## Amanda Dias, Priscila Batista

Análise de Atrasos e Cancelamentos de Voos nos Estados Unidos entre 2019 e 2023.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Atraso, horário do atraso e cancelamento, nos voos do arquivo. |
| Sujeito e recorte | 0,25 | A segunda tem período e horário. A primeira e a terceira pedem “características” sem recortar quais. |
| A resposta muda uma decisão | 0,25 | Dá para imaginar uma decisão operacional. O texto não diz qual. Fica em “estão relacionadas”. |
| As perguntas definem o trabalho | 0,5 | Ano, mês e dia da semana nascem para a segunda. Cancelamento é preservado por causa da terceira. |
| Origem encontrável | 0,5 | Nome, arquivo `flights_sample_2m.csv`, autor e URL. |
| Licença nomeada | 0,0 | A página diz “Other (specified in description)”. O grupo registra isso e não atribui licença. O slide mandava escolher outro dataset. |
| Dicionário e unidade de observação | 0,5 | Uma linha é um voo. A tabela 1 descreve as variáveis principais, não as 32. |
| Mínimos do dataset | 0,25 | 2.000.000 linhas, 32 colunas, data de 2019 a 2023, numéricas, 18 companhias e 380 aeroportos. Eles mesmos mostram que nenhuma coluna cai na faixa de 5% a 50% de vazios: ou é pouco, ou passa de 80%. |
| Entendimento da estrutura e da qualidade | 0,5 | Shape, tipos, distintos, duplicatas zero e a tabela de ausências. |
| Defeitos interpretados | 0,5 | Código de cancelamento vazio é voo que aconteceu. Causa de atraso vazia não é o mesmo que atraso zero. |
| Cada limpeza tem razão | 1,0 | Data convertida. Vazio estrutural mantido. Duplicata conferida e inexistente. |
| Descarte declara a assunção | 1,0 | Remover cancelado apagaria a terceira pergunta. Preencher causa de atraso com zero misturaria situações diferentes. As duas frases estão no texto. |
| Variáveis criadas servem às perguntas | 0,5 | Ano, mês e dia da semana, para comparar períodos. |
| Dataset em condição de ser analisado | 0,5 | Continua com 2.000.000 de linhas e passa a 35 colunas. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,5 | 6 páginas, no teto. Resumo, referências e as quatro seções. |
| Figuras, citações e redação | 0,25 | Citação e tabelas com legenda. Não há gráfico. A redação segura o relatório. |
| **Total** | **7,5** | |

---

## Camila Santos, Flávia Figueiró, Isabela Cadore

Panorama da Infraestrutura Cinematográfica no Brasil.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Acessibilidade, distribuição de assentos e sobrevivência dos complexos, nas salas da ANCINE. |
| Sujeito e recorte | 0,5 | Grupo exibidor, UF, município, itinerante contra permanente, grande grupo contra independente. |
| A resposta muda uma decisão | 0,5 | Onde está o gargalo de acessibilidade, onde há deserto de salas, que tipo de exibidor permanece. |
| As perguntas definem o trabalho | 0,5 | Índice de acessibilidade, tempo de operação e porte do complexo nascem das três. |
| Origem encontrável | 0,5 | Portal da ANCINE, com URL em dados.gov.br. |
| Licença nomeada | 0,25 | Citam a Lei de Acesso à Informação e “licença aberta (Open Data)”. Não copiam o nome de uma licença da página. |
| Dicionário e unidade de observação | 0,5 | Uma linha é uma sala, pelo `REGISTRO_SALA`. O dicionário organiza as 32 variáveis por grupo. |
| Mínimos do dataset | 0,5 | 6.405 linhas, 32 colunas, datas, texto de nome e endereço, ausência de 19% a 32% em assentos adaptados, UF com 27 valores, alvo possível na sala acessível. |
| Entendimento da estrutura e da qualidade | 0,5 | Tipos errados no arquivo, cardinalidade, e percentuais de ausência com o que coincidem. |
| Defeitos interpretados | 0,5 | Data de início vazia em 85,87% impede reconstruir a inauguração. O mesmo percentual em várias colunas sugere registro órfão. Identificador numérico não é grandeza. |
| Cada limpeza tem razão | 0,5 | Os 37 registros sem identificação saem. Colunas de página e complemento saem. Tipos são corrigidos. A coluna de preço de ingresso é inventada, por sorteio entre R$ 18 e R$ 45, “por orientação do docente”. Isso não é limpeza do arquivo. Confirme se a orientação existiu antes de manter ou tirar ponto. |
| Descarte declara a assunção | 0,5 | Assento adaptado vazio vira zero, na premissa de que não declarar é não ter o recurso. Os 37 registros saem por serem corrompidos. A premissa do zero é forte e está escrita. O preço sorteado não declara nada sobre o fenômeno. |
| Variáveis criadas servem às perguntas | 0,25 | O índice de acessibilidade, a flag de sala acessível, o tempo de operação e o porte do complexo servem. O preço simulado não responde pergunta nenhuma da base. |
| Dataset em condição de ser analisado | 0,5 | Fecham em 6.368 salas e 37 atributos. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,5 | 7 páginas, uma acima do teto. Resumo, referências e as quatro seções. As seções 5, 6 e 7 estão só como título vazio. |
| Figuras, citações e redação | 0,25 | Há citação e tabelas. Não há figura. O texto é longo para o que a tabela já dizia. |
| **Total** | **7,25** | |

---

## Helena Machado, Guilherme Machado

Análise de Anúncios do Airbnb em Chicago: Preços, Localização e Características das Acomodações.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Preço por bairro, tipo de acomodação e características ligadas ao preço alto. |
| Sujeito e recorte | 0,5 | Chicago, bairro, tipo de quarto, anúncio. |
| A resposta muda uma decisão | 0,25 | A seção de problema fala em posicionar o anúncio. As perguntas em si pedem como o preço varia e o que está associado. A decisão não está na pergunta. |
| As perguntas definem o trabalho | 0,5 | Preço, bairro, tipo e avaliação organizam o entendimento e a preparação. |
| Origem encontrável | 0,5 | Inside Airbnb, arquivo `listings.csv`, data de referência 24/06/2026, URL. |
| Licença nomeada | 0,5 | CC BY 4.0. |
| Dicionário e unidade de observação | 0,5 | Uma linha é um anúncio, identificado por `id`. Tabela com tipo e descrição. |
| Mínimos do dataset | 0,5 | 6.397 linhas, 16 colunas, 77 bairros, preço contínuo, `last_review` de 2013 a 2020, `name` como texto, 17,70% de ausência, preço como alvo. |
| Entendimento da estrutura e da qualidade | 0,5 | Tipos, distribuição, estatística de preço, ausência e a coincidência com anúncio sem avaliação. |
| Defeitos interpretados | 0,5 | `neighbourhood_group` 100% vazio não informa. Avaliação ausente é anúncio sem review, não erro. Preço zero e preço de US$ 10.000 pedem investigação, não corte automático. |
| Cada limpeza tem razão | 0,5 | A coluna vazia sai, a data é convertida, a flag `sem_avaliacoes` é criada. O preço zero e o máximo ficam para “serão investigados”. A preparação está no futuro: “será removida”, “será convertida”. A duplicata de `id` é um comando, sem o resultado. |
| Descarte declara a assunção | 0,5 | Manter anúncio sem avaliação preserva um caso real. Preço extremo pode ser válido. As duas estão ditas. A decisão do preço zero não foi tomada. |
| Variáveis criadas servem às perguntas | 0,25 | `sem_avaliacoes` serve. Não há outras, e o preço por características da terceira pergunta ainda não ganhou variável. |
| Dataset em condição de ser analisado | 0,25 | O texto diz que o notebook fará a preparação. O relatório não mostra o dataframe pronto nem a contagem depois da limpeza. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,25 | As quatro seções existem, e o PDF segue para resultados, limitações e conclusão. São 9 páginas. |
| Figuras, citações e redação | 0,5 | Tabelas com legenda, referências, texto de relatório. |
| **Total** | **7,0** | |

---

## Bernardo Novaczinski, Rodrigo Cibulski

Inspeção de demanda de reservações de hotéis.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Cancelamento, diária ao longo do ano e canal com depósito. |
| Sujeito e recorte | 0,5 | Reserva, antecedência, mês, tipo de hotel, canal e depósito. |
| A resposta muda uma decisão | 0,5 | Reter ou fazer overbooking, qual combinação gera receita, qual canal priorizar. |
| As perguntas definem o trabalho | 0,5 | As colunas tratadas são as que as perguntas usam: país, crianças, agente, diária. |
| Origem encontrável | 0,5 | Hotel Booking Demand, URL do Kaggle e a citação. |
| Licença nomeada | 0,5 | Creative Commons Attribution 4.0. |
| Dicionário e unidade de observação | 0,5 | Uma linha é uma reserva. O dicionário cobre as variáveis das perguntas, não as 32. |
| Mínimos do dataset | 0,5 | 119.390 linhas, 32 colunas, julho de 2015 a agosto de 2017, `agent` com 13,69% de ausência, país, diária contínua, `is_canceled` como alvo. `market_segment` tem 8 valores. |
| Entendimento da estrutura e da qualidade | 0,5 | Tipos, ausências com percentual e contagem, distintos e defeitos. A frase dos tipos cita uma coluna como se ela fosse o grupo inteiro. O número principal está. |
| Defeitos interpretados | 0,5 | `company` com 94% vazio não serve para cruzar. Reserva com zero hóspedes não é hospedagem. Diária negativa e um valor de 5.400 são pontos fora do padrão. |
| Cada limpeza tem razão | 0,5 | País por extenso, quatro crianças vazias viram zero, país vazio vira “Unknown”, reserva sem hóspede sai, dois valores de diária saem. `agent` e `company` vazios viram zero, e na seção anterior `company` tinha sido chamada de inutilizável. A razão dessa troca para zero é fraca. |
| Descarte declara a assunção | 0,5 | Zero hóspede é reserva de teste ou erro. Zero em `agent` significa sem agência. As duas estão ditas. Tratar código de agente como número que pode ser zero mistura identificador com quantidade. |
| Variáveis criadas servem às perguntas | 0,0 | Não há coluna derivada, nem a frase de que as originais já bastam. |
| Dataset em condição de ser analisado | 0,25 | Há tratamento. Não há o tamanho do arquivo depois de eliminar as reservas sem hóspede. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Não há notebook para conferir. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,5 | 4 páginas, no piso. Resumo, referências e as quatro seções. |
| Figuras, citações e redação | 0,25 | Citação e uma tabela. Não há figura. O texto é curto e alguns tipos estão mal contados. |
| **Total** | **7,0** | |

---

## Gustavo Santos, Leonardo Pavão, Kaue da Rosa

O arquivo se chama “Projeto de Ciência de Dados”. O corpo usa Hotel Bookings. Título e resumo continuam os do modelo da SBC.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Risco de cancelamento, segmento com maior valor cancelado, janela para revender o quarto. |
| Sujeito e recorte | 0,5 | Reserva, antecedência, segmento, dias antes da chegada. |
| A resposta muda uma decisão | 0,5 | Agir antes da chegada, priorizar segmento, tentar vender o quarto de novo. |
| As perguntas definem o trabalho | 0,25 | As perguntas são boas. A preparação trata `children`, `country`, `agent` e `company` sem mostrar como cada uma responde uma delas. |
| Origem encontrável | 0,5 | Kaggle, usuário mexwell, URL, e o artigo original. |
| Licença nomeada | 0,5 | CC BY 4.0 na fonte original. |
| Dicionário e unidade de observação | 0,5 | Uma linha é uma reserva. 40.060 do resort e 79.330 do urbano. Lista do que cada coluna significa. |
| Mínimos do dataset | 0,25 | 119.390 linhas, 32 colunas, 2015 a 2017, `agent` com 13,69% de ausência, diária contínua. País está em código, não em texto livre. A faixa de tipos no entendimento mistura coluna de data com numérica. |
| Entendimento da estrutura e da qualidade | 0,5 | Tamanho, período, lista de faltantes com percentual, cardinalidade e três problemas nomeados. |
| Defeitos interpretados | 0,25 | `company` acima de 90% dificulta a análise. Código de país e de quarto exige consulta externa. O salto de `children` de 3 para 10 é apontado, sem uma conclusão sobre o que ele é. |
| Cada limpeza tem razão | 0,5 | País vazio vira PRT porque é a moda e a fatia é pequena. `agent` vazio vira o código 9 pela mesma lógica. `company` é ignorada porque 94% não dá para imputar. `children` é discutida e a decisão final não fecha. Há razão. Ela imputa identificador pela moda. |
| Descarte declara a assunção | 0,25 | Para `company`, os dois motivos são suposição, e o texto diz que não dá para saber. Preencher agente faltante com o código 9 afirma que aquela reserva foi daquele agente. Isso não está assumido com clareza. |
| Variáveis criadas servem às perguntas | 0,0 | Não há variável derivada ligada às perguntas. |
| Dataset em condição de ser analisado | 0,25 | A seção mostra comandos e decisões. Não mostra o conjunto resultante. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. |
| Números do PDF saem do código | 0,0 | Há comandos colados. Não há saída de notebook para bater. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,0 | Título e resumo são o texto padrão do template, não o trabalho. O PDF tem 10 páginas. As seções 5, 6 e 7 estão vazias. Não há lista de referências no fim. |
| Figuras, citações e redação | 0,0 | O resumo não descreve o trabalho. Não há figura. A redação conta a ferramenta antes da pergunta. |
| **Total** | **5,25** | |

---

## Orion Zancan, Lucas Machado, Cauê Voese

Análise Exploratória de Dados de Animes. O título está no documento. O desconto abaixo não é por título.

| Critério | Nota | Leitura |
|---|---|---|
| Três perguntas cuja resposta sai do dataset | 0,5 | Estúdio e nota, formato e audiência, volume e qualidade ao longo do tempo. Estão num parágrafo, e saem do catálogo. |
| Sujeito e recorte | 0,25 | Estúdio, formato e tempo aparecem. Falta o recorte de quais estúdios e de qual período entram na pergunta. |
| A resposta muda uma decisão | 0,25 | A introdução fala em licenciamento e curadoria. As perguntas perguntam quem tem a maior média. Não dizem a decisão. |
| As perguntas definem o trabalho | 0,25 | O miolo são 14 gráficos. Vários não respondem as três perguntas. |
| Origem encontrável | 0,25 | Sete arquivos com contagem e o site do MyAnimeList. Não há a página do dataset que outra pessoa baixaria igual. |
| Licença nomeada | 0,0 | Não há licença. |
| Dicionário e unidade de observação | 0,25 | A tabela descreve arquivos, não o que cada variável significa. Dá para inferir que uma linha de `anime.csv` é um título. Não está dito. |
| Mínimos do dataset | 0,25 | 10.000 títulos e tabelas grandes. Sinopse é texto. Datas aparecem na análise. 13,4% sem gênero cumpre a faixa de sujeira, dito só na seção de modelagem futura. A conferência dos mínimos não está feita. |
| Entendimento da estrutura e da qualidade | 0,25 | Tamanho dos arquivos sim. Tipos, vazios e distintos do arquivo principal não estão numa seção de entendimento. Aparecem no meio dos resultados. |
| Defeitos interpretados | 0,5 | Popularidade é ranking, não contagem. Gênero veio duplicado por erro de coleta. Contagem de personagens tem teto artificial. Isso está interpretado. |
| Cada limpeza tem razão | 0,25 | A limpeza de gênero duplicado é citada, com a ideia do reparo. Não há a seção de preparação com cada escolha e sua razão. |
| Descarte declara a assunção | 0,25 | O teto de personagens e o gênero ausente ganham recomendação para a modelagem. Não há a assunção ao lado de um descarte feito agora. |
| Variáveis criadas servem às perguntas | 0,0 | Não há variáveis derivadas documentadas para as três perguntas. |
| Dataset em condição de ser analisado | 0,25 | A análise já foi feita, então algum conjunto foi usado. O relatório não entrega o dataset preparado. |
| Outra pessoa roda o notebook | 0,0 | Não há notebook nesta pasta. O texto diz que houve um. |
| Números do PDF saem do código | 0,0 | Cada gráfico cita a métrica. Sem o notebook, o número não foi conferido. |
| Artigo SBC, 4 a 6 páginas, seções 1 a 4 | 0,25 | Há resumo, referências e figuras. A estrutura não é a da Etapa 1. O grosso é exploração, que era a Etapa 2. É DOCX. Não contei as páginas. |
| Figuras, citações e redação | 0,5 | Catorze análises com a métrica dita, referências, texto que se lê. |
| **Total** | **4,25** | |

O trabalho do Cauê responde coisas e mostra gráfico. A nota baixa é porque a Etapa 1 pedia perguntas, dados, entendimento e preparação, e o arquivo entregue é a exploração.
