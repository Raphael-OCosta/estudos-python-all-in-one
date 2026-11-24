# Estudos — *Python All-in-One For Dummies* (John Shovic e Alan Simpson) · trilha prática

> **A melhor forma de estudar um livro técnico é ler e praticar ao mesmo tempo.**
> Aqui a prática vem primeiro: cada capítulo é uma **missão** curta. Você lê só o essencial e constrói uma peça de um projeto que cresce.

O livro cobre Python do básico à inteligência artificial, à ciência de dados, ao Raspberry Pi e à robótica.
Ao longo de 14 missões você constrói o **rover Aurora**, um robô virtual que explora Marte. O rover ganha, nesta ordem:

- painel, sensores e comandos;
- diário de bordo e conexão com o centro de controle;
- uma rede neural feita à mão;
- análise de dados;
- hardware simulado;
- um cérebro que completa a missão sozinho.

## A trilha (105 passos)

| Cap. | Missão | Você constrói |
|---|---|---|
| 1 | Primeiros passos | tipos, operadores, conversões, erros de sintaxe, `painel.py` |
| 2 | Números, texto, datas e fusos | f-strings, `Decimal`, métodos de texto, `datetime`, `zoneinfo`, `formatos.py` |
| 3 | Decisões e repetições | `if/elif`, `for`, `while`, `break/continue`, `navegacao.py` |
| 4 | Listas, tuplas e conjuntos | compreensões, ordenação com chave, operações de conjunto, rota de coleta, `colecoes.py` |
| 5 | Dicionários | `get`, `setdefault`, cópia rasa × profunda, chaves de tupla, `catalogo.py` |
| 6 | Funções | padrões, retorno múltiplo, `*args/**kwargs`, escopo, `lambda`, `calculos.py` |
| 7 | Classes e herança | atributos de classe, `@property`, herança, polimorfismo, `sensores.py` |
| 8 | Erros | `try/except/else/finally`, exceções próprias, interpretador à prova de falhas, `comandos.py` |
| 9 | Arquivos, CSV e JSON | texto, binário, `csv`, `dataclass`, `json`, `diario.py` |
| 10 | Internet e pacotes | servidor HTTP local, GET/POST com `urllib`, `HTMLParser`, biblioteca padrão, `rede.py`, `__init__.py` |
| 11 | Inteligência artificial | neurônio, XOR, **rede neural do zero em NumPy**, MLP do scikit-learn em dígitos (97%), matriz de confusão, `neural.py` |
| 12 | Ciência de dados | gerar, limpar, explorar, modelar e comunicar telemetria; 1 milhão de linhas sem nuvem, `analise.py` |
| 13 | Hardware simulado | LED em Morse, I2C com bytes crus, PWM, servo, motor de passo, painel, `hardware.py` |
| 14 | Robótica | interface do robô, seguir a parede, **cérebro com busca em largura**, câmera + modelo que persegue a bola, `robo.py`, `cerebro.py` |

## Diferenças em relação ao livro

- O livro usa Raspberry Pi, sensores Grove e o kit PiCar-B. Aqui o **hardware é simulado** com o mesmo comportamento: endereços I2C, complemento de dois, *duty cycle*, pulso do servo e sequência das bobinas. Com um Pi, basta trocar o `hardware.py`.
- O TensorFlow (cerca de 500 MB) virou uma rede neural escrita em NumPy, para ver cada passo, e o `MLPClassifier` do scikit-learn.
- O BigQuery (que exige conta no Google Cloud) virou um conjunto de 1 milhão de linhas gerado localmente.
- As páginas indicadas nos cadernos são as do PDF em inglês. A leitura é **opcional** e só do essencial.
- O gabarito inteiro roda em `ferramentas/testar_cadernos.py`, com 0 erros.

## Como usar

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-estudos.txt
.venv\Scripts\python.exe ferramentas\testar_cadernos.py   # opcional: roda o gabarito
```

Abra `praticar/cap01_*.ipynb` no VS Code e escolha o kernel `.venv`. O [Guia de Estudos (PDF)](Guia_de_Estudos.pdf) explica o passo a passo.

## Direitos autorais

O livro **não** está neste repositório. Para estudar, use a sua própria cópia.
As missões, os cadernos, os dados fictícios, os scripts e o guia são autorais e estão sob licença [MIT](LICENSE).
