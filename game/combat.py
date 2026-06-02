"""
combat.py — o sistema de combate por turnos.

Esta é a parte mais "viva" do jogo: um LOOP que se repete a cada turno. Em cada
turno o jogador escolhe uma ação, ela é resolvida, e depois o inimigo reage.
O loop só termina quando alguém fica sem vida (ou o jogador foge).

É um bom exemplo de "máquina de estados" simples: o estado é "quem está vivo",
e as ações mudam esse estado até chegar a um fim (vitória, derrota ou fuga).
"""

import random

from game.difficulty import fator_ouro
from game.ui import Cor, colorir, digitar, ler_opcao, pausar


def _turno_do_inimigo(inimigo, heroi, heroi_defendendo):
    """Resolve o ataque do inimigo contra o herói.

    Se o herói escolheu Defender neste turno, o dano recebido é reduzido pela
    metade. Devolve a mensagem do que aconteceu.
    """
    dano = inimigo.ataque
    if heroi_defendendo:
        dano = dano // 2  # // é divisão inteira (descarta a parte decimal)
    dano_real = heroi.receber_dano(dano)
    msg = f"{inimigo.nome_colorido()} ataca e causa {dano_real} de dano."
    if heroi_defendendo:
        msg += colorir("  (defesa reduziu o golpe!)", Cor.AZUL)
    return msg


def _dar_recompensa(heroi, inimigo):
    """Entrega XP e ouro do inimigo derrotado ao herói, e avisa se subiu de nível.

    Guardamos o nível antes de dar o XP; se depois o nível for maior, é porque
    o herói evoluiu — então mostramos a mensagem de level up.
    """
    nivel_antes = heroi.nivel

    # O ouro ganho é ajustado pelo nível de dificuldade do herói (ex.: Fácil
    # rende mais ouro). getattr usa "Normal" caso o herói não tenha dificuldade.
    fator = fator_ouro(getattr(heroi, "dificuldade", "Normal"))
    ouro_ganho = int(inimigo.ouro_recompensa * fator)

    heroi.ouro += ouro_ganho
    print(colorir(f"  + {inimigo.xp_recompensa} XP", Cor.CIANO))
    print(colorir(f"  + {ouro_ganho} de ouro", Cor.AMARELO))

    heroi.ganhar_xp(inimigo.xp_recompensa)  # isto pode subir o nível sozinho

    if heroi.nivel > nivel_antes:
        print(colorir(
            f"\n★ LEVEL UP! Você alcançou o nível {heroi.nivel}!",
            Cor.VERDE + Cor.NEGRITO,
        ))
        print(colorir("  Seus atributos aumentaram e sua vida foi restaurada.", Cor.VERDE))


def combate(heroi, inimigo, velocidade=0.02):
    """Conduz uma luta entre o herói e um inimigo.

    Retorna uma string com o resultado: "vitoria", "derrota" ou "fuga".
    (A recompensa por vencer é tratada na etapa 6.)
    """
    digitar(colorir(f"\n⚔  Um {inimigo.nome} aparece!\n", Cor.VERMELHO + Cor.NEGRITO), velocidade)

    # O loop principal do combate: roda enquanto os dois estiverem vivos.
    while heroi.esta_vivo() and inimigo.esta_vivo():
        # --- Mostra a situação atual dos dois ---
        print(colorir("-" * 50, Cor.CINZA))
        print(heroi.ficha())
        print(f"\n{inimigo.nome_colorido()}  {inimigo.barra_de_vida()}")
        print(colorir("-" * 50, Cor.CINZA))

        # --- Menu de ações do jogador ---
        print("O que você faz?")
        print(f"  [1] Atacar")
        # A habilidade especial só aparece se o herói tiver uma (classes jogáveis)
        # e energia suficiente para usá-la.
        tem_habilidade = hasattr(heroi, "usar_habilidade")
        if tem_habilidade:
            custo = heroi.custo_habilidade
            disponivel = heroi.energia >= custo
            etiqueta = f"  [2] {heroi.nome_habilidade} (custa {custo} energia)"
            if not disponivel:
                etiqueta = colorir(etiqueta + " — sem energia", Cor.CINZA)
            print(etiqueta)
        print(f"  [3] Defender (reduz o próximo dano)")
        print(f"  [4] Fugir")

        # Opção de usar poção, só aparece se o herói tiver inventário com poções.
        tem_inventario = hasattr(heroi, "inventario")
        opcoes = ["1", "2", "3", "4"]
        if tem_inventario and heroi.inventario.pocoes():
            qtd = len(heroi.inventario.pocoes())
            print(f"  [5] Usar poção ({qtd} disponível(is))")
            opcoes.append("5")

        escolha = ler_opcao("> ", opcoes)
        heroi_defendendo = False

        if escolha == "1":
            dano_real = inimigo.receber_dano(heroi.ataque)
            print(colorir(f"\nVocê ataca e causa {dano_real} de dano!", Cor.VERDE))

        elif escolha == "2":
            if not tem_habilidade:
                print(colorir("\nVocê não tem habilidade especial.", Cor.VERMELHO))
                continue  # volta ao começo do loop sem gastar o turno
            if heroi.energia < heroi.custo_habilidade:
                print(colorir("\nEnergia insuficiente!", Cor.VERMELHO))
                continue
            heroi.energia -= heroi.custo_habilidade
            print("\n" + heroi.usar_habilidade(inimigo))

        elif escolha == "3":
            heroi_defendendo = True
            print(colorir("\nVocê assume posição defensiva.", Cor.AZUL))

        elif escolha == "4":
            # 50% de chance de conseguir fugir. random.random() dá um número
            # entre 0 e 1; se for menor que 0.5, a fuga deu certo.
            if random.random() < 0.5:
                print(colorir("\nVocê conseguiu fugir!", Cor.AMARELO))
                return "fuga"
            print(colorir("\nA fuga falhou!", Cor.VERMELHO))

        elif escolha == "5":
            # Lista as poções e deixa o jogador escolher qual usar.
            pocoes = heroi.inventario.pocoes()
            print("\nQual poção?")
            for i, p in enumerate(pocoes, start=1):
                print(f"  [{i}] {p}")
            indice = ler_opcao("> ", [str(i) for i in range(1, len(pocoes) + 1)])
            escolhida = pocoes[int(indice) - 1]
            print("\n" + heroi.inventario.usar_pocao(escolhida))

        # --- O inimigo morreu? Então o jogador venceu. ---
        if not inimigo.esta_vivo():
            print(colorir(f"\n✔ Você derrotou {inimigo.nome}!", Cor.VERDE + Cor.NEGRITO))
            _dar_recompensa(heroi, inimigo)
            return "vitoria"

        # --- Turno do inimigo ---
        print(_turno_do_inimigo(inimigo, heroi, heroi_defendendo))

        # No fim do turno o herói recupera um pouco de energia.
        heroi.recuperar_energia(5)

        # --- O herói morreu? Então perdeu. ---
        if not heroi.esta_vivo():
            print(colorir(f"\n✘ {heroi.nome} foi derrotado...", Cor.VERMELHO + Cor.NEGRITO))
            return "derrota"

        pausar()

    # Por segurança (o loop normalmente termina pelos return acima):
    return "vitoria" if heroi.esta_vivo() else "derrota"
