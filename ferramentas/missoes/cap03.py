TITULO = "Decisões e repetições: o rover anda pelo mapa"
MISSAO = (
    "Fazer o rover tomar decisões (`if`) e repetir ações (`for`, `while`). Ele vai andar pelo `MAPA`, desviar de "
    "rochas, economizar bateria e contar o que encontrou."
)
ENTREGA = "o módulo `PKG/navegacao.py`, com funções para ler o mapa, achar posições e mover o rover sem bater nas rochas."
LEITURA = [("Making Decisions with if", 147), ("Repeating a Process with for", 154), ("Looping with while", 161)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "- `if / elif / else` escolhe um caminho.\n"
     "- `for` percorre uma coleção.\n"
     "- `while` repete enquanto uma condição for verdadeira, e precisa de uma saída garantida, senão roda para "
     "sempre.\n"
     "- `break` sai do laço, `continue` pula para a próxima volta.\n\n"
     "O `MAPA` é uma lista de textos: `MAPA[linha][coluna]`."),

    ("tarefa",
     "**Modo de operação.** Para cada leitura, decida o modo: `CARREGAR` se a bateria < 75; `DESVIAR` se a distância "
     "< 50 cm; `TEMPESTADE` se a poeira > 0.5; senão `EXPLORAR`. A ordem dos testes importa: pense em qual vem "
     "primeiro.",
     r'''for hora, temp, poeira, bat, dist in LEITURAS:
    if bat < 75:
        modo = "CARREGAR"
    elif poeira > 0.5:
        modo = "TEMPESTADE"
    elif dist < 50:
        modo = "DESVIAR"
    else:
        modo = "EXPLORAR"
    print(hora[11:16], modo)'''),

    ("tarefa",
     "**Percorrer o mapa.** Com dois `for` (linhas e colunas, usando `enumerate`), encontre a posição da base `B` e "
     "de todas as amostras `A`. Conte quantas rochas `#` existem.",
     r'''base, amostras, rochas = None, [], 0
for i, linha in enumerate(MAPA):
    for j, celula in enumerate(linha):
        if celula == "B":
            base = (i, j)
        elif celula == "A":
            amostras.append((i, j))
        elif celula == "#":
            rochas += 1
print("base:", base, "| amostras:", amostras, "| rochas:", rochas)'''),

    ("tarefa",
     "**range, break e continue.** Percorra as leituras com `range(len(LEITURAS))`. Pule (`continue`) as que têm "
     "distância > 300 e pare (`break`) na primeira com distância < 20, mostrando a hora do alerta.",
     r'''for i in range(len(LEITURAS)):
    hora, temp, poeira, bat, dist = LEITURAS[i]
    if dist > 300:
        continue
    print("analisando", hora[11:16], dist)
    if dist < 20:
        print("ALERTA de colisão às", hora[11:16])
        break'''),

    ("tarefa",
     "**while com saída garantida.** O rover gasta 3% de bateria por passo e volta para a base quando chega a 30%. "
     "Começando com 87%, quantos passos ele dá? Use `while` e um contador.",
     r'''bateria, passos = 87, 0
while bateria - 3 >= 30:
    bateria -= 3
    passos += 1
print(passos, "passos, bateria final", bateria)'''),

    ("arquivo",
     "**Módulo de navegação.** Escreva `navegacao.py` com:\n"
     "- `DIRECOES = {\"N\": (-1, 0), \"S\": (1, 0), \"L\": (0, 1), \"O\": (0, -1)}`;\n"
     "- `encontrar(mapa, simbolo)`: lista de posições;\n"
     "- `livre(mapa, pos)`: se a posição está dentro do mapa e não é `#`;\n"
     "- `mover(mapa, pos, comandos)`: aplica uma sequência como `\"SSLL\"`, ignora (sem mover) os passos que "
     "bateriam numa rocha e devolve a posição final e a quantidade de batidas evitadas.",
     "navegacao.py",
     r'''"""Navegação do rover pelo mapa."""
DIRECOES = {"N": (-1, 0), "S": (1, 0), "L": (0, 1), "O": (0, -1)}


def encontrar(mapa: list[str], simbolo: str) -> list[tuple]:
    return [(i, j) for i, linha in enumerate(mapa) for j, c in enumerate(linha) if c == simbolo]


def livre(mapa: list[str], pos: tuple) -> bool:
    i, j = pos
    return 0 <= i < len(mapa) and 0 <= j < len(mapa[i]) and mapa[i][j] != "#"


def mover(mapa: list[str], pos: tuple, comandos: str) -> tuple:
    evitadas = 0
    for c in comandos.upper():
        di, dj = DIRECOES[c]
        nova = (pos[0] + di, pos[1] + dj)
        if livre(mapa, nova):
            pos = nova
        else:
            evitadas += 1
    return pos, evitadas
'''),

    ("tarefa",
     "**Teste a navegação.** Partindo da base, execute `\"SSSSLLLL\"` e depois `\"LLNN\"` e mostre as posições e as "
     "batidas evitadas. Desenhe o mapa com um `R` na posição final.",
     r'''from PKG.navegacao import encontrar, mover
pos = encontrar(MAPA, "B")[0]
pos, ev = mover(MAPA, pos, "SSSSLLLL"); print(pos, "evitadas:", ev)
pos, ev = mover(MAPA, pos, "LLNN"); print(pos, "evitadas:", ev)
for i, linha in enumerate(MAPA):
    print("".join("R" if (i, j) == pos else c for j, c in enumerate(linha)))'''),
]
