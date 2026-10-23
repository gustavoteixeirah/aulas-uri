"""Gera os quatro datasets sujos da aula 5 — a sujeira é toda de propósito.

    dados/vendas-sujas.csv   o caso central: 18 defeitos plantados em 627 linhas
    dados/sensores.csv       série temporal em UTC, com buracos e sentinelas
    dados/rh.csv             folha de pessoal: grafias, faltantes e um outlier
    dados/clinica-suja.csv   o dataset do EXERCÍCIO — as mesmas doenças, outra roupa

Os outros dois arquivos de dados/ são reais e vêm das aulas anteriores:
taxis.csv (aula 3) e titanic.csv (aula 2).

Tudo é sorteado com semente fixa — rodar de novo dá exatamente o mesmo arquivo,
então os números dos slides não mudam.

Uso:  python gerar-dados.py
"""
import csv
import os
import random
from datetime import datetime, timedelta

import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(BASE, "dados")
os.makedirs(DADOS, exist_ok=True)

SEMENTE = 20260828
random.seed(SEMENTE)
rng = np.random.default_rng(SEMENTE)


def escreve(nome, cabecalho, linhas):
    caminho = os.path.join(DADOS, nome)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(cabecalho)
        w.writerows(linhas)
    kb = os.path.getsize(caminho) / 1024
    print(f"ok  {nome:<20} {len(linhas):>5} linhas · {kb:>6.1f} KB")


# ══════════════════════════════════════════════════════════════════════
# 1. vendas-sujas.csv — o dataset principal da aula
# ══════════════════════════════════════════════════════════════════════
# Dezoito defeitos plantados, cada um alvo de um slide:
#   1  espaço sobrando no começo e no fim          cliente, categoria
#   2  caixa inconsistente                          cliente, email, canal
#   3  acento que ora está, ora não                 cidade, categoria
#   4  a mesma UF escrita de cinco jeitos           uf
#   5  CPF com e sem máscara, e sem o zero à esq.   cpf
#   6  telefone em quatro formatos                  telefone
#   7  data em três formatos                        data_pedido
#   8  data que não existe no calendário            data_pedido
#   9  dinheiro em texto: "R$ 1.234,56"             valor
#  10  faltante disfarçado de texto: N/A, n/d, -    vários
#  11  sentinela numérica: -999                     avaliacao
#  12  número que veio como texto: "3 un"           qtd
#  13  linha inteira duplicada                      18 linhas
#  14  quase-duplicata: só o nome mudou de grafia    9 pedidos
#  15  outlier de verdade (a venda corporativa)     valor
#  16  outlier de digitação (qtd 999, prazo 180)    qtd, entrega_dias
#  17  valor negativo onde não pode haver           valor, frete
#  18  código escondido dentro de texto livre       obs

NOMES = [
    "Ana Paula Souza", "Bruno Carvalho", "Carla Menezes", "Diego Antunes",
    "Eduarda Lima", "Fábio Rezende", "Gabriela Nunes", "Henrique Vasques",
    "Isabela Moraes", "João Pedro Alves", "Karina Duarte", "Lucas Ferraz",
    "Mariana Coelho", "Nelson Batista", "Olívia Prado", "Paulo Renato Dias",
    "Queila Ramos", "Rafael Siqueira", "Sabrina Teixeira", "Thiago Barbosa",
    "Úrsula Campos", "Vinícius Rocha", "Wanessa Leal", "Yuri Fontoura",
    "Zilda Marques", "André Bittencourt", "Beatriz Kunz", "Caio Mendonça",
    "Daniela Peixoto", "Emerson Vieira", "Flávia Assunção", "Gustavo Padilha",
]

# (cidade canônica, uf canônica) — as grafias tortas entram depois
PRACAS = [
    ("São Paulo", "SP"), ("Rio de Janeiro", "RJ"), ("Porto Alegre", "RS"),
    ("Belo Horizonte", "MG"), ("Curitiba", "PR"), ("Salvador", "BA"),
    ("Fortaleza", "CE"), ("Florianópolis", "SC"), ("Goiânia", "GO"),
    ("Erechim", "RS"), ("Campinas", "SP"), ("Recife", "PE"),
]

