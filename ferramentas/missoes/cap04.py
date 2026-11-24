TITULO = "Listas, tuplas e conjuntos"
MISSAO = (
    "Organizar coleções de dados da missão: o histórico de leituras numa **lista** (que muda), coordenadas em "
    "**tuplas** (que não mudam) e tipos de rocha em **conjuntos** (sem repetição). No fim, o rover ganha uma rota "
    "para visitar todas as amostras."
)
ENTREGA = "o módulo `PKG/colecoes.py`, com o histórico de leituras e a rota até as amostras."
LEITURA = [("Defining and Using Lists", 167), ("What's a Tuple and Who Cares?", 183), ("Working with Sets", 185)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "- **Lista** `[ ]`: ordenada e mutável (`append`, `insert`, `remove`, `pop`, `sort`, fatias `[a:b]`).\n"
     "- **Tupla** `( )`: ordenada e **imutável**. Serve para coisas que não devem mudar, como coordenadas, e pode "
     "ser chave de dicionário.\n"
     "- **Conjunto** `{ }`: sem ordem e sem repetição, com operações de união e interseção.\n\n"
     "As compreensões (`[x for x in ...]`) criam listas numa linha."),

    ("tarefa",
     "**Lista de temperaturas.** Monte a lista das temperaturas, acrescente uma nova leitura (`append`), insira um "
     "valor no início (`insert`), remova o menor (`remove(min(...))`) e mostre as 3 primeiras, as 3 últimas e a "
     "lista ordenada da mais quente para a mais fria.",
     r'''temps = [l[1] for l in LEITURAS]
temps.append(-60.0)
temps.insert(0, -75.0)
temps.remove(min(temps))
print(temps[:3], temps[-3:])
print(sorted(temps, reverse=True))'''),

    ("tarefa",
     "**Compreensões.** Em uma linha cada: (a) as horas (`HH:MM`) com distância < 100 cm; (b) a bateria convertida "
     "para fração (0 a 1); (c) os pares `(hora, temperatura)` acima de -20 °C.",
     r'''print([l[0][11:16] for l in LEITURAS if l[4] < 100])
print([l[3] / 100 for l in LEITURAS])
print([(l[0][11:16], l[1]) for l in LEITURAS if l[1] > -20])'''),

    ("tarefa",
     "**Ordenar com chave.** Ordene `AMOSTRAS` pela massa (`key=lambda a: a[\"massa_g\"]`) e mostre o id e a massa da "
     "mais leve e da mais pesada.",
     r'''por_massa = sorted(AMOSTRAS, key=lambda a: a["massa_g"])
print(por_massa[0]["id"], por_massa[0]["massa_g"], "|", por_massa[-1]["id"], por_massa[-1]["massa_g"])'''),

    ("tarefa",
     "**Tuplas.** Desempacote a primeira leitura em 5 variáveis numa linha. Tente mudar um item da tupla dentro de "
     "`try/except TypeError`. Use uma tupla `(linha, coluna)` como chave de um dicionário que conta amostras por "
     "posição.",
     r'''hora, temp, poeira, bat, dist = LEITURAS[0]
print(hora, temp)
try:
    LEITURAS[0][1] = 0
except TypeError as e:
    print("imutável:", e)
por_posicao = {}
for a in AMOSTRAS:
    por_posicao[a["pos"]] = por_posicao.get(a["pos"], 0) + 1
print(por_posicao)'''),

    ("tarefa",
     "**Conjuntos.** O laboratório já conhece `{\"basalto\", \"granito\", \"argila\"}`. Com os tipos das `AMOSTRAS`, "
     "mostre: os tipos coletados (sem repetir), os tipos **novos** para o laboratório (diferença), os comuns "
     "(interseção) e todos juntos (união).",
     r'''conhecidos = {"basalto", "granito", "argila"}
coletados = {a["tipo"] for a in AMOSTRAS}
print(coletados, coletados - conhecidos, coletados & conhecidos, coletados | conhecidos)'''),

    ("arquivo",
     "**Módulo de coleções.** Escreva `colecoes.py` com:\n"
     "- a classe simples `Historico` (com uma lista `itens` e um limite `maximo`): `adicionar(leitura)` descarta a "
     "mais antiga quando passa do limite, e `ultimas(n)` devolve as n mais recentes;\n"
     "- `rota_amostras(inicio, alvos)`: a ordem de visita pelo **vizinho mais próximo** (distância de Manhattan "
     "`|di| + |dj|`), sem repetir posições.",
     "colecoes.py",
     r'''"""Coleções da missão: histórico de leituras e rota de coleta."""


class Historico:
    def __init__(self, maximo: int = 5):
        self.maximo = maximo
        self.itens = []

    def adicionar(self, leitura) -> None:
        self.itens.append(leitura)
        if len(self.itens) > self.maximo:
            self.itens.pop(0)

    def ultimas(self, n: int) -> list:
        return self.itens[-n:]


def rota_amostras(inicio: tuple, alvos: list[tuple]) -> list[tuple]:
    pendentes = list(dict.fromkeys(alvos))      # tira repetidos mantendo a ordem
    rota, atual = [], inicio
    while pendentes:
        prox = min(pendentes, key=lambda p: abs(p[0] - atual[0]) + abs(p[1] - atual[1]))
        rota.append(prox)
        pendentes.remove(prox)
        atual = prox
    return rota
'''),

    ("tarefa",
     "**Teste.** Adicione todas as leituras num `Historico(maximo=4)` e mostre as 2 últimas. Calcule a rota da base "
     "até as posições das `AMOSTRAS`.",
     r'''from PKG.colecoes import Historico, rota_amostras
h = Historico(maximo=4)
for l in LEITURAS:
    h.adicionar(l)
print(len(h.itens), [l[0][11:16] for l in h.ultimas(2)])
print(rota_amostras((1, 1), [a["pos"] for a in AMOSTRAS]))'''),
]
