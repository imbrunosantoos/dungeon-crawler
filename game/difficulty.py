"""Difficulty levels: multipliers applied to enemies and gold rewards."""

DIFICULDADES = {
    "Fácil":   {"vida": 0.75, "ataque": 0.75, "ouro": 1.25},
    "Normal":  {"vida": 1.00, "ataque": 1.00, "ouro": 1.00},
    "Difícil": {"vida": 1.30, "ataque": 1.30, "ouro": 1.00},
}

# Fallback when no level is set (e.g. older saves).
DIFICULDADE_PADRAO = "Normal"


def multiplicadores(dificuldade):
    return DIFICULDADES.get(dificuldade, DIFICULDADES[DIFICULDADE_PADRAO])


def aplicar_dificuldade(monstro, dificuldade):
    """Scale a monster's HP and attack in place. Minimum of 1 each."""
    fatores = multiplicadores(dificuldade)
    monstro.hp_max = max(1, int(monstro.hp_max * fatores["vida"]))
    monstro.hp = monstro.hp_max
    monstro.ataque = max(1, int(monstro.ataque * fatores["ataque"]))
    return monstro


def fator_ouro(dificuldade):
    return multiplicadores(dificuldade)["ouro"]
