TITULO = "Arquivos, CSV e JSON: o diário de bordo"
MISSAO = (
    "Fazer o rover **lembrar** de tudo depois de desligar. Você vai gravar e ler um diário de bordo em texto, a "
    "telemetria em **CSV**, a configuração em **JSON** e copiar um arquivo binário (uma \"foto\"). No fim, as "
    "leituras do CSV voltam como objetos."
)
ENTREGA = "o módulo `PKG/diario.py`, que salva e carrega telemetria (CSV) e configuração (JSON)."
LEITURA = [("Opening and Closing Files", 291), ("Reading and Copying a Binary File", 305), ("Conquering CSV Files", 308),
           ("Converting from CSV to Objects and Dictionaries", 317), ("Loading Data from JSON Files", 330),
           ("Dumping Python Data to JSON", 340)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "- Use sempre `with open(...) as f:`: ele fecha o arquivo mesmo se der erro.\n"
     "- Modos: `\"r\"` lê, `\"w\"` sobrescreve, `\"a\"` acrescenta e `\"b\"` é binário. Em texto, informe "
     "`encoding=\"utf-8\"`.\n"
     "- O `csv` cuida de vírgulas e aspas por você.\n"
     "- O `json` converte dicionários e listas em texto e de volta (`dump`/`load`)."),

    ("tarefa",
     "**Diário em texto.** Grave em `../saidas/diario.txt` uma linha por leitura (`hora - modo - bateria`), usando "
     "o modo `\"w\"`. Depois acrescente (`\"a\"`) a linha `FIM DO DIA`. Leia o arquivo de volta, mostre o número de "
     "linhas e as 2 últimas.",
     r'''with open("../saidas/diario.txt", "w", encoding="utf-8") as f:
    for hora, temp, poeira, bat, dist in LEITURAS:
        modo = "DESVIAR" if dist < 50 else "EXPLORAR"
        f.write(f"{hora} - {modo} - {bat}%\n")
with open("../saidas/diario.txt", "a", encoding="utf-8") as f:
    f.write("FIM DO DIA\n")
with open("../saidas/diario.txt", encoding="utf-8") as f:
    linhas = f.readlines()
print(len(linhas), linhas[-2:])'''),

    ("tarefa",
     "**Percorrer linha a linha.** Sem carregar o arquivo inteiro na memória, percorra o diário com `for linha in f` "
     "e conte quantas vezes aparece `DESVIAR`.",
     r'''desvios = 0
with open("../saidas/diario.txt", encoding="utf-8") as f:
    for linha in f:
        desvios += "DESVIAR" in linha
print(desvios)'''),

    ("tarefa",
     "**Arquivo binário.** Crie uma \"foto\" falsa de 50 KB com `os.urandom` em `../saidas/foto.bin`. Copie para "
     "`foto_copia.bin` lendo em blocos de 4 KB (`rb` e `wb`) e confira que as duas são iguais (compare os bytes ou "
     "use `hashlib`).",
     r'''import hashlib
with open("../saidas/foto.bin", "wb") as f:
    f.write(os.urandom(50 * 1024))
with open("../saidas/foto.bin", "rb") as origem, open("../saidas/foto_copia.bin", "wb") as destino:
    while bloco := origem.read(4096):
        destino.write(bloco)
h = lambda p: hashlib.md5(open(p, "rb").read()).hexdigest()
print(h("../saidas/foto.bin") == h("../saidas/foto_copia.bin"), os.path.getsize("../saidas/foto_copia.bin"))'''),

    ("tarefa",
     "**Gravar CSV.** Com `csv.writer`, grave `../saidas/telemetria.csv` com o cabeçalho `hora,temperatura,poeira,"
     "bateria,distancia` e as `LEITURAS`. Use `newline=\"\"` (no Windows, evita linhas em branco).",
     r'''import csv
with open("../saidas/telemetria.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["hora", "temperatura", "poeira", "bateria", "distancia"])
    w.writerows(LEITURAS)
print(open("../saidas/telemetria.csv", encoding="utf-8").read()[:150])'''),

    ("tarefa",
     "**Ler CSV como dicionários.** Com `csv.DictReader`, leia o arquivo, converta os números (tudo chega como texto) "
     "e mostre a média da temperatura. Depois transforme cada linha num objeto `Leitura` (`dataclass`).",
     r'''from dataclasses import dataclass

@dataclass
class Leitura:
    hora: str
    temperatura: float
    poeira: float
    bateria: int
    distancia: int

with open("../saidas/telemetria.csv", encoding="utf-8") as f:
    linhas = list(csv.DictReader(f))
objs = [Leitura(l["hora"], float(l["temperatura"]), float(l["poeira"]), int(l["bateria"]), int(l["distancia"]))
        for l in linhas]
print(round(sum(o.temperatura for o in objs) / len(objs), 2))
objs[0]'''),

    ("tarefa",
     "**JSON.** Grave em `../saidas/config.json` um dicionário de configuração (com uma lista e um dicionário "
     "dentro, e textos acentuados), usando `indent=2` e `ensure_ascii=False`. Leia de volta e confira que é igual. "
     "Tente gravar um `datetime` e veja o erro; resolva com `default=str`.",
     r'''from datetime import datetime
config = {"rover": "Aurora", "modo": "exploração", "sensores": ["temperatura", "distância"],
          "limites": {"bateria_minima": 30, "distancia_minima": 50}}
with open("../saidas/config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
with open("../saidas/config.json", encoding="utf-8") as f:
    print(json.load(f) == config)
try:
    json.dumps({"agora": datetime.now()})
except TypeError as e:
    print("erro:", e)
print(json.dumps({"agora": datetime(2026, 3, 1, 12)}, default=str))'''),

    ("arquivo",
     "**Módulo do diário.** Escreva `diario.py` com:\n"
     "- `salvar_telemetria(caminho, leituras)` e `carregar_telemetria(caminho)` (CSV ↔ lista de dicts com os números "
     "convertidos);\n"
     "- `salvar_config(caminho, config)` e `carregar_config(caminho, padrao)`, que devolve `padrao` se o arquivo não "
     "existir ou estiver corrompido (`json.JSONDecodeError`).",
     "diario.py",
     r'''"""Diário de bordo: telemetria em CSV e configuração em JSON."""
import csv
import json

CAMPOS = ["hora", "temperatura", "poeira", "bateria", "distancia"]
TIPOS = {"temperatura": float, "poeira": float, "bateria": int, "distancia": int}


def salvar_telemetria(caminho: str, leituras: list) -> None:
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(CAMPOS)
        w.writerows(leituras)


def carregar_telemetria(caminho: str) -> list[dict]:
    with open(caminho, encoding="utf-8") as f:
        return [{k: TIPOS.get(k, str)(v) for k, v in linha.items()} for linha in csv.DictReader(f)]


def salvar_config(caminho: str, config: dict) -> None:
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def carregar_config(caminho: str, padrao: dict) -> dict:
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(padrao)
'''),

    ("tarefa",
     "**Teste.** Salve e carregue a telemetria. Mostre a 1ª linha. Carregue uma configuração de um arquivo que não "
     "existe e de um arquivo corrompido (grave `{quebrado` nele antes).",
     r'''from PKG.diario import salvar_telemetria, carregar_telemetria, carregar_config
salvar_telemetria("../saidas/telemetria2.csv", LEITURAS)
print(carregar_telemetria("../saidas/telemetria2.csv")[0])
open("../saidas/quebrado.json", "w").write("{quebrado")
padrao = {"modo": "seguro"}
print(carregar_config("../saidas/nao_existe.json", padrao), carregar_config("../saidas/quebrado.json", padrao))'''),
]
