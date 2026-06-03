"""Playable classes. Each subclasses Character with its own stats and skill set."""

import random

from game.character import ATORDOADO, Character, VENENO
from game.ui import Cor, colorir


class Habilidade:
    """A special move: a name, an energy cost and a callable(alvo) -> message."""

    def __init__(self, nome, custo, executar):
        self.nome = nome
        self.custo = custo
        self.executar = executar


class Warrior(Character):
    """Tanky: lots of HP and defense."""

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=120, ataque=18, defesa=8)
        self.energia_max = 20
        self.energia = self.energia_max

    def habilidades(self):
        return [
            Habilidade("Golpe Poderoso", 10, self._golpe_poderoso),
            Habilidade("Investida", 14, self._investida),
        ]

    def _golpe_poderoso(self, alvo):
        dano_real = alvo.receber_dano(self.ataque * 2)
        return f"{self.nome} usa {colorir('Golpe Poderoso', Cor.VERMELHO)} e causa {dano_real} de dano!"

    def _investida(self, alvo):
        dano_real = alvo.receber_dano(int(self.ataque * 1.5))
        msg = f"{self.nome} avança numa {colorir('Investida', Cor.VERMELHO)} causando {dano_real} de dano"
        if random.random() < 0.4:
            alvo.aplicar_efeito(ATORDOADO, 1)
            msg += " e ATORDOA o inimigo!"
        else:
            msg += "!"
        return msg


class Mage(Character):
    """Glass cannon: low HP, high attack."""

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=80, ataque=24, defesa=4)
        self.energia_max = 30
        self.energia = self.energia_max

    def habilidades(self):
        return [
            Habilidade("Bola de Fogo", 15, self._bola_de_fogo),
            Habilidade("Raio Congelante", 14, self._raio_congelante),
        ]

    def _bola_de_fogo(self, alvo):
        # Hit HP directly so defense is ignored.
        dano = self.ataque + 15
        alvo.hp = max(0, alvo.hp - dano)
        return f"{self.nome} lança {colorir('Bola de Fogo', Cor.MAGENTA)} e causa {dano} de dano mágico (ignora defesa)!"

    def _raio_congelante(self, alvo):
        dano_real = alvo.receber_dano(self.ataque)
        msg = f"{self.nome} conjura {colorir('Raio Congelante', Cor.CIANO)} causando {dano_real} de dano"
        if random.random() < 0.5:
            alvo.aplicar_efeito(ATORDOADO, 1)
            msg += " e CONGELA o inimigo!"
        else:
            msg += "!"
        return msg


class Archer(Character):
    """Balanced ranged fighter."""

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=100, ataque=20, defesa=6)
        self.energia_max = 25
        self.energia = self.energia_max

    def habilidades(self):
        return [
            Habilidade("Tiro Certeiro", 12, self._tiro_certeiro),
            Habilidade("Chuva de Flechas", 16, self._chuva_de_flechas),
        ]

    def _tiro_certeiro(self, alvo):
        # 50% chance to triple the damage.
        critico = random.random() < 0.5
        dano = int(self.ataque * (3 if critico else 1.5))
        dano_real = alvo.receber_dano(dano)
        if critico:
            return f"{self.nome} acerta um {colorir('CRÍTICO', Cor.AMARELO)} com Tiro Certeiro e causa {dano_real} de dano!"
        return f"{self.nome} usa {colorir('Tiro Certeiro', Cor.VERDE)} e causa {dano_real} de dano!"

    def _chuva_de_flechas(self, alvo):
        dano_real = alvo.receber_dano(int(self.ataque * 1.7))
        return f"{self.nome} dispara uma {colorir('Chuva de Flechas', Cor.VERDE)} e causa {dano_real} de dano!"


class Paladin(Character):
    """High defense, with a self-heal."""

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=130, ataque=16, defesa=10)
        self.energia_max = 25
        self.energia = self.energia_max

    def habilidades(self):
        return [
            Habilidade("Luz Curativa", 15, self._luz_curativa),
            Habilidade("Martelo Sagrado", 14, self._martelo_sagrado),
        ]

    def _luz_curativa(self, _alvo):
        # Self-heal, so the target is ignored.
        curado = self.curar(50)
        return f"{self.nome} invoca {colorir('Luz Curativa', Cor.AMARELO)} e recupera {curado} de vida!"

    def _martelo_sagrado(self, alvo):
        dano_real = alvo.receber_dano(int(self.ataque * 1.5))
        msg = f"{self.nome} desce o {colorir('Martelo Sagrado', Cor.AMARELO)} causando {dano_real} de dano"
        if random.random() < 0.4:
            alvo.aplicar_efeito(ATORDOADO, 1)
            msg += " e ATORDOA o inimigo!"
        else:
            msg += "!"
        return msg


class Rogue(Character):
    """Agile and deadly: high accuracy and crit."""

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=95, ataque=21, defesa=5)
        self.energia_max = 25
        self.energia = self.energia_max
        self.precisao = 0.95
        self.chance_critico = 0.25

    def habilidades(self):
        return [
            Habilidade("Golpe Sombrio", 12, self._golpe_sombrio),
            Habilidade("Apunhalar", 14, self._apunhalar),
        ]

    def _golpe_sombrio(self, alvo):
        dano_real = alvo.receber_dano(self.ataque)
        alvo.aplicar_efeito(VENENO, 3)
        return (
            f"{self.nome} desfere {colorir('Golpe Sombrio', Cor.MAGENTA)} "
            f"causando {dano_real} de dano e ENVENENANDO o inimigo!"
        )

    def _apunhalar(self, alvo):
        dano_real = alvo.receber_dano(self.ataque * 2)
        return f"{self.nome} {colorir('Apunhala', Cor.MAGENTA)} pelas costas e causa {dano_real} de dano!"


# Maps a readable name to its class, used by the character creation menu.
CLASSES_JOGAVEIS = {
    "Guerreiro": Warrior,
    "Mago": Mage,
    "Arqueiro": Archer,
    "Paladino": Paladin,
    "Ladino": Rogue,
}
