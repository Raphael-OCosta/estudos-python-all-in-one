TITULO = "Internet, bibliotecas e o seu próprio pacote"
MISSAO = (
    "Conversar com a Terra pela web. Você vai subir um **servidor HTTP local** (o \"centro de controle\"), buscar "
    "páginas e JSON com `urllib`, extrair dados de HTML e enviar telemetria com POST. Depois, conhecer a biblioteca "
    "padrão e organizar o rover como um **pacote** de verdade."
)
ENTREGA = "o módulo `PKG/rede.py` (cliente do centro de controle) e o pacote do rover com `__init__.py` exportando as peças principais."
LEITURA = [("Seeing How the Web Works", 345), ("Understanding the Python Standard Library", 361),
           ("Importing Python Modules", 367), ("Making Your Own Modules", 370)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "A web é feita de pedidos e respostas:\n"
     "- o cliente faz `GET` (buscar) ou `POST` (enviar);\n"
     "- o servidor responde com um **código** (200 ok, 404 não achado) e um corpo (HTML ou JSON).\n\n"
     "Para não depender da internet nem de sites que mudam, você vai subir o seu próprio servidor dentro do caderno, "
     "numa *thread*."),

    ("pronto",
     "O **centro de controle** (já vem pronto): um servidor local na porta 8765 com uma página HTML em `/`, a "
     "previsão do tempo em JSON em `/clima` e um `POST /telemetria` que guarda o que receber.",
     r'''import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

RECEBIDO = []
PAGINA = """<html><head><title>Centro de Controle</title></head><body>
<h1>Missão Aurora</h1><ul class="avisos"><li>Tempestade de poeira às 11h</li><li>Janela de comunicação: 14h</li>
<li>Prioridade: amostras de hematita</li></ul><a href="/clima">clima</a></body></html>"""

class Controle(BaseHTTPRequestHandler):
    def _responder(self, codigo, corpo, tipo):
        dados = corpo.encode("utf-8")
        self.send_response(codigo); self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados))); self.end_headers(); self.wfile.write(dados)

    def do_GET(self):
        if self.path == "/":
            self._responder(200, PAGINA, "text/html; charset=utf-8")
        elif self.path == "/clima":
            self._responder(200, json.dumps({"poeira": 0.42, "vento_kmh": 35, "alerta": True}), "application/json")
        else:
            self._responder(404, "não encontrado", "text/plain; charset=utf-8")

    def do_POST(self):
        corpo = self.rfile.read(int(self.headers["Content-Length"]))
        RECEBIDO.append(json.loads(corpo))
        self._responder(201, json.dumps({"ok": True, "total": len(RECEBIDO)}), "application/json")

    def log_message(self, *args):
        pass

try:
    servidor.shutdown(); servidor.server_close()
except NameError:
    pass
servidor = ThreadingHTTPServer(("127.0.0.1", 8765), Controle)
threading.Thread(target=servidor.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:8765"
print("centro de controle em", BASE)'''),

    ("tarefa",
     "**GET de uma página.** Com `urllib.request.urlopen`, busque `BASE + \"/\"`, mostre o código de status, o "
     "`Content-Type` e os 120 primeiros caracteres do HTML.",
     r'''from urllib.request import urlopen
with urlopen(BASE + "/") as r:
    print(r.status, r.headers["Content-Type"])
    html = r.read().decode("utf-8")
print(html[:120])'''),

    ("tarefa",
     "**Extrair dados do HTML.** Com `html.parser.HTMLParser`, escreva uma classe que guarda o texto de cada `<li>` e "
     "o `<title>`. Mostre os avisos do centro de controle.",
     r'''from html.parser import HTMLParser

class Avisos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dentro, self.atual, self.avisos, self.titulo = None, "", [], ""

    def handle_starttag(self, tag, attrs):
        self.dentro = tag

    def handle_data(self, data):
        if self.dentro == "li":
            self.avisos.append(data.strip())
        elif self.dentro == "title":
            self.titulo = data.strip()

    def handle_endtag(self, tag):
        self.dentro = None

p = Avisos(); p.feed(html)
print(p.titulo, p.avisos)'''),

    ("tarefa",
     "**JSON pela web e erros HTTP.** Busque `/clima` e converta com `json.loads`. Depois busque `/nada` e trate o "
     "`HTTPError` mostrando o código.",
     r'''from urllib.error import HTTPError
with urlopen(BASE + "/clima") as r:
    clima = json.loads(r.read())
print(clima)
try:
    urlopen(BASE + "/nada")
except HTTPError as e:
    print("erro HTTP", e.code)'''),

    ("tarefa",
     "**POST.** Envie as 3 primeiras leituras como JSON para `/telemetria` com `urllib.request.Request` (método "
     "POST, cabeçalho `Content-Type: application/json`). Mostre a resposta e o que o servidor guardou.",
     r'''from urllib.request import Request
for hora, temp, poeira, bat, dist in LEITURAS[:3]:
    corpo = json.dumps({"hora": hora, "temp": temp, "bateria": bat}).encode("utf-8")
    req = Request(BASE + "/telemetria", data=corpo, method="POST", headers={"Content-Type": "application/json"})
    with urlopen(req) as r:
        print(r.status, json.loads(r.read()))
print(RECEBIDO[-1])'''),

    ("tarefa",
     "**A biblioteca padrão.** Sem instalar nada, use: `statistics` (mediana e desvio das temperaturas), `random` "
     "(com semente, sorteie 3 posições livres do mapa), `collections.Counter` (tipos de amostra) e `pathlib` (liste "
     "os arquivos de `../saidas`).",
     r'''import statistics
from collections import Counter
from pathlib import Path
temps = [l[1] for l in LEITURAS]
print(statistics.median(temps), round(statistics.stdev(temps), 2))
random.seed(1)
livres = [(i, j) for i, linha in enumerate(MAPA) for j, c in enumerate(linha) if c == "."]
print(random.sample(livres, 3))
print(Counter(a["tipo"] for a in AMOSTRAS))
print(sorted(p.name for p in Path("../saidas").iterdir())[:6])'''),

    ("arquivo",
     "**Cliente do centro de controle.** Escreva `rede.py` com `buscar_json(url, tempo_limite=5)` e "
     "`enviar_json(url, dados)`. Os dois devolvem `(ok, dados_ou_erro)`: capture `HTTPError`, `URLError` e "
     "`TimeoutError`, para que a falta de conexão **não** derrube o rover.",
     "rede.py",
     r'''"""Cliente HTTP do rover: nunca deixa a falta de conexão derrubar o sistema."""
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def buscar_json(url: str, tempo_limite: float = 5):
    try:
        with urlopen(url, timeout=tempo_limite) as r:
            return True, json.loads(r.read())
    except HTTPError as e:
        return False, f"HTTP {e.code}"
    except (URLError, TimeoutError) as e:
        return False, f"sem conexão: {e}"


def enviar_json(url: str, dados: dict, tempo_limite: float = 5):
    corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
    req = Request(url, data=corpo, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=tempo_limite) as r:
            return True, json.loads(r.read())
    except HTTPError as e:
        return False, f"HTTP {e.code}"
    except (URLError, TimeoutError) as e:
        return False, f"sem conexão: {e}"
'''),

    ("arquivo",
     "**Transforme a pasta num pacote.** Reescreva o `__init__.py` do pacote para documentar o rover e expor as "
     "peças principais (`status`, os sensores, `Interpretador`, `buscar_json`), com `__version__ = \"0.5\"` e "
     "`__all__`.",
     "__init__.py",
     r'''"""Rover Aurora: pacote construído ao longo do Python All-in-One For Dummies."""
from .comandos import Interpretador
from .painel import status
from .rede import buscar_json, enviar_json
from .sensores import SensorBateria, SensorDistancia, SensorTemperatura

__version__ = "0.5"
__all__ = ["status", "SensorTemperatura", "SensorDistancia", "SensorBateria", "Interpretador",
           "buscar_json", "enviar_json"]
'''),

    ("tarefa",
     "**Use o pacote.** Importe o pacote inteiro (`import PKG as rover`), mostre a versão e o `__all__`, busque "
     "`/clima` e uma porta onde não há servidor (`http://127.0.0.1:9`) com `rover.buscar_json`. Por fim, desligue o "
     "servidor (`servidor.shutdown()`).",
     r'''import importlib
import PKG as rover
importlib.reload(rover)
print(rover.__version__, rover.__all__)
print(rover.buscar_json(BASE + "/clima"))
print(rover.buscar_json("http://127.0.0.1:9/x", tempo_limite=2))
servidor.shutdown(); servidor.server_close()'''),
]