CIDADE_TORTA = {
    "São Paulo": ["São Paulo", "SAO PAULO", "sao paulo", " São  Paulo ", "Sao Paulo"],
    "Porto Alegre": ["Porto Alegre", "PORTO ALEGRE", "porto alegre", "Pôrto Alegre"],
    "Florianópolis": ["Florianópolis", "Florianopolis", "FLORIANÓPOLIS"],
    "Goiânia": ["Goiânia", "Goiania", "GOIANIA"],
    "Belo Horizonte": ["Belo Horizonte", "BELO HORIZONTE", "belo horizonte"],
}

UF_TORTA = {
    "SP": ["SP", "sp", " SP", "São Paulo", "S.P."],
    "RS": ["RS", "rs", "RS ", "Rio Grande do Sul"],
    "RJ": ["RJ", "rj", "Rio de Janeiro"],
    "MG": ["MG", "mg", "Minas Gerais"],
    "SC": ["SC", "sc"], "PR": ["PR", "pr"], "BA": ["BA", "ba"],
    "CE": ["CE", "ce"], "GO": ["GO", "go"], "PE": ["PE", "pe"],
}

# (categoria canônica, [grafias], faixa de preço)
CATEGORIAS = [
    ("Eletrônicos", ["Eletrônicos", "eletronicos", "ELETRONICOS", " Eletrônicos ",
                     "eletrônico"], (180, 4200)),
    ("Vestuário", ["Vestuário", "vestuario", "VESTUÁRIO", "Vestuario "], (39, 480)),
    ("Casa", ["Casa", "casa", "CASA", " Casa"], (25, 1900)),
    ("Livros", ["Livros", "livros", "LIVROS", "livro"], (18, 240)),
    ("Esporte", ["Esporte", "esporte", "ESPORTE", "esportes"], (49, 1500)),
]

PRODUTOS = {
    "Eletrônicos": ["Fone Bluetooth", "Notebook 14\"", "Monitor 27\"", "Teclado mecânico",
                    "Smartphone", "Webcam HD"],
    "Vestuário": ["Camiseta básica", "Calça jeans", "Jaqueta corta-vento", "Tênis casual"],
    "Casa": ["Jogo de panelas", "Luminária de mesa", "Aspirador vertical", "Cafeteira"],
    "Livros": ["Estatística prática", "Python para dados", "Romance nacional", "Atlas escolar"],
    "Esporte": ["Halteres 10 kg", "Bicicleta ergométrica", "Bola oficial", "Colchonete"],
}

CANAIS = ["site", "SITE", "Site", "app", "APP", "loja", "Loja", "televendas"]
VAZIOS = ["", "N/A", "n/d", "-", "null", "NULL", "  "]


def cpf_sujo(n):
    """Um CPF em três formatos — e às vezes sem o zero da frente."""
    d = f"{n:011d}"
    sorte = random.random()
    if sorte < 0.45:
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"
    if sorte < 0.80:
        return d
    return d.lstrip("0") or d          # o Excel comeu o zero à esquerda


def telefone_sujo():
    ddd = random.choice([11, 21, 51, 31, 41, 48, 54])
    n = random.randint(900000000, 999999999)
    return random.choice([
        f"({ddd}) {str(n)[:5]}-{str(n)[5:]}",
        f"{ddd}{n}",
        f"+55 {ddd} {str(n)[:5]}-{str(n)[5:]}",
        f"{ddd} {n}",
    ])


def data_suja(d):
    """A mesma data em três formatos — e, de vez em quando, uma que não existe."""
    sorte = random.random()
    if sorte < 0.55:
        return d.strftime("%Y-%m-%d")
    if sorte < 0.88:
        return d.strftime("%d/%m/%Y")
    return d.strftime("%d-%m-%Y")


