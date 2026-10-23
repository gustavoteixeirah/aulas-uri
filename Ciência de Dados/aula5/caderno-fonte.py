# %% [markdown]
# # Aula 05 — caderno de acompanhamento
#
# **Limpeza e transformação · Programação para Ciência de Dados · 2026.1**
#
# Este caderno acompanha os slides **na mesma numeração**. O rodapé da tela
# mostra em que slide a aula está; procure aqui pela seção de mesmo número.
#
# ```
#  ▸ Slide 18 · A sentinela      ←  o 18 é o número que está no rodapé do slide
# ```
#
# Nem todo slide tem célula — capa, divisórias e os de conceito puro ficam de
# fora, e a numeração pula. Os que **têm** estão marcados com `▸ caderno` no
# canto superior direito da tela.
#
# **Rode na ordem.** As células dependem das anteriores: se pular uma, a
# seguinte reclama de um nome que não existe. Se você chegou atrasado, use
# *Run → Run All Above* e siga daí.
#
# No fim há um **apêndice** com o que não coube em slide — para depois da aula.
#
# {{INDICE}}

# %% [markdown]
# ---
# ## Preparação
#
# Rode esta antes de a aula começar.

# %%
import unicodedata
import numpy as np
import pandas as pd

pd.set_option("display.width", 110)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", lambda v: f"{v:,.2f}")

print("pandas", pd.__version__, "· numpy", np.__version__)

# %% [markdown]
# ---
# ## {{datasets}} · Os cinco datasets
#
# Os cinco arquivos da aula, ainda brutos.

# %%
titanic = pd.read_csv("dados/titanic.csv")
taxis = pd.read_csv("dados/taxis.csv", parse_dates=["pickup", "dropoff"])
sensores = pd.read_csv("dados/sensores.csv", parse_dates=["ts_utc"])

for nome, d in [("vendas-sujas", pd.read_csv("dados/vendas-sujas.csv")),
                ("sensores", sensores), ("rh", pd.read_csv("dados/rh.csv")),
                ("titanic", titanic), ("taxis", taxis)]:
    print(f"{nome:<14} {d.shape[0]:>5} linhas × {d.shape[1]:>2} colunas")

# %% [markdown]
# ---
# ## {{ler-errado}} · Passo 1 — o sintoma
#
# O `dtypes` diz **que** há um problema. Não diz qual, nem onde.

# %%
bruto = pd.read_csv("dados/vendas-sujas.csv")
bruto.dtypes

# %% [markdown]
# ---
# ## {{culpado}} · Passo 2 — olhar os valores
#
# Antes de qualquer conversão: **veja o dado com os próprios olhos.**

# %%
for col in ["valor", "data_pedido", "qtd", "frete"]:
    print(f"{col:<13}", list(bruto[col].astype("str").unique()[:5]))

# %% [markdown]
# ---
# ## {{contar-culpados}} · Passo 3 — quantos são
#
# O mesmo comando, dois diagnósticos: exceção a consertar, ou formato a converter.

# %%
for col in ["qtd", "frete", "valor"]:
    culpados = bruto[col][pd.to_numeric(bruto[col], errors="coerce").isna() & bruto[col].notna()]
    print(f"\n{col} — {len(culpados)} de {len(bruto)} não viram número:")
    print(culpados.value_counts().head(4).to_string())

# %% [markdown]
# ---
# ## {{describe-denuncia}} · Passo 4 — o que o tipo esconde
#
# `avaliacao` é `float64` e parece saudável. **Leia o `min` e o `max`.**

# %%
bruto.describe().round(2)

# %% [markdown]
# ---
# ## {{raio-x}} · O raio-x
#
# A função que vai ser usada o caderno inteiro.

# %%
def raio_x(df):
    """Uma linha por coluna: tipo, faltantes, distintos, exemplo e memória."""
    return pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "faltam": df.isna().sum(),
        "faltam_%": (df.isna().mean() * 100).round(1),
        "distintos": df.nunique(dropna=True),
        "exemplo": [df[c].dropna().iloc[0] if df[c].notna().any() else None
                    for c in df.columns],
        "memória_KB": (df.memory_usage(deep=True)[1:] / 1024).round(1),
    })


raio_x(bruto)

# %% [markdown]
# ---
# ## {{27-estados}} · Vinte e sete estados
#
# A loja vende em dez. Cada grafia diferente é um "estado" novo para o computador.

# %%
print("linhas:", len(bruto), "· duplicadas:", bruto.duplicated().sum())
print("valores distintos de uf:", bruto["uf"].nunique())
bruto["uf"].value_counts().head(8)

# %% [markdown]
# ---
# ## {{caras-do-vazio}} · As quatro caras do vazio
#
# `NaN`, `None`, `NaT` e `<NA>` — quatro nomes, uma ideia. O `isna()` vê todos.

# %%
vazios = pd.DataFrame({
    "numero": [1.0, np.nan, 3.0],
    "texto": ["a", None, "c"],
    "data": pd.to_datetime(["2026-01-01", None, "2026-03-01"]),
    "inteiro": pd.array([1, None, 3], dtype="Int64"),
})
print(vazios.dtypes.to_dict())
vazios

# %%
vazios.isna()

# %% [markdown]
# ---
# ## {{nan-nao-e-nan}} · NaN não é igual a NaN
#
# O filtro errado **não dá erro** — devolve vazio, e você conclui que está tudo bem.

# %%
print("np.nan == np.nan →", np.nan == np.nan)
print("\nfiltrando com == :")
print(bruto[bruto["valor"] == np.nan].shape)
print("\nfiltrando com isna():")
print(bruto[bruto["valor"].isna()].shape)

# %% [markdown]
# ---
# ## {{disfarce}} · O disfarce
#
# Dezessete traços derrubam a coluna inteira para texto.

# %%
for col in ["email", "telefone", "frete", "qtd", "data_pedido"]:
    disfarce = bruto[col].astype("str").str.strip().isin(["", "-", "n/d", "sem data", "?"])
    print(f"{col:<13} tipo {str(bruto[col].dtype):<6} · {bruto[col].isna().sum():>3} vazios "
          f"reconhecidos · {disfarce.sum():>3} disfarçados")

# %% [markdown]
# ---
# ## {{na-values}} · na_values
#
# O Pandas já reconhece uma lista própria; `na_values` acrescenta a da sua casa.

# %%
from pandas.io.parsers.readers import STR_NA_VALUES
print("o que o Pandas já reconhece:", sorted(STR_NA_VALUES))

# %%
NULOS = ["", " ", "  ", "-", "n/d", "sem data", "?", "00/00/0000"]

