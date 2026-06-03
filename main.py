"""Entry point: menus, character creation, the stage loop and end screens.

Run with:  python3 main.py
"""

import random

from game.achievements import CONQUISTAS, checar as checar_conquistas, obtidas
from game.bestiary import vistos
from game.classes import CLASSES_JOGAVEIS
from game.combat import combate
from game.difficulty import DIFICULDADES
from game.events import evento_aleatorio
from game.i18n import IDIOMAS, definir_idioma, nome, t
from game.inventory import Inventory
from game.items import pocao_pequena
from game.monster import MODELOS_MONSTROS, criar_boss
from game.quests import objetivo_aleatorio
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
# Language selection
# ---------------------------------------------------------------------------
def escolher_idioma():
    """Pick the interface language. Prompt is trilingual since no language is set yet."""
    limpar_tela()
    titulo("DUNGEON CRAWLER")
    print(colorir("\nEscolha o idioma / Choose language / Elige el idioma\n", Cor.CINZA))
    codigos = list(IDIOMAS.keys())
    for i, code in enumerate(codigos, start=1):
        print(f"  [{i}] {IDIOMAS[code]}")
    escolha = ler_opcao("> ", [str(i) for i in range(1, len(codigos) + 1)])
    definir_idioma(codigos[int(escolha) - 1])


