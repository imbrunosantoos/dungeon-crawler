"""
main.py — ponto de entrada do Dungeon Crawler.

Este arquivo amarra todos os módulos: mostra o menu, cria o personagem, conduz
o jogador pelas fases (chamando o combate) e mostra as telas de vitória/derrota.

Para jogar:  python3 main.py
"""

import random

from game.classes import CLASSES_JOGAVEIS
from game.combat import combate
from game.difficulty import DIFICULDADES
from game.events import evento_aleatorio
from game.inventory import Inventory
from game.items import pocao_pequena
from game.saves import apagar_save, carregar, existe_save, salvar
from game.scores import registrar_pontuacao, top_pontuacoes
from game.shop import abrir_loja
from game.stages import (
    FASES,
    criar_inimigos_da_fase,
    premio_da_fase,
    total_de_fases,
)
from game.ui import Cor, colorir, digitar, limpar_tela, ler_opcao, ler_texto, pausar, titulo


# ---------------------------------------------------------------------------
# Criação do personagem
# ---------------------------------------------------------------------------
def criar_personagem():
    """Pergunta o nome e a classe, cria o herói e lhe dá itens iniciais."""
    limpar_tela()
    titulo("Criação de Personagem")

    nome = ""
    while not nome:  # não aceita nome vazio
        nome = ler_texto("\nQual o nome do seu herói? ")

    # Monta o menu de classes a partir do catálogo (dicionário CLASSES_JOGAVEIS).
    nomes_classes = list(CLASSES_JOGAVEIS.keys())
    print("\nEscolha sua classe:")
    for i, nome_classe in enumerate(nomes_classes, start=1):
        # Cria um exemplo só para mostrar os atributos de cada classe.
        exemplo = CLASSES_JOGAVEIS[nome_classe]("exemplo")
        print(
            f"  [{i}] {colorir(nome_classe, Cor.NEGRITO)} — "
            f"Vida {exemplo.hp_max}, Ataque {exemplo.ataque}, "
            f"Defesa {exemplo.defesa} | Habilidade: {exemplo.nome_habilidade}"
        )

    opcoes = [str(i) for i in range(1, len(nomes_classes) + 1)]
    escolha = ler_opcao("> ", opcoes)
    classe_escolhida = nomes_classes[int(escolha) - 1]

    # Cria o herói da classe escolhida.
    heroi = CLASSES_JOGAVEIS[classe_escolhida](nome)

    # Escolha da dificuldade (escala os inimigos durante toda a aventura).
    nomes_dificuldade = list(DIFICULDADES.keys())
    print("\nEscolha a dificuldade:")
    for i, nome_dif in enumerate(nomes_dificuldade, start=1):
        print(f"  [{i}] {colorir(nome_dif, Cor.NEGRITO)}")
    opcoes_dif = [str(i) for i in range(1, len(nomes_dificuldade) + 1)]
    escolha_dif = ler_opcao("> ", opcoes_dif)
    heroi.dificuldade = nomes_dificuldade[int(escolha_dif) - 1]

    # Todo herói começa com um inventário e duas poções pequenas.
    heroi.inventario = Inventory(heroi)
    heroi.inventario.adicionar(pocao_pequena())
    heroi.inventario.adicionar(pocao_pequena())

    # Começa na primeira fase (índice 0).
    heroi.fase_atual = 0

    print(colorir(f"\n{nome}, o {classe_escolhida}, está pronto para a aventura!", Cor.VERDE))
    pausar()
    return heroi


