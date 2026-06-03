"""Turn-based combat loop."""

import random

from game.character import VENENO
from game.difficulty import fator_ouro
from game.ui import Cor, colorir, digitar, ler_opcao, pausar


def _turno_do_inimigo(inimigo, heroi, heroi_defendendo):
    """Resolve the enemy's attack against the hero and return the message."""
    # Roll to hit first.
    if random.random() > inimigo.precisao:
        return colorir(f"{inimigo.nome_colorido()} ataca, mas ERRA o golpe!", Cor.CIANO)

    dano = inimigo.ataque
    if heroi_defendendo:
        dano = dano // 2
    dano_real = heroi.receber_dano(dano)
    msg = f"{inimigo.nome_colorido()} ataca e causa {dano_real} de dano."
    if heroi_defendendo:
        msg += colorir("  (defesa reduziu o golpe!)", Cor.AZUL)

    # Some monsters can inflict a status effect on hit.
    if inimigo.efeito_ataque:
        nome_efeito, chance, turnos = inimigo.efeito_ataque
        if random.random() < chance:
            heroi.aplicar_efeito(nome_efeito, turnos)
            msg += colorir(f"  Você foi afetado por {nome_efeito}!", Cor.MAGENTA)
    return msg


def _dar_recompensa(heroi, inimigo):
    """Grant XP and gold for a kill and announce a level up if it happens."""
    nivel_antes = heroi.nivel

    # Gold scales with the chosen difficulty.
    fator = fator_ouro(getattr(heroi, "dificuldade", "Normal"))
    ouro_ganho = int(inimigo.ouro_recompensa * fator)

    heroi.ouro += ouro_ganho
    print(colorir(f"  + {inimigo.xp_recompensa} XP", Cor.CIANO))
    print(colorir(f"  + {ouro_ganho} de ouro", Cor.AMARELO))

    heroi.ganhar_xp(inimigo.xp_recompensa)

    if heroi.nivel > nivel_antes:
        print(colorir(
            f"\n★ LEVEL UP! Você alcançou o nível {heroi.nivel}!",
            Cor.VERDE + Cor.NEGRITO,
        ))
        print(colorir("  Seus atributos aumentaram e sua vida foi restaurada.", Cor.VERDE))


