r"""Roda os cadernos de resolvidos/ (gabarito) e mostra o primeiro erro de cada um.

Uso (na raiz):
  .venv\Scripts\python.exe ferramentas\testar_cadernos.py          -> todos os capítulos
  .venv\Scripts\python.exe ferramentas\testar_cadernos.py 3 6      -> só os capítulos 3 e 6
"""
import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

RAIZ = Path(__file__).resolve().parent.parent
caps = {int(a) for a in sys.argv[1:]}
erros = 0
for nb_path in sorted((RAIZ / "resolvidos").glob("cap*.ipynb")):
    if caps and int(nb_path.name[3:5]) not in caps:
        continue
    nb = nbformat.read(nb_path, as_version=4)
    try:
        NotebookClient(nb, timeout=600, kernel_name="python3",
                       resources={"metadata": {"path": str(nb_path.parent)}}).execute()
        print("ok  ", nb_path.name)
    except CellExecutionError as e:
        erros += 1
        linhas = [l for l in str(e).splitlines() if l.strip()]
        print("ERRO", nb_path.name, "->", " | ".join(linhas[-3:])[:400])
print("Cadernos com erro:", erros)
sys.exit(1 if erros else 0)
