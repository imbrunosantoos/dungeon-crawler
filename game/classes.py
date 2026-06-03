"""
classes.py — as classes jogáveis: Guerreiro, Mago e Arqueiro.

Aqui aparece a HERANÇA. Em vez de reescrever vida, ataque, XP e nível, cada
classe jogável HERDA tudo isso de Character (escrevendo `class Warrior(Character)`).
Cada uma só define seus atributos iniciais diferentes e uma HABILIDADE ESPECIAL
própria.

Note também o POLIMORFISMO: as três classes têm um método com o MESMO nome
(`usar_habilidade`), mas cada uma faz uma coisa diferente. O combate poderá
chamar `heroi.usar_habilidade(alvo)` sem se importar com qual classe é.
"""

import random

from game.character import Character, VENENO
from game.ui import Cor, colorir


class Warrior(Character):
    """Guerreiro: muita vida e defesa. Habilidade: Golpe Poderoso (dano alto)."""

    nome_habilidade = "Golpe Poderoso"
    custo_habilidade = 10

    def __init__(self, nome):
        # super().__init__(...) chama o construtor da classe-mãe (Character),
        # aproveitando toda a lógica de criação. Passamos os atributos do guerreiro.
        super().__init__(nome=nome, hp_max=120, ataque=18, defesa=8)
        self.energia_max = 20
        self.energia = self.energia_max

    def usar_habilidade(self, alvo):
        """Golpe Poderoso: causa o dobro do ataque normal."""
        dano = self.ataque * 2
        dano_real = alvo.receber_dano(dano)
        return f"{self.nome} usa {colorir(self.nome_habilidade, Cor.VERMELHO)} e causa {dano_real} de dano!"


class Mage(Character):
    """Mago: pouca vida, ataque forte. Habilidade: Bola de Fogo (ignora defesa)."""

    nome_habilidade = "Bola de Fogo"
    custo_habilidade = 15

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=80, ataque=24, defesa=4)
        self.energia_max = 30
        self.energia = self.energia_max

    def usar_habilidade(self, alvo):
        """Bola de Fogo: dano mágico que IGNORA a defesa do alvo.

        Aqui mexemos direto no hp do alvo (sem passar por receber_dano, que
        desconta defesa) — é assim que representamos "dano que fura armadura".
        """
        dano = self.ataque + 15
        alvo.hp = max(0, alvo.hp - dano)
        return f"{self.nome} lança {colorir(self.nome_habilidade, Cor.MAGENTA)} e causa {dano} de dano mágico (ignora defesa)!"


class Archer(Character):
    """Arqueiro: equilibrado. Habilidade: Tiro Certeiro (chance de acerto crítico)."""

    nome_habilidade = "Tiro Certeiro"
    custo_habilidade = 12

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=100, ataque=20, defesa=6)
        self.energia_max = 25
        self.energia = self.energia_max

    def usar_habilidade(self, alvo):
        """Tiro Certeiro: 50% de chance de causar dano TRIPLO (crítico)."""
        critico = random.random() < 0.5  # sorteia um número entre 0 e 1
        multiplicador = 3 if critico else 1.5
        dano = int(self.ataque * multiplicador)
        dano_real = alvo.receber_dano(dano)
        if critico:
            return f"{self.nome} acerta um {colorir('CRÍTICO', Cor.AMARELO)} com {self.nome_habilidade} e causa {dano_real} de dano!"
        return f"{self.nome} usa {colorir(self.nome_habilidade, Cor.VERDE)} e causa {dano_real} de dano!"


class Paladin(Character):
    """Paladino: muita vida e defesa. Habilidade: Luz Curativa (cura a si mesmo).

    Diferente das outras habilidades, esta NÃO ataca o alvo — ela cura o próprio
    herói. Por isso o método ignora o 'alvo' (usamos _ para indicar que não é
    usado) e chama self.curar().
    """

    nome_habilidade = "Luz Curativa"
    custo_habilidade = 15

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=130, ataque=16, defesa=10)
        self.energia_max = 25
        self.energia = self.energia_max

    def usar_habilidade(self, _alvo):
        """Luz Curativa: recupera 50 de vida do próprio paladino."""
        curado = self.curar(50)
        return f"{self.nome} invoca {colorir(self.nome_habilidade, Cor.AMARELO)} e recupera {curado} de vida!"


class Rogue(Character):
    """Ladino: ágil e mortal. Alta precisão e crítico. Habilidade: Golpe Sombrio
    (dano + envenena o alvo)."""

    nome_habilidade = "Golpe Sombrio"
    custo_habilidade = 12

    def __init__(self, nome):
        super().__init__(nome=nome, hp_max=95, ataque=21, defesa=5)
        self.energia_max = 25
        self.energia = self.energia_max
        # O ladino é mais certeiro e crítico que as outras classes.
        self.precisao = 0.95
        self.chance_critico = 0.25

    def usar_habilidade(self, alvo):
        """Golpe Sombrio: causa dano e aplica VENENO por 3 turnos no alvo."""
        dano_real = alvo.receber_dano(self.ataque)
        alvo.aplicar_efeito(VENENO, 3)
        return (
            f"{self.nome} desfere {colorir(self.nome_habilidade, Cor.MAGENTA)} "
            f"causando {dano_real} de dano e ENVENENANDO o inimigo!"
        )


# Um "catálogo" das classes jogáveis. É um dicionário que liga um nome legível
# à classe correspondente. Vamos usar isso no menu de criação de personagem
# para criar a classe escolhida pelo jogador.
CLASSES_JOGAVEIS = {
    "Guerreiro": Warrior,
    "Mago": Mage,
    "Arqueiro": Archer,
    "Paladino": Paladin,
    "Ladino": Rogue,
}
