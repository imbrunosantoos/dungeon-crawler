"""Playable classes. Each one subclasses Character with its own stats and skill."""

import random

from game.character import Character, VENENO
from game.ui import Cor, colorir


class Warrior(Character):
    """Tanky: lots of HP and defense. Skill: Golpe Poderoso (heavy hit)."""

    nome_habilidade = "Golpe Poderoso"
    custo_habilidade = 10

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=120, ataque=18, defesa=8)
        self.energia_max = 20
        self.energia = self.energia_max

    def usar_habilidade(self, alvo):
        # Double damage.
        dano = self.ataque * 2
        dano_real = alvo.receber_dano(dano)
        return f"{self.nome} usa {colorir(self.nome_habilidade, Cor.VERMELHO)} e causa {dano_real} de dano!"


class Mage(Character):
    """Glass cannon: low HP, high attack. Skill: Bola de Fogo (ignores defense)."""

    nome_habilidade = "Bola de Fogo"
    custo_habilidade = 15

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=80, ataque=24, defesa=4)
        self.energia_max = 30
        self.energia = self.energia_max

    def usar_habilidade(self, alvo):
        # Hit HP directly so defense is ignored.
        dano = self.ataque + 15
        alvo.hp = max(0, alvo.hp - dano)
        return f"{self.nome} lança {colorir(self.nome_habilidade, Cor.MAGENTA)} e causa {dano} de dano mágico (ignora defesa)!"


class Archer(Character):
    """Balanced. Skill: Tiro Certeiro (chance of a critical)."""

    nome_habilidade = "Tiro Certeiro"
    custo_habilidade = 12

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=100, ataque=20, defesa=6)
        self.energia_max = 25
        self.energia = self.energia_max

    def usar_habilidade(self, alvo):
        # 50% chance to deal triple damage.
        critico = random.random() < 0.5
        multiplicador = 3 if critico else 1.5
        dano = int(self.ataque * multiplicador)
        dano_real = alvo.receber_dano(dano)
        if critico:
            return f"{self.nome} acerta um {colorir('CRÍTICO', Cor.AMARELO)} com {self.nome_habilidade} e causa {dano_real} de dano!"
        return f"{self.nome} usa {colorir(self.nome_habilidade, Cor.VERDE)} e causa {dano_real} de dano!"


class Paladin(Character):
    """High defense. Skill: Luz Curativa, which heals the paladin instead of attacking."""

    nome_habilidade = "Luz Curativa"
    custo_habilidade = 15

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=130, ataque=16, defesa=10)
        self.energia_max = 25
        self.energia = self.energia_max

    def usar_habilidade(self, _alvo):
        # Self-heal, so the target is ignored.
        curado = self.curar(50)
        return f"{self.nome} invoca {colorir(self.nome_habilidade, Cor.AMARELO)} e recupera {curado} de vida!"


class Rogue(Character):
    """Agile and deadly: high accuracy and crit. Skill: Golpe Sombrio (damage + poison)."""

    nome_habilidade = "Golpe Sombrio"
    custo_habilidade = 12

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=95, ataque=21, defesa=5)
        self.energia_max = 25
        self.energia = self.energia_max
        self.precisao = 0.95
        self.chance_critico = 0.25

    def usar_habilidade(self, alvo):
        dano_real = alvo.receber_dano(self.ataque)
        alvo.aplicar_efeito(VENENO, 3)
        return (
            f"{self.nome} desfere {colorir(self.nome_habilidade, Cor.MAGENTA)} "
            f"causando {dano_real} de dano e ENVENENANDO o inimigo!"
        )


# Maps a readable name to its class, used by the character creation menu.
CLASSES_JOGAVEIS = {
    "Guerreiro": Warrior,
    "Mago": Mage,
    "Arqueiro": Archer,
    "Paladino": Paladin,
    "Ladino": Rogue,
}
