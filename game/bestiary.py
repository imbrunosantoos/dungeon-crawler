"""Bestiary: monsters discovered as you fight them, saved between runs."""

import json
import os

from game.saves import PASTA_SAVES

ARQUIVO_BESTIARIO = os.path.join(PASTA_SAVES, "bestiary.json")


def _ler():
    if not os.path.exists(ARQUIVO_BESTIARIO):
        return []
    with open(ARQUIVO_BESTIARIO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def vistos():
    """Set of monster ids already discovered."""
    return set(_ler())


def registrar_visto(monstro_id):
    """Mark a monster as discovered (first encounter)."""
    descobertos = set(_ler())
    if monstro_id in descobertos:
        return
    descobertos.add(monstro_id)
    os.makedirs(PASTA_SAVES, exist_ok=True)
    with open(ARQUIVO_BESTIARIO, "w", encoding="utf-8") as arquivo:
        json.dump(sorted(descobertos), arquivo, ensure_ascii=False, indent=2)
