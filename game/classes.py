"""Playable classes. Each subclasses Character with its own stats and skill set."""

import random

from game.character import ATORDOADO, Character, VENENO
from game.i18n import nome, t
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
        dano = alvo.receber_dano(self.ataque * 2)
        return t("hab.golpe_poderoso", hero=self.nome,
                 hab=colorir(nome("Golpe Poderoso"), Cor.VERMELHO), dano=dano)

    def _investida(self, alvo):
        dano = alvo.receber_dano(int(self.ataque * 1.5))
        msg = t("hab.investida", hero=self.nome,
                hab=colorir(nome("Investida"), Cor.VERMELHO), dano=dano)
        if random.random() < 0.4:
            alvo.aplicar_efeito(ATORDOADO, 1)
            return msg + t("hab.sufixo_atordoa")
        return msg + t("hab.fim")


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
        return t("hab.bola_de_fogo", hero=self.nome,
                 hab=colorir(nome("Bola de Fogo"), Cor.MAGENTA), dano=dano)

    def _raio_congelante(self, alvo):
        dano = alvo.receber_dano(self.ataque)
        msg = t("hab.raio", hero=self.nome,
                hab=colorir(nome("Raio Congelante"), Cor.CIANO), dano=dano)
        if random.random() < 0.5:
            alvo.aplicar_efeito(ATORDOADO, 1)
            return msg + t("hab.sufixo_congela")
        return msg + t("hab.fim")


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
        dano = alvo.receber_dano(int(self.ataque * (3 if critico else 1.5)))
        hab = colorir(nome("Tiro Certeiro"), Cor.VERDE)
        if critico:
            return t("hab.tiro_certeiro_crit", hero=self.nome,
                     crit=colorir(t("hab.critico_palavra"), Cor.AMARELO), hab=hab, dano=dano)
        return t("hab.tiro_certeiro", hero=self.nome, hab=hab, dano=dano)

    def _chuva_de_flechas(self, alvo):
        dano = alvo.receber_dano(int(self.ataque * 1.7))
        return t("hab.chuva", hero=self.nome,
                 hab=colorir(nome("Chuva de Flechas"), Cor.VERDE), dano=dano)


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
        cura = self.curar(50)
        return t("hab.luz_curativa", hero=self.nome,
                 hab=colorir(nome("Luz Curativa"), Cor.AMARELO), cura=cura)

    def _martelo_sagrado(self, alvo):
        dano = alvo.receber_dano(int(self.ataque * 1.5))
        msg = t("hab.martelo", hero=self.nome,
                hab=colorir(nome("Martelo Sagrado"), Cor.AMARELO), dano=dano)
        if random.random() < 0.4:
            alvo.aplicar_efeito(ATORDOADO, 1)
            return msg + t("hab.sufixo_atordoa")
        return msg + t("hab.fim")


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
        dano = alvo.receber_dano(self.ataque)
        alvo.aplicar_efeito(VENENO, 3)
        return t("hab.golpe_sombrio", hero=self.nome,
                 hab=colorir(nome("Golpe Sombrio"), Cor.MAGENTA), dano=dano)

    def _apunhalar(self, alvo):
        dano = alvo.receber_dano(self.ataque * 2)
        return t("hab.apunhalar", hero=self.nome,
                 hab=colorir(t("hab.apunhala_verbo"), Cor.MAGENTA), dano=dano)


# Maps a readable name to its class, used by the character creation menu.
CLASSES_JOGAVEIS = {
    "Guerreiro": Warrior,
    "Mago": Mage,
    "Arqueiro": Archer,
    "Paladino": Paladin,
    "Ladino": Rogue,
}
