"""Turn-based combat loop."""

import random

from game.bestiary import registrar_visto
from game.character import VENENO
from game.difficulty import fator_ouro
from game.i18n import nome, t
from game.ui import Cor, colorir, digitar, ler_opcao, pausar


def _turno_do_inimigo(inimigo, heroi, heroi_defendendo):
    """Resolve the enemy's attack against the hero and return the message."""
    # Roll to hit first.
    if random.random() > inimigo.precisao:
        return colorir(t("combate.inimigo_erra", nome=inimigo.nome_colorido()), Cor.CIANO)

    dano = inimigo.ataque
    if heroi_defendendo:
        dano = dano // 2
    dano_real = heroi.receber_dano(dano)
    msg = t("combate.inimigo_ataca", nome=inimigo.nome_colorido(), dano=dano_real)
    if heroi_defendendo:
        msg += colorir(t("combate.defesa_reduziu"), Cor.AZUL)

    # Some monsters can inflict a status effect on hit.
    if inimigo.efeito_ataque:
        nome_efeito, chance, turnos = inimigo.efeito_ataque
        if random.random() < chance:
            heroi.aplicar_efeito(nome_efeito, turnos)
            msg += colorir(t("combate.afetado", efeito=nome(nome_efeito)), Cor.MAGENTA)
    return msg


def _dar_recompensa(heroi, inimigo):
    """Grant XP and gold for a kill and announce a level up if it happens."""
    nivel_antes = heroi.nivel

    # Gold scales with the chosen difficulty.
    fator = fator_ouro(getattr(heroi, "dificuldade", "Normal"))
    ouro_ganho = int(inimigo.ouro_recompensa * fator)

    heroi.ouro += ouro_ganho
    print(colorir(t("combate.recompensa_xp", xp=inimigo.xp_recompensa), Cor.CIANO))
    print(colorir(t("combate.recompensa_ouro", ouro=ouro_ganho), Cor.AMARELO))

    heroi.ganhar_xp(inimigo.xp_recompensa)

    if heroi.nivel > nivel_antes:
        print(colorir(t("combate.level_up", nivel=heroi.nivel), Cor.VERDE + Cor.NEGRITO))
        print(colorir(t("combate.level_up_detalhe"), Cor.VERDE))


