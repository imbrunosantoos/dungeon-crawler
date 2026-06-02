"""
shop.py — a loja do aventureiro.

Entre as fases, o jogador pode gastar o ouro acumulado comprando itens, ou
vender o que não quer por metade do preço. Reaproveitamos o catálogo de itens
(items.CATALOGO_ITENS / criar_item) e o inventário do herói.

A loja é um LOOP de menu: mostra o ouro, lista o que dá para comprar/vender, e
só termina quando o jogador escolhe sair.
"""

from game.items import CATALOGO_ITENS, criar_item
from game.ui import Cor, colorir, limpar_tela, ler_opcao, pausar, titulo


# Preço de compra de cada item. A venda vale metade (ver _vender).
PRECOS = {
    "Poção Pequena": 20,
    "Poção Grande": 50,
    "Armadura de Couro": 70,
    "Espada de Ferro": 80,
    "Armadura de Placas": 140,
    "Machado de Guerra": 150,
}


def _comprar(heroi, nome_item):
    """Tenta comprar um item: confere o ouro, desconta e coloca na mochila."""
    preco = PRECOS[nome_item]
    if heroi.ouro < preco:
        print(colorir("\nOuro insuficiente!", Cor.VERMELHO))
    else:
        heroi.ouro -= preco
        heroi.inventario.adicionar(criar_item(nome_item))
        print(colorir(f"\nVocê comprou {nome_item} por {preco} de ouro.", Cor.VERDE))
    pausar()


def _vender(heroi):
    """Vende um item da mochila por metade do preço de compra."""
    # Só dá para vender itens que têm preço no catálogo.
    vendaveis = [it for it in heroi.inventario.itens if it.nome in PRECOS]
    if not vendaveis:
        print(colorir("\nVocê não tem itens para vender.", Cor.VERMELHO))
        pausar()
        return

    print("\nO que deseja vender? (recebe metade do preço)")
    for i, item in enumerate(vendaveis, start=1):
        print(f"  [{i}] {item.nome} — {PRECOS[item.nome] // 2} de ouro")
    print(f"  [{len(vendaveis) + 1}] Cancelar")

    opcoes = [str(i) for i in range(1, len(vendaveis) + 2)]
    escolha = int(ler_opcao("> ", opcoes))
    if escolha == len(vendaveis) + 1:
        return  # cancelar

    item = vendaveis[escolha - 1]
    valor = PRECOS[item.nome] // 2
    heroi.inventario.itens.remove(item)
    heroi.ouro += valor
    print(colorir(f"\nVocê vendeu {item.nome} por {valor} de ouro.", Cor.AMARELO))
    pausar()


def abrir_loja(heroi):
    """Tela principal da loja, em loop até o jogador sair."""
    # Lista fixa de itens à venda, ordenada por preço (do dicionário PRECOS).
    a_venda = list(PRECOS.keys())

    while True:
        limpar_tela()
        titulo("Loja do Aventureiro")
        print(colorir(f"\nSeu ouro: {heroi.ouro}\n", Cor.AMARELO + Cor.NEGRITO))

        print("Comprar:")
        for i, nome_item in enumerate(a_venda, start=1):
            print(f"  [{i}] {nome_item} — {PRECOS[nome_item]} de ouro")

        # As duas últimas opções são vender e sair.
        opcao_vender = len(a_venda) + 1
        opcao_sair = len(a_venda) + 2
        print(f"\n  [{opcao_vender}] Vender um item")
        print(f"  [{opcao_sair}] Sair da loja")

        opcoes = [str(i) for i in range(1, opcao_sair + 1)]
        escolha = int(ler_opcao("> ", opcoes))

        if escolha == opcao_sair:
            return
        if escolha == opcao_vender:
            _vender(heroi)
        else:
            _comprar(heroi, a_venda[escolha - 1])
