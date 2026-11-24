TITULO = "Funções: comandos reutilizáveis"
MISSAO = (
    "Transformar o código repetido em **funções** com argumentos, valores padrão, retorno de vários valores, "
    "`*args`, `**kwargs` e funções anônimas (`lambda`). O rover ganha uma biblioteca de cálculos de missão."
)
ENTREGA = "o módulo `PKG/calculos.py`, com estatísticas, consumo de bateria e conversões, todos documentados."
LEITURA = [("Creating a Function", 214), ("Passing Information to a Function", 216),
           ("Returning Values from Functions", 226), ("Unmasking Anonymous Functions", 227)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "Uma função empacota um pedaço de lógica com um nome.\n"
     "- A **docstring** explica o que ela faz.\n"
     "- Valores padrão deixam argumentos opcionais.\n"
     "- `return a, b` devolve uma tupla.\n"
     "- `*args` recebe vários argumentos posicionais e `**kwargs` vários nomeados.\n"
     "- `lambda` é uma função de uma linha, útil como `key=` em `sorted`, `max` e `min`."),

    ("tarefa",
     "**Primeira função com docstring.** Escreva `celsius_para_fahrenheit(c)` com docstring e teste com as "
     "temperaturas das 3 primeiras leituras. Mostre a docstring com `help`.",
     r'''def celsius_para_fahrenheit(c):
    """Converte graus Celsius para Fahrenheit."""
    return c * 9 / 5 + 32

print([round(celsius_para_fahrenheit(l[1]), 1) for l in LEITURAS[:3]])
help(celsius_para_fahrenheit)'''),

    ("tarefa",
     "**Padrões e argumentos nomeados.** Escreva `consumo(distancia_cm, terreno=\"plano\", carga_g=0)`, que devolve o "
     "% de bateria gasto: 0,01% por cm, ×1,5 em terreno `\"rochoso\"` e + 0,001% por grama de carga. Chame com só a "
     "distância, com o terreno e com tudo por nome.",
     r'''def consumo(distancia_cm, terreno="plano", carga_g=0):
    """% de bateria gasto para andar distancia_cm."""
    fator = 1.5 if terreno == "rochoso" else 1.0
    return round(distancia_cm * 0.01 * fator + carga_g * 0.001, 2)

print(consumo(500), consumo(500, "rochoso"), consumo(carga_g=300, distancia_cm=500, terreno="rochoso"))'''),

    ("tarefa",
     "**Retornar vários valores.** Escreva `estatisticas(valores)`, que devolve mínimo, máximo e média. Use nas "
     "temperaturas e desempacote em 3 variáveis.",
     r'''def estatisticas(valores):
    """Devolve (mínimo, máximo, média)."""
    return min(valores), max(valores), sum(valores) / len(valores)

mn, mx, media = estatisticas([l[1] for l in LEITURAS])
print(mn, mx, round(media, 2))'''),

    ("tarefa",
     "**`*args` e `**kwargs`.** Escreva `registrar(evento, *detalhes, **dados)`, que monta uma linha como "
     "`[EVENTO] detalhe1 | detalhe2 | chave=valor`. Chame de 3 jeitos.",
     r'''def registrar(evento, *detalhes, **dados):
    partes = list(detalhes) + [f"{k}={v}" for k, v in dados.items()]
    return f"[{evento.upper()}] " + " | ".join(str(p) for p in partes)

print(registrar("inicio"))
print(registrar("coleta", "AM-001", "basalto"))
print(registrar("alerta", "rocha à frente", dist=18, acao="desviar"))'''),

    ("tarefa",
     "**Escopo.** Mostre a diferença entre uma variável local e uma global: uma função que tenta somar 1 a um "
     "contador global sem `global` (capture o `UnboundLocalError`) e outra que **retorna** o novo valor (a forma "
     "recomendada).",
     r'''contador = 0

def incrementa_errado():
    contador += 1

def incrementa(c):
    return c + 1

try:
    incrementa_errado()
except UnboundLocalError as e:
    print("erro:", e)
contador = incrementa(contador)
print(contador)'''),

    ("tarefa",
     "**lambda.** Com `max` e `key=lambda`, ache a leitura com a maior poeira. Ordene a `EQUIPE` pelo tamanho do nome "
     "e use `map` com uma lambda para gerar as baterias em fração.",
     r'''print(max(LEITURAS, key=lambda l: l[2])[0])
print([p["nome"] for p in sorted(EQUIPE, key=lambda p: len(p["nome"]))])
print(list(map(lambda l: l[3] / 100, LEITURAS))[:4])'''),

    ("arquivo",
     "**Módulo de cálculos.** Escreva `calculos.py` com `estatisticas`, `consumo` e `autonomia_cm(bateria, "
     "minima=30, terreno=\"plano\")` (quantos cm o rover anda até chegar à bateria mínima). Cada função tem "
     "docstring e anotações de tipo.",
     "calculos.py",
     r'''"""Cálculos da missão do rover."""


def estatisticas(valores: list[float]) -> tuple[float, float, float]:
    """Devolve (mínimo, máximo, média) de uma lista de números."""
    return min(valores), max(valores), sum(valores) / len(valores)


def consumo(distancia_cm: float, terreno: str = "plano", carga_g: float = 0) -> float:
    """% de bateria gasto para andar distancia_cm, conforme o terreno e a carga."""
    fator = 1.5 if terreno == "rochoso" else 1.0
    return round(distancia_cm * 0.01 * fator + carga_g * 0.001, 2)


def autonomia_cm(bateria: float, minima: float = 30, terreno: str = "plano") -> float:
    """Quantos cm o rover anda até chegar à bateria mínima."""
    fator = 1.5 if terreno == "rochoso" else 1.0
    return max(0.0, (bateria - minima) / (0.01 * fator))
'''),

    ("tarefa",
     "**Teste.** Use `autonomia_cm` com a bateria da última leitura em terreno plano e rochoso.",
     r'''from PKG.calculos import autonomia_cm, estatisticas
bat = LEITURAS[-1][3]
print(autonomia_cm(bat), autonomia_cm(bat, terreno="rochoso"))
print(estatisticas([l[4] for l in LEITURAS]))'''),
]