df = pd.read_csv("dados/vendas-sujas.csv", na_values=NULOS)
print("sem na_values ·", bruto.isna().sum().sum(), "faltantes")
print("com na_values ·", df.isna().sum().sum(), "faltantes")
raio_x(df)[["tipo", "faltam", "faltam_%"]]

# %% [markdown]
# ---
# ## {{sentinela}} · A sentinela
#
# Uma nota média de −120,88 numa escala de 1 a 5.

# %%
print(df["avaliacao"].value_counts(dropna=False).sort_index())
print("\nmédia com a sentinela:", round(df["avaliacao"].mean(), 2))
print("média sem a sentinela:", round(df["avaliacao"].replace(-999, np.nan).mean(), 2))

# %%
df["avaliacao"] = df["avaliacao"].replace(-999, np.nan)
df["avaliacao"].describe()

# %% [markdown]
# ---
# ## {{onde-buracos}} · Onde estão os buracos
#
# Os números do mapa de faltantes projetado na tela.

# %%
(titanic.isna().sum().to_frame("faltam")
    .assign(**{"%": (titanic.isna().mean() * 100).round(1)})
    .query("faltam > 0"))

# %% [markdown]
# ---
# ## {{dropna}} · dropna
#
# Sem argumento nenhum, ele apaga 79% da tabela.

# %%
print("original           ", titanic.shape)
print("dropna()           ", titanic.dropna().shape)
print("subset=['Embarked']", titanic.dropna(subset=["Embarked"]).shape)
print("how='all'          ", titanic.dropna(how="all").shape)
print("thresh=11          ", titanic.dropna(thresh=11).shape)
print("axis=1             ", titanic.dropna(axis=1).shape)

# %% [markdown]
# ---
# ## {{fillna}} · fillna
#
# Uma regra declarada por coluna. Um `fillna(0)` faria cabine virar zero.

# %%
amostra = titanic.loc[[5, 17, 19, 26, 28], ["Name", "Age", "Embarked", "Cabin"]]
amostra

# %%
amostra.fillna({"Age": titanic["Age"].median(), "Embarked": "S", "Cabin": "sem registro"})

# %% [markdown]
# ---
# ## {{media-ou-mediana}} · Média ou mediana
#
# O critério é a assimetria. Com `|skew| > 1`, use a mediana.

# %%
for nome, s in [("Titanic · Age", titanic["Age"]), ("Titanic · Fare", titanic["Fare"])]:
    print(f"{nome:<16} média {s.mean():>8.2f} · mediana {s.median():>8.2f} · skew {s.skew():>5.2f}")

# %%
rh = pd.read_csv("dados/rh.csv", na_values=NULOS)
print(f"salários informados: {rh['salario'].notna().sum()} · em branco: {rh['salario'].isna().sum()}")
print(f"média {rh['salario'].mean():,.2f} · mediana {rh['salario'].median():,.2f} · skew {rh['salario'].skew():.2f}")

pd.DataFrame({
    "original": rh["salario"].describe(),
    "fillna(média)": rh["salario"].fillna(rh["salario"].mean()).describe(),
    "fillna(mediana)": rh["salario"].fillna(rh["salario"].median()).describe(),
})

# %% [markdown]
# ---
# ## {{ffill}} · ffill, bfill e interpolate
#
# Quatro respostas para o mesmo buraco de uma hora. Repare no `-999` sobrevivendo.

# %%
a = sensores[sensores["sensor"] == "A-estufa"].set_index("ts_utc").sort_index()
janela = a.loc["2026-03-02 08:30":"2026-03-02 10:15", "temperatura"]

pd.DataFrame({
    "original": janela,
    "ffill": janela.ffill(),
    "bfill": janela.bfill(),
    "interpolate": janela.interpolate(),
    "média_do_dia": janela.fillna(round(a["temperatura"].mean(), 2)),
})

# %% [markdown]
# ---
# ## {{sensor-caiu}} · O sensor caiu por três horas
#
# O `limit=` é o freio de mão: se o buraco é grande, ele **continua** buraco.

# %%
temp = a["temperatura"].replace(-999.0, np.nan)
print("sem limite     · sobra NaN:", temp.ffill().isna().sum())
print("ffill(limit=1) · sobra NaN:", temp.ffill(limit=1).isna().sum())
print("ffill(limit=2) · sobra NaN:", temp.ffill(limit=2).isna().sum())

# %% [markdown]
# ---
# ## {{linha-inexistente}} · A linha que não existe
#
# Se o sensor caiu, não há `NaN` — não há linha. O `asfreq` revela o silêncio.

# %%
print(a.index.to_series().diff().value_counts().to_frame("quantas vezes"))
print("\nNaN antes do asfreq: ", temp.isna().sum())
print("NaN depois do asfreq:", temp.asfreq("15min").isna().sum())
temp.asfreq("15min").loc["2026-03-03 11:30":"2026-03-03 15:15"]

# %% [markdown]
# ---
# ## {{imputar-grupo}} · Imputar por grupo
#
# `transform` devolve a mediana do grupo de cada linha, do tamanho da coluna.

# %%
titanic.groupby(["Pclass", "Sex"])["Age"].median().unstack()

# %%
por_grupo = titanic.groupby(["Pclass", "Sex"])["Age"].transform("median")

comp = titanic.loc[titanic["Age"].isna(), ["Pclass", "Sex"]].copy()
comp["mediana_geral"] = titanic["Age"].median()
comp["mediana_do_grupo"] = por_grupo[titanic["Age"].isna()]
comp.head(8)

# %% [markdown]
# ---
# ## {{conta-imputacao}} · A conta da imputação
#
# Toda imputação encolhe a variação. Não é errado — é uma consequência.

# %%
titanic["Age_imputada"] = titanic["Age"].fillna(por_grupo)
geral = titanic["Age"].fillna(titanic["Age"].median())

print(f"original     · média {titanic['Age'].mean():.2f} · desvio {titanic['Age'].std():.2f} · faltam {titanic['Age'].isna().sum()}")
print(f"mediana geral· média {geral.mean():.2f} · desvio {geral.std():.2f} · faltam 0")
print(f"por grupo    · média {titanic['Age_imputada'].mean():.2f} · desvio {titanic['Age_imputada'].std():.2f} · faltam 0")

# %% [markdown]
# ---
# ## {{evidencia}} · Guarde a evidência
#
# Quem não tem idade registrada sobreviveu menos. O buraco carregava informação.

# %%
titanic["idade_era_faltante"] = titanic["Age"].isna()
(titanic.groupby("idade_era_faltante")
    .agg(pessoas=("Survived", "size"),
         sobreviveram=("Survived", "mean"),
         tarifa_média=("Fare", "mean"),
         classe_média=("Pclass", "mean")).round(3))