def para_float_br(txt):
    """Lê de volta o que dinheiro_sujo() escreveu — usado só para plantar erros."""
    t = str(txt).replace("R$", "").strip()
    if not t or not any(c.isdigit() for c in t):
        return None
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def dinheiro_sujo(v):
    """Reais com símbolo, ponto de milhar e vírgula decimal — ou já em número."""
    sorte = random.random()
    if sorte < 0.50:
        return f"R$ {v:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    if sorte < 0.80:
        return f"{v:.2f}".replace(".", ",")
    return f"{v:.2f}"


inicio = datetime(2026, 1, 5)
linhas = []
for i in range(600):
    pedido = 100_001 + i
    nome = random.choice(NOMES)
    cidade, uf = random.choice(PRACAS)
    cat, grafias, (pmin, pmax) = random.choice(CATEGORIAS)
    produto = random.choice(PRODUTOS[cat])
    data = inicio + timedelta(days=int(rng.integers(0, 210)),
                              hours=int(rng.integers(8, 22)))
    qtd = int(rng.choice([1, 1, 1, 2, 2, 3, 4, 5]))
    preco = float(np.round(rng.uniform(pmin, pmax), 2))
    valor = round(preco * qtd, 2)

    # ── as grafias tortas ────────────────────────────────────────────
    cliente = nome
    r = random.random()
    if r < 0.18:
        cliente = f"  {nome} "
    elif r < 0.30:
        cliente = nome.upper()
    elif r < 0.38:
        cliente = nome.lower()

    cidade_txt = random.choice(CIDADE_TORTA.get(cidade, [cidade]))
    uf_txt = random.choice(UF_TORTA[uf])
    cat_txt = random.choice(grafias)
    canal = random.choice(CANAIS)
    email = f"{nome.split()[0].lower()}.{nome.split()[-1].lower()}@exemplo.com.br"
    email = email.replace("á", "a").replace("é", "e").replace("í", "i")
    email = email.replace("ó", "o").replace("ú", "u").replace("ç", "c").replace("ã", "a")
    if random.random() < 0.22:
        email = email.upper()
    if random.random() < 0.06:
        email = f" {email} "

    # ── os faltantes, cada um com a sua máscara ──────────────────────
    if random.random() < 0.07:
        email = random.choice(VAZIOS)
    telefone = telefone_sujo() if random.random() > 0.09 else random.choice(VAZIOS)
    desconto = "" if random.random() < 0.11 else f"{int(rng.choice([0, 0, 0, 5, 10, 15, 20, 25]))}"
    frete = round(float(rng.uniform(0, 49)), 2) if random.random() > 0.08 else random.choice(VAZIOS)
    avaliacao = int(rng.choice([1, 2, 3, 4, 4, 5, 5, 5]))
    if random.random() < 0.10:
        avaliacao = -999                      # a sentinela do sistema legado
    elif random.random() < 0.06:
        avaliacao = ""
    entrega = int(rng.integers(1, 21))
    obs = ""
    if random.random() < 0.30:
        obs = random.choice([
            f"cupom PROMO-{random.choice(['VERAO','FRETE','ALUNO','BLACK'])}-{rng.integers(1000, 9999)}",
            "cliente pediu nota fiscal separada",
            f"trocar por PROMO-TROCA-{rng.integers(1000, 9999)} se faltar estoque",
            "entregar na portaria",
        ])

    linhas.append([
        pedido, data_suja(data), cliente, cpf_sujo(rng.integers(1, 99_999_999_999)),
        email, telefone, cidade_txt, uf_txt, cat_txt, produto,
        f"{qtd}", dinheiro_sujo(valor), desconto, frete, canal,
        avaliacao, entrega, obs,
    ])

