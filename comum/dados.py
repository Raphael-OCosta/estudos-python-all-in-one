"""Dados fictícios da missão do rover Aurora (criados para este curso).

O projeto que atravessa o livro é o **rover Aurora**, um robô virtual que explora uma região de Marte.
Você vai programar o painel, os sensores, os motores, o registro da missão, a análise de dados e o
"cérebro" dele, sem precisar de nenhum hardware.

    MAPA             -> grade da região: "." chão livre, "#" rocha, "B" base, "A" amostra para coletar
    LEITURAS         -> leituras de sensores (hora UTC, temperatura °C, poeira, bateria %, distância à frente em cm)
    AMOSTRAS         -> rochas coletadas (id, tipo, massa em g, posição)
    EQUIPE           -> equipe da Terra (nome, função, cidade, fuso horário)
"""

MAPA = [
    "##########",
    "#B..#....#",
    "#.#.#.##.#",
    "#.#...#A.#",
    "#.####.#.#",
    "#......#.#",
    "#.##.#...#",
    "#A...#.#A#",
    "##########",
]

LEITURAS = [
    ("2026-03-01T06:00:00", -71.5, 0.12, 100, 340),
    ("2026-03-01T07:00:00", -65.2, 0.15, 97, 310),
    ("2026-03-01T08:00:00", -52.8, 0.22, 93, 120),
    ("2026-03-01T09:00:00", -40.1, 0.31, 90, 45),
    ("2026-03-01T10:00:00", -28.7, 0.45, 86, 30),
    ("2026-03-01T11:00:00", -18.3, 0.52, 84, 210),
    ("2026-03-01T12:00:00", -12.9, 0.48, 81, 260),
    ("2026-03-01T13:00:00", -10.4, 0.40, 79, 18),
    ("2026-03-01T14:00:00", -14.6, 0.33, 77, 400),
    ("2026-03-01T15:00:00", -22.0, 0.29, 75, 380),
    ("2026-03-01T16:00:00", -35.5, 0.20, 74, 95),
    ("2026-03-01T17:00:00", -49.8, 0.16, 73, 150),
]

AMOSTRAS = [
    {"id": "AM-001", "tipo": "basalto", "massa_g": 182.4, "pos": (3, 7)},
    {"id": "AM-002", "tipo": "argila", "massa_g": 95.0, "pos": (7, 1)},
    {"id": "AM-003", "tipo": "basalto", "massa_g": 210.7, "pos": (7, 8)},
    {"id": "AM-004", "tipo": "hematita", "massa_g": 64.3, "pos": (3, 7)},
    {"id": "AM-005", "tipo": "argila", "massa_g": 120.9, "pos": (7, 1)},
]

EQUIPE = [
    {"nome": "Ana", "funcao": "piloto", "cidade": "Recife", "fuso": "America/Recife"},
    {"nome": "Kenji", "funcao": "geólogo", "cidade": "Tóquio", "fuso": "Asia/Tokyo"},
    {"nome": "Lena", "funcao": "engenheira", "cidade": "Berlim", "fuso": "Europe/Berlin"},
    {"nome": "Omar", "funcao": "cientista de dados", "cidade": "Houston", "fuso": "America/Chicago"},
]
