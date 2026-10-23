"""Roda, sobre o CSV desta pasta, todos os exemplos da seção "Na prática".

Uso:  python saidas.py

Serve para conferir os slides: cada bloco abaixo é exatamente o que está
projetado — comando e saída. Se o CSV ou a versão do pandas mudar e algum
número sair diferente, é aqui que aparece primeiro.
"""
import contextlib
import io
import os

import pandas as pd

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "taxis.csv")

ns = {"pd": pd}
exec(f'df = pd.read_csv(r"{CSV}", parse_dates=["pickup", "dropoff"])', ns)

# (slide, [(tipo, código)]) — tipo: expr mostra o valor, stmt só executa,
# print captura o que a função imprime, show apenas exibe a linha.
SLIDES = [
    ("11 · A tabela", [
        ("expr", 'df.shape'),
        ("expr", 'df[["distance", "fare", "tip", "payment"]].head(3)')]),
    ("12 · info", [
        ("print", 'df[["distance", "fare", "payment"]].info()')]),
    ("13 · describe", [
        ("expr", 'df[["fare", "tip"]].describe()')]),
    ("14 · Uma coluna", [
        ("expr", 'df["fare"].head(3)'),
        ("print", 'print(df["fare"].mean())'),
        ("expr", 'df["fare"].to_numpy()')]),
    ("15 · Filtrar", [
        ("stmt", 'longas = df[df["distance"] > 10]'),
        ("expr", 'longas.shape'),
        ("print", 'print(longas["fare"].mean())')]),
    ("16 · Duas condições", [
        ("expr", 'df[(df["distance"] > 10) & (df["tip"] > 0)].shape'),
        ("expr", 'df.query("distance > 10 and tip > 0").shape')]),
    ("17 · value_counts", [
        ("expr", 'df["payment"].value_counts(dropna=False)'),
        ("expr", 'df["distance"].nunique()')]),
    ("18 · groupby", [
        ("expr", 'df.groupby("payment")["tip"].mean()')]),
]


def roda(tipo, codigo):
    if tipo == "stmt":
        exec(codigo, ns)
        return None
    if tipo == "show":
        return None
    if tipo == "print":
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            eval(codigo, ns)
        return buf.getvalue().rstrip("\n")
    return repr(eval(codigo, ns))


print(f"pandas {pd.__version__} · {os.path.basename(CSV)}\n")
for slide, passos in SLIDES:
    print(f"── {slide} " + "─" * max(0, 56 - len(slide)))
    for tipo, codigo in passos:
        for i, linha in enumerate(codigo.split("\n")):
            print((">>> " if i == 0 else "... ") + linha)
        saida = roda(tipo, codigo)
        if saida is not None:
            print(saida)
    print()
