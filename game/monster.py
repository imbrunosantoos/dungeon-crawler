"""Enemies: regular monsters and the boss."""

from game.character import ATORDOADO, Character, VENENO
from game.i18n import nome as traduzir_nome
from game.ui import Cor, colorir


class Monster(Character):
    def __init__(self, nome, hp_max, ataque, defesa, xp_recompensa, ouro_recompensa,
                 efeito_ataque=None):
        super().__init__(nome=nome, hp_max=hp_max, ataque=ataque, defesa=defesa)
        # What it drops when killed.
        self.xp_recompensa = xp_recompensa
        self.ouro_recompensa = ouro_recompensa
        # Optional status it can inflict on hit: (effect_name, chance, turns).
        self.efeito_ataque = efeito_ataque

    def nome_exibicao(self):
        return traduzir_nome(self.nome)

    def nome_colorido(self):
        return colorir(traduzir_nome(self.nome), Cor.VERMELHO)


class Boss(Monster):
    """A much tougher monster with a flashier name."""

    def __init__(self, nome, hp_max, ataque, defesa, xp_recompensa, ouro_recompensa):
        super().__init__(nome, hp_max, ataque, defesa, xp_recompensa, ouro_recompensa)
        self.eh_boss = True

    def nome_colorido(self):
        return colorir(f"★ {traduzir_nome(self.nome)} ★", Cor.MAGENTA + Cor.NEGRITO)


# Monster templates: name -> base stats. Stages build their enemies from these.
MODELOS_MONSTROS = {
    "Rato Gigante":     {"hp_max": 30,  "ataque": 8,  "defesa": 2,  "xp": 30,  "ouro": 10},
    "Goblin":           {"hp_max": 45,  "ataque": 12, "defesa": 4,  "xp": 50,  "ouro": 20},
    "Morcego":          {"hp_max": 35,  "ataque": 14, "defesa": 1,  "xp": 45,  "ouro": 15},
    "Esqueleto":        {"hp_max": 60,  "ataque": 16, "defesa": 6,  "xp": 70,  "ouro": 30},
    # 50% chance to poison for 3 turns on hit.
    "Aranha Venenosa":  {"hp_max": 55,  "ataque": 14, "defesa": 4,  "xp": 75,  "ouro": 35,
                         "efeito": (VENENO, 0.5, 3)},
    "Lobo Sombrio":     {"hp_max": 70,  "ataque": 20, "defesa": 5,  "xp": 90,  "ouro": 40},
    # 35% chance to stun the hero for a turn.
    "Feiticeiro":       {"hp_max": 65,  "ataque": 18, "defesa": 5,  "xp": 100, "ouro": 60,
                         "efeito": (ATORDOADO, 0.35, 1)},
    "Orc":              {"hp_max": 90,  "ataque": 22, "defesa": 8,  "xp": 110, "ouro": 50},
    "Golem de Pedra":   {"hp_max": 160, "ataque": 24, "defesa": 18, "xp": 180, "ouro": 90},
    "Troll":            {"hp_max": 130, "ataque": 28, "defesa": 12, "xp": 160, "ouro": 80},
    "Cavaleiro Caído":  {"hp_max": 140, "ataque": 30, "defesa": 14, "xp": 200, "ouro": 110},
}


def criar_monstro(nome):
    m = MODELOS_MONSTROS[nome]
    return Monster(nome, m["hp_max"], m["ataque"], m["defesa"], m["xp"], m["ouro"],
                   efeito_ataque=m.get("efeito"))


def criar_boss():
    return Boss(
        nome="Dragão Ancião",
        hp_max=250,
        ataque=35,
        defesa=15,
        xp_recompensa=500,
        ouro_recompensa=300,
    )