def combate(heroi, inimigo, velocidade=0.02):
    """Run a fight. Returns "vitoria", "derrota" or "fuga"."""
    digitar(colorir(f"\n⚔  Um {inimigo.nome} aparece!\n", Cor.VERMELHO + Cor.NEGRITO), velocidade)

    # Clear status effects on both sides when the fight ends.
    def _terminar(resultado):
        heroi.limpar_efeitos()
        inimigo.limpar_efeitos()
        return resultado

    while heroi.esta_vivo() and inimigo.esta_vivo():
        # Hero's turn starts with poison ticking.
        msg_veneno = heroi.processar_veneno()
        if msg_veneno:
            print(msg_veneno)
        if not heroi.esta_vivo():
            print(colorir(f"\n✘ {heroi.nome} sucumbe ao veneno...", Cor.VERMELHO + Cor.NEGRITO))
            return _terminar("derrota")

        print(colorir("-" * 50, Cor.CINZA))
        print(heroi.ficha())
        print(f"\n{inimigo.nome_colorido()}  {inimigo.barra_de_vida()}")
        print(colorir("-" * 50, Cor.CINZA))

        heroi_defendendo = False

        # A stunned hero loses the turn.
        if heroi.consumir_atordoamento():
            print(colorir("\nVocê está ATORDOADO e perde a vez!", Cor.MAGENTA))
        else:
            print("O que você faz?")
            print(f"  [1] Atacar")
            # Ability option only when the hero has special moves.
            tem_habilidade = hasattr(heroi, "habilidades")
            if tem_habilidade:
                print(f"  [2] Habilidades especiais")
            print(f"  [3] Defender (reduz o próximo dano)")
            print(f"  [4] Fugir")

            # Potion option only when there are potions in the bag.
            tem_inventario = hasattr(heroi, "inventario")
            opcoes = ["1", "2", "3", "4"]
            if tem_inventario and heroi.inventario.pocoes():
                qtd = len(heroi.inventario.pocoes())
                print(f"  [5] Usar poção ({qtd} disponível(is))")
                opcoes.append("5")

            escolha = ler_opcao("> ", opcoes)

            if escolha == "1":
                # Roll to hit, then roll for a crit.
                if random.random() > heroi.precisao:
                    print(colorir("\nVocê ataca, mas ERRA o golpe!", Cor.CINZA))
                else:
                    critico = random.random() < heroi.chance_critico
                    dano = heroi.ataque
                    if critico:
                        dano = int(dano * heroi.multiplicador_critico)
                    dano_real = inimigo.receber_dano(dano)
                    if critico:
                        print(colorir(f"\n★ CRÍTICO! Você causa {dano_real} de dano!", Cor.AMARELO + Cor.NEGRITO))
                    else:
                        print(colorir(f"\nVocê ataca e causa {dano_real} de dano!", Cor.VERDE))
                    # A poison-enchanted weapon envenoms on a landed hit.
                    if heroi.veneno_no_ataque > 0:
                        inimigo.aplicar_efeito(VENENO, heroi.veneno_no_ataque)
                        print(colorir("  Sua lâmina ENVENENA o inimigo!", Cor.MAGENTA))

            elif escolha == "2":
                if not tem_habilidade:
                    print(colorir("\nVocê não tem habilidades especiais.", Cor.VERMELHO))
                    continue  # retry the turn
                # Submenu: pick which ability to use.
                habs = heroi.habilidades()
                print("\nQual habilidade?")
                for i, h in enumerate(habs, start=1):
                    etiqueta = f"  [{i}] {h.nome} ({h.custo} energia)"
                    if heroi.energia < h.custo:
                        etiqueta = colorir(etiqueta + " — sem energia", Cor.CINZA)
                    print(etiqueta)
                print(f"  [{len(habs) + 1}] Voltar")
                idx = int(ler_opcao("> ", [str(i) for i in range(1, len(habs) + 2)]))
                if idx == len(habs) + 1:
                    continue  # back out, retry the turn
                escolhida = habs[idx - 1]
                if heroi.energia < escolhida.custo:
                    print(colorir("\nEnergia insuficiente!", Cor.VERMELHO))
                    continue
                heroi.energia -= escolhida.custo
                print("\n" + escolhida.executar(inimigo))

            elif escolha == "3":
                heroi_defendendo = True
                print(colorir("\nVocê assume posição defensiva.", Cor.AZUL))

            elif escolha == "4":
                # 50% chance to escape.
                if random.random() < 0.5:
                    print(colorir("\nVocê conseguiu fugir!", Cor.AMARELO))
                    return _terminar("fuga")
                print(colorir("\nA fuga falhou!", Cor.VERMELHO))

            elif escolha == "5":
                pocoes = heroi.inventario.pocoes()
                print("\nQual poção?")
                for i, p in enumerate(pocoes, start=1):
                    print(f"  [{i}] {p}")
                indice = ler_opcao("> ", [str(i) for i in range(1, len(pocoes) + 1)])
                escolhida = pocoes[int(indice) - 1]
                print("\n" + heroi.inventario.usar_pocao(escolhida))

        if not inimigo.esta_vivo():
            print(colorir(f"\n✔ Você derrotou {inimigo.nome}!", Cor.VERDE + Cor.NEGRITO))
            _dar_recompensa(heroi, inimigo)
            return _terminar("vitoria")

        # Enemy's turn also starts with poison ticking.
        msg_veneno_inimigo = inimigo.processar_veneno()
        if msg_veneno_inimigo:
            print(msg_veneno_inimigo)
        if not inimigo.esta_vivo():
            print(colorir(f"\n✔ {inimigo.nome} sucumbe ao veneno!", Cor.VERDE + Cor.NEGRITO))
            _dar_recompensa(heroi, inimigo)
            return _terminar("vitoria")

        # Enemy attacks unless stunned.
        if inimigo.consumir_atordoamento():
            print(colorir(f"\n{inimigo.nome} está ATORDOADO e perde a vez!", Cor.MAGENTA))
        else:
            print(_turno_do_inimigo(inimigo, heroi, heroi_defendendo))

        heroi.recuperar_energia(5)

        # Regen enchantment heals a bit each round.
        if heroi.regen_por_turno > 0 and heroi.esta_vivo():
            curado = heroi.curar(heroi.regen_por_turno)
            if curado:
                print(colorir(f"Sua armadura rúnica regenera {curado} de vida.", Cor.VERDE))

        if not heroi.esta_vivo():
            print(colorir(f"\n✘ {heroi.nome} foi derrotado...", Cor.VERMELHO + Cor.NEGRITO))
            return _terminar("derrota")

        pausar()

    # Safety net; the loop normally returns above.
    return _terminar("vitoria" if heroi.esta_vivo() else "derrota")