# ---------------------------------------------------------------------------
# Character creation
# ---------------------------------------------------------------------------
def criar_personagem():
    """Ask for name, class and difficulty, then build the hero with starter gear."""
    limpar_tela()
    titulo(t("main.criacao_titulo"))

    nome_heroi = ""
    while not nome_heroi:  # no empty names
        nome_heroi = ler_texto(t("main.pergunta_nome"))

    ids_classes = list(CLASSES_JOGAVEIS.keys())
    print(t("main.escolha_classe"))
    for i, id_classe in enumerate(ids_classes, start=1):
        # Spin up a throwaway instance just to show the class stats and skills.
        exemplo = CLASSES_JOGAVEIS[id_classe]("exemplo")
        skills = ", ".join(nome(h.nome) for h in exemplo.habilidades())
        print(t("main.classe_item", i=i, classe=colorir(nome(id_classe), Cor.NEGRITO),
                hp=exemplo.hp_max, atk=exemplo.ataque, df=exemplo.defesa, skills=skills))

    opcoes = [str(i) for i in range(1, len(ids_classes) + 1)]
    escolha = ler_opcao("> ", opcoes)
    id_classe = ids_classes[int(escolha) - 1]

    heroi = CLASSES_JOGAVEIS[id_classe](nome_heroi)

    # Difficulty scales enemies for the whole run.
    ids_dificuldade = list(DIFICULDADES.keys())
    print(t("main.escolha_dificuldade"))
    for i, id_dif in enumerate(ids_dificuldade, start=1):
        print(f"  [{i}] {colorir(nome(id_dif), Cor.NEGRITO)}")
    opcoes_dif = [str(i) for i in range(1, len(ids_dificuldade) + 1)]
    escolha_dif = ler_opcao("> ", opcoes_dif)
    heroi.dificuldade = ids_dificuldade[int(escolha_dif) - 1]

    # Everyone starts with a bag and two small potions.
    heroi.inventario = Inventory(heroi)
    heroi.inventario.adicionar(pocao_pequena())
    heroi.inventario.adicionar(pocao_pequena())

    heroi.fase_atual = 0

    print(colorir(t("main.pronto", nome=nome_heroi, classe=nome(id_classe)), Cor.VERDE))
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
        print("\n" + t("inv.menu_equipar"))
        print(t("inv.menu_pocao"))
        print(t("inv.menu_voltar"))

        escolha = ler_opcao("> ", ["1", "2", "3"])

        if escolha == "3":
            return

        if escolha == "1":
            equipaveis = [it for it in heroi.inventario.itens if it.tipo in ("arma", "armadura")]
            if not equipaveis:
                print(colorir(t("inv.sem_equipar"), Cor.VERMELHO))
                pausar()
                continue
            print(t("inv.qual_equipar"))
            for i, it in enumerate(equipaveis, start=1):
                print(f"  [{i}] {it}")
            idx = ler_opcao("> ", [str(i) for i in range(1, len(equipaveis) + 1)])
            print("\n" + heroi.inventario.equipar(equipaveis[int(idx) - 1]))
            pausar()

        elif escolha == "2":
            pocoes = heroi.inventario.pocoes()
            if not pocoes:
                print(colorir(t("inv.sem_pocoes"), Cor.VERMELHO))
                pausar()
                continue
            print(t("inv.qual_pocao_usar"))
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
        cabecalho = t("main.fase_titulo", atual=indice + 1, total=total_de_fases(),
                      nome=nome(fase["nome"]))
        limpar_tela()
        titulo(cabecalho)
        print(heroi.ficha())

        # Pre-stage hub: the player can manage gear or shop before entering.
        while True:
            print(colorir(t("main.entrar"), Cor.VERDE))
            print(t("main.abrir_inv"))
            print(t("main.visitar_loja"))
            acao = ler_opcao("> ", ["1", "2", "3"])
            if acao == "1":
                break
            if acao == "2":
                gerenciar_inventario(heroi)
            elif acao == "3":
                abrir_loja(heroi)
            limpar_tela()
            titulo(cabecalho)
            print(heroi.ficha())

        # Optional objective for this stage, tracked across its fights.
        objetivo = objetivo_aleatorio()
        registro = {"pocoes": 0, "habilidades": 0, "dano_recebido": 0}
        print(colorir(t("quest.objetivo_label", desc=t(f"quest.{objetivo['id']}.desc")), Cor.CIANO + Cor.NEGRITO))
        pausar()

        # ~40% chance of a random event before the fights.
        if random.random() < 0.4:
            evento_aleatorio(heroi)

        for inimigo in criar_inimigos_da_fase(indice, heroi.dificuldade):
            # Fleeing pushes you back but the same (damaged) enemy waits; only a
            # win moves on.
            while True:
                resultado = combate(heroi, inimigo, registro=registro)
                if resultado == "vitoria":
                    _anunciar_conquistas(checar_conquistas(heroi, boss=getattr(inimigo, "eh_boss", False)))
                    pausar()
                    break
                if resultado == "derrota":
                    return "derrota"
                print(colorir(t("main.recua"), Cor.AMARELO))
                gerenciar_inventario(heroi)

        # Stage cleared: hand out the prize and advance.
        premio = premio_da_fase(indice)
        heroi.inventario.adicionar(premio)
        print(colorir(t("main.fase_concluida", item=nome(premio.nome)), Cor.CIANO + Cor.NEGRITO))

        # Optional objective payout.
        if objetivo["verificar"](registro):
            heroi.ouro += objetivo["ouro"]
            print(colorir(t("quest.sucesso", ouro=objetivo["ouro"]), Cor.VERDE))
        else:
            print(colorir(t("quest.falha"), Cor.CINZA))

        heroi.fase_atual = indice + 1
        salvar(heroi)  # autosave after each stage
        print(colorir(t("main.salvo"), Cor.CINZA))
        pausar()

    return "vitoria"


# ---------------------------------------------------------------------------
# End-of-game screens
# ---------------------------------------------------------------------------
def tela_vitoria(heroi):
    limpar_tela()
    titulo(t("main.vitoria_titulo"))
    digitar(colorir(t("main.vitoria_texto", nome=heroi.nome), Cor.VERDE + Cor.NEGRITO))
    print(t("main.vitoria_stats", nivel=heroi.nivel, ouro=heroi.ouro))
    pausar()


def tela_derrota(heroi):
    limpar_tela()
    titulo(t("main.derrota_titulo"))
    digitar(colorir(t("main.derrota_texto", nome=heroi.nome), Cor.VERMELHO + Cor.NEGRITO))
    print(t("main.derrota_stats", nivel=heroi.nivel))
    pausar()


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------
def tela_recordes():
    """Show the leaderboard."""
    limpar_tela()
    titulo(t("rec.titulo"))
    melhores = top_pontuacoes()
    if not melhores:
        print(colorir(t("rec.vazio"), Cor.CINZA))
    else:
        print()
        for posicao, s in enumerate(melhores, start=1):
            marca = "✔" if s["venceu"] else "✘"
            linha = t("rec.linha", pontos=colorir(str(s["pontos"]), Cor.AMARELO + Cor.NEGRITO),
                      nome=s["nome"], classe=nome(s["classe"]), nivel=s["nivel"],
                      dificuldade=nome(s["dificuldade"]), marca=marca)
            print(f"  {posicao:>2}. {linha}")
    pausar()


