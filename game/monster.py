"""
monster.py — os inimigos do jogo: monstros comuns e o chefe (Boss).

Mais uma vez usamos HERANÇA: Monster herda de Character (afinal, um monstro
também tem vida, ataque e defesa). E Boss herda de Monster — é um monstro
"turbinado", com mais vida e recompensas maiores.

Cada monstro também guarda quanto XP e ouro dá ao ser derrotado. Isso conecta
o combate (etapa 5) com a progressão de nível (etapa 6).
"""

from game.character import ATORDOADO, Character, VENENO
from game.ui import Cor, colorir


class Monster(Character):
    """Um inimigo comum."""

    def __init__(self, nome, hp_max, ataque, defesa, xp_recompensa, ouro_recompensa,
                 efeito_ataque=None):
        # Reaproveita a criação de Character (vida, ataque, defesa).
        super().__init__(nome=nome, hp_max=hp_max, ataque=ataque, defesa=defesa)
        # Atributos exclusivos do monstro: o que ele dá ao morrer.
        self.xp_recompensa = xp_recompensa
        self.ouro_recompensa = ouro_recompensa
        # Efeito que o monstro pode aplicar ao acertar o herói (v3). É uma tupla
        # (nome_do_efeito, chance, turnos) ou None se o monstro não tem efeito.
        self.efeito_ataque = efeito_ataque

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
    "Rato Gigante":     {"hp_max": 30,  "ataque": 8,  "defesa": 2,  "xp": 30,  "ouro": 10},
    "Goblin":           {"hp_max": 45,  "ataque": 12, "defesa": 4,  "xp": 50,  "ouro": 20},
    "Morcego":          {"hp_max": 35,  "ataque": 14, "defesa": 1,  "xp": 45,  "ouro": 15},
    "Esqueleto":        {"hp_max": 60,  "ataque": 16, "defesa": 6,  "xp": 70,  "ouro": 30},
    # Aranha aplica veneno: 50% de chance de envenenar por 3 turnos ao acertar.
    "Aranha Venenosa":  {"hp_max": 55,  "ataque": 14, "defesa": 4,  "xp": 75,  "ouro": 35,
                         "efeito": (VENENO, 0.5, 3)},
    "Lobo Sombrio":     {"hp_max": 70,  "ataque": 20, "defesa": 5,  "xp": 90,  "ouro": 40},
    # Feiticeiro pode atordoar: 35% de chance de fazer o herói perder a vez.
    "Feiticeiro":       {"hp_max": 65,  "ataque": 18, "defesa": 5,  "xp": 100, "ouro": 60,
                         "efeito": (ATORDOADO, 0.35, 1)},
    "Orc":              {"hp_max": 90,  "ataque": 22, "defesa": 8,  "xp": 110, "ouro": 50},
    "Golem de Pedra":   {"hp_max": 160, "ataque": 24, "defesa": 18, "xp": 180, "ouro": 90},
    "Troll":            {"hp_max": 130, "ataque": 28, "defesa": 12, "xp": 160, "ouro": 80},
    "Cavaleiro Caído":  {"hp_max": 140, "ataque": 30, "defesa": 14, "xp": 200, "ouro": 110},
}


def criar_monstro(nome):
    """Cria um Monster a partir de um modelo do catálogo, pelo nome."""
    m = MODELOS_MONSTROS[nome]
    # .get("efeito") devolve None se o monstro não tiver efeito de ataque.
    return Monster(nome, m["hp_max"], m["ataque"], m["defesa"], m["xp"], m["ouro"],
                   efeito_ataque=m.get("efeito"))


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