# ── defeito 8: doze datas que não existem no calendário ──────────────
for pos in rng.choice(600, 12, replace=False):
    linhas[pos][1] = random.choice(["31/02/2026", "30/02/2026", "2026-13-05",
                                    "", "sem data", "00/00/0000"])

# ── defeito 12: quinze quantidades que vieram como texto ─────────────
for pos in rng.choice(600, 15, replace=False):
    linhas[pos][10] = random.choice(["3 un", "duas", "1 pç", "", "-"])

# ── defeito 9/17: valores impossíveis ────────────────────────────────
for pos in rng.choice(600, 6, replace=False):
    linhas[pos][11] = random.choice(["", "R$ -120,00", "-89,90", "0,00", "N/A"])

# ── defeito 15: quatro vendas corporativas — outlier legítimo ────────
for pos in rng.choice(600, 4, replace=False):
    linhas[pos][10] = str(int(rng.integers(60, 200)))
    linhas[pos][11] = dinheiro_sujo(float(rng.uniform(80_000, 260_000)))
    linhas[pos][17] = "venda corporativa - contrato anual"

# ── defeito 16: erro de digitação no teclado numérico ────────────────
for pos in rng.choice(600, 5, replace=False):
    linhas[pos][10] = "999"
for pos in rng.choice(600, 4, replace=False):
    linhas[pos][16] = int(rng.choice([180, 365, 240]))

# ── defeito 13: dezoito linhas inteiras duplicadas ───────────────────
dups = [list(linhas[p]) for p in rng.choice(600, 18, replace=False)]

# ── defeito 14: nove quase-duplicatas — só a grafia do nome mudou ────
quase = []
for p in rng.choice(600, 9, replace=False):
    copia = list(linhas[p])
    copia[2] = f"  {copia[2].strip().upper()}  "
    copia[6] = copia[6].strip().upper()
    quase.append(copia)

linhas = linhas + dups + quase
random.shuffle(linhas)

escreve("vendas-sujas.csv",
        ["id_pedido", "data_pedido", "cliente", "cpf", "email", "telefone",
         "cidade", "uf", "categoria", "produto", "qtd", "valor", "desconto_pct",
         "frete", "canal", "avaliacao", "entrega_dias", "obs"],
        linhas)


# ══════════════════════════════════════════════════════════════════════
# 2. sensores.csv — série temporal com buraco, sentinela e fuso
# ══════════════════════════════════════════════════════════════════════
# Três sensores de uma estufa, leitura a cada 15 minutos, carimbo em UTC.
# O que está plantado aqui: linhas que simplesmente não existem (o sensor
# caiu), NaN de verdade, a sentinela -999.0 do firmware antigo, picos
# impossíveis de 85 °C e uma bateria que despenca.
#
# Dois buracos do sensor A são plantados em hora fixa, porque a aula precisa
# deles para comparar ffill, bfill e interpolate lado a lado:
#   · 02/03 09:00–09:45 UTC  quatro leituras chegam VAZIAS (a linha existe)
#   · 03/03 12:00–14:45 UTC  três horas em que a linha nem existe (o sensor caiu)

partida = datetime(2026, 3, 2, 3, 0)          # 00h de Brasília, em UTC
NAN_FIXO = (datetime(2026, 3, 2, 9, 0), datetime(2026, 3, 2, 9, 45))
QUEDA_FIXA = (datetime(2026, 3, 3, 12, 0), datetime(2026, 3, 3, 14, 45))

