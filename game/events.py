"""Random events that can trigger when entering a stage."""

import random

from game.items import CATALOGO_ITENS, criar_item
from game.ui import Cor, colorir, ler_opcao, pausar


def evento_bau(heroi):
    """Chest: gives gold or a random item."""
    print(colorir("\n🧰 Você encontra um baú empoeirado!", Cor.AMARELO + Cor.NEGRITO))
    if random.random() < 0.5:
        ouro = random.randint(30, 80)
        heroi.ouro += ouro
        print(colorir(f"Dentro havia {ouro} de ouro!", Cor.AMARELO))
    else:
        nome_item = random.choice(list(CATALOGO_ITENS.keys()))
        heroi.inventario.adicionar(criar_item(nome_item))
        print(colorir(f"Dentro havia: {nome_item}!", Cor.VERDE))
    pausar()


def evento_armadilha(heroi):
    """Trap: deals damage but never kills (leaves at least 1 HP)."""
    print(colorir("\n💥 Uma armadilha dispara!", Cor.VERMELHO + Cor.NEGRITO))
    dano = random.randint(10, 25)
    heroi.hp = max(1, heroi.hp - dano)
    print(colorir(f"Você perde {dano} de vida. {heroi.barra_de_vida()}", Cor.VERMELHO))
    pausar()


def evento_fonte(heroi):
    """Fountain: restores some health and all energy."""
    print(colorir("\n⛲ Você encontra uma fonte mágica reluzente.", Cor.CIANO + Cor.NEGRITO))
    vida = heroi.curar(40)
    heroi.recuperar_energia(heroi.energia_max)
    print(colorir(f"Você recupera {vida} de vida e toda a energia.", Cor.VERDE))
    pausar()


def evento_mercador_misterioso(heroi):
    """Merchant: offers a cheap item; the player chooses to buy or not."""
    nome_item = random.choice(list(CATALOGO_ITENS.keys()))
    preco = random.randint(15, 40)
    print(colorir("\n🧙 Um mercador misterioso surge das sombras...", Cor.MAGENTA + Cor.NEGRITO))
    print(f'"Tenho um {colorir(nome_item, Cor.NEGRITO)} por apenas {preco} de ouro."')
    print(f"(Você tem {heroi.ouro} de ouro)")
    print("\n  [1] Comprar")
    print("  [2] Recusar")

    if ler_opcao("> ", ["1", "2"]) == "1":
        if heroi.ouro >= preco:
            heroi.ouro -= preco
            heroi.inventario.adicionar(criar_item(nome_item))
            print(colorir(f"Você comprou {nome_item}!", Cor.VERDE))
        else:
            print(colorir("Ouro insuficiente. O mercador desaparece.", Cor.VERMELHO))
    else:
        print(colorir("Você segue seu caminho.", Cor.CINZA))
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
