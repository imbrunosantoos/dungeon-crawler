"""Localization: Portuguese / English / Spanish.

Internal IDs (class/monster/item/stage/difficulty names) stay in Portuguese and
are what the save files use; this module only translates what's shown on screen.

Use t("key", **kwargs) for messages and nome("Portuguese Id") for proper names.
"""

IDIOMAS = {"pt": "Português", "en": "English", "es": "Español"}

_idioma = "pt"


def definir_idioma(code):
    global _idioma
    if code in IDIOMAS:
        _idioma = code


def idioma_atual():
    return _idioma


def t(chave, **kwargs):
    """Translated, formatted message for the current language."""
    entrada = TEXTOS.get(chave, {})
    texto = entrada.get(_idioma) or entrada.get("pt") or chave
    return texto.format(**kwargs) if kwargs else texto


def nome(id_pt):
    """Translated proper name; falls back to the id itself if missing."""
    entrada = NOMES.get(id_pt)
    if not entrada:
        return id_pt
    return entrada.get(_idioma) or entrada.get("pt") or id_pt


def descricao(id_pt):
    """Translated item description."""
    entrada = DESCRICOES.get(id_pt)
    if not entrada:
        return id_pt
    return entrada.get(_idioma) or entrada.get("pt") or id_pt


# ---------------------------------------------------------------------------
# Messages (interface, combat, system)
# ---------------------------------------------------------------------------
TEXTOS = {
    # -- generic ui --
    "ui.pausar": {
        "pt": "\nPressione ENTER para continuar...",
        "en": "\nPress ENTER to continue...",
        "es": "\nPresiona ENTER para continuar...",
    },
    "ui.opcao_invalida": {
        "pt": "Opção inválida. Escolha uma de: {opcoes}",
        "en": "Invalid option. Choose one of: {opcoes}",
        "es": "Opción inválida. Elige una de: {opcoes}",
    },
    "ui.voltar": {"pt": "Voltar", "en": "Back", "es": "Volver"},
    "ui.cancelar": {"pt": "Cancelar", "en": "Cancel", "es": "Cancelar"},
    "ui.sim": {"pt": "Sim", "en": "Yes", "es": "Sí"},
    "ui.nao": {"pt": "Não", "en": "No", "es": "No"},

    # -- endless mode --
    "end.onda": {"pt": "Onda {onda}", "en": "Wave {onda}", "es": "Oleada {onda}"},
    "end.lutar": {"pt": "\n  [1] Lutar a onda", "en": "\n  [1] Fight the wave", "es": "\n  [1] Luchar la oleada"},
    "end.oferta": {
        "pt": "\nVocê venceu! Deseja entrar no MODO INFINITO?",
        "en": "\nYou won! Enter ENDLESS MODE?",
        "es": "\n¡Ganaste! ¿Entrar en el MODO INFINITO?",
    },
    "end.fim": {
        "pt": "\nVocê sobreviveu a {ondas} ondas no Modo Infinito!",
        "en": "\nYou survived {ondas} waves in Endless Mode!",
        "es": "\n¡Sobreviviste a {ondas} oleadas en el Modo Infinito!",
    },
    "rec.ondas": {"pt": " · {ondas} ondas", "en": " · {ondas} waves", "es": " · {ondas} oleadas"},

    # -- character sheet labels --
    "ficha.nivel": {"pt": "Nível", "en": "Level", "es": "Nivel"},
    "ficha.vida": {"pt": "Vida", "en": "Health", "es": "Vida"},
    "ficha.energia": {"pt": "Energia", "en": "Energy", "es": "Energía"},
    "ficha.ataque": {"pt": "Ataque", "en": "Attack", "es": "Ataque"},
    "ficha.defesa": {"pt": "Defesa", "en": "Defense", "es": "Defensa"},
    "ficha.ouro": {"pt": "Ouro", "en": "Gold", "es": "Oro"},
    "ficha.efeitos": {"pt": "Efeitos", "en": "Effects", "es": "Efectos"},

    # -- combat --
    "combate.aparece": {
        "pt": "\n⚔  Um {nome} aparece!\n",
        "en": "\n⚔  A {nome} appears!\n",
        "es": "\n⚔  ¡Aparece un {nome}!\n",
    },
    "combate.o_que_faz": {
        "pt": "O que você faz?", "en": "What do you do?", "es": "¿Qué haces?",
    },
    "combate.acao_atacar": {"pt": "  [1] Atacar", "en": "  [1] Attack", "es": "  [1] Atacar"},
    "combate.acao_habilidades": {
        "pt": "  [2] Habilidades especiais",
        "en": "  [2] Special abilities",
        "es": "  [2] Habilidades especiales",
    },
    "combate.acao_defender": {
        "pt": "  [3] Defender (reduz o próximo dano)",
        "en": "  [3] Defend (reduces the next hit)",
        "es": "  [3] Defender (reduce el próximo golpe)",
    },
    "combate.acao_fugir": {"pt": "  [4] Fugir", "en": "  [4] Flee", "es": "  [4] Huir"},
    "combate.acao_pocao": {
        "pt": "  [5] Usar poção ({qtd} disponível(is))",
        "en": "  [5] Use potion ({qtd} available)",
        "es": "  [5] Usar poción ({qtd} disponible(s))",
    },
    "combate.heroi_atordoado": {
        "pt": "\nVocê está ATORDOADO e perde a vez!",
        "en": "\nYou are STUNNED and lose your turn!",
        "es": "\n¡Estás ATURDIDO y pierdes el turno!",
    },
    "combate.voce_erra": {
        "pt": "\nVocê ataca, mas ERRA o golpe!",
        "en": "\nYou attack, but MISS!",
        "es": "\nAtacas, ¡pero FALLAS el golpe!",
    },
    "combate.voce_critico": {
        "pt": "\n★ CRÍTICO! Você causa {dano} de dano!",
        "en": "\n★ CRITICAL! You deal {dano} damage!",
        "es": "\n★ ¡CRÍTICO! ¡Causas {dano} de daño!",
    },
    "combate.voce_ataca": {
        "pt": "\nVocê ataca e causa {dano} de dano!",
        "en": "\nYou attack and deal {dano} damage!",
        "es": "\n¡Atacas y causas {dano} de daño!",
    },
    "combate.lamina_envenena": {
        "pt": "  Sua lâmina ENVENENA o inimigo!",
        "en": "  Your blade POISONS the enemy!",
        "es": "  ¡Tu hoja ENVENENA al enemigo!",
    },
    "combate.sem_habilidade": {
        "pt": "\nVocê não tem habilidades especiais.",
        "en": "\nYou have no special abilities.",
        "es": "\nNo tienes habilidades especiales.",
    },
    "combate.qual_habilidade": {
        "pt": "\nQual habilidade?", "en": "\nWhich ability?", "es": "\n¿Qué habilidad?",
    },
    "combate.habilidade_item": {
        "pt": "  [{i}] {nome} ({custo} energia)",
        "en": "  [{i}] {nome} ({custo} energy)",
        "es": "  [{i}] {nome} ({custo} energía)",
    },
    "combate.sem_energia_sufixo": {
        "pt": " — sem energia", "en": " — no energy", "es": " — sin energía",
    },
    "combate.energia_insuficiente": {
        "pt": "\nEnergia insuficiente!", "en": "\nNot enough energy!", "es": "\n¡Energía insuficiente!",
    },
    "combate.defensiva": {
        "pt": "\nVocê assume posição defensiva.",
        "en": "\nYou take a defensive stance.",
        "es": "\nAdoptas una postura defensiva.",
    },
    "combate.fuga_ok": {
        "pt": "\nVocê conseguiu fugir!", "en": "\nYou managed to flee!", "es": "\n¡Lograste huir!",
    },
    "combate.fuga_falhou": {
        "pt": "\nA fuga falhou!", "en": "\nThe escape failed!", "es": "\n¡La huida falló!",
    },
    "combate.qual_pocao": {
        "pt": "\nQual poção?", "en": "\nWhich potion?", "es": "\n¿Qué poción?",
    },
    "combate.derrotou": {
        "pt": "\n✔ Você derrotou {nome}!",
        "en": "\n✔ You defeated {nome}!",
        "es": "\n✔ ¡Derrotaste a {nome}!",
    },
    "combate.recompensa_xp": {"pt": "  + {xp} XP", "en": "  + {xp} XP", "es": "  + {xp} XP"},
    "combate.recompensa_ouro": {
        "pt": "  + {ouro} de ouro", "en": "  + {ouro} gold", "es": "  + {ouro} de oro",
    },
    "combate.level_up": {
        "pt": "\n★ LEVEL UP! Você alcançou o nível {nivel}!",
        "en": "\n★ LEVEL UP! You reached level {nivel}!",
        "es": "\n★ ¡SUBISTE DE NIVEL! ¡Alcanzaste el nivel {nivel}!",
    },
    "combate.level_up_detalhe": {
        "pt": "  Seus atributos aumentaram e sua vida foi restaurada.",
        "en": "  Your stats grew and your health was restored.",
        "es": "  Tus atributos subieron y tu vida fue restaurada.",
    },
    "combate.inimigo_erra": {
        "pt": "{nome} ataca, mas ERRA o golpe!",
        "en": "{nome} attacks, but MISSES!",
        "es": "{nome} ataca, ¡pero FALLA!",
    },
    "combate.inimigo_ataca": {
        "pt": "{nome} ataca e causa {dano} de dano.",
        "en": "{nome} attacks and deals {dano} damage.",
        "es": "{nome} ataca y causa {dano} de daño.",
    },
    "combate.defesa_reduziu": {
        "pt": "  (defesa reduziu o golpe!)",
        "en": "  (defense softened the blow!)",
        "es": "  (¡la defensa redujo el golpe!)",
    },
    "combate.afetado": {
        "pt": "  Você foi afetado por {efeito}!",
        "en": "  You were affected by {efeito}!",
        "es": "  ¡Fuiste afectado por {efeito}!",
    },
    "combate.inimigo_atordoado": {
        "pt": "\n{nome} está ATORDOADO e perde a vez!",
        "en": "\n{nome} is STUNNED and loses its turn!",
        "es": "\n¡{nome} está ATURDIDO y pierde el turno!",
    },
    "combate.regen": {
        "pt": "Sua armadura rúnica regenera {cura} de vida.",
        "en": "Your runic armor regenerates {cura} health.",
        "es": "Tu armadura rúnica regenera {cura} de vida.",
    },
    "combate.heroi_derrotado": {
        "pt": "\n✘ {nome} foi derrotado...",
        "en": "\n✘ {nome} was defeated...",
        "es": "\n✘ {nome} fue derrotado...",
    },
    "combate.dano_veneno": {
        "pt": "{nome} sofre {dano} de dano de veneno! {barra}",
        "en": "{nome} takes {dano} poison damage! {barra}",
        "es": "¡{nome} sufre {dano} de daño de veneno! {barra}",
    },
    "combate.heroi_veneno_morte": {
        "pt": "\n✘ {nome} sucumbe ao veneno...",
        "en": "\n✘ {nome} succumbs to the poison...",
        "es": "\n✘ {nome} sucumbe al veneno...",
    },
    "combate.inimigo_veneno_morte": {
        "pt": "\n✔ {nome} sucumbe ao veneno!",
        "en": "\n✔ {nome} succumbs to the poison!",
        "es": "\n✔ ¡{nome} sucumbe al veneno!",
    },

    # -- abilities (result messages); {hero}, {hab} colored, {dano}/{cura} numbers --
    "hab.golpe_poderoso": {
        "pt": "{hero} usa {hab} e causa {dano} de dano!",
        "en": "{hero} uses {hab} and deals {dano} damage!",
        "es": "¡{hero} usa {hab} y causa {dano} de daño!",
    },
    "hab.investida": {
        "pt": "{hero} avança numa {hab} causando {dano} de dano",
        "en": "{hero} charges with {hab} dealing {dano} damage",
        "es": "{hero} embiste con {hab} causando {dano} de daño",
    },
    "hab.bola_de_fogo": {
        "pt": "{hero} lança {hab} e causa {dano} de dano mágico (ignora defesa)!",
        "en": "{hero} casts {hab} for {dano} magic damage (ignores defense)!",
        "es": "¡{hero} lanza {hab} y causa {dano} de daño mágico (ignora defensa)!",
    },
    "hab.raio": {
        "pt": "{hero} conjura {hab} causando {dano} de dano",
        "en": "{hero} conjures {hab} dealing {dano} damage",
        "es": "{hero} conjura {hab} causando {dano} de daño",
    },
    "hab.tiro_certeiro_crit": {
        "pt": "{hero} acerta um {crit} com {hab} e causa {dano} de dano!",
        "en": "{hero} lands a {crit} with {hab} dealing {dano} damage!",
        "es": "¡{hero} acierta un {crit} con {hab} y causa {dano} de daño!",
    },
    "hab.tiro_certeiro": {
        "pt": "{hero} usa {hab} e causa {dano} de dano!",
        "en": "{hero} uses {hab} and deals {dano} damage!",
        "es": "¡{hero} usa {hab} y causa {dano} de daño!",
    },
    "hab.chuva": {
        "pt": "{hero} dispara uma {hab} e causa {dano} de dano!",
        "en": "{hero} looses a {hab} dealing {dano} damage!",
        "es": "¡{hero} dispara una {hab} y causa {dano} de daño!",
    },
    "hab.luz_curativa": {
        "pt": "{hero} invoca {hab} e recupera {cura} de vida!",
        "en": "{hero} invokes {hab} and restores {cura} health!",
        "es": "¡{hero} invoca {hab} y recupera {cura} de vida!",
    },
    "hab.martelo": {
        "pt": "{hero} desce o {hab} causando {dano} de dano",
        "en": "{hero} brings down the {hab} dealing {dano} damage",
        "es": "{hero} descarga el {hab} causando {dano} de daño",
    },
    "hab.golpe_sombrio": {
        "pt": "{hero} desfere {hab} causando {dano} de dano e ENVENENANDO o inimigo!",
        "en": "{hero} delivers {hab} for {dano} damage and POISONS the enemy!",
        "es": "¡{hero} asesta {hab} causando {dano} de daño y ENVENENA al enemigo!",
    },
    "hab.apunhalar": {
        "pt": "{hero} {hab} pelas costas e causa {dano} de dano!",
        "en": "{hero} {hab} from behind for {dano} damage!",
        "es": "¡{hero} {hab} por la espalda y causa {dano} de daño!",
    },
    "hab.sufixo_atordoa": {
        "pt": " e ATORDOA o inimigo!",
        "en": " and STUNS the enemy!",
        "es": " ¡y ATURDE al enemigo!",
    },
    "hab.sufixo_congela": {
        "pt": " e CONGELA o inimigo!",
        "en": " and FREEZES the enemy!",
        "es": " ¡y CONGELA al enemigo!",
    },
    "hab.fim": {"pt": "!", "en": "!", "es": "!"},
    "hab.critico_palavra": {"pt": "CRÍTICO", "en": "CRITICAL", "es": "CRÍTICO"},
    "hab.apunhala_verbo": {"pt": "Apunhala", "en": "Backstabs", "es": "Apuñala"},

    # -- items --
    "item.pocao_usada": {
        "pt": "Você usou {nome} e recuperou {cura} de vida.",
        "en": "You used {nome} and recovered {cura} health.",
        "es": "Usaste {nome} y recuperaste {cura} de vida.",
    },

    # -- inventory --
    "inv.mochila": {"pt": "=== Mochila ===", "en": "=== Backpack ===", "es": "=== Mochila ==="},
    "inv.arma_equipada": {
        "pt": "Arma equipada:     {x}", "en": "Weapon equipped:   {x}", "es": "Arma equipada:     {x}",
    },
    "inv.armadura_equipada": {
        "pt": "Armadura equipada: {x}", "en": "Armor equipped:    {x}", "es": "Armadura equipada: {x}",
    },
    "inv.nenhuma": {"pt": "nenhuma", "en": "none", "es": "ninguna"},
    "inv.vazia": {"pt": "(vazia)", "en": "(empty)", "es": "(vacía)"},
    "inv.equipou_arma": {
        "pt": "Você equipou {nome} (+{bonus} de ataque).",
        "en": "You equipped {nome} (+{bonus} attack).",
        "es": "Equipaste {nome} (+{bonus} de ataque).",
    },
    "inv.equipou_armadura": {
        "pt": "Você equipou {nome} (+{bonus} de defesa).",
        "en": "You equipped {nome} (+{bonus} defense).",
        "es": "Equipaste {nome} (+{bonus} de defensa).",
    },
    "inv.nao_equipavel": {
        "pt": "Esse item não pode ser equipado.",
        "en": "That item can't be equipped.",
        "es": "Ese objeto no se puede equipar.",
    },
    "inv.menu_equipar": {"pt": "  [1] Equipar um item", "en": "  [1] Equip an item", "es": "  [1] Equipar un objeto"},
    "inv.menu_pocao": {"pt": "  [2] Usar uma poção", "en": "  [2] Use a potion", "es": "  [2] Usar una poción"},
    "inv.menu_voltar": {"pt": "  [3] Voltar", "en": "  [3] Back", "es": "  [3] Volver"},
    "inv.sem_equipar": {
        "pt": "\nVocê não tem itens para equipar.",
        "en": "\nYou have no items to equip.",
        "es": "\nNo tienes objetos para equipar.",
    },
    "inv.qual_equipar": {"pt": "\nQual item equipar?", "en": "\nEquip which item?", "es": "\n¿Qué objeto equipar?"},
    "inv.sem_pocoes": {"pt": "\nVocê não tem poções.", "en": "\nYou have no potions.", "es": "\nNo tienes pociones."},
    "inv.qual_pocao_usar": {"pt": "\nQual poção usar?", "en": "\nUse which potion?", "es": "\n¿Qué poción usar?"},

    # -- shop --
    "loja.titulo": {"pt": "Loja do Aventureiro", "en": "Adventurer's Shop", "es": "Tienda del Aventurero"},
    "loja.seu_ouro": {"pt": "\nSeu ouro: {ouro}\n", "en": "\nYour gold: {ouro}\n", "es": "\nTu oro: {ouro}\n"},
    "loja.comprar": {"pt": "Comprar:", "en": "Buy:", "es": "Comprar:"},
    "loja.vender": {"pt": "  [{n}] Vender um item", "en": "  [{n}] Sell an item", "es": "  [{n}] Vender un objeto"},
    "loja.sair": {"pt": "  [{n}] Sair da loja", "en": "  [{n}] Leave the shop", "es": "  [{n}] Salir de la tienda"},
    "loja.ouro_insuficiente": {"pt": "\nOuro insuficiente!", "en": "\nNot enough gold!", "es": "\n¡Oro insuficiente!"},
    "loja.comprou": {
        "pt": "\nVocê comprou {nome} por {preco} de ouro.",
        "en": "\nYou bought {nome} for {preco} gold.",
        "es": "\nCompraste {nome} por {preco} de oro.",
    },
    "loja.sem_vender": {
        "pt": "\nVocê não tem itens para vender.",
        "en": "\nYou have no items to sell.",
        "es": "\nNo tienes objetos para vender.",
    },
    "loja.o_que_vender": {
        "pt": "\nO que deseja vender? (recebe metade do preço)",
        "en": "\nWhat do you want to sell? (half price)",
        "es": "\n¿Qué quieres vender? (mitad del precio)",
    },
    "loja.item_compra": {
        "pt": "  [{i}] {nome} — {preco} de ouro",
        "en": "  [{i}] {nome} — {preco} gold",
        "es": "  [{i}] {nome} — {preco} de oro",
    },
    "loja.item_venda": {
        "pt": "  [{i}] {nome} — {valor} de ouro",
        "en": "  [{i}] {nome} — {valor} gold",
        "es": "  [{i}] {nome} — {valor} de oro",
    },
    "loja.vendeu": {
        "pt": "\nVocê vendeu {nome} por {valor} de ouro.",
        "en": "\nYou sold {nome} for {valor} gold.",
        "es": "\nVendiste {nome} por {valor} de oro.",
    },

    # -- events --
    "evt.bau": {
        "pt": "\n🧰 Você encontra um baú empoeirado!",
        "en": "\n🧰 You find a dusty chest!",
        "es": "\n🧰 ¡Encuentras un cofre polvoriento!",
    },
    "evt.bau_ouro": {
        "pt": "Dentro havia {ouro} de ouro!",
        "en": "Inside there were {ouro} gold!",
        "es": "¡Dentro había {ouro} de oro!",
    },
    "evt.bau_item": {
        "pt": "Dentro havia: {item}!",
        "en": "Inside there was: {item}!",
        "es": "¡Dentro había: {item}!",
    },
    "evt.armadilha": {
        "pt": "\n💥 Uma armadilha dispara!",
        "en": "\n💥 A trap springs!",
        "es": "\n💥 ¡Se activa una trampa!",
    },
    "evt.armadilha_dano": {
        "pt": "Você perde {dano} de vida. {barra}",
        "en": "You lose {dano} health. {barra}",
        "es": "Pierdes {dano} de vida. {barra}",
    },
    "evt.fonte": {
        "pt": "\n⛲ Você encontra uma fonte mágica reluzente.",
        "en": "\n⛲ You find a shimmering magic fountain.",
        "es": "\n⛲ Encuentras una fuente mágica reluciente.",
    },
    "evt.fonte_cura": {
        "pt": "Você recupera {vida} de vida e toda a energia.",
        "en": "You recover {vida} health and all your energy.",
        "es": "Recuperas {vida} de vida y toda la energía.",
    },
    "evt.mercador": {
        "pt": "\n🧙 Um mercador misterioso surge das sombras...",
        "en": "\n🧙 A mysterious merchant emerges from the shadows...",
        "es": "\n🧙 Un mercader misterioso surge de las sombras...",
    },
    "evt.mercador_oferta": {
        "pt": '"Tenho um {item} por apenas {preco} de ouro."',
        "en": '"I have a {item} for just {preco} gold."',
        "es": '"Tengo un {item} por solo {preco} de oro."',
    },
    "evt.mercador_ouro": {
        "pt": "(Você tem {ouro} de ouro)",
        "en": "(You have {ouro} gold)",
        "es": "(Tienes {ouro} de oro)",
    },
    "evt.comprar": {"pt": "  [1] Comprar", "en": "  [1] Buy", "es": "  [1] Comprar"},
    "evt.recusar": {"pt": "  [2] Recusar", "en": "  [2] Decline", "es": "  [2] Rechazar"},
    "evt.mercador_comprou": {
        "pt": "Você comprou {item}!", "en": "You bought {item}!", "es": "¡Compraste {item}!",
    },
    "evt.mercador_sem_ouro": {
        "pt": "Ouro insuficiente. O mercador desaparece.",
        "en": "Not enough gold. The merchant vanishes.",
        "es": "Oro insuficiente. El mercader desaparece.",
    },
    "evt.mercador_recusou": {
        "pt": "Você segue seu caminho.", "en": "You go on your way.", "es": "Sigues tu camino.",
    },

    # -- leaderboard --
    "rec.titulo": {"pt": "PLACAR DE RECORDES", "en": "LEADERBOARD", "es": "TABLA DE RÉCORDS"},
    "rec.vazio": {
        "pt": "\nAinda não há recordes. Seja o primeiro!",
        "en": "\nNo records yet. Be the first!",
        "es": "\nAún no hay récords. ¡Sé el primero!",
    },
    "rec.linha": {
        "pt": "{pontos} pts — {nome} ({classe}, nível {nivel}, {dificuldade}) {marca}",
        "en": "{pontos} pts — {nome} ({classe}, level {nivel}, {dificuldade}) {marca}",
        "es": "{pontos} pts — {nome} ({classe}, nivel {nivel}, {dificuldade}) {marca}",
    },

    # -- stage objectives --
    "quest.objetivo_label": {
        "pt": "🎯 Objetivo desta fase: {desc}",
        "en": "🎯 Stage objective: {desc}",
        "es": "🎯 Objetivo de la etapa: {desc}",
    },
    "quest.sucesso": {
        "pt": "\n🎯 Objetivo cumprido! +{ouro} de ouro",
        "en": "\n🎯 Objective complete! +{ouro} gold",
        "es": "\n🎯 ¡Objetivo cumplido! +{ouro} de oro",
    },
    "quest.falha": {
        "pt": "\n🎯 Objetivo não cumprido.",
        "en": "\n🎯 Objective not met.",
        "es": "\n🎯 Objetivo no cumplido.",
    },
    "quest.sem_pocao.desc": {
        "pt": "Termine a fase sem usar poções",
        "en": "Clear the stage without using potions",
        "es": "Completa la etapa sin usar pociones",
    },
    "quest.usar_habilidade.desc": {
        "pt": "Use ao menos uma habilidade especial",
        "en": "Use at least one special ability",
        "es": "Usa al menos una habilidad especial",
    },
    "quest.pouco_dano.desc": {
        "pt": "Receba menos de 40 de dano na fase",
        "en": "Take less than 40 damage in the stage",
        "es": "Recibe menos de 40 de daño en la etapa",
    },

    # -- bestiary --
    "best.titulo": {"pt": "BESTIÁRIO", "en": "BESTIARY", "es": "BESTIARIO"},
    "best.progresso": {
        "pt": "\nDescobertos: {vistos}/{total}\n",
        "en": "\nDiscovered: {vistos}/{total}\n",
        "es": "\nDescubiertos: {vistos}/{total}\n",
    },
    "best.linha": {
        "pt": "{nome} — Vida {hp}, Ataque {atk}, Defesa {df}",
        "en": "{nome} — HP {hp}, Attack {atk}, Defense {df}",
        "es": "{nome} — Vida {hp}, Ataque {atk}, Defensa {df}",
    },
    "best.efeito": {
        "pt": " (inflige {efeito})", "en": " (inflicts {efeito})", "es": " (inflige {efeito})",
    },
    "best.desconhecido": {
        "pt": "??? (não descoberto)", "en": "??? (undiscovered)", "es": "??? (no descubierto)",
    },

    # -- achievements --
    "conq.titulo": {"pt": "CONQUISTAS", "en": "ACHIEVEMENTS", "es": "LOGROS"},
    "conq.progresso": {
        "pt": "\nObtidas: {n}/{total}\n",
        "en": "\nUnlocked: {n}/{total}\n",
        "es": "\nObtenidos: {n}/{total}\n",
    },
    "conq.desbloqueada": {
        "pt": "\n🏅 Conquista desbloqueada: {nome}!",
        "en": "\n🏅 Achievement unlocked: {nome}!",
        "es": "\n🏅 ¡Logro desbloqueado: {nome}!",
    },
    "conq.primeiro_chefe.nome": {"pt": "Caçador de Chefes", "en": "Boss Slayer", "es": "Cazador de Jefes"},
    "conq.primeiro_chefe.desc": {"pt": "Derrote um chefe", "en": "Defeat a boss", "es": "Derrota a un jefe"},
    "conq.nivel_10.nome": {"pt": "Veterano", "en": "Veteran", "es": "Veterano"},
    "conq.nivel_10.desc": {"pt": "Alcance o nível 10", "en": "Reach level 10", "es": "Alcanza el nivel 10"},
    "conq.rico.nome": {"pt": "Tesoureiro", "en": "Treasurer", "es": "Tesorero"},
    "conq.rico.desc": {"pt": "Acumule 1000 de ouro", "en": "Hold 1000 gold", "es": "Acumula 1000 de oro"},
    "conq.dificil.nome": {"pt": "Implacável", "en": "Relentless", "es": "Implacable"},
    "conq.dificil.desc": {"pt": "Vença o jogo no Difícil", "en": "Beat the game on Hard", "es": "Gana el juego en Difícil"},
    "conq.ondas_10.nome": {"pt": "Sobrevivente", "en": "Survivor", "es": "Superviviente"},
    "conq.ondas_10.desc": {"pt": "Sobreviva 10 ondas no modo infinito", "en": "Survive 10 endless waves", "es": "Sobrevive 10 oleadas infinitas"},
    "conq.bestiario_completo.nome": {"pt": "Estudioso", "en": "Scholar", "es": "Erudito"},
    "conq.bestiario_completo.desc": {"pt": "Descubra todos os monstros", "en": "Discover every monster", "es": "Descubre todos los monstruos"},

    # -- main / menus --
    "main.tagline": {"pt": "Um RPG de terminal", "en": "A terminal RPG", "es": "Un RPG de terminal"},
    "main.novo": {"pt": "Novo jogo", "en": "New game", "es": "Nuevo juego"},
    "main.continuar": {"pt": "Continuar", "en": "Continue", "es": "Continuar"},
    "main.recordes": {"pt": "Ver recordes", "en": "Leaderboard", "es": "Ver récords"},
    "main.bestiario": {"pt": "Bestiário", "en": "Bestiary", "es": "Bestiario"},
    "main.conquistas": {"pt": "Conquistas", "en": "Achievements", "es": "Logros"},
    "main.idioma": {"pt": "Idioma", "en": "Language", "es": "Idioma"},
    "main.sair": {"pt": "Sair", "en": "Quit", "es": "Salir"},
    "main.ate_a_proxima": {
        "pt": "\nAté a próxima, aventureiro!",
        "en": "\nUntil next time, adventurer!",
        "es": "\n¡Hasta la próxima, aventurero!",
    },
    "main.escolha_idioma": {
        "pt": "Escolha o idioma", "en": "Choose your language", "es": "Elige el idioma",
    },
    "main.criacao_titulo": {
        "pt": "Criação de Personagem", "en": "Character Creation", "es": "Creación de Personaje",
    },
    "main.pergunta_nome": {
        "pt": "\nQual o nome do seu herói? ",
        "en": "\nWhat is your hero's name? ",
        "es": "\n¿Cómo se llama tu héroe? ",
    },
    "main.escolha_classe": {"pt": "\nEscolha sua classe:", "en": "\nChoose your class:", "es": "\nElige tu clase:"},
    "main.classe_item": {
        "pt": "  [{i}] {classe} — Vida {hp}, Ataque {atk}, Defesa {df} | Habilidades: {skills}",
        "en": "  [{i}] {classe} — HP {hp}, Attack {atk}, Defense {df} | Abilities: {skills}",
        "es": "  [{i}] {classe} — Vida {hp}, Ataque {atk}, Defensa {df} | Habilidades: {skills}",
    },
    "main.escolha_dificuldade": {
        "pt": "\nEscolha a dificuldade:", "en": "\nChoose the difficulty:", "es": "\nElige la dificultad:",
    },
    "main.pronto": {
        "pt": "\n{nome}, o {classe}, está pronto para a aventura!",
        "en": "\n{nome} the {classe} is ready for the adventure!",
        "es": "\n¡{nome}, el {classe}, está listo para la aventura!",
    },
    "main.fase_titulo": {
        "pt": "Fase {atual}/{total}: {nome}",
        "en": "Stage {atual}/{total}: {nome}",
        "es": "Etapa {atual}/{total}: {nome}",
    },
    "main.entrar": {"pt": "\n  [1] Entrar na fase", "en": "\n  [1] Enter the stage", "es": "\n  [1] Entrar en la etapa"},
    "main.abrir_inv": {"pt": "  [2] Abrir inventário", "en": "  [2] Open inventory", "es": "  [2] Abrir inventario"},
    "main.visitar_loja": {"pt": "  [3] Visitar a loja", "en": "  [3] Visit the shop", "es": "  [3] Visitar la tienda"},
    "main.fase_concluida": {
        "pt": "\n🎁 Fase concluída! Você recebeu: {item}",
        "en": "\n🎁 Stage cleared! You received: {item}",
        "es": "\n🎁 ¡Etapa completada! Recibiste: {item}",
    },
    "main.salvo": {"pt": "Progresso salvo.", "en": "Progress saved.", "es": "Progreso guardado."},
    "main.recua": {
        "pt": "\nVocê recua para recuperar o fôlego, mas o inimigo te espera...",
        "en": "\nYou pull back to catch your breath, but the enemy waits...",
        "es": "\nRetrocedes para recuperar el aliento, pero el enemigo te espera...",
    },
    "main.vitoria_titulo": {"pt": "VITÓRIA!", "en": "VICTORY!", "es": "¡VICTORIA!"},
    "main.vitoria_texto": {
        "pt": "\n{nome} derrotou o Dragão Ancião e salvou o reino!",
        "en": "\n{nome} defeated the Ancient Dragon and saved the realm!",
        "es": "\n¡{nome} derrotó al Dragón Anciano y salvó el reino!",
    },
    "main.vitoria_stats": {
        "pt": "\nNível final: {nivel} | Ouro acumulado: {ouro}",
        "en": "\nFinal level: {nivel} | Gold collected: {ouro}",
        "es": "\nNivel final: {nivel} | Oro acumulado: {ouro}",
    },
    "main.derrota_titulo": {"pt": "FIM DE JOGO", "en": "GAME OVER", "es": "FIN DEL JUEGO"},
    "main.derrota_texto": {
        "pt": "\n{nome} tombou na masmorra. A aventura termina aqui...",
        "en": "\n{nome} fell in the dungeon. The adventure ends here...",
        "es": "\n{nome} cayó en la mazmorra. La aventura termina aquí...",
    },
    "main.derrota_stats": {
        "pt": "\nVocê chegou ao nível {nivel}.",
        "en": "\nYou reached level {nivel}.",
        "es": "\nLlegaste al nivel {nivel}.",
    },
    "main.sua_pontuacao": {
        "pt": "\nSua pontuação: {pontos} pontos",
        "en": "\nYour score: {pontos} points",
        "es": "\nTu puntuación: {pontos} puntos",
    },
}


