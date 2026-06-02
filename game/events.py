"""
events.py — eventos aleatórios entre/durante as fases.

Ao entrar numa fase, às vezes algo acontece antes da luta: um baú, uma
armadilha, uma fonte mágica ou um mercador misterioso. Isso deixa a aventura
imprevisível e mais divertida.

Cada evento é uma FUNÇÃO que recebe o herói, narra o que acontece e aplica o
efeito. Guardamos todas numa lista (EVENTOS) e sorteamos uma com random.choice.
"""

import random

from game.items import CATALOGO_ITENS, criar_item
from game.ui import Cor, colorir, ler_opcao, pausar


def evento_bau(heroi):
    """Um baú: dá ouro ou um item, na sorte."""
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
    """Uma armadilha: causa dano, mas nunca mata (deixa ao menos 1 de vida)."""
    print(colorir("\n💥 Uma armadilha dispara!", Cor.VERMELHO + Cor.NEGRITO))
    dano = random.randint(10, 25)
    heroi.hp = max(1, heroi.hp - dano)  # max(1, ...) garante que não morre aqui
    print(colorir(f"Você perde {dano} de vida. {heroi.barra_de_vida()}", Cor.VERMELHO))
    pausar()


def evento_fonte(heroi):
    """Uma fonte mágica: restaura vida e energia."""
    print(colorir("\n⛲ Você encontra uma fonte mágica reluzente.", Cor.CIANO + Cor.NEGRITO))
    vida = heroi.curar(40)
    heroi.recuperar_energia(heroi.energia_max)  # energia totalmente restaurada
    print(colorir(f"Você recupera {vida} de vida e toda a energia.", Cor.VERDE))
    pausar()


def evento_mercador_misterioso(heroi):
    """Um mercador oferece um item com desconto. O jogador decide se compra."""
    nome_item = random.choice(list(CATALOGO_ITENS.keys()))
    preco = random.randint(15, 40)  # preço camarada
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


# Lista de todos os eventos possíveis. Para criar um novo evento, basta escrever
# a função acima e adicioná-la aqui.
EVENTOS = [
    evento_bau,
    evento_armadilha,
    evento_fonte,
    evento_mercador_misterioso,
]


def evento_aleatorio(heroi):
    """Sorteia um evento da lista e o executa."""
    evento = random.choice(EVENTOS)
    evento(heroi)