linhas = []
for sensor, base, deriva in [("A-estufa", 24.0, 0.0), ("B-galpao", 19.5, -0.004),
                             ("C-externo", 17.0, 0.0)]:
    bateria = 100.0
    for k in range(4 * 24 * 4):               # 4 dias, de 15 em 15 minutos
        t = partida + timedelta(minutes=15 * k)
        hora = t.hour + t.minute / 60
        # ciclo diário: mais quente à tarde (o carimbo é UTC, Brasília = UTC-3)
        temp = base + 4.5 * np.sin((hora - 3 - 9) / 24 * 2 * np.pi) + deriva * k
        temp += float(rng.normal(0, 0.35))
        umid = 62 - (temp - base) * 2.4 + float(rng.normal(0, 2.5))
        bateria = max(0.0, bateria - float(rng.uniform(0.01, 0.05)))

        if sensor == "A-estufa":
            if QUEDA_FIXA[0] <= t <= QUEDA_FIXA[1]:
                continue                      # a queda de três horas
            if NAN_FIXO[0] <= t <= NAN_FIXO[1]:
                linhas.append([t.strftime("%Y-%m-%dT%H:%M:%SZ"), sensor, "",
                               f"{umid:.1f}", f"{bateria:.1f}"])
                continue                      # a linha existe, o valor não

        if rng.random() < 0.055:              # o sensor caiu: a linha nem existe
            continue
        t_txt = f"{temp:.2f}"
        if rng.random() < 0.035:
            t_txt = ""                        # veio vazio
        elif rng.random() < 0.015:
            t_txt = "-999.0"                  # a sentinela do firmware
        elif rng.random() < 0.008:
            t_txt = "85.00"                   # pico impossível
        linhas.append([t.strftime("%Y-%m-%dT%H:%M:%SZ"), sensor, t_txt,
                       f"{umid:.1f}" if rng.random() > 0.03 else "",
                       f"{bateria:.1f}"])

linhas.sort(key=lambda r: (r[0], r[1]))
escreve("sensores.csv", ["ts_utc", "sensor", "temperatura", "umidade", "bateria"], linhas)


# ══════════════════════════════════════════════════════════════════════
# 3. rh.csv — folha de pessoal: grafia, faltante e um outlier legítimo
# ══════════════════════════════════════════════════════════════════════
# Aqui o alvo são três coisas: imputar salário pela mediana do departamento
# (groupby + transform), cortar em faixas (pd.cut, pd.qcut) e discutir o
# outlier que NÃO se remove — o salário da diretoria é real.

DEPTOS = {
    "Tecnologia": (["Tecnologia", "TI", "T.I.", "tecnologia", "Tecnologia da Informação",
                    "TECNOLOGIA"], 9800, 0.42),
    "Comercial": (["Comercial", "comercial", "COMERCIAL", "Vendas"], 6200, 0.38),
    "Operações": (["Operações", "Operacoes", "OPERAÇÕES", "operações"], 4100, 0.30),
    "Financeiro": (["Financeiro", "financeiro", "FINANCEIRO", "Fin."], 7300, 0.34),
    "Pessoas": (["Pessoas", "RH", "R.H.", "Recursos Humanos"], 5600, 0.30),
}
CARGOS = ["Analista", "Analista Sênior", "Especialista", "Coordenador", "Gerente"]

linhas = []
for i in range(220):
    dep, (grafias, mediana, sigma) = random.choice(list(DEPTOS.items()))
    nome = random.choice(NOMES)
    nasc = datetime(1962, 1, 1) + timedelta(days=int(rng.integers(0, 365 * 42)))
    adm = datetime(2009, 1, 1) + timedelta(days=int(rng.integers(0, 365 * 17)))
    cargo = random.choice(CARGOS)
    # os degraus são bem separados de propósito: a aula ordena a categoria
    # `cargo` e mostra a mediana subindo degrau a degrau
    peso = {"Analista": 0.62, "Analista Sênior": 0.92, "Especialista": 1.30,
            "Coordenador": 1.85, "Gerente": 2.60}[cargo]
    salario = float(np.round(mediana * peso * np.exp(rng.normal(0, sigma)), 2))

    sal_txt = f"{salario:.2f}"
    if rng.random() < 0.14:                   # 14% sem salário informado
        sal_txt = random.choice(["", "N/A", "-"])
    nota = round(float(np.clip(rng.normal(3.6, 0.8), 1, 5)), 1)
    nota_txt = f"{nota}".replace(".", ",") if rng.random() < 0.5 else f"{nota}"
    if rng.random() < 0.09:
        nota_txt = ""
    deslig = ""
    if rng.random() < 0.17:
        d = adm + timedelta(days=int(rng.integers(200, 365 * 12)))
        if d < datetime(2026, 8, 1):
            deslig = d.strftime("%d/%m/%Y")

    linhas.append([
        f"M{4000 + i}", nome, nasc.strftime("%d/%m/%Y"), adm.strftime("%d/%m/%Y"),
        random.choice(grafias), cargo, sal_txt,
        int(rng.choice([40, 40, 40, 30, 20, 44])), nota_txt, deslig,
    ])

