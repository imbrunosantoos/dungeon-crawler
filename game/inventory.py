"""The hero's inventory: hold items, use potions and equip gear."""

from game.ui import Cor, colorir


class Inventory:
    def __init__(self, dono):
        self.dono = dono
        self.itens = []
        self.arma_equipada = None
        self.armadura_equipada = None

    def adicionar(self, item):
        self.itens.append(item)

    def pocoes(self):
        return [item for item in self.itens if item.tipo == "pocao"]

    def usar_pocao(self, item):
        """Consume a potion: heal the owner and drop it from the bag."""
        mensagem = item.usar(self.dono)
        self.itens.remove(item)
        return mensagem

    def equipar(self, item):
        """Equip a weapon or armor, swapping out whatever was there before.

        Base stat bonus and any enchantment of the old item are removed first,
        then the new item's are applied.
        """
        if item.tipo == "arma":
            if self.arma_equipada:
                self.dono.ataque -= self.arma_equipada.bonus_ataque
                if self.arma_equipada.encantamento:
                    self.arma_equipada.encantamento.remover(self.dono)
            self.arma_equipada = item
            self.dono.ataque += item.bonus_ataque
            if item.encantamento:
                item.encantamento.aplicar(self.dono)
            return colorir(f"Você equipou {item.nome} (+{item.bonus_ataque} de ataque).", Cor.VERDE)

        if item.tipo == "armadura":
            if self.armadura_equipada:
                self.dono.defesa -= self.armadura_equipada.bonus_defesa
                if self.armadura_equipada.encantamento:
                    self.armadura_equipada.encantamento.remover(self.dono)
            self.armadura_equipada = item
            self.dono.defesa += item.bonus_defesa
            if item.encantamento:
                item.encantamento.aplicar(self.dono)
            return colorir(f"Você equipou {item.nome} (+{item.bonus_defesa} de defesa).", Cor.VERDE)

        return colorir("Esse item não pode ser equipado.", Cor.VERMELHO)

    def listar(self):
        """Text view of the bag plus what's currently equipped."""
        linhas = [colorir("=== Mochila ===", Cor.CIANO)]

        arma = self.arma_equipada.nome if self.arma_equipada else "nenhuma"
        armadura = self.armadura_equipada.nome if self.armadura_equipada else "nenhuma"
        linhas.append(f"Arma equipada:     {arma}")
        linhas.append(f"Armadura equipada: {armadura}")
        linhas.append("")

        if not self.itens:
            linhas.append("(vazia)")
        else:
            for i, item in enumerate(self.itens, start=1):
                linhas.append(f"  [{i}] {item}")

        return "\n".join(linhas)