# ---------------------------------------------------------------------------
# Proper names (internal id in Portuguese -> localized name)
# ---------------------------------------------------------------------------
NOMES = {
    # classes
    "Guerreiro": {"pt": "Guerreiro", "en": "Warrior", "es": "Guerrero"},
    "Mago": {"pt": "Mago", "en": "Mage", "es": "Mago"},
    "Arqueiro": {"pt": "Arqueiro", "en": "Archer", "es": "Arquero"},
    "Paladino": {"pt": "Paladino", "en": "Paladin", "es": "Paladín"},
    "Ladino": {"pt": "Ladino", "en": "Rogue", "es": "Pícaro"},
    # difficulties
    "Fácil": {"pt": "Fácil", "en": "Easy", "es": "Fácil"},
    "Normal": {"pt": "Normal", "en": "Normal", "es": "Normal"},
    "Difícil": {"pt": "Difícil", "en": "Hard", "es": "Difícil"},
    # effects
    "veneno": {"pt": "veneno", "en": "poison", "es": "veneno"},
    "atordoado": {"pt": "atordoado", "en": "stunned", "es": "aturdido"},
    # monsters
    "Rato Gigante": {"pt": "Rato Gigante", "en": "Giant Rat", "es": "Rata Gigante"},
    "Goblin": {"pt": "Goblin", "en": "Goblin", "es": "Goblin"},
    "Morcego": {"pt": "Morcego", "en": "Bat", "es": "Murciélago"},
    "Esqueleto": {"pt": "Esqueleto", "en": "Skeleton", "es": "Esqueleto"},
    "Aranha Venenosa": {"pt": "Aranha Venenosa", "en": "Venomous Spider", "es": "Araña Venenosa"},
    "Lobo Sombrio": {"pt": "Lobo Sombrio", "en": "Dire Wolf", "es": "Lobo Sombrío"},
    "Feiticeiro": {"pt": "Feiticeiro", "en": "Sorcerer", "es": "Hechicero"},
    "Orc": {"pt": "Orc", "en": "Orc", "es": "Orco"},
    "Golem de Pedra": {"pt": "Golem de Pedra", "en": "Stone Golem", "es": "Gólem de Piedra"},
    "Troll": {"pt": "Troll", "en": "Troll", "es": "Trol"},
    "Cavaleiro Caído": {"pt": "Cavaleiro Caído", "en": "Fallen Knight", "es": "Caballero Caído"},
    "Dragão Ancião": {"pt": "Dragão Ancião", "en": "Ancient Dragon", "es": "Dragón Anciano"},
    # abilities
    "Golpe Poderoso": {"pt": "Golpe Poderoso", "en": "Mighty Blow", "es": "Golpe Poderoso"},
    "Investida": {"pt": "Investida", "en": "Charge", "es": "Embestida"},
    "Bola de Fogo": {"pt": "Bola de Fogo", "en": "Fireball", "es": "Bola de Fuego"},
    "Raio Congelante": {"pt": "Raio Congelante", "en": "Frost Bolt", "es": "Rayo Congelante"},
    "Tiro Certeiro": {"pt": "Tiro Certeiro", "en": "Precise Shot", "es": "Tiro Certero"},
    "Chuva de Flechas": {"pt": "Chuva de Flechas", "en": "Arrow Rain", "es": "Lluvia de Flechas"},
    "Luz Curativa": {"pt": "Luz Curativa", "en": "Healing Light", "es": "Luz Curativa"},
    "Martelo Sagrado": {"pt": "Martelo Sagrado", "en": "Holy Hammer", "es": "Martillo Sagrado"},
    "Golpe Sombrio": {"pt": "Golpe Sombrio", "en": "Shadow Strike", "es": "Golpe Sombrío"},
    "Apunhalar": {"pt": "Apunhalar", "en": "Backstab", "es": "Apuñalar"},
    # items
    "Poção Pequena": {"pt": "Poção Pequena", "en": "Small Potion", "es": "Poción Pequeña"},
    "Poção Grande": {"pt": "Poção Grande", "en": "Large Potion", "es": "Poción Grande"},
    "Poção Suprema": {"pt": "Poção Suprema", "en": "Supreme Potion", "es": "Poción Suprema"},
    "Espada de Ferro": {"pt": "Espada de Ferro", "en": "Iron Sword", "es": "Espada de Hierro"},
    "Machado de Guerra": {"pt": "Machado de Guerra", "en": "War Axe", "es": "Hacha de Guerra"},
    "Espada Flamejante": {"pt": "Espada Flamejante", "en": "Flaming Sword", "es": "Espada Flamígera"},
    "Armadura de Couro": {"pt": "Armadura de Couro", "en": "Leather Armor", "es": "Armadura de Cuero"},
    "Armadura de Placas": {"pt": "Armadura de Placas", "en": "Plate Armor", "es": "Armadura de Placas"},
    "Escudo de Aço": {"pt": "Escudo de Aço", "en": "Steel Shield", "es": "Escudo de Acero"},
    "Adaga Afiada": {"pt": "Adaga Afiada", "en": "Sharp Dagger", "es": "Daga Afilada"},
    "Arco Élfico": {"pt": "Arco Élfico", "en": "Elven Bow", "es": "Arco Élfico"},
    "Lâmina Venenosa": {"pt": "Lâmina Venenosa", "en": "Venom Blade", "es": "Hoja Venenosa"},
    "Armadura Rúnica": {"pt": "Armadura Rúnica", "en": "Runic Armor", "es": "Armadura Rúnica"},
    # enchantment labels
    "Afiada": {"pt": "Afiada", "en": "Sharp", "es": "Afilada"},
    "Élfico": {"pt": "Élfico", "en": "Elven", "es": "Élfico"},
    "Peçonhenta": {"pt": "Peçonhenta", "en": "Venomous", "es": "Venenosa"},
    "Rúnica": {"pt": "Rúnica", "en": "Runic", "es": "Rúnica"},
    # stages
    "Caverna dos Ratos": {"pt": "Caverna dos Ratos", "en": "Cave of Rats", "es": "Caverna de las Ratas"},
    "Floresta Sombria": {"pt": "Floresta Sombria", "en": "Dark Forest", "es": "Bosque Sombrío"},
    "Ruínas Antigas": {"pt": "Ruínas Antigas", "en": "Ancient Ruins", "es": "Ruinas Antiguas"},
    "Montanha do Trovão": {"pt": "Montanha do Trovão", "en": "Thunder Mountain", "es": "Montaña del Trueno"},
    "Ninho das Aranhas": {"pt": "Ninho das Aranhas", "en": "Spider Nest", "es": "Nido de Arañas"},
    "Torre do Feiticeiro": {"pt": "Torre do Feiticeiro", "en": "Sorcerer's Tower", "es": "Torre del Hechicero"},
    "Fortaleza Esquecida": {"pt": "Fortaleza Esquecida", "en": "Forgotten Fortress", "es": "Fortaleza Olvidada"},
    "Covil do Dragão": {"pt": "Covil do Dragão", "en": "Dragon's Den", "es": "Guarida del Dragón"},
}


