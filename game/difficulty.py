"""
difficulty.py — níveis de dificuldade do jogo.

A dificuldade é um conjunto de MULTIPLICADORES aplicados aos inimigos:
  - "vida":   multiplica a vida do monstro
  - "ataque": multiplica o ataque do monstro
  - "ouro":   multiplica o ouro que o herói ganha (recompensa)

Guardar isso num dicionário deixa fácil ajustar o balanceamento ou criar novos
níveis sem mexer na lógica do jogo — basta editar/adicionar uma entrada aqui.
"""

# Cada nível liga seu nome a três multiplicadores.
DIFICULDADES = {
    "Fácil":   {"vida": 0.75, "ataque": 0.75, "ouro": 1.25},
    "Normal":  {"vida": 1.00, "ataque": 1.00, "ouro": 1.00},
    "Difícil": {"vida": 1.30, "ataque": 1.30, "ouro": 1.00},
}

# Nível usado quando nenhum foi escolhido (e para saves antigos da v1).
DIFICULDADE_PADRAO = "Normal"


def multiplicadores(dificuldade):
    """Devolve o dicionário de multiplicadores de um nível.

    Se o nome não existir (ex.: save antigo sem dificuldade), cai no padrão.
    """
    return DIFICULDADES.get(dificuldade, DIFICULDADES[DIFICULDADE_PADRAO])


def aplicar_dificuldade(monstro, dificuldade):
    """Escala a vida e o ataque de um monstro conforme o nível escolhido.

    Recebe o monstro já criado e ajusta seus atributos no lugar. Usamos int()
    porque vida e ataque são números inteiros. Garantimos o mínimo de 1 para
    nada ficar zerado em dificuldades baixas.
    """
    fatores = multiplicadores(dificuldade)
    monstro.hp_max = max(1, int(monstro.hp_max * fatores["vida"]))
    monstro.hp = monstro.hp_max  # entra em campo com a vida cheia
    monstro.ataque = max(1, int(monstro.ataque * fatores["ataque"]))
    return monstro


def fator_ouro(dificuldade):
    """Multiplicador de ouro do nível (usado ao dar a recompensa de combate)."""
    return multiplicadores(dificuldade)["ouro"]
