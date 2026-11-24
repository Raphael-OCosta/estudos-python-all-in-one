TITULO = "Inteligência artificial: uma rede neural do zero"
MISSAO = (
    "Dar ao rover a capacidade de **aprender**. Primeiro, uma rede neural escrita à mão com NumPy, para ver cada "
    "peça funcionando: pesos, ativação, propagação, erro e retropropagação. Depois, um classificador de verdade com "
    "scikit-learn, que reconhece dígitos escritos à mão (o livro usa TensorFlow com roupas; a ideia é a mesma, sem "
    "instalar 500 MB), e gráficos com Matplotlib."
)
ENTREGA = "o módulo `PKG/neural.py` (rede neural de 2 camadas em NumPy) e um modelo que classifica imagens com mais de 90% de acerto."
LEITURA = [("AI Is a Collection of Techniques", 378), ("Understanding Neural Networks", 388),
           ("Building a Simple Neural Network in Python", 392), ("Creating a Machine-Learning Network for Detecting Clothes Types", 419),
           ("Visualizing with MatPlotLib", 433)]

PASSOS = [
    ("texto",
     "## Ideia em 30 segundos\n"
     "Um neurônio faz `ativação(soma dos pesos × entradas + viés)`. Uma rede junta camadas de neurônios. Para "
     "aprender, ela:\n"
     "1. faz uma previsão (*forward*);\n"
     "2. mede o erro;\n"
     "3. calcula quanto cada peso contribuiu para o erro (*backpropagation*);\n"
     "4. ajusta um pouquinho na direção que reduz o erro (gradiente).\n\n"
     "Repita milhares de vezes e pronto."),

    ("tarefa",
     "**Um neurônio.** Implemente a sigmoide `1 / (1 + e^-x)` e um neurônio com pesos `[0.8, -0.5]` e viés `0.1`. "
     "Calcule a saída para as entradas `[1, 0]`, `[0, 1]` e `[1, 1]`.",
     r'''import numpy as np

def sigmoide(x):
    return 1 / (1 + np.exp(-x))

w, b = np.array([0.8, -0.5]), 0.1
for x in ([1, 0], [0, 1], [1, 1]):
    print(x, round(float(sigmoide(np.dot(w, x) + b)), 3))'''),

    ("tarefa",
     "**Por que uma camada não basta.** O XOR (saída 1 quando as entradas são diferentes) não tem como ser separado "
     "por uma reta. Monte os 4 casos em `X` e `y` e desenhe-os num gráfico de dispersão com Matplotlib (cores pela "
     "classe).",
     r'''import matplotlib.pyplot as plt
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)
plt.scatter(X[:, 0], X[:, 1], c=y.ravel(), s=200, cmap="coolwarm")
plt.title("XOR: nenhuma reta separa as cores"); plt.show()'''),

    ("arquivo",
     "**Rede neural do zero.** Escreva `neural.py` com a classe `RedeNeural(entradas, ocultos, saidas, semente=0)`:\n"
     "- pesos `W1`, `W2` aleatórios pequenos e vieses `b1`, `b2` zerados;\n"
     "- `prever(X)`: sigmoide nas duas camadas;\n"
     "- `treinar(X, y, epocas=5000, taxa=1.0)`: a cada época faz o *forward*, calcula o erro quadrático médio, "
     "retropropaga (derivada da sigmoide: `s × (1 - s)`) e atualiza os pesos; guarda a perda em `self.perdas`.",
     "neural.py",
     r'''"""Rede neural de 2 camadas escrita só com NumPy."""
import numpy as np


def _sig(x):
    return 1 / (1 + np.exp(-x))


class RedeNeural:
    def __init__(self, entradas: int, ocultos: int, saidas: int, semente: int = 0):
        rng = np.random.default_rng(semente)
        self.W1 = rng.normal(0, 1, (entradas, ocultos))
        self.b1 = np.zeros((1, ocultos))
        self.W2 = rng.normal(0, 1, (ocultos, saidas))
        self.b2 = np.zeros((1, saidas))
        self.perdas: list[float] = []

    def _forward(self, X):
        self.h = _sig(X @ self.W1 + self.b1)
        self.o = _sig(self.h @ self.W2 + self.b2)
        return self.o

    def prever(self, X):
        return self._forward(np.asarray(X, dtype=float))

    def treinar(self, X, y, epocas: int = 5000, taxa: float = 1.0):
        X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
        for _ in range(epocas):
            o = self._forward(X)
            erro = o - y
            self.perdas.append(float((erro ** 2).mean()))
            d_o = erro * o * (1 - o)                       # gradiente na saída
            d_h = (d_o @ self.W2.T) * self.h * (1 - self.h)  # retropropagado para a camada oculta
            self.W2 -= taxa * self.h.T @ d_o / len(X)
            self.b2 -= taxa * d_o.mean(axis=0, keepdims=True)
            self.W1 -= taxa * X.T @ d_h / len(X)
            self.b1 -= taxa * d_h.mean(axis=0, keepdims=True)
        return self
'''),

    ("tarefa",
     "**Treine no XOR.** Crie `RedeNeural(2, 4, 1)`, treine por 10.000 épocas com taxa 2.0, mostre as previsões "
     "arredondadas e desenhe a curva de perda.",
     r'''from PKG.neural import RedeNeural
rede = RedeNeural(2, 4, 1, semente=1).treinar(X, y, epocas=10000, taxa=2.0)
print(rede.prever(X).round(3).ravel(), "| esperado:", y.ravel())
plt.plot(rede.perdas); plt.yscale("log"); plt.xlabel("época"); plt.ylabel("perda"); plt.show()'''),

    ("tarefa",
     "**Imagens de verdade.** Carregue `load_digits` do scikit-learn (imagens 8×8 de dígitos, já vêm na "
     "biblioteca). Mostre 8 imagens com o rótulo no título (`plt.subplots(1, 8)` e `imshow`).",
     r'''from sklearn.datasets import load_digits
dig = load_digits()
print(dig.images.shape)
fig, eixos = plt.subplots(1, 8, figsize=(10, 2))
for ax, img, rot in zip(eixos, dig.images, dig.target):
    ax.imshow(img, cmap="gray_r"); ax.set_title(rot); ax.axis("off")
plt.show()'''),

    ("tarefa",
     "**Treine um classificador.** Separe treino e teste (`train_test_split`, 25% de teste, `random_state=0`), "
     "padronize (`StandardScaler`) e treine um `MLPClassifier(hidden_layer_sizes=(64,), max_iter=500, "
     "random_state=0)`. Mostre a acurácia no teste.",
     r'''from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
Xtr, Xte, ytr, yte = train_test_split(dig.data, dig.target, test_size=0.25, random_state=0)
esc = StandardScaler().fit(Xtr)
mlp = MLPClassifier(hidden_layer_sizes=(64,), max_iter=500, random_state=0).fit(esc.transform(Xtr), ytr)
print("acurácia no teste:", round(mlp.score(esc.transform(Xte), yte), 3))'''),

    ("tarefa",
     "**Onde o modelo erra.** Mostre a matriz de confusão (`ConfusionMatrixDisplay.from_predictions`) e as 6 primeiras "
     "imagens que ele errou, com o título `real→previsto`.",
     r'''from sklearn.metrics import ConfusionMatrixDisplay
prev = mlp.predict(esc.transform(Xte))
ConfusionMatrixDisplay.from_predictions(yte, prev); plt.show()
erros = np.where(prev != yte)[0][:6]
fig, eixos = plt.subplots(1, max(1, len(erros)), figsize=(8, 2))
for ax, i in zip(np.atleast_1d(eixos), erros):
    ax.imshow(Xte[i].reshape(8, 8), cmap="gray_r"); ax.set_title(f"{yte[i]}→{prev[i]}"); ax.axis("off")
plt.show()'''),

    ("tarefa",
     "**Sua rede × scikit-learn.** Use a sua `RedeNeural` para diferenciar só os dígitos 0 e 1: filtre os dados, "
     "normalize os pixels (÷16), treine `RedeNeural(64, 16, 1)` por 2.000 épocas e calcule a acurácia no teste "
     "(previsão > 0,5 = dígito 1).",
     r'''mask_tr, mask_te = np.isin(ytr, [0, 1]), np.isin(yte, [0, 1])
Xa, ya = Xtr[mask_tr] / 16, (ytr[mask_tr] == 1).reshape(-1, 1)
Xb, yb = Xte[mask_te] / 16, (yte[mask_te] == 1)
minha = RedeNeural(64, 16, 1, semente=0).treinar(Xa, ya, epocas=2000, taxa=1.0)
print("acurácia da sua rede (0 × 1):", round(float(((minha.prever(Xb).ravel() > 0.5) == yb).mean()), 3))'''),
]
