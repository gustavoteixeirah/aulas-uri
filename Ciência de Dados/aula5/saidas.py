"""Roda, sobre os dados desta pasta, todos os exemplos projetados nos slides.

Uso:  python saidas.py

Cada bloco abaixo é exatamente o que está na tela — comando e saída. Se um
arquivo ou a versão do pandas mudar e algum número sair diferente, é aqui que
aparece primeiro. Ao final, um conjunto de asserções confere os números que os
slides afirmam em negrito.
"""
import contextlib
import io
import os
import re

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(BASE, "dados") + os.sep


def numero_do_slide():
    """chave -> número, lido do data-nb do index.html (a mesma fonte do caderno)."""
    html = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
    secoes = re.findall(r'<section class="slide[^"]*"([^>]*)>', html)
    mapa = {}
    for i, attrs in enumerate(secoes, 1):
        ch = re.search(r'data-nb="([^"]+)"', attrs)
        if ch:
            mapa[ch.group(1)] = i
    return mapa


SLIDE = numero_do_slide()

NULOS = ["", " ", "  ", "-", "n/d", "sem data", "?", "00/00/0000"]

pd.set_option("display.width", 96)
pd.set_option("display.max_columns", 20)


def chave(s):
    return (s.astype("str")
             .str.normalize("NFKD").str.encode("ascii", "ignore").str.decode("ascii")
             .str.replace(r"\s+", " ", regex=True)
             .str.strip().str.lower())


