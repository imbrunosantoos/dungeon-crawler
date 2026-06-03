"""
scores.py — o placar de recordes (high scores).

Ao fim de cada partida (vitória ou derrota), calculamos uma pontuação e a
guardamos num arquivo JSON. O menu inicial pode então mostrar o ranking dos
melhores resultados.

Reaproveitamos a pasta de saves (game.saves.PASTA_SAVES) para guardar o arquivo
de recordes. Como JSON é só texto, conseguimos ler e escrever uma lista de
pontuações facilmente.
"""

import json
import os

from game.saves import PASTA_SAVES, _nome_da_classe

# Arquivo onde o ranking é guardado, e quantos recordes mantemos.
ARQUIVO_SCORES = os.path.join(PASTA_SAVES, "scores.json")
MAX_RECORDES = 10

# Bônus de pontuação por dificuldade (jogar no difícil vale mais pontos).
_BONUS_DIFICULDADE = {"Fácil": 0, "Normal": 200, "Difícil": 500}


def pontuar(nivel, ouro, dificuldade, venceu):
    """Calcula a pontuação de uma partida.

    Fórmula: nível conta muito (×100), somado ao ouro, a um bônus por
    dificuldade e a um grande bônus se o jogador venceu o jogo.
    """
    pontos = nivel * 100 + ouro
    pontos += _BONUS_DIFICULDADE.get(dificuldade, 0)
    if venceu:
        pontos += 1000
    return pontos


def _ler_scores():
    """Lê a lista de recordes do arquivo. Se não existir, devolve lista vazia."""
    if not os.path.exists(ARQUIVO_SCORES):
        return []
    with open(ARQUIVO_SCORES, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def registrar_pontuacao(heroi, venceu):
    """Registra o resultado de uma partida no placar e devolve os pontos.

    Lê os recordes atuais, acrescenta o novo, ordena do maior para o menor e
    mantém só os MAX_RECORDES melhores.
    """
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
    # sorted com key e reverse=True ordena do maior pontos para o menor.
    scores = sorted(scores, key=lambda s: s["pontos"], reverse=True)[:MAX_RECORDES]

    with open(ARQUIVO_SCORES, "w", encoding="utf-8") as arquivo:
        json.dump(scores, arquivo, ensure_ascii=False, indent=2)

    return pontos


def top_pontuacoes(n=MAX_RECORDES):
    """Devolve as N melhores pontuações (já ordenadas)."""
    return _ler_scores()[:n]
