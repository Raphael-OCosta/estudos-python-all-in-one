TITULO = "Classes e herança: os sensores do rover"
MISSAO = (
    "Modelar as peças do rover como **objetos**: uma classe base `Sensor` e sensores especializados por **herança** "
    "(temperatura, distância, bateria), com atributos, métodos, propriedades e representação em texto."
)
ENTREGA = "o módulo `PKG/sensores.py`, com a hierarquia de sensores que os próximos capítulos usam."
LEITURA = [("Creating a Class", 238), ("Giving an Object Its Attributes", 240), ("Giving a Class Methods", 246),
           ("Understanding Class Inheritance", 256)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "Uma **classe** é a planta, e o **objeto** é a peça construída a partir dela.\n"
     "- `__init__` prepara o objeto, e `self` é o próprio objeto.\n"
     "- **Herança** (`class Filho(Pai)`) reaproveita o que é comum e muda só o que é diferente; `super()` chama "
     "o pai.\n"
     "- `__repr__` diz como o objeto aparece quando é mostrado."),

    ("tarefa",
     "**Primeira classe.** Escreva `Motor` com `nome` e `velocidade` (começa em 0), os métodos `acelerar(delta)` "
     "(sem passar de 100) e `parar()`, e `__repr__`. Crie dois motores e mostre que cada um tem o seu estado.",
     r'''class Motor:
    def __init__(self, nome):
        self.nome = nome
        self.velocidade = 0

    def acelerar(self, delta):
        self.velocidade = min(100, self.velocidade + delta)

    def parar(self):
        self.velocidade = 0

    def __repr__(self):
        return f"Motor({self.nome!r}, velocidade={self.velocidade})"

esq, dir_ = Motor("esquerdo"), Motor("direito")
esq.acelerar(70); esq.acelerar(50); dir_.acelerar(30)
print(esq, dir_)'''),

    ("tarefa",
     "**Atributo de classe × de instância.** Acrescente a `Motor` um atributo de classe `total = 0` que conta "
     "quantos motores foram criados (incremente no `__init__` com `Motor.total += 1`). Crie 3 e mostre a contagem.",
     r'''class Motor:
    total = 0

    def __init__(self, nome):
        self.nome = nome
        self.velocidade = 0
        Motor.total += 1

for n in ("A", "B", "C"):
    Motor(n)
print(Motor.total)'''),

    ("tarefa",
     "**Propriedade com validação.** Escreva a classe `Bateria` com uma `@property` `nivel` cujo *setter* recusa "
     "valores fora de 0–100 (`ValueError`). Teste um valor válido e um inválido.",
     r'''class Bateria:
    def __init__(self, nivel=100):
        self.nivel = nivel

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):
        if not 0 <= valor <= 100:
            raise ValueError(f"nível inválido: {valor}")
        self._nivel = valor

b = Bateria(); b.nivel = 55; print(b.nivel)
try:
    b.nivel = 140
except ValueError as e:
    print(e)'''),

    ("arquivo",
     "**Hierarquia de sensores.** Escreva `sensores.py` com:\n"
     "- `Sensor(nome, unidade)`: guarda um histórico; `registrar(valor)` valida com `validar()` (no pai, aceita "
     "tudo) e devolve `False` se recusar; `ultimo` (propriedade); `media()`; `__repr__`;\n"
     "- `SensorTemperatura`: unidade `°C`, válido entre -130 e 40;\n"
     "- `SensorDistancia`: unidade `cm`, válido entre 0 e 400, com o método `obstaculo(limite=50)`;\n"
     "- `SensorBateria`: unidade `%`, válido entre 0 e 100, com o método `critica(minima=30)`.\n\n"
     "Os filhos usam `super().__init__`.",
     "sensores.py",
     r'''"""Sensores do rover: uma classe base e especializações por herança."""


class Sensor:
    def __init__(self, nome: str, unidade: str):
        self.nome = nome
        self.unidade = unidade
        self.historico: list[float] = []

    def validar(self, valor: float) -> bool:
        return True

    def registrar(self, valor: float) -> bool:
        if not self.validar(valor):
            return False
        self.historico.append(valor)
        return True

    @property
    def ultimo(self):
        return self.historico[-1] if self.historico else None

    def media(self) -> float:
        return sum(self.historico) / len(self.historico) if self.historico else 0.0

    def __repr__(self):
        return f"{type(self).__name__}({self.nome!r}, último={self.ultimo} {self.unidade}, n={len(self.historico)})"


class SensorTemperatura(Sensor):
    def __init__(self, nome: str = "temperatura"):
        super().__init__(nome, "°C")

    def validar(self, valor: float) -> bool:
        return -130 <= valor <= 40


class SensorDistancia(Sensor):
    def __init__(self, nome: str = "distancia"):
        super().__init__(nome, "cm")

    def validar(self, valor: float) -> bool:
        return 0 <= valor <= 400

    def obstaculo(self, limite: float = 50) -> bool:
        return self.ultimo is not None and self.ultimo < limite


class SensorBateria(Sensor):
    def __init__(self, nome: str = "bateria"):
        super().__init__(nome, "%")

    def validar(self, valor: float) -> bool:
        return 0 <= valor <= 100

    def critica(self, minima: float = 30) -> bool:
        return self.ultimo is not None and self.ultimo < minima
'''),

    ("tarefa",
     "**Teste os sensores.** Crie um de cada, registre os valores de `LEITURAS` (mais um valor inválido de "
     "temperatura, 99) e mostre os objetos, a média da temperatura e se há obstáculo na última leitura.",
     r'''from PKG.sensores import SensorTemperatura, SensorDistancia, SensorBateria
t, d, b = SensorTemperatura(), SensorDistancia(), SensorBateria()
for hora, temp, poeira, bat, dist in LEITURAS:
    t.registrar(temp); d.registrar(dist); b.registrar(bat)
print("aceitou 99 °C?", t.registrar(99))
print(t, d, b, sep="\n")
print(round(t.media(), 1), d.obstaculo(), b.critica())'''),

    ("tarefa",
     "**Polimorfismo.** Coloque os 3 sensores numa lista e, num único `for`, mostre `nome`, `ultimo` e `unidade`. Use "
     "`isinstance` para chamar `obstaculo()` só no sensor de distância.",
     r'''for s in (t, d, b):
    extra = f" | obstáculo: {s.obstaculo()}" if isinstance(s, SensorDistancia) else ""
    print(f"{s.nome:12} {s.ultimo} {s.unidade}{extra}")'''),
]