def combate(heroi, inimigo, velocidade=0.02):
    """Run a fight. Returns "vitoria", "derrota" or "fuga"."""
    registrar_visto(inimigo.nome)  # discover this monster in the bestiary
    digitar(colorir(t("combate.aparece", nome=nome(inimigo.nome)), Cor.VERMELHO + Cor.NEGRITO), velocidade)

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
            print(colorir(t("combate.heroi_veneno_morte", nome=heroi.nome), Cor.VERMELHO + Cor.NEGRITO))
            return _terminar("derrota")

        print(colorir("-" * 50, Cor.CINZA))
        print(heroi.ficha())
        print(f"\n{inimigo.nome_colorido()}  {inimigo.barra_de_vida()}")
        print(colorir("-" * 50, Cor.CINZA))

        heroi_defendendo = False

        # A stunned hero loses the turn.
        if heroi.consumir_atordoamento():
            print(colorir(t("combate.heroi_atordoado"), Cor.MAGENTA))
        else:
            print(t("combate.o_que_faz"))
            print(t("combate.acao_atacar"))
            # Ability option only when the hero has special moves.
            tem_habilidade = hasattr(heroi, "habilidades")
            if tem_habilidade:
                print(t("combate.acao_habilidades"))
            print(t("combate.acao_defender"))
            print(t("combate.acao_fugir"))

            # Potion option only when there are potions in the bag.
            tem_inventario = hasattr(heroi, "inventario")
            opcoes = ["1", "2", "3", "4"]
            if tem_inventario and heroi.inventario.pocoes():
                print(t("combate.acao_pocao", qtd=len(heroi.inventario.pocoes())))
                opcoes.append("5")

            escolha = ler_opcao("> ", opcoes)

            if escolha == "1":
                # Roll to hit, then roll for a crit.
                if random.random() > heroi.precisao:
                    print(colorir(t("combate.voce_erra"), Cor.CINZA))
                else:
                    critico = random.random() < heroi.chance_critico
                    dano = heroi.ataque
                    if critico:
                        dano = int(dano * heroi.multiplicador_critico)
                    dano_real = inimigo.receber_dano(dano)
                    if critico:
                        print(colorir(t("combate.voce_critico", dano=dano_real), Cor.AMARELO + Cor.NEGRITO))
                    else:
                        print(colorir(t("combate.voce_ataca", dano=dano_real), Cor.VERDE))
                    # A poison-enchanted weapon envenoms on a landed hit.
                    if heroi.veneno_no_ataque > 0:
                        inimigo.aplicar_efeito(VENENO, heroi.veneno_no_ataque)
                        print(colorir(t("combate.lamina_envenena"), Cor.MAGENTA))

            elif escolha == "2":
                if not tem_habilidade:
                    print(colorir(t("combate.sem_habilidade"), Cor.VERMELHO))
                    continue  # retry the turn
                # Submenu: pick which ability to use.
                habs = heroi.habilidades()
                print(t("combate.qual_habilidade"))
                for i, h in enumerate(habs, start=1):
                    etiqueta = t("combate.habilidade_item", i=i, nome=nome(h.nome), custo=h.custo)
                    if heroi.energia < h.custo:
                        etiqueta = colorir(etiqueta + t("combate.sem_energia_sufixo"), Cor.CINZA)
                    print(etiqueta)
                print(f"  [{len(habs) + 1}] {t('ui.voltar')}")
                idx = int(ler_opcao("> ", [str(i) for i in range(1, len(habs) + 2)]))
                if idx == len(habs) + 1:
                    continue  # back out, retry the turn
                escolhida = habs[idx - 1]
                if heroi.energia < escolhida.custo:
                    print(colorir(t("combate.energia_insuficiente"), Cor.VERMELHO))
                    continue
                heroi.energia -= escolhida.custo
                print("\n" + escolhida.executar(inimigo))

            elif escolha == "3":
                heroi_defendendo = True
                print(colorir(t("combate.defensiva"), Cor.AZUL))

            elif escolha == "4":
                # 50% chance to escape.
                if random.random() < 0.5:
                    print(colorir(t("combate.fuga_ok"), Cor.AMARELO))
                    return _terminar("fuga")
                print(colorir(t("combate.fuga_falhou"), Cor.VERMELHO))

            elif escolha == "5":
                pocoes = heroi.inventario.pocoes()
                print(t("combate.qual_pocao"))
                for i, p in enumerate(pocoes, start=1):
                    print(f"  [{i}] {p}")
                indice = ler_opcao("> ", [str(i) for i in range(1, len(pocoes) + 1)])
                escolhida = pocoes[int(indice) - 1]
                print("\n" + heroi.inventario.usar_pocao(escolhida))

        if not inimigo.esta_vivo():
            print(colorir(t("combate.derrotou", nome=nome(inimigo.nome)), Cor.VERDE + Cor.NEGRITO))
            _dar_recompensa(heroi, inimigo)
            return _terminar("vitoria")

        # Enemy's turn also starts with poison ticking.
        msg_veneno_inimigo = inimigo.processar_veneno()
        if msg_veneno_inimigo:
            print(msg_veneno_inimigo)
        if not inimigo.esta_vivo():
            print(colorir(t("combate.inimigo_veneno_morte", nome=nome(inimigo.nome)), Cor.VERDE + Cor.NEGRITO))
            _dar_recompensa(heroi, inimigo)
            return _terminar("vitoria")

        # Enemy attacks unless stunned.
        if inimigo.consumir_atordoamento():
            print(colorir(t("combate.inimigo_atordoado", nome=nome(inimigo.nome)), Cor.MAGENTA))
        else:
            print(_turno_do_inimigo(inimigo, heroi, heroi_defendendo))

        heroi.recuperar_energia(5)

        # Regen enchantment heals a bit each round.
        if heroi.regen_por_turno > 0 and heroi.esta_vivo():
            curado = heroi.curar(heroi.regen_por_turno)
            if curado:
                print(colorir(t("combate.regen", cura=curado), Cor.VERDE))

        if not heroi.esta_vivo():
            print(colorir(t("combate.heroi_derrotado", nome=heroi.nome), Cor.VERMELHO + Cor.NEGRITO))
            return _terminar("derrota")

        pausar()

    # Safety net; the loop normally returns above.
    return _terminar("vitoria" if heroi.esta_vivo() else "derrota")