# %% [markdown]
# ---
# ## {{duplicated}} · duplicated
#
# `keep=False` é para olhar; `keep="first"` é para remover.

# %%
print("keep='first' (padrão) →", df.duplicated().sum())
print("keep='last'           →", df.duplicated(keep="last").sum())
print("keep=False            →", df.duplicated(keep=False).sum())
df[df.duplicated(keep=False)].sort_values("id_pedido")[
    ["id_pedido", "cliente", "cidade", "valor"]].head(6)

# %% [markdown]
# ---
# ## {{grao}} · O grão da tabela
#
# 609 linhas para 600 pedidos. Sobram nove.

# %%
sem_dup = df.drop_duplicates()
print(len(df), "→", len(sem_dup), "linhas")
print("pedidos distintos:", sem_dup["id_pedido"].nunique())

repetidos = sem_dup[sem_dup.duplicated("id_pedido", keep=False)].sort_values("id_pedido")
repetidos[["id_pedido", "cliente", "cidade", "valor"]].head(6)

# %% [markdown]
# ---
# ## {{quase-duplicata}} · A quase-duplicata
#
# Comparar por uma **chave normalizada**, não pelo texto bruto.

# %%
def chave(s):
    """Texto reduzido ao essencial: sem acento, sem espaço extra, minúsculo."""
    return (s.astype("str")
             .str.normalize("NFKD").str.encode("ascii", "ignore").str.decode("ascii")
             .str.replace(r"\s+", " ", regex=True)
             .str.strip().str.lower())


limpo = sem_dup.assign(_k=chave(sem_dup["cliente"]))
limpo = limpo.drop_duplicates(subset=["id_pedido", "_k", "produto"]).drop(columns="_k")

print(f"627 → {len(sem_dup)} → {len(limpo)} linhas")
print("uma linha por pedido?", limpo["id_pedido"].is_unique)

# %% [markdown]
# ---
# ## {{dup-legitima}} · A duplicata que não é erro
#
# 935 "duplicatas" que são corridas distintas — o horário prova.

# %%
colunas_valor = ["distance", "fare", "tip", "payment"]
print("olhando só", colunas_valor, "→", taxis.duplicated(colunas_valor).sum())
print("olhando a linha inteira      →", taxis.duplicated().sum())
taxis[taxis.duplicated(colunas_valor, keep=False)].sort_values("fare")[
    ["pickup", "distance", "fare", "tip", "payment"]].head(5)

# %% [markdown]
# ---
# ## {{tipos}} · int64 e Int64
#
# O minúsculo não representa ausência: um buraco e a coluna vira `float64`.

# %%
print(pd.Series([1, 2, None]).dtype, "←  int virou float por causa do None")
print(pd.Series([1, 2, None], dtype="Int64").dtype, "  ←  continua inteiro, com <NA>")
pd.Series([1, 2, None], dtype="Int64")

# %% [markdown]
# ---
# ## {{astype-tonumeric}} · astype × to_numeric
#
# O rígido falha; o tolerante converte e **você conta** quem ficou pelo caminho.

# %%
for descrição, serie in [("com NaN na coluna", limpo["qtd"]),
                         ("sem NaN, com texto", limpo["qtd"].dropna())]:
    try:
        serie.astype("int")
        print(f"{descrição:<20} → converteu")
    except Exception as e:
        print(f"{descrição:<20} → {type(e).__name__}: {e}")

# %%
qtd_num = pd.to_numeric(limpo["qtd"], errors="coerce")
virou_nan = qtd_num.isna() & limpo["qtd"].notna()

print("valores que não viraram número:", virou_nan.sum())
print(limpo.loc[virou_nan, ["id_pedido", "qtd"]].to_string(index=False))

limpo["qtd"] = qtd_num.astype("Int64")

# %% [markdown]
# ---
# ## {{dinheiro}} · Dinheiro brasileiro
#
# A receita ingênua multiplica por cem quem já vinha com ponto decimal.

# %%
exemplos = pd.Series(["R$ 1.234,56", "977,76", "1004.84", "R$ -120,00"])
ingenuo = (exemplos.str.replace("R$ ", "", regex=False)
                   .str.replace(".", "", regex=False)
                   .str.replace(",", ".", regex=False))
pd.DataFrame({"bruto": exemplos, "receita ingênua": pd.to_numeric(ingenuo, errors="coerce")})

