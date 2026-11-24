TITULO = "Primeiros passos: o painel do rover"
MISSAO = (
    "Ligar o rover Aurora pela primeira vez: tipos de dados, operadores, variáveis e regras de sintaxe, já usados "
    "para montar o **painel de status** do rover. O livro gasta muitas páginas instalando ferramentas; aqui o VS "
    "Code e o Jupyter já estão prontos, então vamos direto ao código."
)
ENTREGA = "o módulo `PKG/painel.py`, com a função `status()` que mostra o estado do rover formatado."
LEITURA = [("The Zen of Python", 71), ("Understanding Python Data Types", 84), ("Working with Python Operators", 89),
           ("Creating and Using Variables", 92)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "Todo valor em Python tem um **tipo**: `int` (inteiro), `float` (decimal), `str` (texto), `bool` "
     "(verdadeiro/falso) e `None` (nada). Uma **variável** é só um nome que aponta para um valor. Já a **indentação** "
     "(os 4 espaços) não é estética: ela define os blocos de código."),

    ("tarefa",
     "**O Zen do Python.** Rode `import this` e escolha 2 frases que você quer seguir no seu código.",
     r'''import this'''),

    ("tarefa",
     "**Variáveis do rover.** Crie `nome = \"Aurora\"`, `bateria = 87` (int), `temperatura = -42.5` (float), "
     "`ligado = True` e `missao = None`. Mostre o valor e o `type` de cada uma.",
     r'''nome, bateria, temperatura, ligado, missao = "Aurora", 87, -42.5, True, None
for valor in (nome, bateria, temperatura, ligado, missao):
    print(repr(valor), type(valor).__name__)'''),

    ("tarefa",
     "**Operadores.** O rover andou 1.250 cm em 3 trechos iguais. Calcule com `/`, `//` e `%` o tamanho de cada "
     "trecho e o que sobra. Depois use `**` para a área de uma cratera circular de raio 4,2 m (`math.pi`).",
     r'''import math
total = 1250
print(total / 3, total // 3, total % 3)
print(f"área da cratera: {math.pi * 4.2 ** 2:.2f} m²")'''),

    ("tarefa",
     "**Comparações e lógica.** Escreva expressões que digam se: a bateria está acima de 20, a temperatura está entre "
     "-80 e 0, e o rover pode andar (ligado **e** bateria > 20). Use `and`, `or` e `not`.",
     r'''bateria, temperatura, ligado = 87, -42.5, True
print(bateria > 20, -80 <= temperatura <= 0, ligado and bateria > 20, not ligado)'''),

    ("tarefa",
     "**Conversões.** O sensor manda tudo como texto: `\"87\"`, `\"-42.5\"`, `\"sim\"`. Converta para `int`, "
     "`float` e `bool` (cuidado: `bool(\"não\")` é `True`!). Escreva a conversão certa do texto para booleano.",
     r'''bat, temp, txt = "87", "-42.5", "sim"
print(int(bat) + 1, float(temp) * 2)
print(bool("não"))                       # qualquer texto não vazio é True
print(txt.strip().lower() in ("sim", "s", "true", "1"))'''),

    ("tarefa",
     "**Erros de sintaxe.** Rode cada linha com problema (uma por vez, dentro de `try/except` com `exec`) e leia a "
     "mensagem: um parêntese faltando, um `if` sem dois-pontos e uma indentação errada.",
     r'''for codigo in ('print("ola"', 'if True print(1)', 'if True:\nprint(1)'):
    try:
        exec(codigo)
    except SyntaxError as e:
        print(type(e).__name__, "->", e.msg)'''),

    ("arquivo",
     "**Primeiro módulo do rover.** Escreva `painel.py` com as constantes `NOME = \"Aurora\"` e `VERSAO = \"0.1\"` e "
     "a função `status(bateria, temperatura, ligado)`, que devolve um texto de várias linhas: nome e versão, bateria "
     "com `%`, temperatura com 1 casa e `°C`, e o estado `LIGADO` / `DESLIGADO`.",
     "painel.py",
     r'''"""Painel de status do rover Aurora."""
NOME = "Aurora"
VERSAO = "0.1"


def status(bateria: int, temperatura: float, ligado: bool) -> str:
    estado = "LIGADO" if ligado else "DESLIGADO"
    return (f"Rover {NOME} v{VERSAO}\n"
            f"  bateria: {bateria}%\n"
            f"  temperatura: {temperatura:.1f} °C\n"
            f"  estado: {estado}")
'''),

    ("tarefa",
     "**Teste o painel.** Importe `status` de `PKG.painel` e mostre o painel com a última leitura de `LEITURAS` "
     "(cada leitura é `(hora, temperatura, poeira, bateria, distância)`).",
     r'''from PKG.painel import status
hora, temp, poeira, bat, dist = LEITURAS[-1]
print(status(bat, temp, True))'''),
]
