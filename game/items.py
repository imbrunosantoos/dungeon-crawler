"""Game items: potions (consumable), weapons and armor (equippable)."""

from game.ui import Cor, colorir


class Item:
    # 'tipo' tags the category so we don't have to check the class by hand.
    tipo = "item"

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return f"{self.nome} — {self.descricao}"


class Potion(Item):
    tipo = "pocao"

    def __init__(self, nome, descricao, cura):
        super().__init__(nome, descricao)
        self.cura = cura

    def usar(self, alvo):
        """Heal the target and return the message."""
        curado = alvo.curar(self.cura)
        return colorir(f"Você usou {self.nome} e recuperou {curado} de vida.", Cor.VERDE)


class Weapon(Item):
    tipo = "arma"

    def __init__(self, nome, descricao, bonus_ataque):
        super().__init__(nome, descricao)
        self.bonus_ataque = bonus_ataque


class Armor(Item):
    tipo = "armadura"

    def __init__(self, nome, descricao, bonus_defesa):
        super().__init__(nome, descricao)
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
}


def criar_item(nome):
    """Rebuild an item from its name (used when loading a save)."""
    return CATALOGO_ITENS[nome]()
