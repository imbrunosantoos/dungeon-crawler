"""Optional per-stage objectives that grant bonus gold when met."""

import random

# Each objective checks the stage 'registro' filled in by combat.
# Description lives in i18n as "quest.<id>.desc".
OBJETIVOS = [
    {"id": "sem_pocao", "ouro": 40, "verificar": lambda r: r.get("pocoes", 0) == 0},
    {"id": "usar_habilidade", "ouro": 30, "verificar": lambda r: r.get("habilidades", 0) >= 1},
    {"id": "pouco_dano", "ouro": 50, "verificar": lambda r: r.get("dano_recebido", 0) < 40},
]


def objetivo_aleatorio():
    return random.choice(OBJETIVOS)
