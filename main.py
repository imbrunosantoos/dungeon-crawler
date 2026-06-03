"""Entry point: menus, character creation, the stage loop and end screens.

Run with:  python3 main.py
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
# Character creation
# ---------------------------------------------------------------------------
def criar_personagem():
    """Ask for name, class and difficulty, then build the hero with starter gear."""
    limpar_tela()
    titulo("Criação de Personagem")

    nome = ""
    while not nome:  # no empty names
        nome = ler_texto("\nQual o nome do seu herói? ")

    nomes_classes = list(CLASSES_JOGAVEIS.keys())
    print("\nEscolha sua classe:")
    for i, nome_classe in enumerate(nomes_classes, start=1):
        # Spin up a throwaway instance just to show the class stats.
        exemplo = CLASSES_JOGAVEIS[nome_classe]("exemplo")
        print(
            f"  [{i}] {colorir(nome_classe, Cor.NEGRITO)} — "
            f"Vida {exemplo.hp_max}, Ataque {exemplo.ataque}, "
            f"Defesa {exemplo.defesa} | Habilidade: {exemplo.nome_habilidade}"
        )

    opcoes = [str(i) for i in range(1, len(nomes_classes) + 1)]
    escolha = ler_opcao("> ", opcoes)
    classe_escolhida = nomes_classes[int(escolha) - 1]

    heroi = CLASSES_JOGAVEIS[classe_escolhida](nome)

    # Difficulty scales enemies for the whole run.
    nomes_dificuldade = list(DIFICULDADES.keys())
    print("\nEscolha a dificuldade:")
    for i, nome_dif in enumerate(nomes_dificuldade, start=1):
        print(f"  [{i}] {colorir(nome_dif, Cor.NEGRITO)}")
    opcoes_dif = [str(i) for i in range(1, len(nomes_dificuldade) + 1)]
    escolha_dif = ler_opcao("> ", opcoes_dif)
    heroi.dificuldade = nomes_dificuldade[int(escolha_dif) - 1]

    # Everyone starts with a bag and two small potions.
    heroi.inventario = Inventory(heroi)
    heroi.inventario.adicionar(pocao_pequena())
    heroi.inventario.adicionar(pocao_pequena())

    heroi.fase_atual = 0

    print(colorir(f"\n{nome}, o {classe_escolhida}, está pronto para a aventura!", Cor.VERDE))
    pausar()
    return heroi


# ---------------------------------------------------------------------------
# Inventory between battles
# ---------------------------------------------------------------------------
def gerenciar_inventario(heroi):
    """Out-of-combat menu to view, equip and use items."""
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
# Main adventure loop: go through the stages
# ---------------------------------------------------------------------------
def jogar(heroi):
    """Run the hero through the stages, resuming from heroi.fase_atual.

    Returns 'vitoria' or 'derrota'.
    """
    while heroi.fase_atual < total_de_fases():
        indice = heroi.fase_atual
        fase = FASES[indice]
        limpar_tela()
        titulo(f"Fase {indice + 1}/{total_de_fases()}: {fase['nome']}")
        print(heroi.ficha())

        # Pre-stage hub: the player can manage gear or shop before entering.
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
            # Redraw the header after inventory/shop.
            limpar_tela()
            titulo(f"Fase {indice + 1}/{total_de_fases()}: {fase['nome']}")
            print(heroi.ficha())

        # ~40% chance of a random event before the fights.
        if random.random() < 0.4:
            evento_aleatorio(heroi)

        for inimigo in criar_inimigos_da_fase(indice, heroi.dificuldade):
            # Fleeing pushes you back but the same (damaged) enemy waits; only a
            # win moves on.
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

        # Stage cleared: hand out the prize and advance.
        premio = premio_da_fase(indice)
        heroi.inventario.adicionar(premio)
        print(colorir(f"\n🎁 Fase concluída! Você recebeu: {premio.nome}", Cor.CIANO + Cor.NEGRITO))

        heroi.fase_atual = indice + 1
        salvar(heroi)  # autosave after each stage
        print(colorir("Progresso salvo.", Cor.CINZA))
        pausar()

    return "vitoria"


# ---------------------------------------------------------------------------
# End-of-game screens
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
# Main menu
# ---------------------------------------------------------------------------
def tela_recordes():
    """Show the leaderboard."""
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
    """Show the main menu and return a code string for the choice.

    Codes ('novo', 'continuar', 'recordes', 'sair') keep the caller independent
    of the numbering, which shifts when 'Continuar' is present.
    """
    limpar_tela()
    titulo("DUNGEON CRAWLER")
    print(colorir("\nUm RPG de terminal\n", Cor.CINZA))

    # Build the option list dynamically, each mapping a number to a code.
    itens = [("Novo jogo", "novo")]
    if existe_save():
        itens.append(("Continuar", "continuar"))
    itens.append(("Ver recordes", "recordes"))
    itens.append(("Sair", "sair"))

    for i, (rotulo, _codigo) in enumerate(itens, start=1):
        print(f"  [{i}] {rotulo}")

    escolha = ler_opcao("> ", [str(i) for i in range(1, len(itens) + 1)])
    return itens[int(escolha) - 1][1]


def main():
    while True:
        escolha = menu_principal()

        if escolha == "sair":
            print(colorir("\nAté a próxima, aventureiro!", Cor.CIANO))
            return

        if escolha == "recordes":
            tela_recordes()
            continue

        if escolha == "continuar":
            heroi = carregar()
        else:
            heroi = criar_personagem()

        resultado = jogar(heroi)

        # Game over (win or loss): drop the save so it can't be continued.
        apagar_save()
        venceu = resultado == "vitoria"

        pontos = registrar_pontuacao(heroi, venceu)

        if venceu:
            tela_vitoria(heroi)
        else:
            tela_derrota(heroi)
        print(colorir(f"\nSua pontuação: {pontos} pontos", Cor.AMARELO + Cor.NEGRITO))
        pausar()


# Only run the game when executed directly, not when imported.
if __name__ == "__main__":
    main()