# ---------------------------------------------------------------------------
# Inventário entre as batalhas
# ---------------------------------------------------------------------------
def gerenciar_inventario(heroi):
    """Menu para o jogador ver/usar/equipar itens fora do combate."""
    while True:
        limpar_tela()
        print(heroi.ficha())
        print()
        print(heroi.inventario.listar())
        print("\n  [1] Equipar um item")
        print("  [2] Usar uma poção")
        print("  [3] Voltar")

        escolha = ler_opcao("> ", ["1", "2", "3"])

        if escolha == "3":
            return

        if escolha == "1":
            equipaveis = [it for it in heroi.inventario.itens if it.tipo in ("arma", "armadura")]
            if not equipaveis:
                print(colorir("\nVocê não tem itens para equipar.", Cor.VERMELHO))
                pausar()
                continue
            print("\nQual item equipar?")
            for i, it in enumerate(equipaveis, start=1):
                print(f"  [{i}] {it}")
            idx = ler_opcao("> ", [str(i) for i in range(1, len(equipaveis) + 1)])
            print("\n" + heroi.inventario.equipar(equipaveis[int(idx) - 1]))
            pausar()

        elif escolha == "2":
            pocoes = heroi.inventario.pocoes()
            if not pocoes:
                print(colorir("\nVocê não tem poções.", Cor.VERMELHO))
                pausar()
                continue
            print("\nQual poção usar?")
            for i, p in enumerate(pocoes, start=1):
                print(f"  [{i}] {p}")
            idx = ler_opcao("> ", [str(i) for i in range(1, len(pocoes) + 1)])
            print("\n" + heroi.inventario.usar_pocao(pocoes[int(idx) - 1]))
            pausar()


# ---------------------------------------------------------------------------
# O loop principal da aventura: percorrer as fases
# ---------------------------------------------------------------------------
def jogar(heroi):
    """Conduz o herói pelas fases, começando da fase em que ele parou.

    Usamos heroi.fase_atual (e não um range fixo) para que um jogo CARREGADO
    continue da fase certa. Devolve 'vitoria' ou 'derrota'.
    """
    while heroi.fase_atual < total_de_fases():
        indice = heroi.fase_atual
        fase = FASES[indice]
        limpar_tela()
        titulo(f"Fase {indice + 1}/{total_de_fases()}: {fase['nome']}")
        print(heroi.ficha())

        # Antes de entrar, deixa o jogador ajustar o inventário ou ir à loja.
        # Fica num loop para o jogador poder fazer várias coisas antes de entrar.
        while True:
            print(colorir("\n  [1] Entrar na fase", Cor.VERDE))
            print("  [2] Abrir inventário")
            print("  [3] Visitar a loja")
            acao = ler_opcao("> ", ["1", "2", "3"])
            if acao == "1":
                break
            if acao == "2":
                gerenciar_inventario(heroi)
            elif acao == "3":
                abrir_loja(heroi)
            # Após inventário/loja, volta a mostrar a ficha e o menu.
            limpar_tela()
            titulo(f"Fase {indice + 1}/{total_de_fases()}: {fase['nome']}")
            print(heroi.ficha())

        # Ao explorar a fase, há ~40% de chance de acontecer um evento aleatório
        # (baú, armadilha, fonte ou mercador) antes dos combates.
        if random.random() < 0.4:
            evento_aleatorio(heroi)

        # Enfrenta cada inimigo da fase, na ordem (escalados pela dificuldade).
        for inimigo in criar_inimigos_da_fase(indice, heroi.dificuldade):
            # Se o jogador fugir, ele recua mas precisa enfrentar de novo o mesmo
            # inimigo (que continua com a vida que tinha). Só avança ao vencer.
            while True:
                resultado = combate(heroi, inimigo)
                if resultado == "vitoria":
                    pausar()
                    break
                if resultado == "derrota":
                    return "derrota"
                # resultado == "fuga"
                print(colorir("\nVocê recua para recuperar o fôlego, mas o inimigo te espera...", Cor.AMARELO))
                gerenciar_inventario(heroi)

        # Fase concluída: entrega o prêmio e avança o marcador de fase.
        premio = premio_da_fase(indice)
        heroi.inventario.adicionar(premio)
        print(colorir(f"\n🎁 Fase concluída! Você recebeu: {premio.nome}", Cor.CIANO + Cor.NEGRITO))

        heroi.fase_atual = indice + 1
        salvar(heroi)  # salva o progresso automaticamente ao fim de cada fase
        print(colorir("Progresso salvo.", Cor.CINZA))
        pausar()

    return "vitoria"