def para_real(s):
    t = s.astype("str").str.replace(r"[R$\s]", "", regex=True)
    tem_virgula = t.str.contains(",", na=False)
    t = t.mask(tem_virgula, t.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(t, errors="coerce")


def para_data(s, formatos=("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")):
    saida = pd.Series(pd.NaT, index=s.index, dtype="datetime64[us]")
    for f in formatos:
        pendente = saida.isna() & s.notna()
        if not pendente.any():
            break
        saida[pendente] = pd.to_datetime(s[pendente], format=f, errors="coerce")
    return saida


ns = {"pd": pd, "np": np, "chave": chave, "para_real": para_real, "para_data": para_data}

exec(f'''
bruto   = pd.read_csv(r"{D}vendas-sujas.csv")
df    = pd.read_csv(r"{D}vendas-sujas.csv", na_values={NULOS!r})
titanic   = pd.read_csv(r"{D}titanic.csv")
rh    = pd.read_csv(r"{D}rh.csv", na_values={NULOS!r})
taxis = pd.read_csv(r"{D}taxis.csv", parse_dates=["pickup", "dropoff"])
sens  = pd.read_csv(r"{D}sensores.csv", parse_dates=["ts_utc"])
a     = sens[sens["sensor"] == "A-estufa"].set_index("ts_utc").sort_index()
FALTANTES_CRU, FALTANTES_NA = bruto.isna().sum().sum(), df.isna().sum().sum()
df["avaliacao_original"] = df["avaliacao"]
''', ns)

# (slide, [(tipo, código)]) — expr mostra o valor, stmt só executa, print captura
SLIDES = [
    (("ler-errado", "Ler errado"), [
        ("expr", 'bruto.dtypes.head(6)')]),
    (("27-estados", "27 estados"), [
        ("expr", 'bruto["uf"].nunique()'),
        ("expr", 'bruto["uf"].value_counts().head(6)')]),
    (("disfarce", "O disfarce"), [
        ("expr", 'bruto["frete"].dtype'),
        ("expr", 'bruto["frete"].isna().sum()'),
        ("expr", 'bruto["frete"].isin(["-", "n/d", "  "]).sum()')]),
    (("na-values", "na_values"), [
        ("print", 'print("sem na_values ·", bruto.isna().sum().sum())'),
        ("print", 'print("com na_values ·", df.isna().sum().sum())')]),
    (("sentinela", "A sentinela"), [
        ("expr", 'df["avaliacao"].value_counts().sort_index()'),
        ("expr", 'round(df["avaliacao"].mean(), 2)'),
        ("stmt", 'df["avaliacao"] = df["avaliacao"].replace(-999, np.nan)'),
        ("expr", 'round(df["avaliacao"].mean(), 2)')]),
    (("dropna", "dropna"), [
        ("expr", 'titanic.shape'),
        ("expr", 'titanic.dropna().shape'),
        ("expr", 'titanic.dropna(subset=["Embarked"]).shape'),
        ("expr", 'titanic.dropna(thresh=11).shape')]),
    (("media-ou-mediana", "Média ou mediana"), [
        ("print", 'print(f\'Age  · média {titanic["Age"].mean():.2f} · mediana {titanic["Age"].median():.2f} · skew {titanic["Age"].skew():.2f}\')'),
        ("print", 'print(f\'salário · média {rh["salario"].mean():,.2f} · mediana {rh["salario"].median():,.2f} · skew {rh["salario"].skew():.2f}\')')]),
    (("linha-inexistente", "A linha que não existe"), [
        ("expr", 'a.index.to_series().diff().value_counts()'),
        ("expr", 'a["temperatura"].replace(-999.0, np.nan).isna().sum()'),
        ("expr", 'a["temperatura"].replace(-999.0, np.nan).asfreq("15min").isna().sum()')]),
    (("imputar-grupo", "Imputar por grupo"), [
        ("expr", 'titanic.groupby(["Pclass", "Sex"])["Age"].median().unstack()'),
        ("expr", 'round(titanic["Age"].median(), 1)')]),
    (("conta-imputacao", "A conta da imputação"), [
        ("stmt", 'porgrupo = titanic.groupby(["Pclass", "Sex"])["Age"].transform("median")'),
        ("print", 'print(f\'desvio: original {titanic["Age"].std():.2f} · geral {titanic["Age"].fillna(titanic["Age"].median()).std():.2f} · grupo {titanic["Age"].fillna(porgrupo).std():.2f}\')')]),
    (("evidencia", "Guarde a evidência"), [
        ("expr", 'titanic.groupby(titanic["Age"].isna())[["Survived", "Pclass"]].mean().round(3)')]),
    (("duplicated", "duplicated"), [
        ("expr", 'df.duplicated().sum()'),
        ("expr", 'df.duplicated(keep=False).sum()'),
        ("expr", 'df.drop_duplicates().shape')]),
    (("grao", "O grão da tabela"), [
        ("stmt", 'sem_dup = df.drop_duplicates()'),
        ("expr", 'sem_dup["id_pedido"].nunique()'),
        ("stmt", 'limpo = sem_dup.assign(_k=chave(sem_dup["cliente"])).drop_duplicates(subset=["id_pedido", "_k", "produto"]).drop(columns="_k")'),
        ("expr", 'limpo.shape')]),
    (("dup-legitima", "A que não é erro"), [
        ("expr", 'taxis.duplicated(["distance", "fare", "tip", "payment"]).sum()'),
        ("expr", 'taxis.duplicated().sum()')]),
    (("astype-tonumeric", "astype × to_numeric"), [
        ("stmt", 'qtd_num = pd.to_numeric(limpo["qtd"], errors="coerce")'),
        ("expr", '(qtd_num.isna() & limpo["qtd"].notna()).sum()'),
        ("expr", 'limpo.loc[qtd_num.isna() & limpo["qtd"].notna(), "qtd"].tolist()'),
        ("stmt", 'limpo["qtd"] = qtd_num.astype("Int64")')]),
    (("dinheiro", "Dinheiro brasileiro"), [
        ("stmt", 'ex = pd.Series(["R$ 1.234,56", "977,76", "1004.84"])'),
        ("expr", 'pd.to_numeric(ex.str.replace("R$ ", "", regex=False).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)).tolist()'),
        ("expr", 'para_real(ex).tolist()'),
        ("stmt", 'limpo["valor"] = para_real(limpo["valor"])')]),
    (("category", "category"), [
        ("stmt", 'g = pd.Series(np.random.default_rng(1).choice(limpo["produto"].unique(), 6_000_000))'),
        ("print", 'print(f"str      {g.memory_usage(deep=True)/1024**2:8.1f} MB")'),
        ("print", 'print(f"category {g.astype(\'category\').memory_usage(deep=True)/1024**2:8.1f} MB")'),
        ("stmt", 'del g')]),
    (("category-ordem", "category com ordem"), [
        ("stmt", 'NIVEIS = ["Analista", "Analista Sênior", "Especialista", "Coordenador", "Gerente", "Diretor", "Diretora"]'),
        ("stmt", 'rh["cargo"] = pd.Categorical(rh["cargo"], NIVEIS, ordered=True)'),
        ("expr", 'int((rh["cargo"] > "Especialista").sum())'),
        ("expr", 'rh.groupby("cargo", observed=True)["salario"].median().round(0)')]),
    (("ato1", "Ato 1 — o palpite"), [
        ("expr", 'pd.to_datetime(limpo["data_pedido"], errors="coerce").isna().sum()')]),
    (("ato2", "Ato 2 — mixed"), [
        ("stmt", 'misto = pd.to_datetime(limpo["data_pedido"], format="mixed", dayfirst=True, errors="coerce")'),
        ("expr", 'misto.isna().sum()'),
        ("expr", '(misto.min().date(), misto.max().date())')]),
    (("ato3", "Ato 3 — o estrago"), [
        ("stmt", 'cascata = para_data(limpo["data_pedido"])'),
        ("expr", 'cascata.isna().sum()'),
        ("expr", 'int(((misto != cascata) & misto.notna() & cascata.notna()).sum())'),
        ("expr", '(cascata.min().date(), cascata.max().date())'),
        ("stmt", 'limpo["data_pedido"] = cascata')]),
    (("receita-datas", "A receita segura"), [
        ("expr", 'int((~misto.between("2026-01-01", "2026-08-28") & misto.notna()).sum())')]),
    (("acessador-dt", "O acessador .dt"), [
        ("expr", 'limpo.groupby(limpo["data_pedido"].dt.day_name())["valor"].sum().nlargest(3).round(2)')]),
    (("fuso", "Fuso horário"), [
        ("stmt", 'temp = a["temperatura"].replace(-999.0, np.nan).where(lambda s: s < 40)'),
        ("expr", 'int(temp.groupby(temp.index.hour).mean().idxmax())'),
        ("stmt", 'loc = temp.tz_convert("America/Sao_Paulo")'),
        ("expr", 'int(loc.groupby(loc.index.hour).mean().idxmax())')]),
    (("uf-27-10", "De 27 para 10"), [
        ("stmt", 'MAPA_UF = {"sao paulo": "SP", "s.p.": "SP", "rio de janeiro": "RJ", "rio grande do sul": "RS", "minas gerais": "MG"}'),
        ("stmt", 'limpo["uf"] = chave(limpo["uf"]).replace(MAPA_UF).str.upper()'),
        ("expr", 'limpo["uf"].nunique()'),
        ("expr", 'limpo["uf"].value_counts()')]),
    (("map-replace", "map × replace"), [
        ("expr", 'rh["departamento"].nunique()')]),
    (("zfill", "zfill"), [
        ("stmt", 'cpf = limpo["cpf"].astype("str").str.replace(r"\\D", "", regex=True)'),
        ("expr", 'cpf.str.len().value_counts()'),
        ("expr", 'cpf.str.zfill(11).str.len().value_counts()')]),
    (("where-select", "np.where e np.select"), [
        ("stmt", 'limpo["frete"] = limpo["frete"].fillna(0); limpo["desconto_pct"] = limpo["desconto_pct"].fillna(0)'),
        ("stmt", 'v = limpo["valor"] * (1 - limpo["desconto_pct"] / 100) + limpo["frete"]'),
        ("stmt", 'faixa = np.select([v >= 50_000, v >= 5_000, v >= 500, v >= 0], ["corporativo", "alto", "médio", "baixo"], default="a conferir")'),
        ("expr", 'pd.Series(faixa).value_counts()')]),
    (("apply-lento", "apply é lento"), [
        ("stmt", 'import time'),
        ("stmt", 'grande = pd.concat([limpo] * 200, ignore_index=True)'),
        ("print", 'print(f"{len(grande):,} linhas")'),
        ("print", '''
for nome, f in [("apply(axis=1)", lambda: grande.apply(lambda r: r["valor"] * 1.1, axis=1)),
                ("apply na coluna", lambda: grande["valor"].apply(lambda x: x * 1.1)),
                ("vetorizado", lambda: grande["valor"] * 1.1)]:
    t = time.perf_counter()
    for _ in range(5):
        f()
    print(f"  {nome:<18} {(time.perf_counter()-t)/5*1000:7.2f} ms")
'''.strip()),
        ("stmt", 'del grande')]),
    (("cut-qcut", "cut × qcut"), [
        ("expr", 'pd.cut(rh["salario"], 4).value_counts().sort_index().tolist()'),
        ("expr", 'pd.qcut(rh["salario"], 4).value_counts().sort_index().tolist()')]),
    (("olhe-antes", "Olhe antes"), [
        ("expr", 'v.quantile([.25, .50, .75, .95, .99, 1]).round(2)')]),
    (("zscore", "z-score e MAD"), [
        ("stmt", 'z = (v - v.mean()) / v.std()'),
        ("stmt", 'mad = (v - v.median()).abs().median(); zr = 0.6745 * (v - v.median()) / mad'),
        ("print", 'print("z comum   · |z|>3:", int((z.abs() > 3).sum()))'),
        ("print", 'print("z robusto · |z|>3:", int((zr.abs() > 3).sum()))'),
        ("print", 'print("a maior venda: z", round(z.max(), 2), "· z robusto", round(zr.max(), 2))')]),
    (("tres-tipos", "Os três tipos"), [
        ("stmt", 'corp = limpo["obs"].str.contains("corporativa", na=False)'),
        ("print", 'print(int(corp.sum()), "pedidos ·", f"{v[corp].sum()/v.sum()*100:.1f}% do faturamento")')]),
    (("preco-decisao", "O preço da decisão"), [
        ("stmt", 'q1, q3 = v.quantile(.25), v.quantile(.75); alto = q3 + 1.5 * (q3 - q1); fora = (v < q1 - 1.5*(q3-q1)) | (v > alto)'),
        ("expr", '''pd.DataFrame({
    "pedidos": [v.size, v[~fora].size, v.size, v[v > 0].size],
    "média":   [v.mean(), v[~fora].mean(), v.clip(upper=alto).mean(), v[v > 0].mean()],
    "total":   [v.sum(), v[~fora].sum(), v.clip(upper=alto).sum(), v[v > 0].sum()],
}, index=["tudo", "removendo pelo IQR", "clip no limite", "só positivos"]).round(2)''')]),
]


def roda(tipo, codigo):
    if tipo == "stmt":
        exec(codigo, ns)
        return None
    if tipo == "print":
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(codigo, ns)
        return buf.getvalue().rstrip("\n")
    return repr(eval(codigo, ns))


print(f"pandas {pd.__version__} · numpy {np.__version__}\n")
for (chave, titulo), passos in SLIDES:
    slide = f"Slide {SLIDE[chave]:>2} · {titulo}"
    print(f"── {slide} " + "─" * max(0, 60 - len(slide)))
    for tipo, codigo in passos:
        for i, linha in enumerate(codigo.split("\n")):
            print((">>> " if i == 0 else "... ") + linha)
        saida = roda(tipo, codigo)
        if saida is not None:
            print(saida)
    print()


# ── as afirmações que os slides fazem em negrito ─────────────────────────
print("═" * 62)
print("CONFERINDO OS NÚMEROS QUE OS SLIDES AFIRMAM\n")

v = ns["v"]
verificacoes = [
    ("uf tem 27 grafias", ns["bruto"]["uf"].nunique() == 27),
    ("frete tem 17 traços", int(ns["bruto"]["frete"].isin(["-", "n/d", "  "]).sum()) == 17),
    ("624 → 677 faltantes", (ns["FALTANTES_CRU"], ns["FALTANTES_NA"]) == (624, 677)),
    ("média com sentinela = −120,88", round(ns["df"]["avaliacao_original"].mean(), 2) == -120.88),
    ("dropna() deixa 183 de 891", len(ns["titanic"].dropna()) == 183),
    ("skew do salário = 7,16", round(ns["rh"]["salario"].skew(), 2) == 7.16),
    ("sobrevivência 40,6% × 29,4%",
     ns["titanic"].groupby(ns["titanic"]["Age"].isna())["Survived"].mean().round(3).tolist() == [0.406, 0.294]),
    ("18 linhas idênticas", int(ns["df"].duplicated().sum()) == 18),
    ("627 → 609 → 600", len(ns["limpo"]) == 600 and ns["limpo"]["id_pedido"].is_unique),
    ("935 falsas duplicatas nos táxis",
     int(ns["taxis"].duplicated(["distance", "fare", "tip", "payment"]).sum()) == 935),
    ("palpite automático perde 534", int(ns["misto"].isna().sum()) == 12),
    ("112 datas trocadas de mês",
     int(((ns["misto"] != ns["cascata"]) & ns["misto"].notna() & ns["cascata"].notna()).sum()) == 112),
    ("a faixa pega 30 delas",
     int((~ns["misto"].between("2026-01-01", "2026-08-28") & ns["misto"].notna()).sum()) == 30),
    ("pico 18h UTC = 15h Brasília",
     (int(ns["temp"].groupby(ns["temp"].index.hour).mean().idxmax()),
      int(ns["loc"].groupby(ns["loc"].index.hour).mean().idxmax())) == (18, 15)),
    ("de 27 UFs para 10", ns["limpo"]["uf"].nunique() == 10),
    ("22 grafias de departamento", ns["rh"]["departamento"].nunique() == 22),
    ("11 CPFs de 10 dígitos", int((ns["cpf"].str.len() == 10).sum()) == 11),
    ("cut = 183·3·0·2", pd.cut(ns["rh"]["salario"], 4).value_counts().sort_index().tolist() == [183, 3, 0, 2]),
    ("corporativas = 30,7% do faturamento",
     round(v[ns["corp"]].sum() / v.sum() * 100, 1) == 30.7),
    ("total 1.662.243 × 703.001",
     (round(v.sum()), round(v[~ns["fora"]].sum())) == (1662243, 703001)),
]

erros = 0
for texto, ok in verificacoes:
    print(f"  {'✓' if ok else '✗ FALHOU'}  {texto}")
    erros += not ok
print(f"\n{len(verificacoes) - erros} de {len(verificacoes)} conferem.")