# a diretoria: outlier de verdade, o que a aula usa para dizer "não remova"
linhas.append(["M0001", "Roberto Salles", "12/05/1968", "03/02/2009", "Tecnologia",
               "Diretor", "182400.00", 40, "4,8", ""])
linhas.append(["M0002", "Helena Vidal", "27/09/1971", "15/07/2011", "Financeiro",
               "Diretora", "164900.00", 40, "4,6", ""])

random.shuffle(linhas)
escreve("rh.csv",
        ["matricula", "nome", "nascimento", "admissao", "departamento", "cargo",
         "salario", "horas_semana", "avaliacao", "desligamento"], linhas)

print("\nsemente", SEMENTE, "— rodar de novo produz exatamente os mesmos arquivos")


# ══════════════════════════════════════════════════════════════════════
# 4. clinica-suja.csv — o dataset do EXERCÍCIO (Lista 2)
# ══════════════════════════════════════════════════════════════════════
# Mesmas doenças do vendas-sujas, em outra roupa: o aluno não pode copiar as
# respostas da aula, mas todo defeito daqui foi visto lá.
#
#   · convênio e especialidade em várias grafias
#   · data e hora em três formatos, e algumas impossíveis
#   · dinheiro em texto brasileiro
#   · 1900-01-01 como sentinela de nascimento desconhecido
#   · -1 em dias_ate_retorno significando "não marcou"
#   · duração 0 e 999 (erro de digitação)
#   · duplicatas exatas e quase-duplicatas
#   · consultas legítimas de altíssimo valor (cirurgias) — o outlier que fica

CONVENIOS = {
    "Unimed": ["Unimed", "UNIMED", "unimed", "Uni med", " Unimed "],
    "Bradesco Saúde": ["Bradesco Saúde", "Bradesco Saude", "BRADESCO SAÚDE", "bradesco"],
    "SulAmérica": ["SulAmérica", "Sulamerica", "SUL AMÉRICA", "sul america"],
    "Particular": ["Particular", "particular", "PARTICULAR", "part."],
    "IPE Saúde": ["IPE Saúde", "IPE", "ipe saude", "I.P.E."],
}
ESPECIALIDADES = {
    "Cardiologia": (["Cardiologia", "cardiologia", "CARDIOLOGIA"], 320, 40),
    "Pediatria": (["Pediatria", "pediatria", "PEDIATRIA", "Pediatría"], 240, 30),
    "Ortopedia": (["Ortopedia", "ortopedia", "ORTOPEDIA"], 380, 30),
    "Dermatologia": (["Dermatologia", "dermatologia", "DERMATOLOGIA"], 300, 25),
    "Clínica Geral": (["Clínica Geral", "Clinica Geral", "CLÍNICA GERAL", "clinica geral"], 180, 20),
}
UNIDADES = ["Centro", "CENTRO", " Centro ", "Zona Sul", "zona sul", "ZONA SUL",
            "Barra", "barra", "Norte", "NORTE"]
STATUS = ["realizado", "Realizado", "REALIZADO", "cancelado", "Cancelado",
          "faltou", "Faltou", "FALTA", "remarcado"]

