"""The shop: spend gold between stages to buy items, or sell for half price."""

from game.i18n import nome, t
from game.items import CATALOGO_ITENS, criar_item
from game.ui import Cor, colorir, limpar_tela, ler_opcao, pausar, titulo


# Buy price per item; selling gives half (see _vender).
PRECOS = {
    "Poção Pequena": 20,
    "Poção Grande": 50,
    "Armadura de Couro": 70,
    "Espada de Ferro": 80,
    "Poção Suprema": 120,
    "Armadura de Placas": 140,
    "Machado de Guerra": 150,
    "Adaga Afiada": 160,
    "Arco Élfico": 170,
    "Lâmina Venenosa": 180,
    "Armadura Rúnica": 190,
    "Escudo de Aço": 200,
    "Espada Flamejante": 220,
}


def _comprar(heroi, nome_item):
    """Buy an item if the hero can afford it."""
    preco = PRECOS[nome_item]
    if heroi.ouro < preco:
        print(colorir(t("loja.ouro_insuficiente"), Cor.VERMELHO))
    else:
        heroi.ouro -= preco
        heroi.inventario.adicionar(criar_item(nome_item))
        print(colorir(t("loja.comprou", nome=nome(nome_item), preco=preco), Cor.VERDE))
    pausar()


def _vender(heroi):
    """Sell a bag item for half its buy price."""
    # Only items that have a price can be sold.
    vendaveis = [it for it in heroi.inventario.itens if it.nome in PRECOS]
    if not vendaveis:
        print(colorir(t("loja.sem_vender"), Cor.VERMELHO))
        pausar()
        return

    print(t("loja.o_que_vender"))
    for i, item in enumerate(vendaveis, start=1):
        print(t("loja.item_venda", i=i, nome=nome(item.nome), valor=PRECOS[item.nome] // 2))
    print(f"  [{len(vendaveis) + 1}] {t('ui.cancelar')}")

    opcoes = [str(i) for i in range(1, len(vendaveis) + 2)]
    escolha = int(ler_opcao("> ", opcoes))
    if escolha == len(vendaveis) + 1:
        return  # cancel

    item = vendaveis[escolha - 1]
    valor = PRECOS[item.nome] // 2
    heroi.inventario.itens.remove(item)
    heroi.ouro += valor
    print(colorir(t("loja.vendeu", nome=nome(item.nome), valor=valor), Cor.AMARELO))
    pausar()


def abrir_loja(heroi):
    """Shop screen, looping until the player leaves."""
    a_venda = list(PRECOS.keys())

    while True:
        limpar_tela()
        titulo(t("loja.titulo"))
        print(colorir(t("loja.seu_ouro", ouro=heroi.ouro), Cor.AMARELO + Cor.NEGRITO))

        print(t("loja.comprar"))
        for i, nome_item in enumerate(a_venda, start=1):
            print(t("loja.item_compra", i=i, nome=nome(nome_item), preco=PRECOS[nome_item]))

        # Last two options are sell and exit.
        opcao_vender = len(a_venda) + 1
        opcao_sair = len(a_venda) + 2
        print(t("loja.vender", n=opcao_vender))
        print(t("loja.sair", n=opcao_sair))

        opcoes = [str(i) for i in range(1, opcao_sair + 1)]
        escolha = int(ler_opcao("> ", opcoes))

        if escolha == opcao_sair:
            return
        if escolha == opcao_vender:
            _vender(heroi)
        else:
            _comprar(heroi, a_venda[escolha - 1])
