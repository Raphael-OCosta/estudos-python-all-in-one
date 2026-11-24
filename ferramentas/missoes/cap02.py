TITULO = "Números, texto, datas e fusos horários"
MISSAO = (
    "Tratar os dados brutos que chegam do rover: arredondar e formatar números, limpar e montar textos, converter "
    "horários em UTC para o fuso de cada pessoa da equipe na Terra e calcular quanto tempo passou entre leituras."
)
ENTREGA = "o módulo `PKG/formatos.py`, com funções para formatar leituras e converter horários entre fusos."
LEITURA = [("Calculating Numbers with Functions", 105), ("Formatting Numbers", 111), ("Manipulating Strings", 121),
           ("Uncovering Dates and Times", 128), ("Working with Time Zones", 140)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "- `round`, `abs`, `math` e as f-strings (`f\"{x:.2f}\"`) resolvem quase toda formatação de números.\n"
     "- Textos têm dezenas de métodos (`strip`, `split`, `upper`, `replace`, `startswith`...).\n"
     "- Para datas, o padrão é: guardar sempre em **UTC** e converter para o fuso local só na hora de mostrar "
     "(`zoneinfo`)."),

    ("tarefa",
     "**Funções numéricas.** Com as temperaturas de `LEITURAS`, mostre a mínima, a máxima, a amplitude "
     "(`max - min`), a média arredondada em 1 casa e a raiz quadrada da amplitude (`math.sqrt`).",
     r'''temps = [l[1] for l in LEITURAS]
amplitude = max(temps) - min(temps)
print(min(temps), max(temps), round(amplitude, 1), round(sum(temps) / len(temps), 1), round(math.sqrt(amplitude), 2))'''),

    ("tarefa",
     "**Formatar números.** Mostre a distância 1250.5678 cm de 5 formas com f-strings: 2 casas, sem casas, com "
     "separador de milhar (`,`), em notação científica e como porcentagem de 5.000 cm (`:.1%`). Depois alinhe uma "
     "tabelinha de 3 leituras com largura fixa (`:>8`).",
     r'''d = 1250.5678
print(f"{d:.2f} | {d:.0f} | {d:,.2f} | {d:.3e} | {d / 5000:.1%}")
for hora, temp, poeira, bat, dist in LEITURAS[:3]:
    print(f"{hora[11:16]:>6} {temp:>8.1f} °C {bat:>5}% {dist:>6} cm")'''),

    ("tarefa",
     "**Números estranhos.** Mostre que `0.1 + 0.2 != 0.3`, resolva com `math.isclose` e com `decimal.Decimal(\"0.1\")`. "
     "Use também `fractions.Fraction(1, 3) * 3`.",
     r'''from decimal import Decimal
from fractions import Fraction
print(0.1 + 0.2, 0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3))
print(Decimal("0.1") + Decimal("0.2"), Fraction(1, 3) * 3)'''),

    ("tarefa",
     "**Textos.** A mensagem do rover chega assim: `\"  status: OK ; bateria=87 ; modo=EXPLORAR  \"`. Limpe os "
     "espaços, separe pelo `;`, transforme num dicionário (`chave: valor`, com `=` ou `:`) e mostre o modo em "
     "minúsculas. Por fim, junte as chaves numa só frase com `\", \".join`.",
     r'''msg = "  status: OK ; bateria=87 ; modo=EXPLORAR  "
campos = {}
for parte in msg.strip().split(";"):
    chave, valor = parte.replace(":", "=").split("=", 1)
    campos[chave.strip()] = valor.strip()
print(campos, campos["modo"].lower())
print(", ".join(campos))'''),

    ("tarefa",
     "**Datas.** Converta a hora da primeira e da última leitura com `datetime.fromisoformat`. Calcule quanto tempo "
     "passou (`timedelta`), em horas, e mostre a data por extenso no formato `01/03/2026 06:00`.",
     r'''from datetime import datetime
inicio = datetime.fromisoformat(LEITURAS[0][0])
fim = datetime.fromisoformat(LEITURAS[-1][0])
duracao = fim - inicio
print(duracao, duracao.total_seconds() / 3600, "horas")
print(inicio.strftime("%d/%m/%Y %H:%M"))'''),

    ("tarefa",
     "**Fusos horários.** As leituras estão em UTC. Para cada pessoa de `EQUIPE`, mostre que horas eram na cidade "
     "dela quando chegou a leitura das 12:00 UTC (`ZoneInfo`). Quem estava dormindo (entre 23h e 6h)?",
     r'''from datetime import datetime, timezone
from zoneinfo import ZoneInfo
utc = datetime.fromisoformat("2026-03-01T12:00:00").replace(tzinfo=timezone.utc)
for p in EQUIPE:
    local = utc.astimezone(ZoneInfo(p["fuso"]))
    dormindo = local.hour >= 23 or local.hour < 6
    print(f"{p['nome']:6} {p['cidade']:8} {local:%d/%m %H:%M} {'(dormindo)' if dormindo else ''}")'''),

    ("arquivo",
     "**Módulo de formatos.** Escreva `formatos.py` com `formatar_leitura(leitura)`, que devolve uma linha alinhada "
     "com hora, temperatura, bateria e distância, e `para_fuso(hora_utc_iso, fuso)`, que devolve o `datetime` no fuso "
     "pedido.",
     "formatos.py",
     r'''"""Formatação de leituras e conversão de fusos horários."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def formatar_leitura(leitura: tuple) -> str:
    hora, temp, poeira, bateria, dist = leitura
    return f"{hora[11:16]:>5} | {temp:>7.1f} °C | poeira {poeira:.2f} | {bateria:>3}% | {dist:>4} cm"


def para_fuso(hora_utc_iso: str, fuso: str) -> datetime:
    utc = datetime.fromisoformat(hora_utc_iso).replace(tzinfo=timezone.utc)
    return utc.astimezone(ZoneInfo(fuso))
'''),

    ("tarefa",
     "**Use o módulo.** Mostre todas as leituras formatadas e a hora da última leitura no fuso de Tóquio.",
     r'''from PKG.formatos import formatar_leitura, para_fuso
for l in LEITURAS:
    print(formatar_leitura(l))
print(para_fuso(LEITURAS[-1][0], "Asia/Tokyo"))'''),
]
