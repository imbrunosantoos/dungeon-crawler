"""
stages.py — as fases (stages) do jogo.

Cada fase é representada por um dicionário com:
  - "nome":     título da fase
  - "monstros": lista de nomes de monstros a enfrentar, em ordem
  - "premio":   função que cria o item de recompensa ao terminar a fase
  - "eh_final": True só na última fase (onde está o boss)

Guardar as fases como uma LISTA de dicionários deixa fácil adicionar, remover
ou reordenar fases sem mexer na lógica do jogo. Para criar uma fase nova, basta
acrescentar mais um item nesta lista.
"""

from game.items import (
    armadura_de_couro,
    armadura_de_placas,
    espada_de_ferro,
    machado_de_guerra,
    pocao_grande,
    pocao_pequena,
)
from game.monster import criar_boss, criar_monstro


FASES = [
    {
        "nome": "Caverna dos Ratos",
        "monstros": ["Rato Gigante", "Rato Gigante", "Goblin"],
        "premio": pocao_pequena,
        "eh_final": False,
    },
    {
        "nome": "Floresta Sombria",
        "monstros": ["Goblin", "Esqueleto", "Esqueleto"],
        "premio": espada_de_ferro,
        "eh_final": False,
    },
    {
        "nome": "Ruínas Antigas",
        "monstros": ["Esqueleto", "Orc", "Orc"],
        "premio": armadura_de_couro,
        "eh_final": False,
    },
    {
        "nome": "Montanha do Trovão",
        "monstros": ["Orc", "Troll", "Troll"],
        "premio": pocao_grande,
        "eh_final": False,
    },
    {
        "nome": "Covil do Dragão",
        "monstros": ["Troll"],          # alguns lacaios antes do chefe...
        "premio": machado_de_guerra,
        "eh_final": True,               # ...e o boss no fim (ver criar_inimigos)
    },
]


def total_de_fases():
    """Quantidade de fases do jogo."""
    return len(FASES)


def criar_inimigos_da_fase(indice):
    """Cria os objetos inimigos de uma fase, na ordem em que serão enfrentados.

    'indice' começa em 0 (a primeira fase é a de índice 0). Se a fase for a
    final, acrescentamos o boss ao fim da lista de inimigos.
    """
    fase = FASES[indice]
    inimigos = [criar_monstro(nome) for nome in fase["monstros"]]
    if fase["eh_final"]:
        inimigos.append(criar_boss())
    return inimigos


def premio_da_fase(indice):
    """Cria e devolve o item de recompensa por concluir a fase."""
    return FASES[indice]["premio"]()
