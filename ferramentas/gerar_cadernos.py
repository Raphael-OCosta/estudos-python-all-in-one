"""Gera a trilha prática do Python All-in-One For Dummies a partir de ferramentas/missoes/capNN.py.

  praticar/capNN_*.ipynb   -> missão + explicação curta + célula vazia: você digita o código (pacote meu_rover)
  resolvidos/capNN_*.ipynb -> a mesma trilha com o código pronto (pacote gabarito_rover)

Cada arquivo de missão define:
  TITULO, MISSAO (o que e por quê), ENTREGA (o que você terá no fim),
  LEITURA = [(seção do livro, página do PDF em inglês), ...]   -> leitura essencial e opcional
  PASSOS, com quatro tipos de passo:
    ("texto", markdown)                       -> explicação curta (igual nos dois)
    ("tarefa", markdown, codigo)              -> você digita o código numa célula vazia
    ("arquivo", markdown, "nome.py", codigo)  -> você escreve um módulo do projeto (%%writefile já vem pronto)
    ("pronto", markdown, codigo)              -> código de apoio, já preenchido nos dois

Uso (na raiz):  .venv\\Scripts\\python.exe ferramentas\\gerar_cadernos.py
Nunca sobrescreve um caderno de praticar/ que já existe.
"""
import importlib.util
import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACOTES = {"praticar": "meu_rover", "resolvidos": "gabarito_rover"}

PREPARACAO = '''import os, sys, json, time, math, random
sys.path.insert(0, "../comum")                 # dados.py (dados da missão do rover)
sys.path.insert(0, "..")                       # raiz: onde fica o seu pacote PKG/
os.makedirs("../PKG", exist_ok=True)
open("../PKG/__init__.py", "a").close()        # PKG/ é o rover que você constrói ao longo do livro
os.makedirs("../saidas", exist_ok=True)        # arquivos gerados nos exercícios
from dados import *
%load_ext autoreload
%autoreload 2
print("Pronto. Python", sys.version.split()[0], "| seu pacote: PKG")'''


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")[:45].strip("_")


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": s}


def code(s=""):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s}


def caderno(cells):
    for i, c in enumerate(cells):
        c["id"] = f"c{i:03d}"
    return {"cells": cells, "nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"},
                         "language_info": {"name": "python"}}}


def carregar(arq):
    spec = importlib.util.spec_from_file_location(arq.stem, arq)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


total = 0
for arq in sorted((RAIZ / "ferramentas" / "missoes").glob("cap*.py")):
    s = carregar(arq)
    n = int(re.search(r"\d+", arq.stem).group())
    nome = f"cap{n:02d}_{slug(s.TITULO)}.ipynb"
    leitura = "\n".join(f"- {sec} · PDF p. {pag}" for sec, pag in s.LEITURA)
    for pasta, pkg in PACOTES.items():
        sub = lambda t: t.replace("PKG", pkg)
        pratica = pasta == "praticar"
        cab = (f"# Capítulo {n} — {s.TITULO}\n\n"
               f"## Missão\n{s.MISSAO}\n\n"
               f"**No fim deste caderno você terá:** {sub(s.ENTREGA)}\n\n"
               f"**Leitura essencial (opcional, livro em inglês):**\n{leitura}\n\n"
               + ("**Como usar:** cada passo tem uma explicação curta e uma célula vazia. Digite o código e rode com "
                  "`Shift+Enter`. Travou por mais de 10 minutos? O mesmo passo pronto está em "
                  f"`../resolvidos/{nome}`." if pratica else
                  "**Gabarito:** a mesma trilha com o código pronto. Tente primeiro em `praticar/`."))
        cells = [md(cab), md("## Preparação\nConfiguração do caderno (já vem pronta). Rode antes de tudo."),
                 code(sub(PREPARACAO))]
        k = 0
        for passo in s.PASSOS:
            tipo = passo[0]
            if tipo == "texto":
                cells.append(md(sub(passo[1])))
            elif tipo == "pronto":
                cells += [md(sub(passo[1])), code(sub(passo[2]))]
            elif tipo == "tarefa":
                k += 1
                cells += [md(f"### {n}.{k} " + sub(passo[1])), code("" if pratica else sub(passo[2]))]
            elif tipo == "arquivo":
                k += 1
                topo = f"%%writefile ../{pkg}/{passo[2]}\n"
                cells += [md(f"### {n}.{k} " + sub(passo[1]) + f"\n\n_A célula grava `{pkg}/{passo[2]}`: a 1ª linha "
                             "(`%%writefile`) já vem pronta, digite o código embaixo dela._"),
                          code(topo + ("" if pratica else sub(passo[3])))]
        cells.append(md("## Fechamento\n\n- O que eu construí hoje:\n- O que me surpreendeu:\n- O que quero tentar "
                        "sozinho a seguir:\n"))
        destino = RAIZ / pasta / nome
        destino.parent.mkdir(exist_ok=True)
        if pratica and destino.exists():
            print("já existe, mantido:", destino.relative_to(RAIZ))
            continue
        destino.write_text(json.dumps(caderno(cells), ensure_ascii=False, indent=1), encoding="utf-8")
    total += k
    print(f"cap {n:02d}: {k} passos -> {nome}")
print("Total de passos:", total)
