"""
inventory.py — o inventário do herói.

O inventário é uma LISTA de itens com regras: guardar, listar, usar poções e
equipar armas/armaduras. Quando o herói equipa algo, somamos o bônus aos seus
atributos; ao trocar de equipamento, primeiro removemos o bônus do antigo.

Cada inventário pertence a um "dono" (o herói), guardado em self.dono — é nele
que aplicamos curas e bônus.
"""

from game.ui import Cor, colorir


class Inventory:
    def __init__(self, dono):
        self.dono = dono          # o personagem dono deste inventário
        self.itens = []           # lista de objetos Item (poções, armas, ...)
        self.arma_equipada = None
        self.armadura_equipada = None

    # -----------------------------------------------------------------
    def adicionar(self, item):
        """Coloca um item na mochila."""
        self.itens.append(item)

    def pocoes(self):
        """Devolve só os itens que são poções (úteis no combate)."""
        return [item for item in self.itens if item.tipo == "pocao"]

    # -----------------------------------------------------------------
    def usar_pocao(self, item):
        """Usa uma poção: cura o dono e remove a poção da mochila (consumível)."""
        mensagem = item.usar(self.dono)
        self.itens.remove(item)
        return mensagem

    def equipar(self, item):
        """Equipa uma arma ou armadura, aplicando o bônus ao dono.

        Se já houver algo equipado naquele espaço, removemos o bônus do antigo
        antes de vestir o novo (assim os bônus não se acumulam errado).
        """
        if item.tipo == "arma":
            if self.arma_equipada:
                self.dono.ataque -= self.arma_equipada.bonus_ataque
            self.arma_equipada = item
            self.dono.ataque += item.bonus_ataque
            return colorir(f"Você equipou {item.nome} (+{item.bonus_ataque} de ataque).", Cor.VERDE)

        if item.tipo == "armadura":
            if self.armadura_equipada:
                self.dono.defesa -= self.armadura_equipada.bonus_defesa
            self.armadura_equipada = item
            self.dono.defesa += item.bonus_defesa
            return colorir(f"Você equipou {item.nome} (+{item.bonus_defesa} de defesa).", Cor.VERDE)

        return colorir("Esse item não pode ser equipado.", Cor.VERMELHO)

    # -----------------------------------------------------------------
    def listar(self):
        """Devolve um texto com tudo que há na mochila e o que está equipado."""
        linhas = [colorir("=== Mochila ===", Cor.CIANO)]

        arma = self.arma_equipada.nome if self.arma_equipada else "nenhuma"
        armadura = self.armadura_equipada.nome if self.armadura_equipada else "nenhuma"
        linhas.append(f"Arma equipada:     {arma}")
        linhas.append(f"Armadura equipada: {armadura}")
        linhas.append("")

        if not self.itens:
            linhas.append("(vazia)")
        else:
            # enumerate dá o índice (começando em 1) junto com cada item, para
            # o jogador poder escolher pelo número.
            for i, item in enumerate(self.itens, start=1):
                linhas.append(f"  [{i}] {item}")

        return "\n".join(linhas)
