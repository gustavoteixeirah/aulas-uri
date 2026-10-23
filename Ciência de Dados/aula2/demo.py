"""
Aula 02 — Anatomia de um dataset
Demonstração ao vivo · dataset Titanic (Kaggle: `train.csv`)

Rode bloco a bloco. Cada função é um momento da aula e corresponde
a um slide. Para executar tudo de uma vez:

    python demo.py

Para executar um bloco só:

    python demo.py 5
"""

import sys
from pathlib import Path

import pandas as pd

CSV = Path(__file__).parent / "dados" / "titanic.csv"
pd.set_option("display.width", 100)


def titulo(n, texto):
    print(f"\n{'=' * 62}\n  {n}. {texto}\n{'=' * 62}")


# ─────────────────────────────────────────────────────────────────
# 1 · Carregar — a linha mais importante da disciplina
# ─────────────────────────────────────────────────────────────────
def bloco_1():
    titulo(1, "Carregar o arquivo")
    df = pd.read_csv(CSV)
    print(type(df))
    print(df.shape)          # (linhas, colunas)
    return df


# ─────────────────────────────────────────────────────────────────
# 2 · O ritual de chegada — os quatro comandos de sempre
# ─────────────────────────────────────────────────────────────────
def bloco_2(df):
    titulo(2, "O ritual de chegada")

    print(">>> df.shape");   print(df.shape)
    print("\n>>> df.head(3)"); print(df.head(3))
    print("\n>>> df.dtypes"); print(df.dtypes)
    print("\n>>> df.info()"); df.info()


# ─────────────────────────────────────────────────────────────────
# 3 · Anatomia — linha, coluna, célula, índice
# ─────────────────────────────────────────────────────────────────
def bloco_3(df):
    titulo(3, "Anatomia: linha = observação, coluna = variável")

    print(">>> df['Age']            uma coluna é uma Series")
    print(type(df["Age"]), df["Age"].shape)

    print("\n>>> df.loc[0]           uma linha é uma observação")
    print(df.loc[0])

    print("\n>>> df.loc[0, 'Name']   uma célula é um valor")
    print(repr(df.loc[0, "Name"]))


# ─────────────────────────────────────────────────────────────────
# 4 · Que tipo de variável é cada coluna?
# ─────────────────────────────────────────────────────────────────
def bloco_4(df):
    titulo(4, "Cardinalidade revela o tipo de variável")

    perfil = pd.DataFrame({
        "dtype": df.dtypes,
        "distintos": df.nunique(),
        "faltantes": df.isna().sum(),
        "% faltante": (df.isna().mean() * 100).round(1),
    })
    print(perfil)

    print("\n>>> df['Embarked'].value_counts(dropna=False)")
    print(df["Embarked"].value_counts(dropna=False))


# ─────────────────────────────────────────────────────────────────
# 5 · Qualidade — o que está faltando, e o que está duplicado
# ─────────────────────────────────────────────────────────────────
def bloco_5(df):
    titulo(5, "Qualidade do dado")

    print(">>> faltantes por coluna (só as que têm)")
    faltam = df.isna().sum()
    print(faltam[faltam > 0])

    print("\n>>> linhas duplicadas:", df.duplicated().sum())
    print(">>> bilhetes repetidos:", df["Ticket"].duplicated().sum())

    print("\n>>> Cabin: 77% ausente. Isso é ruído — ou é informação?")
    tem_cabine = df["Cabin"].notna()
    print(df.groupby(tem_cabine)["Survived"].agg(["count", "mean"]).round(3))


# ─────────────────────────────────────────────────────────────────
# 6 · describe() — e por que a média mente
# ─────────────────────────────────────────────────────────────────
def bloco_6(df):
    titulo(6, "describe(): o resumo estatístico")

    print(df[["Age", "Fare", "SibSp", "Parch"]].describe().round(2))

    print("\n>>> Fare: média vs mediana")
    print("média   :", round(df["Fare"].mean(), 2))
    print("mediana :", round(df["Fare"].median(), 2))
    print("máximo  :", round(df["Fare"].max(), 2))
    print("\nA média é mais que o DOBRO da mediana (32.20 vs 14.45).")
    print("A distribuição é assimétrica: poucas tarifas altíssimas")
    print("puxam a média para cima. Metade pagou menos de £14,45.")


