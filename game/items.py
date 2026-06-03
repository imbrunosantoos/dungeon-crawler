"""Game items: potions (consumable), weapons and armor (equippable)."""

from game.character import VENENO
from game.i18n import descricao, nome, t
from game.ui import Cor, colorir


class Encantamento:
    """A bonus carried by a weapon/armor, applied while it's equipped."""

    def __init__(self, nome, bonus_critico=0.0, bonus_precisao=0.0, regen=0, veneno_turnos=0):
        self.nome = nome
        self.bonus_critico = bonus_critico
        self.bonus_precisao = bonus_precisao
        self.regen = regen
        self.veneno_turnos = veneno_turnos

    def aplicar(self, personagem):
        personagem.chance_critico += self.bonus_critico
        personagem.precisao += self.bonus_precisao
        personagem.regen_por_turno += self.regen
        if self.veneno_turnos:
            personagem.veneno_no_ataque = self.veneno_turnos

    def remover(self, personagem):
        personagem.chance_critico -= self.bonus_critico
        personagem.precisao -= self.bonus_precisao
        personagem.regen_por_turno -= self.regen
        if self.veneno_turnos:
            personagem.veneno_no_ataque = 0


class Item:
    tipo = "item"

    def __init__(self, nome, descricao, encantamento=None):
        self.nome = nome
        self.descricao = descricao
        self.encantamento = encantamento

    def __str__(self):
        texto = f"{nome(self.nome)} — {descricao(self.nome)}"
        if self.encantamento:
            texto += colorir(f" [{nome(self.encantamento.nome)}]", Cor.MAGENTA)
        return texto


class Potion(Item):
    tipo = "pocao"

    def __init__(self, nome, descricao, cura):
        super().__init__(nome, descricao)
        self.cura = cura

    def usar(self, alvo):
        """Heal the target and return the message."""
        curado = alvo.curar(self.cura)
        return colorir(t("item.pocao_usada", nome=nome(self.nome), cura=curado), Cor.VERDE)


class Weapon(Item):
    tipo = "arma"

    def __init__(self, nome, descricao, bonus_ataque, encantamento=None):
        super().__init__(nome, descricao, encantamento)
        self.bonus_ataque = bonus_ataque


class Armor(Item):
    tipo = "armadura"

    def __init__(self, nome, descricao, bonus_defesa, encantamento=None):
        super().__init__(nome, descricao, encantamento)
        self.bonus_defesa = bonus_defesa


# Factories return a fresh item each time, so two potions aren't the same object.
def pocao_pequena():
    return Potion("Poção Pequena", "Recupera 30 de vida", cura=30)


def pocao_grande():
    return Potion("Poção Grande", "Recupera 80 de vida", cura=80)


def espada_de_ferro():
    return Weapon("Espada de Ferro", "+8 de ataque", bonus_ataque=8)


def machado_de_guerra():
    return Weapon("Machado de Guerra", "+15 de ataque", bonus_ataque=15)


def armadura_de_couro():
    return Armor("Armadura de Couro", "+5 de defesa", bonus_defesa=5)


def armadura_de_placas():
    return Armor("Armadura de Placas", "+12 de defesa", bonus_defesa=12)


# Stronger gear for the later stages.
def pocao_suprema():
    return Potion("Poção Suprema", "Recupera 150 de vida", cura=150)


def espada_flamejante():
    return Weapon("Espada Flamejante", "+20 de ataque", bonus_ataque=20)


def escudo_de_aco():
    return Armor("Escudo de Aço", "+18 de defesa", bonus_defesa=18)


# Enchanted gear: a stat bonus plus an extra effect while equipped.
def adaga_afiada():
    return Weapon("Adaga Afiada", "+10 de ataque, +15% de crítico", bonus_ataque=10,
                  encantamento=Encantamento("Afiada", bonus_critico=0.15))


def arco_elfico():
    return Weapon("Arco Élfico", "+12 de ataque, +5% de precisão", bonus_ataque=12,
                  encantamento=Encantamento("Élfico", bonus_precisao=0.05))


def lamina_venenosa():
    return Weapon("Lâmina Venenosa", "+10 de ataque, envenena no acerto", bonus_ataque=10,
                  encantamento=Encantamento("Peçonhenta", veneno_turnos=2))


def armadura_runica():
    return Armor("Armadura Rúnica", "+10 de defesa, regenera 5 por turno", bonus_defesa=10,
                 encantamento=Encantamento("Rúnica", regen=5))


# Name -> factory. Saves store only the name and rebuild the item from here.
CATALOGO_ITENS = {
    "Poção Pequena": pocao_pequena,
    "Poção Grande": pocao_grande,
    "Poção Suprema": pocao_suprema,
    "Espada de Ferro": espada_de_ferro,
    "Machado de Guerra": machado_de_guerra,
    "Espada Flamejante": espada_flamejante,
    "Armadura de Couro": armadura_de_couro,
    "Armadura de Placas": armadura_de_placas,
    "Escudo de Aço": escudo_de_aco,
    "Adaga Afiada": adaga_afiada,
    "Arco Élfico": arco_elfico,
    "Lâmina Venenosa": lamina_venenosa,
    "Armadura Rúnica": armadura_runica,
}


def criar_item(nome):
    """Rebuild an item from its name (used when loading a save)."""
    return CATALOGO_ITENS[nome]()