# ---------------------------------------------------------------------------
# Telas de fim de jogo
# ---------------------------------------------------------------------------
def tela_vitoria(heroi):
    limpar_tela()
    titulo("VITÓRIA!")
    digitar(colorir(
        f"\n{heroi.nome} derrotou o Dragão Ancião e salvou o reino!",
        Cor.VERDE + Cor.NEGRITO,
    ))
    print(f"\nNível final: {heroi.nivel} | Ouro acumulado: {heroi.ouro}")
    pausar()


def tela_derrota(heroi):
    limpar_tela()
    titulo("FIM DE JOGO")
    digitar(colorir(
        f"\n{heroi.nome} tombou na masmorra. A aventura termina aqui...",
        Cor.VERMELHO + Cor.NEGRITO,
    ))
    print(f"\nVocê chegou ao nível {heroi.nivel}.")
    pausar()


# ---------------------------------------------------------------------------
# Menu inicial
# ---------------------------------------------------------------------------
def tela_recordes():
    """Mostra o placar com as melhores pontuações."""
    limpar_tela()
    titulo("PLACAR DE RECORDES")
    melhores = top_pontuacoes()
    if not melhores:
        print(colorir("\nAinda não há recordes. Seja o primeiro!", Cor.CINZA))
    else:
        print()
        for posicao, s in enumerate(melhores, start=1):
            marca = "✔" if s["venceu"] else "✘"
            print(
                f"  {posicao:>2}. {colorir(str(s['pontos']) + ' pts', Cor.AMARELO + Cor.NEGRITO)}"
                f" — {s['nome']} ({s['classe']}, nível {s['nivel']}, {s['dificuldade']}) {marca}"
            )
    pausar()


def menu_principal():
    """Mostra o menu inicial e devolve um CÓDIGO da escolha.

    Usar códigos ('novo', 'continuar', 'recordes', 'sair') em vez de números
    deixa o resto do programa independente da numeração — que muda conforme a
    opção 'Continuar' aparece ou não.
    """
    limpar_tela()
    titulo("DUNGEON CRAWLER")
    print(colorir("\nUm RPG de terminal\n", Cor.CINZA))

    # Monta a lista de opções dinamicamente: cada item liga um número a um código.
    itens = [("Novo jogo", "novo")]
    if existe_save():
        itens.append(("Continuar", "continuar"))
    itens.append(("Ver recordes", "recordes"))
    itens.append(("Sair", "sair"))

    for i, (rotulo, _codigo) in enumerate(itens, start=1):
        print(f"  [{i}] {rotulo}")

    escolha = ler_opcao("> ", [str(i) for i in range(1, len(itens) + 1)])
    return itens[int(escolha) - 1][1]  # devolve o código da opção escolhida


def main():
    """Função principal: roda o menu e inicia o jogo."""
    while True:
        escolha = menu_principal()

        if escolha == "sair":
            print(colorir("\nAté a próxima, aventureiro!", Cor.CIANO))
            return

        if escolha == "recordes":
            tela_recordes()
            continue

        if escolha == "continuar":
            heroi = carregar()  # continuar de onde parou
        else:
            heroi = criar_personagem()  # novo jogo

        resultado = jogar(heroi)

        # O jogo acabou (venceu ou perdeu): apaga o save para não continuar nele.
        apagar_save()
        venceu = resultado == "vitoria"

        # Registra a pontuação no placar de recordes.
        pontos = registrar_pontuacao(heroi, venceu)

        if venceu:
            tela_vitoria(heroi)
        else:
            tela_derrota(heroi)
        print(colorir(f"\nSua pontuação: {pontos} pontos", Cor.AMARELO + Cor.NEGRITO))
        pausar()


# Esta verificação garante que main() só roda quando executamos este arquivo
# diretamente (python3 main.py), e não quando ele é importado por outro módulo.
if __name__ == "__main__":
    main()
