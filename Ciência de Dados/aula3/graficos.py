"""Gera os gráficos da aula 3 — NumPy faz a conta, o gráfico só recebe o resultado.

Fundo transparente e cores que funcionam no tema claro e no escuro dos slides.
"""
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

OUT = "/Users/teixeirah/code/uri/Ciência de Dados/aula3/img/"
ROXO, AMBAR, VERDE, CINZA = "#5b56e0", "#d9820b", "#0a9d70", "#8a90a0"

plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.transparent": True, "savefig.bbox": "tight",
    "font.size": 11, "text.color": CINZA,
    "axes.labelcolor": CINZA, "axes.edgecolor": CINZA,
    "xtick.color": CINZA, "ytick.color": CINZA,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "none", "axes.facecolor": "none",
})

df = pd.read_csv("/Users/teixeirah/code/uri/Ciência de Dados/aula3/dados/taxis.csv",
                 parse_dates=["pickup", "dropoff"])
dist = df["distance"].to_numpy()
fare = df["fare"].to_numpy()
tip = df["tip"].to_numpy()
hora = df["pickup"].dt.hour.to_numpy()
pagto = df["payment"].to_numpy()
dur = (df["dropoff"] - df["pickup"]).dt.total_seconds().to_numpy() / 60


def salva(fig, nome):
    fig.savefig(OUT + nome, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print("ok", nome)


# 1 — histograma de distâncias
alturas, bordas = np.histogram(dist, bins=np.arange(0, 21, 1))
fig, ax = plt.subplots(figsize=(7.2, 3.1))
ax.bar(bordas[:-1], alturas, width=.9, align="edge", color=ROXO)
ax.set_xlabel("distância da corrida (milhas)")
ax.set_ylabel("corridas")
ax.set_xticks(range(0, 21, 2))
salva(fig, "g1-histograma.png")
print("  pico:", alturas.max(), "na faixa", bordas[alturas.argmax()])

# 2 — corridas por hora
por_hora = np.bincount(hora, minlength=24)
cores = [AMBAR if h == por_hora.argmax() else ROXO for h in range(24)]
fig, ax = plt.subplots(figsize=(7.2, 3.1))
ax.bar(np.arange(24), por_hora, color=cores, width=.8)
ax.set_xlabel("hora do dia")
ax.set_ylabel("corridas")
ax.set_xticks(range(0, 24, 3))
salva(fig, "g2-por-hora.png")
print("  pico hora:", por_hora.argmax(), por_hora.max(), "vale:", por_hora.argmin(), por_hora.min())

# 3 — tarifa média por hora
media_hora = np.array([fare[hora == h].mean() for h in range(24)])
fig, ax = plt.subplots(figsize=(7.2, 3.1))
ax.plot(np.arange(24), media_hora, color=ROXO, lw=2.4, marker="o", ms=4)
ax.set_xlabel("hora do dia")
ax.set_ylabel("tarifa média (US$)")
ax.set_xticks(range(0, 24, 3))
salva(fig, "g3-tarifa-hora.png")
print("  maior:", media_hora.argmax(), round(media_hora.max(), 2),
      "menor:", media_hora.argmin(), round(media_hora.min(), 2))

# 4 — distância × tarifa, com a reta do np.polyfit
a, b = np.polyfit(dist, fare, 1)
x = np.linspace(0, dist.max(), 100)
fig, ax = plt.subplots(figsize=(7.2, 3.1))
ax.scatter(dist, fare, s=6, alpha=.25, color=ROXO, edgecolors="none")
ax.plot(x, a * x + b, color=AMBAR, lw=2.4)
ax.set_xlabel("distância (milhas)")
ax.set_ylabel("tarifa (US$)")
salva(fig, "g4-reta.png")
print("  reta: fare = %.2f * dist + %.2f" % (a, b))

# 5 — gorjeta média por forma de pagamento
cartao = tip[pagto == "credit card"].mean()
dinheiro = tip[pagto == "cash"].mean()
fig, ax = plt.subplots(figsize=(7.2, 2.9))
ax.barh(["dinheiro", "cartão"], [dinheiro, cartao], color=[AMBAR, ROXO], height=.55)
ax.set_xlabel("gorjeta média (US$)")
for i, v in enumerate([dinheiro, cartao]):
    ax.text(v + .06, i, f"{v:.2f}", va="center", color=CINZA, fontsize=11)
ax.set_xlim(0, 3.4)
salva(fig, "g5-gorjeta.png")
print("  cartao %.2f dinheiro %.2f" % (cartao, dinheiro))

# 6 — acumulado: que fatia das corridas cabe até X milhas
alturas2, bordas2 = np.histogram(dist, bins=np.arange(0, 21, .5))
acum = np.cumsum(alturas2) / len(dist) * 100
fig, ax = plt.subplots(figsize=(7.2, 3.1))
ax.plot(bordas2[1:], acum, color=VERDE, lw=2.6)
ax.axhline(80, color=CINZA, ls="--", lw=1)
ax.set_xlabel("distância (milhas)")
ax.set_ylabel("% das corridas até aqui")
ax.set_ylim(0, 100)
salva(fig, "g6-acumulado.png")
i80 = np.argmax(acum >= 80)
print("  80% das corridas até", bordas2[1:][i80], "milhas")

# números extras usados nos slides
print("\n--- números ---")
print("corridas:", len(df))
print("dist media %.2f mediana %.2f max %.1f" % (dist.mean(), np.median(dist), dist.max()))
print("fare media %.2f mediana %.2f max %.0f" % (fare.mean(), np.median(fare), fare.max()))
print("km: %.2f" % (dist[0] * 1.60934), "primeira dist:", dist[0])
print("faturamento total: %.2f" % fare.sum())
print("longas >10:", (dist > 10).sum(), "%.1f%%" % ((dist > 10).mean() * 100))
print("longas com gorjeta:", ((dist > 10) & (tip > 0)).sum())
print("velocidade mediana: %.1f mph" % np.median(dist / np.where(dur == 0, np.nan, dur) * 60))
print("gorjeta %% mediana de quem deu: %.1f" % np.median((tip / fare * 100)[tip > 0]))
print("dist zero:", (dist == 0).sum())
print("mais cara: idx", fare.argmax(), "US$", fare.max(), "dist", dist[fare.argmax()])
print("top5 tarifas:", np.sort(fare)[-5:])
print("deram gorjeta: %.1f%%" % ((tip > 0).mean() * 100))
