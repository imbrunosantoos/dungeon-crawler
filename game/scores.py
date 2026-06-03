"""High score leaderboard, stored as JSON alongside the saves."""

import json
import os

from game.saves import PASTA_SAVES, _nome_da_classe

ARQUIVO_SCORES = os.path.join(PASTA_SAVES, "scores.json")
MAX_RECORDES = 10

# Extra points for harder difficulties.
_BONUS_DIFICULDADE = {"Fácil": 0, "Normal": 200, "Difícil": 500}


def pontuar(nivel, ouro, dificuldade, venceu):
    """Score = level*100 + gold + difficulty bonus + a big bonus for winning."""
    pontos = nivel * 100 + ouro
    pontos += _BONUS_DIFICULDADE.get(dificuldade, 0)
    if venceu:
        pontos += 1000
    return pontos


def _ler_scores():
    """Read the leaderboard, or an empty list if there isn't one yet."""
    if not os.path.exists(ARQUIVO_SCORES):
        return []
    with open(ARQUIVO_SCORES, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def registrar_pontuacao(heroi, venceu):
    """Record a run, keep the top MAX_RECORDES, and return its score."""
    os.makedirs(PASTA_SAVES, exist_ok=True)
    dificuldade = getattr(heroi, "dificuldade", "Normal")
    pontos = pontuar(heroi.nivel, heroi.ouro, dificuldade, venceu)

    scores = _ler_scores()
    scores.append({
        "nome": heroi.nome,
        "classe": _nome_da_classe(heroi),
        "nivel": heroi.nivel,
        "ouro": heroi.ouro,
        "dificuldade": dificuldade,
        "venceu": venceu,
        "pontos": pontos,
    })
    # Highest score first.
    scores = sorted(scores, key=lambda s: s["pontos"], reverse=True)[:MAX_RECORDES]

    with open(ARQUIVO_SCORES, "w", encoding="utf-8") as arquivo:
        json.dump(scores, arquivo, ensure_ascii=False, indent=2)

    return pontos


def top_pontuacoes(n=MAX_RECORDES):
    """Return the top N scores (already sorted)."""
    return _ler_scores()[:n]
