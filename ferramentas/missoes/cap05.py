TITULO = "Dicionários: o catálogo da missão"
MISSAO = (
    "Usar dicionários, a estrutura mais usada em Python, para montar o **catálogo de amostras** e a "
    "**configuração** do rover. Você vai criar, ler com segurança, percorrer, copiar sem armadilhas, apagar e usar "
    "dicionários com várias chaves e aninhados."
)
ENTREGA = "o módulo `PKG/catalogo.py`, com o catálogo de amostras indexado por id e agrupado por tipo."
LEITURA = [("Creating a Data Dictionary", 192), ("Looping through a Dictionary", 200), ("Data Dictionary Methods", 201),
           ("Copying a Dictionary", 202), ("Having Fun with Multi-Key Dictionaries", 206)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "Um dicionário liga **chaves** a **valores** e acha qualquer chave instantaneamente.\n"
     "- `d[chave]` dá erro se a chave não existe; `d.get(chave, padrão)` não dá.\n"
     "- `items()` percorre os pares.\n"
     "- Cuidado: `b = a` **não copia**: os dois nomes apontam para o mesmo dicionário."),

    ("tarefa",
     "**Configuração do rover.** Crie o dicionário `config` com `velocidade_max` (cm/s), `bateria_minima`, `camera` "
     "(True) e `modo` (\"EXPLORAR\"). Mude o modo, acrescente `antena`, leia uma chave inexistente com `get` e mostre "
     "`len`, `keys` e `values`.",
     r'''config = {"velocidade_max": 15, "bateria_minima": 30, "camera": True, "modo": "EXPLORAR"}
config["modo"] = "COLETAR"
config["antena"] = "alto ganho"
print(config.get("laser", "não instalado"), len(config))
print(list(config.keys()), list(config.values()))'''),

    ("tarefa",
     "**Percorrer.** Percorra `config.items()` mostrando `chave = valor` em ordem alfabética das chaves.",
     r'''for chave, valor in sorted(config.items()):
    print(f"{chave:15} = {valor}")'''),

    ("tarefa",
     "**Métodos úteis.** Com `update`, mude 2 valores de uma vez; com `setdefault`, garanta uma chave `log` com uma "
     "lista vazia e acrescente uma mensagem; com `pop`, remova `antena` guardando o valor.",
     r'''config.update({"velocidade_max": 10, "camera": False})
config.setdefault("log", []).append("configuração atualizada")
antena = config.pop("antena")
print(antena, config)'''),

    ("tarefa",
     "**A armadilha da cópia.** Faça `b = config` e mude `b[\"modo\"]`: o que acontece com `config`? Refaça com "
     "`config.copy()`. Depois mostre que `copy()` é **raso**: mexer na lista `log` da cópia altera a original. "
     "Resolva com `copy.deepcopy`.",
     r'''import copy
b = config
b["modo"] = "TESTE"
print(config["modo"])                        # mudou junto: é o mesmo objeto
c = config.copy()
c["log"].append("mexi na cópia")
print(config["log"])                         # a lista interna é compartilhada
d = copy.deepcopy(config)
d["log"].append("só na cópia profunda")
print(config["log"], "|", d["log"])'''),

    ("tarefa",
     "**Dicionários aninhados e com várias chaves.** Monte `leituras_por_hora`: a chave é a hora (`HH:MM`) e o valor "
     "é um dicionário com `temp`, `bateria` e `dist`. Mostre a temperatura das 12:00. Depois crie um dicionário cuja "
     "chave é a **tupla** `(linha, coluna)` e cujo valor é a lista de ids das amostras naquela posição.",
     r'''leituras_por_hora = {l[0][11:16]: {"temp": l[1], "bateria": l[3], "dist": l[4]} for l in LEITURAS}
print(leituras_por_hora["12:00"]["temp"])
por_pos = {}
for a in AMOSTRAS:
    por_pos.setdefault(a["pos"], []).append(a["id"])
print(por_pos)'''),

    ("tarefa",
     "**Apagar com segurança.** Remova de `leituras_por_hora` todas as horas com bateria abaixo de 80. Por que não "
     "dá para apagar enquanto percorre o próprio dicionário? Percorra uma cópia das chaves (`list(...)`).",
     r'''for hora in list(leituras_por_hora):
    if leituras_por_hora[hora]["bateria"] < 80:
        del leituras_por_hora[hora]
print(list(leituras_por_hora))'''),

    ("arquivo",
     "**Módulo do catálogo.** Escreva `catalogo.py` com:\n"
     "- `indexar(amostras)`: dicionário id → amostra;\n"
     "- `agrupar_por_tipo(amostras)`: tipo → lista de ids;\n"
     "- `resumo(amostras)`: tipo → `{\"quantidade\": n, \"massa_total_g\": soma}`.",
     "catalogo.py",
     r'''"""Catálogo de amostras coletadas pelo rover."""


def indexar(amostras: list[dict]) -> dict:
    return {a["id"]: a for a in amostras}


def agrupar_por_tipo(amostras: list[dict]) -> dict:
    grupos = {}
    for a in amostras:
        grupos.setdefault(a["tipo"], []).append(a["id"])
    return grupos


def resumo(amostras: list[dict]) -> dict:
    saida = {}
    for a in amostras:
        r = saida.setdefault(a["tipo"], {"quantidade": 0, "massa_total_g": 0.0})
        r["quantidade"] += 1
        r["massa_total_g"] = round(r["massa_total_g"] + a["massa_g"], 1)
    return saida
'''),

    ("tarefa",
     "**Teste o catálogo.** Mostre a amostra `AM-003` pelo índice, os grupos por tipo e o resumo.",
     r'''from PKG.catalogo import indexar, agrupar_por_tipo, resumo
print(indexar(AMOSTRAS)["AM-003"])
print(agrupar_por_tipo(AMOSTRAS))
resumo(AMOSTRAS)'''),
]
