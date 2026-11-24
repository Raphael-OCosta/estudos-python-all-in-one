TITULO = "Hardware simulado: LEDs, sensores I2C e motores"
MISSAO = (
    "O livro usa um Raspberry Pi, sensores Grove e motores de verdade. Aqui você constrói um **laboratório de "
    "hardware em software**, que reproduz o comportamento real:\n"
    "- pinos GPIO e LED piscando;\n"
    "- barramento I2C com endereços e registradores;\n"
    "- leitura de bytes crus convertida em temperatura;\n"
    "- PWM controlando motor DC;\n"
    "- servo por largura de pulso;\n"
    "- motor de passo pela sequência das bobinas.\n\n"
    "Quando você tiver um Raspberry Pi, a lógica é a mesma; só muda a biblioteca que fala com os pinos."
)
ENTREGA = "o módulo `PKG/hardware.py`, com GPIO, I2C, PWM, motor DC, servo e motor de passo simulados, e um painel de instrumentos."
LEITURA = [("Controlling an LED with Python", 505), ("Understanding I2C", 527), ("Controlling a DC Motor", 562),
           ("Running a Servo Motor", 569), ("Making a Stepper Motor Step", 576)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "- **GPIO**: pinos que ligam (1) ou desligam (0).\n"
     "- **I2C**: dois fios compartilhados por vários sensores; cada um tem um **endereço** (ex.: `0x48`) e "
     "registradores com bytes.\n"
     "- **PWM**: liga e desliga muito rápido; a fração do tempo ligado (*duty cycle*) controla a potência.\n"
     "- **Servo**: vai a um ângulo conforme a largura do pulso (~0,5 a 2,5 ms).\n"
     "- **Motor de passo**: gira um passo por vez, energizando as bobinas numa sequência."),

    ("arquivo",
     "**Laboratório de hardware.** Escreva `hardware.py` com:\n"
     "- `Pino(numero)`: `ligar()`, `desligar()`, `estado` e um histórico `(tempo, estado)` (o tempo é um relógio "
     "simulado em ms, para não esperar de verdade);\n"
     "- `BarramentoI2C`: `conectar(endereco, dispositivo)`, `escanear()` (endereços presentes) e "
     "`ler_registrador(endereco, reg, n=2)`, que devolve bytes;\n"
     "- `SensorTemperaturaI2C(valores)`: o registrador `0x00` devolve a temperatura atual em 2 bytes, em "
     "complemento de dois, com resolução de 1/128 °C; a cada leitura ele avança para o próximo valor;\n"
     "- `MotorDC`: `ajustar(duty)` (entre -1 e 1; o sinal é o sentido) e `rpm` (máximo 120);\n"
     "- `Servo`: `ir_para(angulo)` (0–180), que devolve a largura do pulso em microssegundos (500 a 2.500);\n"
     "- `MotorPasso(passos_por_volta=2048)`: `girar(graus)` devolve a lista de estados das 4 bobinas (sequência de "
     "onda completa) e atualiza o `angulo`.",
     "hardware.py",
     r'''"""Hardware do rover simulado em software (GPIO, I2C, PWM, servo, motor de passo)."""


class Pino:
    def __init__(self, numero: int):
        self.numero = numero
        self.estado = 0
        self.relogio_ms = 0
        self.historico: list[tuple[int, int]] = []

    def _mudar(self, valor: int, duracao_ms: int = 0):
        self.estado = valor
        self.historico.append((self.relogio_ms, valor))
        self.relogio_ms += duracao_ms

    def ligar(self, duracao_ms: int = 0):
        self._mudar(1, duracao_ms)

    def desligar(self, duracao_ms: int = 0):
        self._mudar(0, duracao_ms)


class BarramentoI2C:
    def __init__(self):
        self.dispositivos = {}

    def conectar(self, endereco: int, dispositivo) -> None:
        self.dispositivos[endereco] = dispositivo

    def escanear(self) -> list[int]:
        return sorted(self.dispositivos)

    def ler_registrador(self, endereco: int, reg: int, n: int = 2) -> bytes:
        if endereco not in self.dispositivos:
            raise OSError(f"nenhum dispositivo no endereço {endereco:#04x}")
        return self.dispositivos[endereco].ler(reg, n)


class SensorTemperaturaI2C:
    def __init__(self, valores: list[float]):
        self.valores = list(valores)
        self.i = 0

    def ler(self, reg: int, n: int) -> bytes:
        if reg != 0x00:
            return bytes(n)
        t = self.valores[self.i % len(self.valores)]
        self.i += 1
        cru = int(round(t * 128)) & 0xFFFF          # complemento de dois em 16 bits
        return cru.to_bytes(2, "big")


class MotorDC:
    RPM_MAX = 120

    def __init__(self):
        self.duty = 0.0

    def ajustar(self, duty: float) -> None:
        self.duty = max(-1.0, min(1.0, duty))

    @property
    def rpm(self) -> float:
        return round(self.duty * self.RPM_MAX, 1)


class Servo:
    def __init__(self):
        self.angulo = 90

    def ir_para(self, angulo: float) -> int:
        self.angulo = max(0, min(180, angulo))
        return int(500 + self.angulo / 180 * 2000)


class MotorPasso:
    SEQUENCIA = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]

    def __init__(self, passos_por_volta: int = 2048):
        self.passos_por_volta = passos_por_volta
        self.angulo = 0.0
        self.fase = 0

    def girar(self, graus: float) -> list[tuple]:
        passos = round(abs(graus) / 360 * self.passos_por_volta)
        direcao = 1 if graus >= 0 else -1
        estados = []
        for _ in range(passos):
            self.fase = (self.fase + direcao) % 4
            estados.append(self.SEQUENCIA[self.fase])
        self.angulo = (self.angulo + direcao * passos * 360 / self.passos_por_volta) % 360
        return estados
'''),

    ("tarefa",
     "**LED em código Morse.** Com um `Pino(17)`, pisque `SOS` (S = 3 pontos, O = 3 traços). Ponto = ligado 200 ms; "
     "traço = 600 ms; pausa de 200 ms entre sinais e de 600 ms entre letras. Mostre a duração total e desenhe o sinal "
     "no tempo com `plt.step`.",
     r'''import matplotlib.pyplot as plt
from PKG.hardware import Pino
led = Pino(17)
MORSE = {"S": "...", "O": "---"}
for letra in "SOS":
    for sinal in MORSE[letra]:
        led.ligar(200 if sinal == "." else 600)
        led.desligar(200)
    led.desligar(400)
print("duração:", led.relogio_ms, "ms")
t, v = zip(*led.historico)
plt.step(t, v, where="post"); plt.yticks([0, 1]); plt.xlabel("ms"); plt.title("SOS no pino 17"); plt.show()'''),

    ("tarefa",
     "**Escanear o I2C.** Monte um barramento com o sensor de temperatura em `0x48` (alimentado com as temperaturas "
     "de `LEITURAS`) e um dispositivo qualquer em `0x76`. Escaneie e mostre os endereços em hexadecimal. Tente ler "
     "o endereço `0x20` e trate o `OSError`.",
     r'''from PKG.hardware import BarramentoI2C, SensorTemperaturaI2C
i2c = BarramentoI2C()
i2c.conectar(0x48, SensorTemperaturaI2C([l[1] for l in LEITURAS]))
i2c.conectar(0x76, SensorTemperaturaI2C([0.0]))
print([hex(a) for a in i2c.escanear()])
try:
    i2c.ler_registrador(0x20, 0x00)
except OSError as e:
    print(e)'''),

    ("tarefa",
     "**De bytes para °C.** Leia 4 vezes o registrador `0x00` do sensor `0x48`. Para cada leitura: mostre os bytes "
     "em hexadecimal, junte num inteiro de 16 bits (`int.from_bytes(..., \"big\")`), trate o sinal (complemento de "
     "dois: se `>= 0x8000`, subtraia `0x10000`) e divida por 128.",
     r'''for _ in range(4):
    cru = i2c.ler_registrador(0x48, 0x00)
    valor = int.from_bytes(cru, "big")
    if valor >= 0x8000:
        valor -= 0x10000
    print(cru.hex(), "->", valor / 128, "°C")'''),

    ("tarefa",
     "**PWM e motor DC.** Varie o *duty cycle* de -1 a 1 em passos de 0,25 e mostre a rotação. Faça uma rampa suave "
     "de 0 a 0,8 em 5 passos (aceleração gradual evita derrapar na areia).",
     r'''from PKG.hardware import MotorDC
m = MotorDC()
for d in [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]:
    m.ajustar(d); print(f"duty {d:+.2f} -> {m.rpm:+.1f} rpm")
for passo in range(1, 6):
    m.ajustar(0.8 * passo / 5); print("rampa", m.rpm)'''),

    ("tarefa",
     "**Servo.** Mova o servo da câmera para 0°, 45°, 90°, 135° e 180° e monte a tabela ângulo → pulso (µs). O que "
     "acontece se você pedir 200°?",
     r'''from PKG.hardware import Servo
s = Servo()
for a in (0, 45, 90, 135, 180, 200):
    print(f"{a:3}° -> {s.ir_para(a)} µs (ângulo final {s.angulo})")'''),

    ("tarefa",
     "**Motor de passo.** Gire 90° e mostre quantos passos foram, os 6 primeiros estados das bobinas e o ângulo. "
     "Depois gire -45° e confira o ângulo final.",
     r'''from PKG.hardware import MotorPasso
mp = MotorPasso()
estados = mp.girar(90)
print(len(estados), "passos |", estados[:6], "| ângulo:", mp.angulo)
mp.girar(-45); print("ângulo final:", mp.angulo)'''),

    ("tarefa",
     "**Painel de instrumentos.** No lugar do aplicativo Blynk do livro, faça um painel com Matplotlib (3 gráficos "
     "lado a lado): um medidor de barra da bateria (última leitura), a temperatura ao longo do dia e a distância à "
     "frente com uma faixa vermelha abaixo de 50 cm.",
     r'''import matplotlib.pyplot as plt
horas = [l[0][11:16] for l in LEITURAS]
fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(13, 3.5))
a1.barh(["bateria"], [LEITURAS[-1][3]], color="green"); a1.set_xlim(0, 100); a1.set_title(f"Bateria {LEITURAS[-1][3]}%")
a2.plot(horas, [l[1] for l in LEITURAS], marker="o"); a2.set_title("Temperatura (°C)"); a2.tick_params(axis="x", rotation=60)
a3.bar(horas, [l[4] for l in LEITURAS]); a3.axhspan(0, 50, color="red", alpha=0.2); a3.set_title("Distância à frente (cm)")
a3.tick_params(axis="x", rotation=60)
plt.tight_layout(); plt.show()'''),
]