inicio = datetime(2026, 2, 2)
linhas = []
for i in range(780):
    conv, grafias_c = random.choice(list(CONVENIOS.items()))
    esp, (grafias_e, base, dur) = random.choice(list(ESPECIALIDADES.items()))
    nome = random.choice(NOMES)
    quando = inicio + timedelta(days=int(rng.integers(0, 180)),
                                hours=int(rng.integers(7, 19)),
                                minutes=int(rng.choice([0, 15, 30, 45])))
    nasc = datetime(1940, 1, 1) + timedelta(days=int(rng.integers(0, 365 * 78)))
    nasc_txt = nasc.strftime("%d/%m/%Y")
    if rng.random() < 0.06:
        nasc_txt = "01/01/1900"                 # a sentinela do cadastro antigo

    preco = float(np.round(base * np.exp(rng.normal(0, 0.22)), 2))
    duracao = int(np.clip(rng.normal(dur, 6), 10, 90))
    if rng.random() < 0.02:
        duracao = int(rng.choice([0, 999, 480]))

    st = random.choice(STATUS)
    retorno = int(rng.integers(7, 120)) if rng.random() < 0.55 else -1
    tel = telefone_sujo() if rng.random() > 0.10 else random.choice(VAZIOS)
    obs = ""
    if rng.random() < 0.22:
        obs = random.choice([
            "paciente encaminhado pela UBS",
            f"exame REQ-{rng.integers(10000, 99999)} solicitado",
            "primeira consulta",
            f"retorno de REQ-{rng.integers(10000, 99999)}",
        ])

    if rng.random() < 0.55:
        dh = quando.strftime("%Y-%m-%d %H:%M")
    elif rng.random() < 0.75:
        dh = quando.strftime("%d/%m/%Y %H:%M")
    else:
        dh = quando.strftime("%d-%m-%Y %H:%M")

    paciente = nome
    r = random.random()
    if r < 0.16:
        paciente = f"  {nome} "
    elif r < 0.28:
        paciente = nome.upper()

    linhas.append([
        f"AG{20000 + i}", paciente, nasc_txt, random.choice(grafias_c),
        random.choice(grafias_e), random.choice(UNIDADES), dh, duracao,
        dinheiro_sujo(preco) if rng.random() > 0.07 else random.choice(VAZIOS),
        st, retorno, tel, obs,
    ])

# datas impossíveis
for pos in rng.choice(780, 14, replace=False):
    linhas[pos][6] = random.choice(["31/04/2026 10:00", "2026-02-30 08:00", "",
                                    "a definir", "00/00/0000 00:00"])

# as cirurgias: outlier legítimo, com a explicação escrita na observação
for pos in rng.choice(780, 6, replace=False):
    linhas[pos][8] = dinheiro_sujo(float(rng.uniform(8_000, 32_000)))
    linhas[pos][7] = int(rng.integers(120, 300))
    linhas[pos][12] = "procedimento cirúrgico em centro cirúrgico"

# o erro de digitação: o zero a mais no teclado numérico (sem obs que explique)
for pos in rng.choice(780, 5, replace=False):
    atual = para_float_br(linhas[pos][8])
    if atual is not None:
        linhas[pos][8] = dinheiro_sujo(atual * 10)

# o impossível: valor negativo numa consulta
for pos in rng.choice(780, 4, replace=False):
    linhas[pos][8] = random.choice(["R$ -250,00", "-180,00", "-1"])

# duplicatas exatas e quase-duplicatas
dups = [list(linhas[p]) for p in rng.choice(780, 23, replace=False)]
quase = []
for p in rng.choice(780, 11, replace=False):
    c = list(linhas[p])
    c[1] = f" {c[1].strip().upper()}  "
    c[5] = c[5].strip().lower()
    quase.append(c)

linhas = linhas + dups + quase
random.shuffle(linhas)

escreve("clinica-suja.csv",
        ["id_agendamento", "paciente", "nascimento", "convenio", "especialidade",
         "unidade", "data_hora", "duracao_min", "valor_consulta", "status",
         "dias_ate_retorno", "telefone", "obs"],
        linhas)
