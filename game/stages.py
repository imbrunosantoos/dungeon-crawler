"""Game stages. Each one is a dict: name, monster list, prize and a boss flag."""

from game.items import (
    adaga_afiada,
    armadura_de_couro,
    armadura_runica,
    espada_de_ferro,
    espada_flamejante,
    machado_de_guerra,
    pocao_grande,
    pocao_pequena,
)
from game.difficulty import aplicar_dificuldade
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
        "nome": "Ninho das Aranhas",
        "monstros": ["Aranha Venenosa", "Morcego", "Aranha Venenosa"],
        "premio": adaga_afiada,
        "eh_final": False,
    },
    {
        "nome": "Torre do Feiticeiro",
        "monstros": ["Lobo Sombrio", "Feiticeiro", "Feiticeiro"],
        "premio": armadura_runica,
        "eh_final": False,
    },
    {
        "nome": "Fortaleza Esquecida",
        "monstros": ["Golem de Pedra", "Cavaleiro Caído", "Cavaleiro Caído"],
        "premio": espada_flamejante,
        "eh_final": False,
    },
    {
        "nome": "Covil do Dragão",
        "monstros": ["Troll"],          # minions before the boss...
        "premio": machado_de_guerra,
        "eh_final": True,               # ...and the boss is appended in criar_inimigos
    },
]


def total_de_fases():
    return len(FASES)


def criar_inimigos_da_fase(indice, dificuldade="Normal"):
    """Build a stage's enemies in order, scaled by difficulty. Boss goes last."""
    fase = FASES[indice]
    inimigos = [criar_monstro(nome) for nome in fase["monstros"]]
    if fase["eh_final"]:
        inimigos.append(criar_boss())

    for inimigo in inimigos:
        aplicar_dificuldade(inimigo, dificuldade)
    return inimigos


def premio_da_fase(indice):
    """Create the reward item for clearing a stage."""
    return FASES[indice]["premio"]()