# ─────────────────────────────────────────────────────────────────
# 7 · A pergunta de negócio — groupby
# ─────────────────────────────────────────────────────────────────
def bloco_7(df):
    titulo(7, "Quem sobreviveu? (groupby)")

    print(">>> por sexo")
    print(df.groupby("Sex")["Survived"].mean().round(3))

    print("\n>>> por classe")
    print(df.groupby("Pclass")["Survived"].mean().round(3))

    print("\n>>> por sexo E classe (pivot_table)")
    print(pd.pivot_table(df, values="Survived",
                         index="Sex", columns="Pclass",
                         aggfunc="mean").round(3))

    print("\n>>> agora com o tamanho de cada grupo — sempre olhe o n")
    print(df.groupby(["Sex", "Pclass"])["Survived"]
            .agg(n="count", taxa="mean").round(3))


# ─────────────────────────────────────────────────────────────────
# 8 · Colunas derivadas — o dado que estava escondido
# ─────────────────────────────────────────────────────────────────
def bloco_8(df):
    titulo(8, "Feature engineering: extrair o que já estava lá")

    df = df.copy()

    # O título social está preso dentro do nome.
    df["Titulo"] = df["Name"].str.extract(r",\s*([^\.]+)\.")
    print(">>> títulos extraídos de Name")
    print(df["Titulo"].value_counts().head(6))

    # Tamanho da família: duas colunas viram uma ideia.
    df["Familia"] = df["SibSp"] + df["Parch"] + 1
    print("\n>>> sobrevivência por tamanho de família")
    print(df.groupby("Familia")["Survived"].agg(n="count", taxa="mean").round(3))

    # Contínua vira ordinal.
    df["Faixa"] = pd.cut(df["Age"],
                         bins=[0, 12, 18, 35, 60, 100],
                         labels=["criança", "adolescente", "adulto jovem",
                                 "adulto", "idoso"])
    print("\n>>> sobrevivência por faixa etária")
    print(df.groupby("Faixa", observed=True)["Survived"]
            .agg(n="count", taxa="mean").round(3))
    return df


# ─────────────────────────────────────────────────────────────────
# 9 · Imputação — e a decisão de negócio por trás dela
# ─────────────────────────────────────────────────────────────────
def bloco_9(df):
    titulo(9, "Imputar idade: três respostas, três consequências")

    idade = df["Age"]
    print("faltantes em Age:", idade.isna().sum(), f"({idade.isna().mean():.1%})")
    print("\nopção A — descartar as linhas :", df.dropna(subset=["Age"]).shape)
    print("opção B — preencher com média :", round(idade.mean(), 1))
    print("opção C — mediana por título  :")

    titulos = df["Name"].str.extract(r",\s*([^\.]+)\.")[0].rename("Titulo")
    print(df.groupby(titulos)["Age"]
            .agg(n="count", mediana="median")
            .sort_values("n", ascending=False).head(5))

    print("\nNenhuma é 'certa'. Cada uma é uma hipótese — e vai no relatório.")


# ─────────────────────────────────────────────────────────────────
# 10 · Um gráfico (opcional — precisa de matplotlib/seaborn)
# ─────────────────────────────────────────────────────────────────
def bloco_10(df):
    titulo(10, "Do número ao gráfico")
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        print("matplotlib/seaborn não instalados — pulando.")
        return

    fig, eixos = plt.subplots(1, 2, figsize=(11, 4.2))
    sns.histplot(df, x="Age", hue="Survived", multiple="stack", bins=30, ax=eixos[0])
    eixos[0].set_title("Idade × sobrevivência")
    sns.barplot(df, x="Pclass", y="Survived", hue="Sex", errorbar=None, ax=eixos[1])
    eixos[1].set_title("Taxa de sobrevivência por classe e sexo")
    fig.tight_layout()

    saida = Path(__file__).parent / "titanic.png"
    fig.savefig(saida, dpi=140)
    print("gráfico salvo em", saida.name)


def main():
    df = bloco_1()
    blocos = {2: bloco_2, 3: bloco_3, 4: bloco_4, 5: bloco_5, 6: bloco_6,
              7: bloco_7, 8: bloco_8, 9: bloco_9, 10: bloco_10}

    if len(sys.argv) > 1:
        n = int(sys.argv[1])
        (blocos[n] if n > 1 else lambda _: None)(df)
        return

    for n in sorted(blocos):
        resultado = blocos[n](df)
        if n == 8:
            df = resultado


if __name__ == "__main__":
    main()
