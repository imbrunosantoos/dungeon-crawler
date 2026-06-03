"""Achievements unlocked across runs, saved in saves/achievements.json."""

import json
import os

from game.bestiary import vistos
from game.monster import MODELOS_MONSTROS
from game.saves import PASTA_SAVES

ARQUIVO_CONQUISTAS = os.path.join(PASTA_SAVES, "achievements.json")

# Display order. Each id has "conq.<id>.nome" / ".desc" in i18n.
CONQUISTAS = [
    "primeiro_chefe",
    "nivel_10",
    "rico",
    "dificil",
    "ondas_10",
    "bestiario_completo",
]


def _ler():
    if not os.path.exists(ARQUIVO_CONQUISTAS):
        return []
    with open(ARQUIVO_CONQUISTAS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def obtidas():
    return set(_ler())


def desbloquear(cid):
    """Unlock an achievement. Returns True only if it's newly unlocked."""
    atuais = set(_ler())
    if cid in atuais:
        return False
    atuais.add(cid)
    os.makedirs(PASTA_SAVES, exist_ok=True)
    with open(ARQUIVO_CONQUISTAS, "w", encoding="utf-8") as arquivo:
        json.dump(sorted(atuais), arquivo, ensure_ascii=False, indent=2)
    return True


def checar(heroi, boss=False, venceu=False, ondas=0):
    """Evaluate conditions and unlock any that are newly met.

    Returns the list of newly unlocked ids so the caller can announce them.
    """
    novas = []

    def tenta(cid, condicao):
        if condicao and desbloquear(cid):
            novas.append(cid)

    tenta("primeiro_chefe", boss)
    tenta("nivel_10", heroi.nivel >= 10)
    tenta("rico", heroi.ouro >= 1000)
    tenta("dificil", venceu and getattr(heroi, "dificuldade", "Normal") == "Difícil")
    tenta("ondas_10", ondas >= 10)
    todos_monstros = set(MODELOS_MONSTROS.keys()) | {"Dragão Ancião"}
    tenta("bestiario_completo", todos_monstros <= vistos())

    return novas
