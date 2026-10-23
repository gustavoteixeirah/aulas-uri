"""Monta o aula05.ipynb a partir do fonte, resolvendo os números dos slides.

O caderno acompanha os slides na mesma numeração. Para que os dois nunca saiam
de sincronia, o fonte (`caderno-fonte.py`) não escreve números: escreve chaves.

    ## {{sentinela}} · A sentinela

Cada slide do `index.html` que tem célula no caderno carrega a mesma chave:

    <section class="slide" data-title="★ A sentinela" data-nb="sentinela" ...>

Este script lê o HTML, descobre em que posição cada chave está, e troca
`{{sentinela}}` por `▸ Slide 18`. Se um slide for inserido, movido ou removido,
basta rodar de novo — a numeração do caderno acompanha sozinha.

Também confere a consistência nos dois sentidos e recusa a montagem se algum
slide marcado ficou sem célula, ou alguma célula aponta para um slide que não
existe.

Uso:  python montar-caderno.py            monta e executa
      python montar-caderno.py --so-checar   só confere o alinhamento
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "index.html")
FONTE = os.path.join(BASE, "caderno-fonte.py")
SAIDA = os.path.join(BASE, "aula05.ipynb")


def numeros_dos_slides():
    """chave -> (número do slide, título), lendo o data-nb do HTML."""
    html = open(HTML, encoding="utf-8").read()
    slides = re.findall(r'<section class="slide[^"]*"([^>]*)>', html)
    mapa = {}
    for i, attrs in enumerate(slides, 1):
        ch = re.search(r'data-nb="([^"]+)"', attrs)
        tit = re.search(r'data-title="([^"]*)"', attrs)
        if ch:
            mapa[ch.group(1)] = (i, tit.group(1) if tit else "")
    return mapa, len(slides)


def confere(mapa, fonte):
    """Os dois lados têm que falar das mesmas chaves."""
    no_caderno = set(re.findall(r"\{\{([a-z0-9-]+)\}\}", fonte))
    nos_slides = set(mapa)

    orfas = no_caderno - nos_slides      # o caderno cita um slide que não existe
    mudas = nos_slides - no_caderno      # o slide diz ter célula e não tem

    for ch in sorted(orfas):
        print(f"  ✗ o caderno cita {{{{{ch}}}}}, mas nenhum slide tem data-nb=\"{ch}\"")
    for ch in sorted(mudas):
        n, tit = mapa[ch]
        print(f"  ✗ o slide {n} ({tit}) promete célula, e o caderno não tem {{{{{ch}}}}}")
    return not (orfas or mudas)


def main():
    mapa, total = numeros_dos_slides()
    fonte = open(FONTE, encoding="utf-8").read()

    print(f"{total} slides · {len(mapa)} marcados com célula no caderno")
    if not confere(mapa, fonte):
        print("\nAlinhamento quebrado — nada foi gravado.")
        return 1
    print("  ✓ todas as chaves batem nos dois sentidos")

    if "--so-checar" in sys.argv:
        return 0

    # o índice de consulta rápida, gerado a partir do próprio HTML
    por_numero = sorted((n, ch, tit) for ch, (n, tit) in mapa.items())
    linhas = ["<details>", "<summary><b>Índice — slide por slide</b> (clique para abrir)</summary>",
              "", "| slide | assunto | slide | assunto |", "|---|---|---|---|"]
    meio = (len(por_numero) + 1) // 2
    esq, dir_ = por_numero[:meio], por_numero[meio:]
    for i in range(meio):
        a = f"**{esq[i][0]}** | {esq[i][2].lstrip('★ ')}"
        b = f"**{dir_[i][0]}** | {dir_[i][2].lstrip('★ ')}" if i < len(dir_) else " | "
        linhas.append(f"| {a} | {b} |")
    linhas += ["", "</details>"]
    indice = "\n".join(linhas)

    # {{chave}} vira "▸ Slide 18"; {{INDICE}} vira a tabela acima
    resolvido = fonte.replace("{{INDICE}}", indice)
    resolvido = re.sub(r"\{\{([a-z0-9-]+)\}\}",
                       lambda m: f"▸ Slide {mapa[m.group(1)][0]}", resolvido)

    import nbformat
    from nbclient import NotebookClient

    nb = nbformat.v4.new_notebook()
    blocos = re.split(r"^# %%(.*)$", resolvido, flags=re.M)
    for marca, corpo in zip(blocos[1::2], blocos[2::2]):
        corpo = corpo.strip("\n")
        if "[markdown]" in marca:
            texto = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#")
                              for l in corpo.split("\n"))
            nb.cells.append(nbformat.v4.new_markdown_cell(texto.strip("\n")))
        elif corpo.strip():
            nb.cells.append(nbformat.v4.new_code_cell(corpo))

    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    }

    codigo = sum(1 for c in nb.cells if c.cell_type == "code")
    print(f"\nmontando: {len(nb.cells)} células ({codigo} de código) — executando…")
    NotebookClient(nb, timeout=600, kernel_name="python3",
                   resources={"metadata": {"path": BASE}}).execute()
    nbformat.write(nb, SAIDA)
    print(f"gravado: {os.path.basename(SAIDA)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
