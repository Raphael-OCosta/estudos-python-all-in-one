TITULO = "Ciência de dados: analisando a missão"
MISSAO = (
    "Aplicar o processo de ciência de dados aos dados da missão:\n"
    "1. capturar;\n"
    "2. limpar;\n"
    "3. explorar;\n"
    "4. modelar;\n"
    "5. comunicar.\n\n"
    "Com NumPy, pandas e Matplotlib, você analisa um mês simulado de telemetria. Depois troca o BigQuery do livro "
    "(que exige conta no Google Cloud) por um conjunto grande gerado localmente: **1 milhão de linhas**, agregadas "
    "em segundos."
)
ENTREGA = "o módulo `PKG/analise.py`, que gera, limpa e resume a telemetria, e um relatório com gráficos da missão."
LEITURA = [("Cooking with Gas: The Five-Step Process of Data Science", 456), ("Introducing NumPy, Pandas, and MatPlotLib", 460),
           ("Doing Your First Data Science Project", 462), ("Reading the Medicare Big Data", 478)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "- **NumPy** faz contas em vetores inteiros, sem laço.\n"
     "- **pandas** é uma planilha programável (`DataFrame`): filtrar, agrupar, juntar, limpar.\n"
     "- **Matplotlib** desenha.\n\n"
     "O segredo para dados grandes é deixar o pandas/NumPy fazer o trabalho em bloco (vetorizado) em vez de usar "
     "`for` linha a linha."),

    ("arquivo",
     "**Gerador de telemetria.** Escreva `analise.py` com `gerar_telemetria(dias=30, semente=0)`. Ela devolve um "
     "`DataFrame` com uma linha por hora, com:\n"
     "- `hora` (`pd.date_range` a partir de 2026-03-01, em UTC);\n"
     "- `temperatura`: um ciclo diário com seno (mínima ~-75 às 5h, máxima ~-10 às 14h) mais ruído;\n"
     "- `poeira` (entre 0 e 1);\n"
     "- `bateria`: cai de dia e recarrega até 100;\n"
     "- `distancia` (0–400).\n\n"
     "Para testar a limpeza, coloque **de propósito** 2% de temperaturas faltando e 5 leituras impossíveis "
     "(+500 °C).",
     "analise.py",
     r'''"""Geração, limpeza e resumo da telemetria do rover."""
import numpy as np
import pandas as pd


def gerar_telemetria(dias: int = 30, semente: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(semente)
    hora = pd.date_range("2026-03-01", periods=dias * 24, freq="h", tz="UTC")
    h = hora.hour.to_numpy()
    temperatura = -42.5 + 32.5 * np.sin((h - 9.5) / 24 * 2 * np.pi) + rng.normal(0, 3, len(h))
    poeira = np.clip(rng.beta(2, 5, len(h)) + 0.15 * (h >= 11) * (h <= 15), 0, 1)
    bateria = np.empty(len(h))
    nivel = 100.0
    for i, hh in enumerate(h):
        nivel = min(100.0, nivel + 6) if (hh < 6 or hh > 20) else max(5.0, nivel - rng.uniform(1, 4))
        bateria[i] = nivel
    distancia = rng.integers(0, 401, len(h))
    df = pd.DataFrame({"hora": hora, "temperatura": temperatura.round(1), "poeira": poeira.round(2),
                       "bateria": bateria.round(1), "distancia": distancia})
    faltando = rng.choice(len(df), int(0.02 * len(df)), replace=False)
    df.loc[faltando, "temperatura"] = np.nan
    df.loc[rng.choice(len(df), 5, replace=False), "temperatura"] = 500.0
    return df


def limpar(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.loc[~df.temperatura.between(-130, 40), "temperatura"] = np.nan    # impossíveis viram faltantes
    df["temperatura"] = df.temperatura.interpolate(limit_direction="both")
    return df


def resumo_diario(df: pd.DataFrame) -> pd.DataFrame:
    return (df.set_index("hora").resample("D")
              .agg(temp_min=("temperatura", "min"), temp_max=("temperatura", "max"),
                   poeira_media=("poeira", "mean"), bateria_min=("bateria", "min")).round(2))
'''),

    ("tarefa",
     "**Capturar e inspecionar.** Importe `numpy`, `pandas` e `matplotlib.pyplot` (como `np`, `pd` e `plt`), gere 30 dias e mostre: `shape`, `head()`, `info()` e `describe()`. Quantos valores "
     "faltam em cada coluna? Há algo impossível nas temperaturas?",
     r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PKG.analise import gerar_telemetria, limpar, resumo_diario
df = gerar_telemetria(30)
print(df.shape)
display(df.head())
df.info()
display(df.describe().round(1))
print(df.isna().sum())'''),

    ("tarefa",
     "**NumPy vetorizado.** Converta todas as temperaturas para Fahrenheit de dois jeitos: com um `for` em Python e "
     "com NumPy direto no array. Compare o tempo com `time.perf_counter` (use 1 milhão de valores aleatórios).",
     r'''arr = np.random.default_rng(0).normal(-40, 20, 1_000_000)
t0 = time.perf_counter(); lista = [c * 9 / 5 + 32 for c in arr]; t_for = time.perf_counter() - t0
t0 = time.perf_counter(); vet = arr * 9 / 5 + 32; t_np = time.perf_counter() - t0
print(f"for: {t_for:.3f}s | NumPy: {t_np:.4f}s | {t_for / t_np:.0f}x mais rápido | iguais: {np.allclose(lista, vet)}")'''),

    ("tarefa",
     "**Limpar.** Use `limpar(df)` e confira: nenhuma temperatura fora de -130 a 40 e nenhum valor faltando. Mostre "
     "as linhas que tinham 500 °C antes e depois.",
     r'''sujas = df.index[df.temperatura > 40]
limpo = limpar(df)
print(limpo.temperatura.between(-130, 40).all(), limpo.temperatura.isna().sum())
pd.DataFrame({"antes": df.loc[sujas, "temperatura"], "depois": limpo.loc[sujas, "temperatura"]})'''),

    ("tarefa",
     "**Explorar.** Calcule a temperatura média por **hora do dia** (`groupby(df.hora.dt.hour)`) e desenhe o ciclo "
     "diário. Em que hora a poeira é maior? Mostre a correlação entre as colunas numéricas.",
     r'''por_hora = limpo.groupby(limpo.hora.dt.hour)[["temperatura", "poeira"]].mean()
ax = por_hora.temperatura.plot(marker="o", title="Ciclo diário da temperatura")
ax.set_xlabel("hora (UTC)"); ax.set_ylabel("°C"); plt.show()
print("hora com mais poeira:", por_hora.poeira.idxmax())
limpo[["temperatura", "poeira", "bateria", "distancia"]].corr().round(2)'''),

    ("tarefa",
     "**Resumo diário e gráfico de comunicação.** Use `resumo_diario` e faça uma figura com 2 gráficos: as faixas "
     "mínima e máxima de temperatura por dia (`fill_between`) e a bateria mínima por dia com uma linha de alerta em 20%.",
     r'''rd = resumo_diario(limpo)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
a1.fill_between(rd.index, rd.temp_min, rd.temp_max, alpha=0.4); a1.set_ylabel("°C"); a1.set_title("Temperatura diária")
a2.plot(rd.index, rd.bateria_min, marker="."); a2.axhline(20, color="red", ls="--"); a2.set_ylabel("bateria mín. %")
plt.tight_layout(); plt.show()
rd.head()'''),

    ("tarefa",
     "**Modelar (simples).** Ajuste uma reta (`np.polyfit`, grau 1) entre poeira e bateria e diga quanto a bateria "
     "cai, em média, para cada +0,1 de poeira.",
     r'''a, b = np.polyfit(limpo.poeira, limpo.bateria, 1)
print(f"bateria ≈ {a:.1f} × poeira + {b:.1f} -> a cada +0,1 de poeira: {a * 0.1:+.2f} pontos")'''),

    ("tarefa",
     "**Dados grandes sem nuvem.** Gere 1 milhão de leituras de 20 rovers fictícios (colunas `rover`, "
     "`temperatura`, `poeira`, com NumPy direto), e com pandas encontre o rover com a maior poeira média e os 3 "
     "mais frios. Grave tudo em CSV, mostre o tamanho do arquivo em MB e meça o tempo total.",
     r'''t0 = time.perf_counter()
rng = np.random.default_rng(42)
n = 1_000_000
grande = pd.DataFrame({"rover": rng.integers(1, 21, n), "temperatura": rng.normal(-45, 18, n).round(1),
                       "poeira": rng.beta(2, 5, n).round(3)})
grande["temperatura"] += grande.rover * 0.5          # cada rover em um lugar um pouco diferente
ag = grande.groupby("rover").agg(poeira_media=("poeira", "mean"), temp_media=("temperatura", "mean"))
print("mais poeira:", ag.poeira_media.idxmax(), "| mais frios:", list(ag.temp_media.nsmallest(3).index))
grande.to_csv("../saidas/grande.csv", index=False)
print(f"{time.perf_counter() - t0:.1f}s | arquivo: {os.path.getsize('../saidas/grande.csv') / 1e6:.1f} MB")'''),
]