# ---------------------------------------------------------------------------
# Item descriptions (internal id -> localized description)
# ---------------------------------------------------------------------------
DESCRICOES = {
    "Poção Pequena": {"pt": "Recupera 30 de vida", "en": "Restores 30 health", "es": "Recupera 30 de vida"},
    "Poção Grande": {"pt": "Recupera 80 de vida", "en": "Restores 80 health", "es": "Recupera 80 de vida"},
    "Poção Suprema": {"pt": "Recupera 150 de vida", "en": "Restores 150 health", "es": "Recupera 150 de vida"},
    "Espada de Ferro": {"pt": "+8 de ataque", "en": "+8 attack", "es": "+8 de ataque"},
    "Machado de Guerra": {"pt": "+15 de ataque", "en": "+15 attack", "es": "+15 de ataque"},
    "Espada Flamejante": {"pt": "+20 de ataque", "en": "+20 attack", "es": "+20 de ataque"},
    "Armadura de Couro": {"pt": "+5 de defesa", "en": "+5 defense", "es": "+5 de defensa"},
    "Armadura de Placas": {"pt": "+12 de defesa", "en": "+12 defense", "es": "+12 de defensa"},
    "Escudo de Aço": {"pt": "+18 de defesa", "en": "+18 defense", "es": "+18 de defensa"},
    "Adaga Afiada": {
        "pt": "+10 de ataque, +15% de crítico",
        "en": "+10 attack, +15% crit",
        "es": "+10 de ataque, +15% de crítico",
    },
    "Arco Élfico": {
        "pt": "+12 de ataque, +5% de precisão",
        "en": "+12 attack, +5% accuracy",
        "es": "+12 de ataque, +5% de precisión",
    },
    "Lâmina Venenosa": {
        "pt": "+10 de ataque, envenena no acerto",
        "en": "+10 attack, poisons on hit",
        "es": "+10 de ataque, envenena al golpear",
    },
    "Armadura Rúnica": {
        "pt": "+10 de defesa, regenera 5 por turno",
        "en": "+10 defense, regenerates 5 per turn",
        "es": "+10 de defensa, regenera 5 por turno",
    },
}
