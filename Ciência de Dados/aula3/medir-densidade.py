"""Mede a densidade de texto de cada slide e aponta os carregados.

Uso:  python medir-densidade.py

O deck é para uma turma que precisa entender o slide de relance. Os limites
abaixo foram calibrados olhando os slides projetados — passar deles não é erro,
é sinal de que vale reler e cortar.
"""
import re
import os

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

MAX_PALAVRAS = 55      # texto do slide, sem contar o código
MAX_CALLOUT = 30       # a frase de fecho
MAX_CARD = 20          # a descrição de um card
MAX_KICKER = 8       # a etiqueta de cima (o prefixo "Exemplo N ·" conta 3)


def limpa(html):
    html = re.sub(r"<pre class=\"code.*?</pre>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    html = html.replace("&nbsp;", " ").replace("&amp;", "&")
    html = html.replace("&lt;", "<").replace("&gt;", ">")
    return re.sub(r"\s+", " ", html).strip()


def palavras(html):
    t = limpa(html)
    return len(t.split()) if t else 0


s = open(ARQ, encoding="utf-8").read()
slides = re.findall(
    r"<section class=\"slide[^\"]*\" data-title=\"([^\"]*)\"[^>]*>(.*?)</section>", s, re.S
)

total, carregados = [], []
for i, (titulo, corpo) in enumerate(slides, 1):
    p = palavras(corpo)
    total.append(p)
    callouts = [palavras(c) for c in re.findall(r"<div class=\"callout[^\"]*\">(.*?)</div>", corpo, re.S)]
    cards = [palavras(c) for c in re.findall(r"<small>(.*?)</small>", corpo, re.S)]
    kicker = [palavras(k) for k in re.findall(r"<span class=\"kicker\">(.*?)</span>", corpo, re.S)]

    motivos = []
    if p > MAX_PALAVRAS:
        motivos.append(f"{p} palavras")
    if any(c > MAX_CALLOUT for c in callouts):
        motivos.append(f"callout de {max(callouts)}")
    if cards and max(cards) > MAX_CARD:
        motivos.append(f"card de {max(cards)}")
    if kicker and max(kicker) > MAX_KICKER:
        motivos.append(f"kicker de {max(kicker)}")
    if motivos:
        carregados.append((i, titulo, ", ".join(motivos)))

print(f"{len(slides)} slides · média de {sum(total)/len(total):.1f} palavras · maior com {max(total)}")
if carregados:
    print(f"\n{len(carregados)} para reler:")
    for i, t, m in carregados:
        print(f"  {i:>3}  {t:<32} {m}")
else:
    print("\nNenhum slide acima dos limites.")
