"""
monster.py — os inimigos do jogo: monstros comuns e o chefe (Boss).

Mais uma vez usamos HERANÇA: Monster herda de Character (afinal, um monstro
também tem vida, ataque e defesa). E Boss herda de Monster — é um monstro
"turbinado", com mais vida e recompensas maiores.

Cada monstro também guarda quanto XP e ouro dá ao ser derrotado. Isso conecta
o combate (etapa 5) com a progressão de nível (etapa 6).
"""

from game.character import Character
from game.ui import Cor, colorir


class Monster(Character):
    """Um inimigo comum."""

    def __init__(self, nome, hp_max, ataque, defesa, xp_recompensa, ouro_recompensa):
        # Reaproveita a criação de Character (vida, ataque, defesa).
        super().__init__(nome=nome, hp_max=hp_max, ataque=ataque, defesa=defesa)
        # Atributos exclusivos do monstro: o que ele dá ao morrer.
        self.xp_recompensa = xp_recompensa
        self.ouro_recompensa = ouro_recompensa

    def nome_colorido(self):
        """Nome do monstro em vermelho, para destacar o inimigo na tela."""
        return colorir(self.nome, Cor.VERMELHO)


class Boss(Monster):
    """Um chefe: um monstro bem mais forte, com nome destacado em magenta.

    Como herda de Monster, já vem com xp_recompensa e ouro_recompensa. Aqui só
    deixamos claro que é um chefe (atributo eh_boss) e mudamos a cor do nome.
    """

    def __init__(self, nome, hp_max, ataque, defesa, xp_recompensa, ouro_recompensa):
        super().__init__(nome, hp_max, ataque, defesa, xp_recompensa, ouro_recompensa)
        self.eh_boss = True

    def nome_colorido(self):
        # Sobrescreve (override) o método da classe-mãe para usar outra cor.
        return colorir(f"★ {self.nome} ★", Cor.MAGENTA + Cor.NEGRITO)


# ---------------------------------------------------------------------------
# "Fábrica" de monstros
# ---------------------------------------------------------------------------
# Em vez de espalhar números mágicos pelo código, guardamos aqui os modelos de
# monstro. É um dicionário: nome -> atributos base. As fases (etapa 9) vão usar
# isso para montar os inimigos de cada nível.
MODELOS_MONSTROS = {
    "Rato Gigante":   {"hp_max": 30,  "ataque": 8,  "defesa": 2,  "xp": 30,  "ouro": 10},
    "Goblin":         {"hp_max": 45,  "ataque": 12, "defesa": 4,  "xp": 50,  "ouro": 20},
    "Esqueleto":      {"hp_max": 60,  "ataque": 16, "defesa": 6,  "xp": 70,  "ouro": 30},
    "Orc":            {"hp_max": 90,  "ataque": 22, "defesa": 8,  "xp": 110, "ouro": 50},
    "Troll":          {"hp_max": 130, "ataque": 28, "defesa": 12, "xp": 160, "ouro": 80},
}


def criar_monstro(nome):
    """Cria um Monster a partir de um modelo do catálogo, pelo nome."""
    m = MODELOS_MONSTROS[nome]
    return Monster(nome, m["hp_max"], m["ataque"], m["defesa"], m["xp"], m["ouro"])


def criar_boss():
    """Cria o chefe final do jogo: o Dragão Ancião."""
    return Boss(
        nome="Dragão Ancião",
        hp_max=250,
        ataque=35,
        defesa=15,
        xp_recompensa=500,
        ouro_recompensa=300,
    )
