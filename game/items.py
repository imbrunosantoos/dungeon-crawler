"""
items.py — os itens do jogo: poções, armas e armaduras.

Modelamos cada tipo de item como uma classe. A base é Item (só tem nome e
descrição). A partir dela:
  - Potion: ao usar, cura vida.
  - Weapon: ao equipar, dá bônus de ataque.
  - Armor:  ao equipar, dá bônus de defesa.

Note a diferença de comportamento: poção é CONSUMÍVEL (some depois de usar);
arma e armadura são EQUIPÁVEIS (ficam vestidas, mudando os atributos). O
inventário (etapa 8) é quem vai tratar isso.
"""

from game.ui import Cor, colorir


class Item:
    """Item genérico. Toda subclasse tem ao menos um nome e uma descrição."""

    # 'tipo' ajuda a identificar a categoria do item sem precisar checar a
    # classe na mão. Cada subclasse sobrescreve com seu próprio valor.
    tipo = "item"

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        # __str__ define como o objeto aparece quando o imprimimos (print).
        return f"{self.nome} — {self.descricao}"


class Potion(Item):
    """Poção de cura: consumível. Ao usar, recupera 'cura' pontos de vida."""

    tipo = "pocao"

    def __init__(self, nome, descricao, cura):
        super().__init__(nome, descricao)
        self.cura = cura

    def usar(self, alvo):
        """Aplica a cura no alvo (geralmente o herói). Devolve a mensagem."""
        curado = alvo.curar(self.cura)
        return colorir(f"Você usou {self.nome} e recuperou {curado} de vida.", Cor.VERDE)


class Weapon(Item):
    """Arma: equipável. Enquanto equipada, soma 'bonus_ataque' ao ataque."""

    tipo = "arma"

    def __init__(self, nome, descricao, bonus_ataque):
        super().__init__(nome, descricao)
        self.bonus_ataque = bonus_ataque


class Armor(Item):
    """Armadura: equipável. Enquanto equipada, soma 'bonus_defesa' à defesa."""

    tipo = "armadura"

    def __init__(self, nome, descricao, bonus_defesa):
        super().__init__(nome, descricao)
        self.bonus_defesa = bonus_defesa


# ---------------------------------------------------------------------------
# Catálogo de itens — funções que criam cópias novas dos itens do jogo.
# ---------------------------------------------------------------------------
# Usamos funções (em vez de objetos prontos) para que cada item criado seja
# independente: assim duas poções no inventário não são "o mesmo objeto".
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
