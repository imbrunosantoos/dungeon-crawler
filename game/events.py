"""Random events that can trigger when entering a stage."""

import random

from game.i18n import nome, t
from game.items import CATALOGO_ITENS, criar_item
from game.ui import Cor, colorir, ler_opcao, pausar


def evento_bau(heroi):
    """Chest: gives gold or a random item."""
    print(colorir(t("evt.bau"), Cor.AMARELO + Cor.NEGRITO))
    if random.random() < 0.5:
        ouro = random.randint(30, 80)
        heroi.ouro += ouro
        print(colorir(t("evt.bau_ouro", ouro=ouro), Cor.AMARELO))
    else:
        nome_item = random.choice(list(CATALOGO_ITENS.keys()))
        heroi.inventario.adicionar(criar_item(nome_item))
        print(colorir(t("evt.bau_item", item=nome(nome_item)), Cor.VERDE))
    pausar()


def evento_armadilha(heroi):
    """Trap: deals damage but never kills (leaves at least 1 HP)."""
    print(colorir(t("evt.armadilha"), Cor.VERMELHO + Cor.NEGRITO))
    dano = random.randint(10, 25)
    heroi.hp = max(1, heroi.hp - dano)
    print(colorir(t("evt.armadilha_dano", dano=dano, barra=heroi.barra_de_vida()), Cor.VERMELHO))
    pausar()


def evento_fonte(heroi):
    """Fountain: restores some health and all energy."""
    print(colorir(t("evt.fonte"), Cor.CIANO + Cor.NEGRITO))
    vida = heroi.curar(40)
    heroi.recuperar_energia(heroi.energia_max)
    print(colorir(t("evt.fonte_cura", vida=vida), Cor.VERDE))
    pausar()


def evento_mercador_misterioso(heroi):
    """Merchant: offers a cheap item; the player chooses to buy or not."""
    nome_item = random.choice(list(CATALOGO_ITENS.keys()))
    preco = random.randint(15, 40)
    print(colorir(t("evt.mercador"), Cor.MAGENTA + Cor.NEGRITO))
    print(t("evt.mercador_oferta", item=colorir(nome(nome_item), Cor.NEGRITO), preco=preco))
    print(t("evt.mercador_ouro", ouro=heroi.ouro))
    print("\n" + t("evt.comprar"))
    print(t("evt.recusar"))

    if ler_opcao("> ", ["1", "2"]) == "1":
        if heroi.ouro >= preco:
            heroi.ouro -= preco
            heroi.inventario.adicionar(criar_item(nome_item))
            print(colorir(t("evt.mercador_comprou", item=nome(nome_item)), Cor.VERDE))
        else:
            print(colorir(t("evt.mercador_sem_ouro"), Cor.VERMELHO))
    else:
        print(colorir(t("evt.mercador_recusou"), Cor.CINZA))
    pausar()


# All possible events. Add a new function above and list it here.
EVENTOS = [
    evento_bau,
    evento_armadilha,
    evento_fonte,
    evento_mercador_misterioso,
]


def evento_aleatorio(heroi):
    """Pick a random event and run it."""
    evento = random.choice(EVENTOS)
    evento(heroi)