def _anunciar_conquistas(novas):
    """Print a line for each newly unlocked achievement."""
    for cid in novas:
        print(colorir(t("conq.desbloqueada", nome=t(f"conq.{cid}.nome")), Cor.AMARELO + Cor.NEGRITO))


def tela_conquistas():
    """List every achievement, marking the unlocked ones."""
    limpar_tela()
    titulo(t("conq.titulo"))
    feitas = obtidas()
    print(t("conq.progresso", n=len(feitas & set(CONQUISTAS)), total=len(CONQUISTAS)))
    for cid in CONQUISTAS:
        marca = "🏅" if cid in feitas else "🔒"
        cor = Cor.AMARELO if cid in feitas else Cor.CINZA
        print(colorir(f"  {marca} {t(f'conq.{cid}.nome')} — {t(f'conq.{cid}.desc')}", cor))
    pausar()


def tela_bestiario():
    """Monster codex: discovered monsters show their stats, the rest show '???'."""
    limpar_tela()
    titulo(t("best.titulo"))
    descobertos = vistos()
    ids = list(MODELOS_MONSTROS.keys()) + ["Dragão Ancião"]
    print(t("best.progresso", vistos=len(descobertos & set(ids)), total=len(ids)))
    for mid in ids:
        if mid not in descobertos:
            print("  " + colorir(t("best.desconhecido"), Cor.CINZA))
            continue
        if mid == "Dragão Ancião":
            b = criar_boss()
            hp, atk, df, efeito = b.hp_max, b.ataque, b.defesa, None
        else:
            m = MODELOS_MONSTROS[mid]
            hp, atk, df, efeito = m["hp_max"], m["ataque"], m["defesa"], m.get("efeito")
        linha = t("best.linha", nome=nome(mid), hp=hp, atk=atk, df=df)
        if efeito:
            linha += t("best.efeito", efeito=nome(efeito[0]))
        print("  " + linha)
    pausar()


def menu_principal():
    """Show the main menu and return a code string for the choice."""
    limpar_tela()
    titulo("DUNGEON CRAWLER")
    print(colorir("\n" + t("main.tagline") + "\n", Cor.CINZA))

    itens = [(t("main.novo"), "novo")]
    if existe_save():
        itens.append((t("main.continuar"), "continuar"))
    itens.append((t("main.recordes"), "recordes"))
    itens.append((t("main.bestiario"), "bestiario"))
    itens.append((t("main.conquistas"), "conquistas"))
    itens.append((t("main.idioma"), "idioma"))
    itens.append((t("main.sair"), "sair"))

    for i, (rotulo, _codigo) in enumerate(itens, start=1):
        print(f"  [{i}] {rotulo}")

    escolha = ler_opcao("> ", [str(i) for i in range(1, len(itens) + 1)])
    return itens[int(escolha) - 1][1]


def main():
    escolher_idioma()  # ask the language once at startup
    while True:
        escolha = menu_principal()

        if escolha == "sair":
            print(colorir(t("main.ate_a_proxima"), Cor.CIANO))
            return

        if escolha == "idioma":
            escolher_idioma()
            continue

        if escolha == "recordes":
            tela_recordes()
            continue

        if escolha == "bestiario":
            tela_bestiario()
            continue

        if escolha == "conquistas":
            tela_conquistas()
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
        novas_conquistas = checar_conquistas(heroi, venceu=venceu)

        if venceu:
            tela_vitoria(heroi)
        else:
            tela_derrota(heroi)
        print(colorir(t("main.sua_pontuacao", pontos=pontos), Cor.AMARELO + Cor.NEGRITO))
        _anunciar_conquistas(novas_conquistas)
        pausar()


# Only run the game when executed directly, not when imported.
if __name__ == "__main__":
    main()
