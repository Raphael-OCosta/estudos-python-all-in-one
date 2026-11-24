TITULO = "Erros sob controle: o rover não pode travar"
MISSAO = (
    "Em Marte não existe botão de reiniciar. Você vai tratar erros com `try / except / else / finally`, ser "
    "específico nas exceções, criar exceções próprias da missão e escrever um interpretador de comandos que "
    "**nunca** derruba o rover."
)
ENTREGA = "o módulo `PKG/comandos.py`, que interpreta comandos de texto da Terra com exceções próprias e registro de falhas."
LEITURA = [("Handling Errors Gracefully", 272), ("Being Specific about Exceptions", 273),
           ("Using try . . . except . . . else . . . finally", 279), ("Raising Your Own Exceptions", 281)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "- `try` tenta o código; `except TipoDeErro` trata o erro.\n"
     "- `else` roda só se não houve erro; `finally` roda **sempre** (é a hora de fechar ou limpar).\n"
     "- Capture o erro mais específico possível. Um `except:` sem tipo esconde bugs.\n"
     "- `raise` levanta um erro, inclusive os seus, que são classes que herdam de `Exception`."),

    ("tarefa",
     "**Tratando erros.** Converta para número os textos `[\"87\", \"abc\", \"\", \"42.5\"]`. Trate o `ValueError` "
     "mostrando qual texto falhou, sem parar o laço.",
     r'''for texto in ["87", "abc", "", "42.5"]:
    try:
        print(float(texto))
    except ValueError:
        print(f"não é número: {texto!r}")'''),

    ("tarefa",
     "**Vários except.** Escreva `media_por_hora(leituras, hora)`, que pega a temperatura de um dicionário hora → "
     "temp e divide pela quantidade de leituras da hora (que pode ser 0). Trate `KeyError` e `ZeroDivisionError` com "
     "mensagens diferentes.",
     r'''temps = {"06:00": -71.5, "12:00": -12.9}
contagem = {"06:00": 1, "12:00": 0}

def media_por_hora(hora):
    try:
        return temps[hora] / contagem[hora]
    except KeyError:
        return f"sem leitura às {hora}"
    except ZeroDivisionError:
        return f"nenhuma leitura contada às {hora}"

for h in ("06:00", "12:00", "09:00"):
    print(h, media_por_hora(h))'''),

    ("tarefa",
     "**else e finally.** Simule abrir o canal de rádio: num `try`, leia uma posição de `LEITURAS` (índice 3 e "
     "depois 99). No `else`, mostre a leitura; no `finally`, mostre \"canal fechado\" em todos os casos.",
     r'''for i in (3, 99):
    try:
        leitura = LEITURAS[i]
    except IndexError:
        print(f"não existe a leitura {i}")
    else:
        print("leitura:", leitura)
    finally:
        print("canal fechado")'''),

    ("tarefa",
     "**Exceções próprias.** Crie `ErroDoRover(Exception)` e duas filhas: `BateriaInsuficiente` e "
     "`ComandoInvalido`. Escreva `andar(bateria, distancia)`, que levanta `BateriaInsuficiente` se o consumo "
     "(`0,01 × distância`) deixar menos de 30%. Capture pela classe **mãe**.",
     r'''class ErroDoRover(Exception):
    pass

class BateriaInsuficiente(ErroDoRover):
    pass

class ComandoInvalido(ErroDoRover):
    pass

def andar(bateria, distancia):
    restante = bateria - 0.01 * distancia
    if restante < 30:
        raise BateriaInsuficiente(f"restariam {restante:.1f}%")
    return restante

for dist in (1000, 6000):
    try:
        print("bateria depois:", andar(73, dist))
    except ErroDoRover as e:
        print(type(e).__name__, "->", e)'''),

    ("arquivo",
     "**Interpretador de comandos.** Escreva `comandos.py` com as exceções do passo anterior e a classe "
     "`Interpretador(bateria=100)`:\n"
     "- `executar(texto)` aceita `ANDAR <cm>`, `GIRAR <graus>` e `FOTO`;\n"
     "- comando desconhecido ou número inválido levantam `ComandoInvalido`; falta de bateria levanta "
     "`BateriaInsuficiente`;\n"
     "- `executar_lote(linhas)` roda todos, **sem parar** em erro, e guarda em `self.falhas` as tuplas "
     "`(linha, tipo do erro, mensagem)`. Devolve quantos deram certo.",
     "comandos.py",
     r'''"""Interpretador de comandos enviados da Terra, à prova de falhas."""


class ErroDoRover(Exception):
    pass


class BateriaInsuficiente(ErroDoRover):
    pass


class ComandoInvalido(ErroDoRover):
    pass


class Interpretador:
    def __init__(self, bateria: float = 100):
        self.bateria = bateria
        self.falhas: list[tuple] = []
        self.fotos = 0

    def executar(self, texto: str) -> str:
        partes = texto.strip().upper().split()
        if not partes:
            raise ComandoInvalido("comando vazio")
        nome, args = partes[0], partes[1:]
        if nome == "FOTO":
            self.fotos += 1
            return f"foto {self.fotos}"
        if nome in ("ANDAR", "GIRAR"):
            try:
                valor = float(args[0])
            except (IndexError, ValueError):
                raise ComandoInvalido(f"{nome} precisa de um número") from None
            if nome == "GIRAR":
                return f"girou {valor % 360:.0f} graus"
            if self.bateria - 0.01 * valor < 30:
                raise BateriaInsuficiente(f"bateria {self.bateria:.1f}% não basta para {valor:.0f} cm")
            self.bateria -= 0.01 * valor
            return f"andou {valor:.0f} cm, bateria {self.bateria:.1f}%"
        raise ComandoInvalido(f"comando desconhecido: {nome}")

    def executar_lote(self, linhas: list[str]) -> int:
        ok = 0
        for linha in linhas:
            try:
                print(self.executar(linha))
                ok += 1
            except ErroDoRover as e:
                self.falhas.append((linha, type(e).__name__, str(e)))
        return ok
'''),

    ("tarefa",
     "**Teste o lote.** Rode a sequência `[\"ANDAR 2000\", \"GIRAR 450\", \"FOTO\", \"PULAR 3\", \"ANDAR muito\", "
     "\"ANDAR 6000\", \"\", \"FOTO\"]` com bateria 80. Mostre quantos deram certo e as falhas numa tabela.",
     r'''from PKG.comandos import Interpretador
rover = Interpretador(bateria=80)
ok = rover.executar_lote(["ANDAR 2000", "GIRAR 450", "FOTO", "PULAR 3", "ANDAR muito", "ANDAR 6000", "", "FOTO"])
print(f"{ok} comandos executados")
for falha in rover.falhas:
    print(falha)'''),
]
