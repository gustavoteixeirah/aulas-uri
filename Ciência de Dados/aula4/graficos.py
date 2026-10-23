"""Gera os quatro gráficos da aula 4 — nenhum sairia de uma lista de números.

    1. mapa de calor            hora × dia da semana
    2. barras empilhadas 100%   forma de pagamento por bairro
    3. gráfico de linhas        março dia a dia, com média móvel
    4. gráfico de linhas        2019 inteiro — o mesmo código, 365 dias

Cada um precisa de algo que só a tabela tem: cruzar duas colunas numa matriz,
dividir cada linha pelo seu próprio total, ou ter data no índice. Fundo
transparente e cores que funcionam no tema claro e no escuro dos slides.

Uso:  python graficos.py
"""
import os

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "img") + os.sep
os.makedirs(OUT, exist_ok=True)

ROXO, AMBAR, VERDE, CINZA = "#5b56e0", "#d9820b", "#0a9d70", "#8a90a0"
# escala quente de verdade — creme, amarelo, âmbar, tijolo, vinho — legível nos
# dois temas do deck: mesmo a célula mais clara tem cor, não fica branca
CALOR = LinearSegmentedColormap.from_list(
    "calor", ["#fff6df", "#fddb7d", "#f5a83a", AMBAR, "#a83a12", "#6e1a12"])

plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.transparent": True, "savefig.bbox": "tight",
    "font.size": 11, "text.color": CINZA,
    "axes.labelcolor": CINZA, "axes.edgecolor": CINZA,
    "xtick.color": CINZA, "ytick.color": CINZA,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "none", "axes.facecolor": "none",
})

df = pd.read_csv(os.path.join(BASE, "dados", "taxis.csv"), parse_dates=["pickup", "dropoff"])

DIAS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PT = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def salva(fig, nome):
    fig.savefig(OUT + nome, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print("ok", nome)


# 1 — MAPA DE CALOR de hora × dia da semana: a pivot_table vira imagem
mapa = df.pivot_table(index=df["pickup"].dt.day_name(),
                      columns=df["pickup"].dt.hour,
                      aggfunc="size").reindex(DIAS).fillna(0)
fig, ax = plt.subplots(figsize=(7.6, 2.9))
im = ax.imshow(mapa.values, cmap=CALOR, aspect="auto")
ax.set_xticks(range(0, 24, 3), [f"{h}h" for h in range(0, 24, 3)])
ax.set_yticks(range(7), PT)
ax.set_xlabel("hora da coleta")
for lado in ax.spines.values():
    lado.set_visible(False)
pico = mapa.stack().idxmax()
# emoldura a célula do pico em vez de marcá-la com um ponto, que taparia a cor
ax.add_patch(Rectangle((pico[1] - .5, DIAS.index(pico[0]) - .5), 1, 1,
                       fill=False, ec="#ffffff", lw=2))
cb = fig.colorbar(im, ax=ax, pad=.015, fraction=.03)
cb.outline.set_visible(False)
cb.set_label("corridas", color=CINZA, fontsize=10)
salva(fig, "g1-calor-hora-dia.png")
print("   pico:", pico, int(mapa.stack().max()), "· vale:", mapa.stack().idxmin(), int(mapa.stack().min()))

# 2 — BARRAS EMPILHADAS 100% de pagamento por bairro: unstack e div por eixo
qtd = df.groupby(["pickup_borough", "payment"]).size().unstack()
pct = qtd.div(qtd.sum(axis=1), axis=0) * 100          # cada linha vale 100
pct = pct.sort_values("cash")
fig, ax = plt.subplots(figsize=(7.4, 2.8))
pct.plot(kind="barh", stacked=True, ax=ax, width=.62, color=[AMBAR, ROXO], legend=False)
ax.set_xlim(0, 100)
ax.set_xlabel("% das corridas do bairro")
ax.set_ylabel("")
for i, v in enumerate(pct["cash"]):
    ax.text(v / 2, i, f"{v:.0f}%", va="center", ha="center", color="#ffffff", fontsize=10.5)
ax.legend(["dinheiro", "cartão"], frameon=False, fontsize=10, labelcolor=CINZA,
          ncols=2, loc="lower center", bbox_to_anchor=(.5, -.42))
salva(fig, "g2-dinheiro-bairro.png")
print("  ", pct["cash"].round(1).to_dict(), "· corridas por bairro:", qtd.sum(axis=1).to_dict())

# 3 — GRÁFICO DE LINHAS de março dia a dia: índice de data e janela móvel
marco = df.set_index("pickup").loc["2019-03"]
por_dia = marco.resample("D").size()
fig, ax = plt.subplots(figsize=(7.4, 2.9))
por_dia.plot(ax=ax, color=CINZA, lw=1, label="por dia")
por_dia.rolling(7).mean().plot(ax=ax, color=ROXO, lw=2.6, label="média de 7 dias")
ax.set_xlabel("")
ax.set_ylabel("corridas")
ax.legend(frameon=False, fontsize=10, labelcolor=CINZA, loc="lower left")
salva(fig, "g3-marco-dia-a-dia.png")
print("   máx:", por_dia.idxmax().date(), por_dia.max(), "· mín:", por_dia.idxmin().date(), por_dia.min())

# 4 — GRÁFICO DE LINHAS do ano inteiro: o mesmo resample, agora em 365 dias.
# O CSV vem do baixa-ano-2019.py — 84,6 milhões de corridas resumidas por dia.
ano = pd.read_csv(os.path.join(BASE, "dados", "corridas-2019.csv"),
                  parse_dates=["dia"], index_col="dia")
mil = ano["corridas"] / 1000
fig, ax = plt.subplots(figsize=(7.6, 2.9))
mil.plot(ax=ax, color=CINZA, lw=.8, label="por dia")
mil.rolling(7).mean().plot(ax=ax, color=ROXO, lw=2.6, label="média de 7 dias")
ax.axvspan(pd.Timestamp("2019-03-01"), pd.Timestamp("2019-03-31"), color=AMBAR, alpha=.16, lw=0)
ax.annotate("março, o mês\nda aula", (pd.Timestamp("2019-03-16"), 314), color=AMBAR,
            fontsize=9.5, ha="center", va="top")
natal = mil.idxmin()
mil.loc[[natal]].plot(ax=ax, marker="o", ms=6, lw=0, color=AMBAR, label="_nolegend_")
ax.annotate("Natal", (natal, mil.min()), xytext=(-38, -3), textcoords="offset points",
            color=AMBAR, fontsize=9.5)
ax.set_xticks(pd.date_range("2019-01-01", "2019-12-01", freq="MS"))
ax.set_xticklabels(MESES)
ax.set_xlabel("")
ax.set_ylabel("mil corridas por dia")
ax.set_ylim(80, 320)
ax.legend(frameon=False, fontsize=10, labelcolor=CINZA, loc="lower left", ncols=2)
salva(fig, "g4-ano-2019.png")
mm = ano["corridas"].resample("ME").sum()
print("   topo:", mm.idxmax().strftime("%m"), f"{mm.max():,}", "· fundo:", mm.idxmin().strftime("%m"),
      f"{mm.min():,}", "· menor dia:", ano["corridas"].idxmin().date())