# %%
def para_real(s):
    """Converte dinheiro em texto para float, tolerando os dois padrões."""
    t = s.astype("str").str.replace(r"[R$\s]", "", regex=True)
    tem_virgula = t.str.contains(",", na=False)
    t = t.mask(tem_virgula, t.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(t, errors="coerce")


pd.DataFrame({"bruto": exemplos, "receita segura": para_real(exemplos)})

# %%
limpo["valor"] = para_real(limpo["valor"])
limpo["valor"].describe()

# %% [markdown]
# ---
# ## {{category}} · category
#
# 422,9 MB contra 5,7 MB. Em 600 linhas não muda nada; em seis milhões, muda tudo.

# %%
grande = pd.Series(np.random.default_rng(1).choice(limpo["produto"].unique(), 6_000_000))
print(f"6 milhões como str:      {grande.memory_usage(deep=True)/1024**2:8.1f} MB")
print(f"6 milhões como category: {grande.astype('category').memory_usage(deep=True)/1024**2:8.1f} MB")
del grande

# %% [markdown]
# ---
# ## {{category-ordem}} · category com ordem
#
# Sem a ordem declarada, o `groupby` devolveria alfabético.

# %%
NIVEIS = ["Analista", "Analista Sênior", "Especialista", "Coordenador",
          "Gerente", "Diretor", "Diretora"]
rh["cargo"] = pd.Categorical(rh["cargo"], categories=NIVEIS, ordered=True)

print("acima de Especialista:", int((rh["cargo"] > "Especialista").sum()), "pessoas")
rh.groupby("cargo", observed=True)["salario"].median().round(2)

# %% [markdown]
# ---
# ## {{tres-formatos}} · Três formatos numa coluna
#
# Um sistema, três exportações, dez anos de história.

# %%
limpo["data_pedido"].dropna().sample(8, random_state=3).to_frame()

# %% [markdown]
# ---
# ## {{ato1}} · Ato 1 — o palpite
#
# Ele decide **um** formato e aplica em todas. Perde 534 de 600 — mas avisa.

# %%
ingenuo = pd.to_datetime(limpo["data_pedido"], errors="coerce")
print("viraram NaT:", ingenuo.isna().sum(), "de", len(limpo))

# %% [markdown]
# ---
# ## {{ato2}} · Ato 2 — format="mixed"
#
# Só 12 perdidas. **Olhe o fim do período antes de comemorar.**

# %%
misto = pd.to_datetime(limpo["data_pedido"], format="mixed", dayfirst=True, errors="coerce")
print("viraram NaT:", misto.isna().sum(), "de", len(limpo))
print("período:", misto.min().date(), "→", misto.max().date())

# %% [markdown]
# ---
# ## {{ato3}} · Ato 3 — o estrago
#
# O `dayfirst=True` valeu também para as datas em ISO: 112 trocaram de mês.

# %%
def para_data(s, formatos=("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")):
    """Tenta cada formato explícito, na ordem; só mexe no que ainda está vazio."""
    saida = pd.Series(pd.NaT, index=s.index, dtype="datetime64[us]")
    for f in formatos:
        pendente = saida.isna() & s.notna()
        if not pendente.any():
            break
        saida[pendente] = pd.to_datetime(s[pendente], format=f, errors="coerce")
    return saida


cascata = para_data(limpo["data_pedido"])
divergem = (misto != cascata) & misto.notna() & cascata.notna()

print("NaT na cascata:", cascata.isna().sum())
print("datas em que os dois métodos DISCORDAM:", divergem.sum())
pd.DataFrame({"texto": limpo["data_pedido"], "format='mixed'": misto,
              "cascata explícita": cascata})[divergem].head(8)

# %% [markdown]
# ---
# ## {{receita-datas}} · A receita segura
#
# Conferir a faixa pega 30 das 112. As outras 82 ficam ali, plausíveis e erradas.

# %%
limpo["data_pedido"] = cascata
ABERTURA, HOJE = pd.Timestamp("2026-01-01"), pd.Timestamp("2026-08-28")

pegas = int((~misto.between(ABERTURA, HOJE) & misto.notna()).sum())
print("cascata      · faixa:", cascata.min().date(), "→", cascata.max().date())
print("format=mixed · fora da faixa do negócio:", pegas, f"de {int(divergem.sum())} corrompidas")
print(f"\no teste de faixa pegaria {pegas}; as outras {int(divergem.sum()) - pegas} passariam batido.")

# %%
# as 5 datas que não existem no calendário
texto = sem_dup.loc[limpo.index, "data_pedido"]
limpo.loc[cascata.isna() & texto.notna(), ["id_pedido"]].assign(
    texto=texto[cascata.isna() & texto.notna()])

# %% [markdown]
# ---
# ## {{acessador-dt}} · O acessador .dt
#
# Uma data vira dez colunas — e a pergunta "que dia da semana vende mais?".

# %%
d = limpo["data_pedido"]
pd.DataFrame({
    "data": d, "ano": d.dt.year, "mês": d.dt.month, "dia": d.dt.day,
    "semana": d.dt.isocalendar().week, "dia_semana": d.dt.dayofweek,
    "nome_do_dia": d.dt.day_name(), "trimestre": d.dt.quarter,
    "fim_de_mês?": d.dt.is_month_end, "dias_no_mês": d.dt.days_in_month,
}).head(6)

# %%
(limpo.assign(dia=d.dt.day_name())
      .groupby("dia", observed=True)["valor"].agg(pedidos="size", faturamento="sum")
      .sort_values("faturamento", ascending=False).round(2))

# %% [markdown]
# ---
# ## {{fuso}} · Fuso horário
#
# Três horas de erro numa resposta que parecia trivial.

# %%
temp = a["temperatura"].replace(-999.0, np.nan).where(lambda s: s < 40)
temp_local = temp.tz_convert("America/Sao_Paulo")

print("hora mais quente lendo o carimbo bruto (UTC):",
      temp.groupby(temp.index.hour).mean().idxmax(), "h")
print("hora mais quente no fuso de Brasília:      ",
      temp_local.groupby(temp_local.index.hour).mean().idxmax(), "h")

# %%
# tz_localize ROTULA (não move); tz_convert TRADUZ (move)
sem_fuso = a.index.tz_localize(None)
print("sem fuso nenhum:      ", sem_fuso[0])
print("tz_localize (rotula): ", sem_fuso[:1].tz_localize("America/Sao_Paulo")[0])
print("tz_convert  (traduz): ", a.index[:1].tz_convert("America/Sao_Paulo")[0])
# %% [markdown]
# ---
# ## {{acessador-str}} · O acessador .str
#
# A coluna inteira de uma vez, pulando os `NaN` sozinho.

# %%
nomes = limpo["cliente"].head(6)
pd.DataFrame({
    "bruto": nomes,
    "strip": nomes.str.strip(),
    "lower": nomes.str.lower(),
    "title": nomes.str.title(),
    "tamanho": nomes.str.len(),
})

# %% [markdown]
# ---
# ## {{espaco}} · O espaço que ninguém vê
#
# `strip()` só limpa as pontas. O do meio precisa de `\s+`.

# %%
sujo = pd.Series(["  São  Paulo ", "Rio\tde Janeiro", "Porto   Alegre"])
pd.DataFrame({
    "bruto": sujo.str.replace(" ", "·"),
    "só_strip": sujo.str.strip().str.replace(" ", "·"),
    "strip_+_regex": sujo.str.replace(r"\s+", " ", regex=True).str.strip().str.replace(" ", "·"),
})

# %% [markdown]
# ---
# ## {{acento}} · Dois jeitos de escrever "ã"
#
# Visualmente idênticos; byte a byte, diferentes.

# %%
composto = "São Paulo"
decomposto = unicodedata.normalize("NFD", composto)

print("iguais?", composto == decomposto, "· tamanhos:", len(composto), len(decomposto))
print("composto:  ", [hex(ord(c)) for c in composto[:3]])
print("decomposto:", [hex(ord(c)) for c in decomposto[:4]])

# %% [markdown]
# ---
# ## {{funcao-chave}} · A função chave, por dentro
#
# A mesma `chave()` já usada nas duplicatas — agora vendo o efeito passo a passo.

# %%
cidades = pd.Series(["São Paulo", "SAO PAULO", " São  Paulo ", "Sao Paulo",
                     "Florianópolis", "Florianopolis", "Goiânia", "GOIANIA"])
pd.DataFrame({"bruto": cidades, "chave": chave(cidades)})

# %%
print("valores distintos antes: ", cidades.nunique())
print("valores distintos depois:", chave(cidades).nunique())

# %% [markdown]
# ---
# ## {{uf-27-10}} · De 27 estados para 10
#
# Normalizar resolve a grafia; o **dicionário** resolve o significado.

# %%
print("antes:", limpo["uf"].nunique(), "valores distintos")
print(sorted(limpo["uf"].unique()))

# %%
MAPA_UF = {"sao paulo": "SP", "s.p.": "SP", "rio de janeiro": "RJ",
           "rio grande do sul": "RS", "minas gerais": "MG"}

limpo["uf"] = chave(limpo["uf"]).replace(MAPA_UF).str.upper()
print("depois:", limpo["uf"].nunique(), "valores distintos")
limpo["uf"].value_counts()

# %% [markdown]
# ---
# ## {{map-replace}} · map avisa; replace não
#
# A contagem de `NaN` depois do `map` é o teste de que o dicionário está completo.

# %%
print("categoria — antes:", limpo["categoria"].nunique())
MAPA_CAT = {"eletronicos": "Eletrônicos", "eletronico": "Eletrônicos",
            "vestuario": "Vestuário", "casa": "Casa", "livros": "Livros",
            "livro": "Livros", "esporte": "Esporte", "esportes": "Esporte"}
limpo["categoria"] = chave(limpo["categoria"]).map(MAPA_CAT)
print("categoria — depois:", limpo["categoria"].nunique(),
      "· sem tradução:", limpo["categoria"].isna().sum())
limpo["categoria"].value_counts()

# %%
print("departamento no RH — antes:", rh["departamento"].nunique())
MAPA_DEPTO = {
    "ti": "Tecnologia", "t.i.": "Tecnologia", "tecnologia": "Tecnologia",
    "tecnologia da informacao": "Tecnologia",
    "comercial": "Comercial", "vendas": "Comercial",
    "operacoes": "Operações", "financeiro": "Financeiro", "fin.": "Financeiro",
    "pessoas": "Pessoas", "rh": "Pessoas", "r.h.": "Pessoas",
    "recursos humanos": "Pessoas",
}
rh["departamento"] = chave(rh["departamento"]).map(MAPA_DEPTO)
print("departamento — depois:", rh["departamento"].nunique(),
      "· sem tradução:", rh["departamento"].isna().sum())

# %% [markdown]
# ---
# ## {{extract}} · extract com grupos nomeados
#
# Cada grupo da expressão regular vira uma coluna.

# %%
cupons = limpo["obs"].str.extract(r"PROMO-(?P<campanha>[A-Z]+)-(?P<codigo>\d{4})")
limpo[["campanha", "cupom"]] = cupons
print(cupons.dropna().head(6).to_string())
limpo["campanha"].value_counts(dropna=False)

# %% [markdown]
# ---
# ## {{zfill}} · O CPF que o Excel comeu
#
# Todo CPF tem 11 dígitos. Os de 10 passaram por uma planilha.

# %%
cpf = limpo["cpf"].astype("str").str.replace(r"\D", "", regex=True)
print(cpf.str.len().value_counts().sort_index().to_frame("quantos CPFs"))
print("\nos que perderam o zero:")
print(cpf[cpf.str.len() < 11].head(4).to_string())

limpo["cpf"] = cpf.str.zfill(11)
print("\ndepois do zfill:", limpo["cpf"].str.len().value_counts().to_dict())

# %% [markdown]
# ---
# ## {{assign}} · assign encadeado
#
# Dentro do `lambda d:`, `d` é a tabela **como está naquele passo**.

# %%
limpo["frete"] = limpo["frete"].fillna(0)
limpo["desconto_pct"] = limpo["desconto_pct"].fillna(0)

pedidos = limpo.assign(
    subtotal=lambda d: d["valor"],
    desconto=lambda d: d["valor"] * d["desconto_pct"] / 100,
    liquido=lambda d: d["subtotal"] - d["desconto"] + d["frete"],
    ticket=lambda d: d["liquido"] / d["qtd"],
)
pedidos[["valor", "desconto_pct", "frete", "qtd", "desconto", "liquido", "ticket"]].head()

# %% [markdown]
# ---
# ## {{where-select}} · np.where e np.select
#
# O `default` é a parte importante: ele entrega o que ninguém previu.

# %%
REGIAO = {"SP": "Sudeste", "RJ": "Sudeste", "MG": "Sudeste", "RS": "Sul",
          "SC": "Sul", "PR": "Sul", "BA": "Nordeste", "PE": "Nordeste",
          "CE": "Nordeste", "GO": "Centro-Oeste"}
pedidos["regiao"] = pedidos["uf"].map(REGIAO)
pedidos["porte"] = np.where(pedidos["liquido"] > 1000, "grande", "pequeno")

condicoes = [pedidos["liquido"] >= 50_000, pedidos["liquido"] >= 5_000,
             pedidos["liquido"] >= 500, pedidos["liquido"] >= 0]
pedidos["faixa"] = np.select(condicoes, ["corporativo", "alto", "médio", "baixo"],
                             default="a conferir")
pedidos["faixa"].value_counts()

# %%
# o que o default pegou — e que um default="baixo" teria enterrado
pedidos.loc[pedidos["faixa"] == "a conferir",
            ["id_pedido", "produto", "qtd", "valor", "liquido"]]

# %% [markdown]
# ---
# ## {{apply-lento}} · apply é lento
#
# A mesma conta, três formas, duas ordens de grandeza.

# %%
import time

def cronometra(nome, f, repeticoes=5):
    t = time.perf_counter()
    for _ in range(repeticoes):
        r = f()
    print(f"{nome:<34} {(time.perf_counter() - t) / repeticoes * 1000:7.2f} ms")
    return r


grande = pd.concat([pedidos] * 200, ignore_index=True)
print(f"{len(grande):,} linhas\n")

a1 = cronometra("apply linha a linha (axis=1)", lambda: grande.apply(lambda r: r["valor"] * 1.1, axis=1))
a2 = cronometra("apply na coluna", lambda: grande["valor"].apply(lambda v: v * 1.1))
a3 = cronometra("vetorizado (a coluna inteira)", lambda: grande["valor"] * 1.1)

print("\nos três dão o mesmo resultado:", np.allclose(a1.fillna(0), a3.fillna(0)))
del grande

# %% [markdown]
# ---
# ## {{cut-qcut}} · cut × qcut
#
# `cut` corta em valores; `qcut` corta em quantis. Com distribuição torta, muda tudo.

# %%
rh["idade"] = ((pd.Timestamp("2026-08-28")
                - pd.to_datetime(rh["nascimento"], format="%d/%m/%Y")).dt.days / 365.25).astype(int)

rh["faixa_etaria"] = pd.cut(rh["idade"], bins=[0, 25, 35, 45, 60, 120],
                            labels=["até 25", "26-35", "36-45", "46-60", "60+"])
rh["faixa_etaria"].value_counts().sort_index().to_frame("pessoas")

# %%
print("cut(4)  — fatias iguais de VALOR:")
print(pd.cut(rh["salario"], 4).value_counts().sort_index().to_string())
print("\nqcut(4) — fatias iguais de GENTE:")
print(pd.qcut(rh["salario"], 4).value_counts().sort_index().to_string())

# %% [markdown]
# ---
# ## {{pipe}} · pipe
#
# Cada passo com nome. Seis meses depois, a resposta está na lista.

# %%
def sem_cancelados(d):
    return d[d["liquido"] > 0]

def com_mes(d):
    return d.assign(mes=d["data_pedido"].dt.to_period("M"))

def so_colunas(d, colunas):
    return d[colunas]


(pedidos
 .pipe(sem_cancelados)
 .pipe(com_mes)
 .pipe(so_colunas, ["mes", "regiao", "liquido"])
 .groupby(["mes", "regiao"], observed=True)["liquido"].sum()
 .unstack().round(0))

# %% [markdown]
# ---
# ## {{olhe-antes}} · Olhe antes de decidir
#
# O degrau entre o percentil 99 e o máximo é a assinatura do outlier.

# %%
v = pedidos["liquido"]
pd.DataFrame({
    "quantil": [0, .01, .25, .50, .75, .95, .99, 1],
    "valor": [v.quantile(q) for q in [0, .01, .25, .50, .75, .95, .99, 1]],
}).round(2)

# %% [markdown]
# ---
# ## {{iqr}} · O método IQR
#
# O corpo dos dados vai do 1º ao 3º quartil; 1,5 amplitudes além, é candidato.

# %%
def limites_iqr(s, k=1.5):
    q1, q3 = s.quantile(.25), s.quantile(.75)
    return q1 - k * (q3 - q1), q3 + k * (q3 - q1)


baixo, alto = limites_iqr(v)
fora = (v < baixo) | (v > alto)
print(f"limites IQR: {baixo:,.2f} a {alto:,.2f}")
print(f"fora dos limites: {fora.sum()} pedidos ({fora.mean() * 100:.1f}%)")

# %% [markdown]
# ---
# ## {{zscore}} · z-score e o z robusto
#
# O z comum usa média e desvio — as duas coisas que o outlier estraga.

# %%
z = (v - v.mean()) / v.std()

def z_robusto(s):
    mediana = s.median()
    mad = (s - mediana).abs().median()
    return 0.6745 * (s - mediana) / mad          # 0,6745 calibra contra a normal


zr = z_robusto(v)
print("z comum   · |z| > 3:", int((z.abs() > 3).sum()), "pedidos")
print("z robusto · |z| > 3:", int((zr.abs() > 3).sum()), "pedidos")

pedidos.assign(z=z.round(2), z_robusto=zr.round(2)).nlargest(5, "liquido")[
    ["id_pedido", "liquido", "z", "z_robusto"]]

# %% [markdown]
# ---
# ## {{tres-tipos}} · Os três tipos de outlier
#
# **Leia a coluna `obs`.** É ela que separa o erro do fato.

# %%
pedidos.loc[fora, ["id_pedido", "produto", "qtd", "liquido", "obs"]].nlargest(6, "liquido")

# %%
print("— erro de digitação: qtd 999 —")
print(pedidos.nlargest(3, "qtd")[["id_pedido", "produto", "qtd", "valor"]].to_string(index=False))

print("\n— erro de digitação: prazo de entrega —")
print(pedidos.nlargest(3, "entrega_dias")[["id_pedido", "produto", "entrega_dias"]].to_string(index=False))

print("\n— valor impossível: negativo —")
print(pedidos[pedidos["valor"] < 0][["id_pedido", "produto", "valor"]].to_string(index=False))

# %%
corporativas = pedidos[pedidos["obs"].str.contains("corporativa", na=False)]
print(f"{len(corporativas)} pedidos corporativos = "
      f"{corporativas['liquido'].sum() / pedidos['liquido'].sum() * 100:.1f}% do faturamento")
corporativas[["id_pedido", "produto", "qtd", "liquido"]]

# %% [markdown]
# ---
# ## {{preco-decisao}} · O preço da decisão
#
# Quatro respostas defensáveis para "quanto vendemos". Escolha e **escreva por quê**.

# %%
def resumo(s, rotulo):
    return pd.Series({"pedidos": s.size, "média": s.mean(), "mediana": s.median(),
                      "total": s.sum(), "desvio": s.std()}, name=rotulo)


pd.DataFrame([
    resumo(v, "tudo"),
    resumo(v[~fora], "removendo pelo IQR"),
    resumo(v.clip(upper=alto), "aparando no limite (clip)"),
    resumo(v[v > 0], "só os positivos"),
]).round(2)

# %% [markdown]
# ---
# ## {{loc-iloc}} · loc × iloc
#
# A fatia do `loc` **inclui** o fim; a do `iloc` **exclui**.

# %%
amostra = pedidos.head(5)[["id_pedido", "produto", "liquido"]]
amostra.index = ["a", "b", "c", "d", "e"]

print("loc['b':'d'] →", list(amostra.loc["b":"d"].index), " (inclui o fim)")
print("iloc[1:3]    →", list(amostra.iloc[1:3].index), "      (exclui o fim)")
amostra

# %% [markdown]
# ---
# ## {{copia}} · A cópia e o Copy-on-Write
#
# No pandas 3, escrever numa fatia **nunca** altera o original.

# %%
teste = pedidos[["id_pedido", "liquido"]].head(5).copy()
caros = teste[teste["liquido"] > teste["liquido"].median()]
caros["liquido"] = 0                     # sem erro, sem aviso

print("a fatia mudou:")
print(caros.to_string(index=False))
print("\nmas o original NÃO mudou:")
print(teste.to_string(index=False))

# %%
# para alterar de verdade: um comando só, com .loc
teste.loc[teste["liquido"] > teste["liquido"].median(), "liquido"] = 0
print(teste.to_string(index=False))

# %% [markdown]
# ---
# ## {{pipeline}} · O pipeline inteiro
#
# Tudo o que decidimos, numa função que se pode rodar de novo no mês que vem.

# %%
def limpar_vendas(caminho, verbose=True):
    """Do CSV bruto à tabela pronta, com relatório de cada etapa."""
    log = []

    def anota(passo, d):
        log.append((passo, len(d), int(d.isna().sum().sum())))
        return d

    d = anota("1. leitura com na_values", pd.read_csv(caminho, na_values=NULOS))

    d = anota("2. sem linhas idênticas", d.drop_duplicates())
    d = d.assign(_k=chave(d["cliente"]))
    d = anota("3. sem quase-duplicatas",
              d.drop_duplicates(subset=["id_pedido", "_k", "produto"]).drop(columns="_k"))

    d["avaliacao"] = d["avaliacao"].replace(-999, np.nan)
    d["valor"] = para_real(d["valor"])
    d["qtd"] = pd.to_numeric(d["qtd"], errors="coerce").astype("Int64")
    d["data_pedido"] = para_data(d["data_pedido"])
    d = anota("4. tipos convertidos", d)

    d["cliente"] = d["cliente"].str.replace(r"\s+", " ", regex=True).str.strip().str.title()
    d["cidade"] = (d["cidade"].str.replace(r"\s+", " ", regex=True).str.strip().str.title()
                    .str.replace(r"\b(De|Do|Da|Dos|Das)\b", lambda m: m.group().lower(), regex=True))
    d["uf"] = chave(d["uf"]).replace(MAPA_UF).str.upper()
    d["categoria"] = chave(d["categoria"]).map(MAPA_CAT)
    d["canal"] = d["canal"].str.strip().str.lower()
    d["cpf"] = d["cpf"].astype("str").str.replace(r"\D", "", regex=True).str.zfill(11)
    email = d["email"].astype("str").str.strip().str.lower()
    d["email"] = email.where(email.str.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+"))
    tel = d["telefone"].astype("str").str.replace(r"\D", "", regex=True).str.replace(r"^55", "", regex=True)
    d["telefone"] = tel.where(tel.str.len().isin([10, 11]))
    d = anota("5. texto padronizado", d)

    d["avaliacao_faltava"] = d["avaliacao"].isna()
    d["frete"] = d["frete"].fillna(0)
    d["desconto_pct"] = d["desconto_pct"].fillna(0)
    d["qtd"] = d["qtd"].fillna(d.groupby("categoria")["qtd"].transform("median")).astype("Int64")
    d = anota("6. faltantes tratados", d)

    d = d.assign(
        liquido=lambda x: x["valor"] * (1 - x["desconto_pct"] / 100) + x["frete"],
        regiao=lambda x: x["uf"].map(REGIAO),
        mes=lambda x: x["data_pedido"].dt.to_period("M"),
        dia_semana=lambda x: x["data_pedido"].dt.day_name(),
        campanha=lambda x: x["obs"].str.extract(r"PROMO-([A-Z]+)-")[0],
        corporativo=lambda x: x["obs"].str.contains("corporativa", na=False),
    )
    d["categoria"] = d["categoria"].astype("category")
    d["uf"] = d["uf"].astype("category")
    d = anota("7. derivadas e categorias", d)

    impossivel = (d["valor"] < 0) | (d["qtd"] > 100) & (~d["corporativo"])
    d.loc[impossivel, ["valor", "liquido"]] = np.nan
    d = anota(f"8. {int(impossivel.sum())} valores impossíveis anulados", d)

    if verbose:
        print(pd.DataFrame(log, columns=["etapa", "linhas", "faltantes"]).to_string(index=False))
    return d


vendas = limpar_vendas("dados/vendas-sujas.csv")

# %%
raio_x(vendas)

# %% [markdown]
# ---
# ## {{auditoria}} · A auditoria
#
# Cada linha é uma promessa. O valor delas aparece no mês que vem.

# %%
def auditar(d):
    testes = {
        "uma linha por pedido": d["id_pedido"].is_unique,
        "sem linhas duplicadas": not d.duplicated().any(),
        "data é data": pd.api.types.is_datetime64_any_dtype(d["data_pedido"]),
        "valor é número": pd.api.types.is_numeric_dtype(d["valor"]),
        "UF com 2 letras": d["uf"].dropna().astype("str").str.fullmatch(r"[A-Z]{2}").all(),
        "no máximo 27 UFs": d["uf"].nunique() <= 27,
        "CPF com 11 dígitos": d["cpf"].str.len().eq(11).all(),
        "sem valor negativo": (d["valor"].dropna() >= 0).all(),
        "avaliação entre 1 e 5": d["avaliacao"].dropna().between(1, 5).all(),
        "datas dentro do período": d["data_pedido"].dropna().between(
            pd.Timestamp("2026-01-01"), pd.Timestamp("2026-08-28")).all(),
        "categoria sem buraco": d["categoria"].notna().all(),
        "frete sem buraco": d["frete"].notna().all(),
    }
    return pd.Series(testes).map({True: "✓ passou", False: "✗ FALHOU"}).to_frame("resultado")


auditar(vendas)

# %% [markdown]
# ---
# ## {{gravar}} · Gravar — e o que se perde
#
# O CSV não guarda tipo. Todo o trabalho de tipagem evapora na gravação.

# %%
vendas.to_csv("dados/vendas-limpas.csv", index=False)
relida = pd.read_csv("dados/vendas-limpas.csv")

pd.DataFrame({
    "antes de gravar": vendas.dtypes.astype(str),
    "depois de reler": relida.dtypes.astype(str),
}).loc[["data_pedido", "categoria", "uf", "qtd", "valor"]]

# %% [markdown]
# > Se o destino for outro programa Python, `to_parquet` preserva os tipos,
# > ocupa menos e lê mais rápido.
# %% [markdown]
# ---
# ---
# # Apêndice — o que não coube em slide
#
# Daqui para baixo **não há slide correspondente**. É material para depois da
# aula, para a Lista 2 e para consulta.

# %% [markdown]
# ---
# ## A.1 — `interpolate` que conhece o relógio
#
# O `interpolate()` puro conta **linhas**; com índice de data, `method="time"`
# conta **minutos**. Nas leituras do sensor as linhas não são regulares.

# %%
grade = temp.asfreq("15min")
pd.DataFrame({
    "original": grade,
    "linear": grade.interpolate(),
    "por_tempo": grade.interpolate(method="time"),
    "limite_2": grade.interpolate(limit=2),
}).loc["2026-03-03 11:30":"2026-03-03 15:15"].round(2)

# %% [markdown]
# ---
# ## A.2 — A árvore de decisão do faltante
#
# | situação | decisão |
# |---|---|
# | falta em < 5% e a linha não é preciosa | `dropna(subset=[...])` |
# | falta em 5–40%, número simétrico | `fillna(média)` |
# | falta em 5–40%, número assimétrico | `fillna(mediana)` |
# | falta em 5–40% e há grupo natural | `groupby().transform("median")` |
# | falta em série temporal ordenada | `ffill(limit=n)` ou `interpolate` |
# | falta em > 50% | descarte a coluna, ou vire uma flag |
# | falta porque **não se aplica** | preencha com a categoria "não se aplica" |
#
# A última linha é a mais esquecida: `data_cancelamento` vazia num pedido
# entregue não é buraco nenhum — é a resposta certa.

# %% [markdown]
# ---
# ## A.3 — `convert_dtypes`: útil como sugestão, nunca como decisão

# %%
vendas.convert_dtypes().dtypes.to_frame("sugestão do Pandas").head(12)

# %% [markdown]
# Ele acerta o óbvio e não sabe que `avaliacao` é uma escala de 1 a 5, nem que
# `uf` tem 27 valores possíveis. **O tipo certo depende do significado**, e
# significado não se infere de um arquivo.

# %% [markdown]
# ---
# ## A.4 — `contains` e o `NaN`: o que mudou no pandas 3
#
# No tipo `str` novo, `contains` já devolve `False` para o vazio. No velho
# `object` — que você vai encontrar em código de antes — devolve `NaN`.

# %%
como_str = vendas["obs"].str.contains("PROMO")
como_object = vendas["obs"].astype(object).str.contains("PROMO")

print("dtype str    →", como_str.dtype, "· tem NaN?", como_str.isna().any())
print("dtype object →", como_object.dtype, "· tem NaN?", como_object.isna().any())
print("\npor isso o hábito de escrever na=False continua valendo.")

# %% [markdown]
# ---
# ## A.5 — Validar com expressão regular: e-mail e telefone

# %%
email = vendas["email"].astype("str").str.strip().str.lower()
valido = email.str.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+")
print("e-mails válidos:", int(valido.sum()), "· inválidos ou vazios:", int(len(email) - valido.sum()))

tel = vendas["telefone"].astype("str").str.replace(r"\D", "", regex=True)
print("\ncomprimento dos telefones:", tel.str.len().value_counts().to_dict())

# %% [markdown]
# ---
# ## A.6 — Titanic: a tabela pronta em oito linhas
#
# Tudo o que a aula ensinou, aplicado de uma vez.

# %%
t = (pd.read_csv("dados/titanic.csv")
       .drop(columns=["Cabin", "Ticket"])
       .dropna(subset=["Embarked"])
       .assign(
           idade_faltava=lambda d: d["Age"].isna(),
           Age=lambda d: d["Age"].fillna(d.groupby(["Pclass", "Sex"])["Age"].transform("median")),
           faixa=lambda d: pd.cut(d["Age"], [0, 12, 18, 35, 60, 100],
                                  labels=["criança", "adolescente", "adulto jovem",
                                          "adulto", "idoso"]),
           sozinho=lambda d: (d["SibSp"] + d["Parch"]) == 0,
       ))
print(t.shape, "· faltantes restantes:", t.isna().sum().sum())
t.groupby(["faixa", "Sex"], observed=True)["Survived"].agg(pessoas="size", taxa="mean").round(3)

# %% [markdown]
# ---
# ## A.7 — Táxis: seis perguntas que o `isna()` não responde
#
# Valores **presentes e coerentes com o tipo**, e incoerentes com o mundo.

# %%
tx = taxis.assign(
    minutos=lambda d: (d["dropoff"] - d["pickup"]).dt.total_seconds() / 60,
    payment=lambda d: d["payment"].fillna("não informado"),
)
pd.Series({
    "distância zero": (tx["distance"] == 0).sum(),
    "duração zero ou negativa": (tx["minutos"] <= 0).sum(),
    "zero passageiros": (tx["passengers"] == 0).sum(),
    "mais de uma hora": (tx["minutos"] > 60).sum(),
    "gorjeta maior que a corrida": (tx["tip"] > tx["fare"]).sum(),
    "total ≠ tarifa+gorjeta+pedágio": (
        (tx["total"] - (tx["fare"] + tx["tip"] + tx["tolls"])).abs() > 0.01).sum(),
}).to_frame("corridas")

# %% [markdown]
# Uma delas dá **zero**, e isso também é resposta. A última é a interessante: a
# conta não fecha em 6.411 das 6.433 corridas. Antes de gritar "erro", olhe o
# **tamanho** da diferença:

# %%
(tx["total"] - (tx["fare"] + tx["tip"] + tx["tolls"])).round(2).value_counts().head(6).to_frame("corridas")

# %% [markdown]
# **A diferença assume meia dúzia de valores fixos.** Não é dado corrompido: são
# as taxas de Nova York — sobretaxa do MTA, taxa de congestionamento, adicional
# noturno. A coluna que explicaria a conta não veio no arquivo.
#
# *Um analista apressado "corrigiria" 6.411 linhas. O certo era perguntar.*

# %% [markdown]
# ---
# ## A.8 — A coluna derivada que denuncia
#
# Nenhum campo do arquivo é a velocidade. Ela nasce de dois outros.

# %%
velocidade = (tx["distance"] / (tx["minutos"] / 60)).replace([np.inf, -np.inf], np.nan)
print("mediana:", round(velocidade.median(), 1), "milhas por hora — trânsito de Manhattan")
print("acima de 100 mph:", int((velocidade > 100).sum()), "corridas")
tx.assign(vel=velocidade.round(1)).nlargest(5, "vel")[
    ["pickup", "distance", "minutos", "fare", "vel"]]

# %% [markdown]
# Nove milhas em sete segundos. O taxímetro registrou a distância certa e o
# relógio errado. A **coluna derivada denunciou o que as duas originais
# escondiam** — e essa é a razão de derivar antes de confiar.

# %% [markdown]
# ---
# # As dez regras
#
# 1. **Descreva antes de mexer.** `dtypes`, `unique`, `describe`, `isna().sum()`,
#    `duplicated().sum()`.
# 2. **O vazio tem disfarces:** `""`, `"-"`, `-999`, e a linha que nem existe.
# 3. **Imputar é afirmar algo sobre o mundo** — e encolhe a variância. Guarde a
#    flag `_faltava`.
# 4. **Duplicata só existe depois que você define o grão** da tabela.
# 5. **Converta com `errors="coerce"` e conte** o que virou `NaN`. Nunca em silêncio.
# 6. **Data: formato explícito, `dayfirst` consciente, e confira a faixa.**
# 7. **Normalize antes de comparar:** acento, caixa e espaço.
# 8. **Vetorizado primeiro;** `apply(axis=1)` é o último recurso.
# 9. **Outlier não se remove por fórmula.** Erro de digitação, evento raro e
#    valor impossível pedem coisas diferentes.
# 10. **Escreva o pipeline como função e audite o resultado.** Limpeza que não se
#     repete não é limpeza, é conserto.
#
# ---
#
# ### Próximo passo
#
# `exercicio-aula05.ipynb` — a Lista 2, com um dataset que você ainda não viu.
