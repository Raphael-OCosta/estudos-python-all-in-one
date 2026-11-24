TITULO = "Robótica: o rover autônomo"
MISSAO = (
    "Juntar tudo num **robô autônomo**. Você vai escrever uma interface de alto nível (andar, girar, medir a "
    "distância à frente) sobre o mapa, coordenar sensores e motores para não bater, dar ao rover um **cérebro** que "
    "planeja rotas (busca em largura) para coletar todas as amostras e voltar à base, e terminar com IA: um modelo "
    "treinado que olha a \"câmera\" e decide para onde virar para perseguir uma bola."
)
ENTREGA = "os módulos `PKG/robo.py` (interface do robô) e `PKG/cerebro.py` (planejador de missão), e um rover que completa a missão sozinho."
LEITURA = [("Understanding the Main Parts of a Robot", 594), ("Building a Simple, High-Level Python Interface", 619),
           ("Coordinating Motor Movements with Sensors", 635), ("Making a Python Brain for Our Robot", 639),
           ("Machine Learning Using TensorFlow", 651), ("The FindAndChaseTheBall.py Python Program", 673)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "Todo robô tem:\n"
     "- **sensores** (percebe);\n"
     "- **controlador** (decide);\n"
     "- **atuadores** (age);\n"
     "- energia.\n\n"
     "Uma boa interface de alto nível esconde os detalhes (\"ande 3 passos\" em vez de \"PWM 0,6 por 2,3 s\"). O "
     "cérebro fica em cima dela e roda o ciclo perceber → decidir → agir."),

    ("arquivo",
     "**Interface do robô.** Escreva `robo.py` com a classe `Robo(mapa, inicio=None)`:\n"
     "- estado: `pos` (começa na base `B`), `direcao` (`\"N\"`, `\"L\"`, `\"S\"`, `\"O\"`), `bateria` (100), "
     "`coletadas` (conjunto) e `registro` (lista de ações);\n"
     "- `girar_direita()` e `girar_esquerda()` (custam 0,2% de bateria);\n"
     "- `distancia_frente()`: quantas células livres até uma rocha, olhando na direção atual (o \"ultrassom\");\n"
     "- `frente(passos=1)`: anda até `passos` células, para antes de uma rocha, custa 1% por célula e devolve "
     "quantas andou;\n"
     "- `coletar()`: se estiver sobre um `A` ainda não coletado, guarda a posição;\n"
     "- `desenhar()`: o mapa com a seta do robô (`^ > v <`) e as amostras já coletadas como `x`.",
     "robo.py",
     r'''"""Interface de alto nível do rover sobre o mapa."""
DIRS = ["N", "L", "S", "O"]
PASSO = {"N": (-1, 0), "L": (0, 1), "S": (1, 0), "O": (0, -1)}
SETA = {"N": "^", "L": ">", "S": "v", "O": "<"}


class Robo:
    def __init__(self, mapa: list[str], inicio: tuple | None = None):
        self.mapa = mapa
        self.pos = inicio or next((i, j) for i, l in enumerate(mapa) for j, c in enumerate(l) if c == "B")
        self.direcao = "N"
        self.bateria = 100.0
        self.coletadas: set[tuple] = set()
        self.registro: list[str] = []

    def _livre(self, p):
        i, j = p
        return 0 <= i < len(self.mapa) and 0 <= j < len(self.mapa[i]) and self.mapa[i][j] != "#"

    def _virar(self, delta):
        self.direcao = DIRS[(DIRS.index(self.direcao) + delta) % 4]
        self.bateria -= 0.2
        self.registro.append(f"girar -> {self.direcao}")

    def girar_direita(self):
        self._virar(1)

    def girar_esquerda(self):
        self._virar(-1)

    def distancia_frente(self) -> int:
        di, dj = PASSO[self.direcao]
        n, p = 0, self.pos
        while self._livre((p[0] + di, p[1] + dj)):
            p = (p[0] + di, p[1] + dj)
            n += 1
        return n

    def frente(self, passos: int = 1) -> int:
        di, dj = PASSO[self.direcao]
        andou = 0
        for _ in range(passos):
            nova = (self.pos[0] + di, self.pos[1] + dj)
            if not self._livre(nova) or self.bateria < 1:
                break
            self.pos, self.bateria, andou = nova, self.bateria - 1, andou + 1
        self.registro.append(f"frente {andou}/{passos} -> {self.pos}")
        return andou

    def coletar(self) -> bool:
        i, j = self.pos
        if self.mapa[i][j] == "A" and self.pos not in self.coletadas:
            self.coletadas.add(self.pos)
            self.registro.append(f"coletou {self.pos}")
            return True
        return False

    def desenhar(self) -> str:
        linhas = []
        for i, l in enumerate(self.mapa):
            linhas.append("".join(SETA[self.direcao] if (i, j) == self.pos else
                                  ("x" if (i, j) in self.coletadas else c) for j, c in enumerate(l)))
        return "\n".join(linhas)
'''),

    ("tarefa",
     "**Teste a interface.** Crie o robô, gire para o Sul, meça a distância à frente, ande 10 (ele deve parar antes "
     "da rocha), gire para o Leste, ande 2, e mostre o desenho, a bateria e o registro.",
     r'''from PKG.robo import Robo
r = Robo(MAPA)
r.girar_direita(); r.girar_direita()
print("livre à frente:", r.distancia_frente())
print("andou:", r.frente(10))
r.girar_esquerda(); print("andou:", r.frente(2))
print(r.desenhar()); print(round(r.bateria, 1), r.registro)'''),

    ("tarefa",
     "**Sensores + motores: seguir a parede.** Implemente a regra da mão direita: a cada ciclo, se a direita estiver "
     "livre, vira à direita e anda; senão, se a frente estiver livre, anda; senão, vira à esquerda. Rode 60 ciclos "
     "coletando as amostras pelo caminho. Quantas o rover pegou e quanta bateria sobrou?",
     r'''r = Robo(MAPA)
for _ in range(60):
    r.girar_direita()
    if r.distancia_frente() > 0:
        r.frente(1)
    else:
        r.girar_esquerda()
        while r.distancia_frente() == 0:
            r.girar_esquerda()
        r.frente(1)
    r.coletar()
print(r.desenhar())
print("coletadas:", len(r.coletadas), "| bateria:", round(r.bateria, 1))'''),

    ("arquivo",
     "**O cérebro.** Escreva `cerebro.py` com:\n"
     "- `caminho(mapa, inicio, fim)`: busca em largura (BFS, com `collections.deque`) e devolve a lista de posições "
     "do menor caminho (ou `None`);\n"
     "- `para_comandos(caminho)`: transforma posições em direções (`\"N\"`, `\"S\"`, `\"L\"`, `\"O\"`);\n"
     "- `executar(robo, direcoes)`: gira o robô até a direção certa e anda 1 a cada passo;\n"
     "- `missao_completa(robo)`: visita as amostras sempre indo para a mais próxima **pelo caminho real**, coleta "
     "cada uma, volta à base e devolve um resumo (coletadas, passos, bateria).",
     "cerebro.py",
     r'''"""Cérebro do rover: planejamento de rotas com busca em largura."""
from collections import deque

from .robo import DIRS, PASSO


def caminho(mapa, inicio, fim):
    fila, veio_de = deque([inicio]), {inicio: None}
    while fila:
        atual = fila.popleft()
        if atual == fim:
            rota = []
            while atual is not None:
                rota.append(atual)
                atual = veio_de[atual]
            return rota[::-1]
        for di, dj in PASSO.values():
            v = (atual[0] + di, atual[1] + dj)
            if 0 <= v[0] < len(mapa) and 0 <= v[1] < len(mapa[0]) and mapa[v[0]][v[1]] != "#" and v not in veio_de:
                veio_de[v] = atual
                fila.append(v)
    return None


def para_comandos(rota):
    inverso = {v: k for k, v in PASSO.items()}
    return [inverso[(b[0] - a[0], b[1] - a[1])] for a, b in zip(rota, rota[1:])]


def executar(robo, direcoes):
    for d in direcoes:
        while robo.direcao != d:
            if (DIRS.index(d) - DIRS.index(robo.direcao)) % 4 == 3:
                robo.girar_esquerda()
            else:
                robo.girar_direita()
        robo.frente(1)


def missao_completa(robo):
    base = robo.pos
    alvos = {(i, j) for i, l in enumerate(robo.mapa) for j, c in enumerate(l) if c == "A"}
    passos = 0
    while alvos - robo.coletadas:
        rotas = {a: caminho(robo.mapa, robo.pos, a) for a in alvos - robo.coletadas}
        rotas = {a: r for a, r in rotas.items() if r}
        if not rotas:
            break
        alvo = min(rotas, key=lambda a: len(rotas[a]))
        executar(robo, para_comandos(rotas[alvo]))
        passos += len(rotas[alvo]) - 1
        robo.coletar()
    volta = caminho(robo.mapa, robo.pos, base)
    executar(robo, para_comandos(volta))
    passos += len(volta) - 1
    return {"coletadas": len(robo.coletadas), "passos": passos, "bateria": round(robo.bateria, 1),
            "na_base": robo.pos == base}
'''),

    ("tarefa",
     "**Missão autônoma.** Rode `missao_completa` num robô novo e compare com o \"seguir a parede\": quantas "
     "amostras, quantos passos e quanta bateria sobrou. Mostre o desenho final.",
     r'''from PKG.cerebro import caminho, missao_completa
r2 = Robo(MAPA)
print(missao_completa(r2))
print(r2.desenhar())'''),

    ("tarefa",
     "**IA no robô: a câmera.** Simule a câmera do rover: uma imagem de 1×30 pixels (brilho de 0 a 1) com ruído e, "
     "às vezes, uma \"bola\" clara (uma faixa de 4 pixels com brilho ~0,9) em uma posição aleatória. O rótulo é "
     "`esquerda`, `frente` ou `direita` (terço da imagem onde está o centro da bola) ou `nenhuma`. Gere 3.000 "
     "exemplos com semente fixa.",
     r'''import numpy as np
rng = np.random.default_rng(7)

def camera(rng):
    img = rng.uniform(0, 0.4, 30)
    if rng.random() < 0.25:
        return img, "nenhuma"
    c = int(rng.integers(2, 28))
    img[c - 2:c + 2] = rng.uniform(0.8, 1.0, 4)
    return img, ["esquerda", "frente", "direita"][min(2, c // 10)]

dados = [camera(rng) for _ in range(3000)]
Xc = np.array([d[0] for d in dados]); yc = np.array([d[1] for d in dados])
print(Xc.shape, {k: int((yc == k).sum()) for k in set(yc)})'''),

    ("tarefa",
     "**Treine o \"olho\" do robô.** Treine um `RandomForestClassifier(n_estimators=100, random_state=0)` com 80% "
     "dos dados e mostre a acurácia no restante.",
     r'''from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
Xa, Xb, ya, yb = train_test_split(Xc, yc, test_size=0.2, random_state=0)
olho = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xa, ya)
print("acurácia:", round(olho.score(Xb, yb), 3))'''),

    ("tarefa",
     "**Persiga a bola.** Simule a perseguição: a bola começa num ângulo aleatório entre -90° e 90° em relação à "
     "frente do robô. A câmera vê o ângulo como posição na imagem (`c = 15 + ângulo / 6`; fora de 0–29 = não vê). A "
     "cada ciclo o modelo decide: `esquerda` (gira +15°), `direita` (-15°), `frente` (avança: a distância cai 20%) ou "
     "`nenhuma` (gira 30° procurando). Considere que pegou quando a distância < 0,3. Rode 5 perseguições e mostre "
     "em quantos ciclos cada uma terminou.",
     r'''def imagem_do_angulo(angulo, rng):
    img = rng.uniform(0, 0.4, 30)
    c = int(round(15 + angulo / 6))
    if 2 <= c <= 27:
        img[c - 2:c + 2] = rng.uniform(0.8, 1.0, 4)
    return img

def perseguir(rng, max_ciclos=60):
    angulo, distancia = rng.uniform(-90, 90), 5.0      # ângulo da bola em relação à frente do robô
    for ciclo in range(1, max_ciclos + 1):
        decisao = olho.predict([imagem_do_angulo(angulo, rng)])[0]
        if decisao == "esquerda":
            angulo += 15
        elif decisao == "direita":
            angulo -= 15
        elif decisao == "frente":
            distancia *= 0.8
        else:
            angulo += 30
        angulo = (angulo + 180) % 360 - 180
        if distancia < 0.3:
            return ciclo
    return None

rng2 = np.random.default_rng(3)
print([perseguir(rng2) for _ in range(5)])'''),

    ("texto",
     "## E com um robô de verdade?\n"
     "A arquitetura é a mesma: `robo.py` passa a chamar a biblioteca do fabricante (no livro, o kit PiCar-B), em vez "
     "de mexer na grade, e o \"olho\" passa a receber os quadros de uma câmera real reduzidos para poucos pixels. "
     "Como o seu cérebro (`cerebro.py`) só usa a interface de alto nível, ele **não precisa mudar**. Esse é o maior "
     "ganho de separar as camadas."),
]
