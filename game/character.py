"""
character.py — a classe base de qualquer personagem do jogo.

Aqui mora o conceito central de Programação Orientada a Objetos (POO):
uma CLASSE é um "molde", e um OBJETO é uma "coisa" criada a partir desse molde.

A classe Character é o molde de qualquer ser vivo com vida, ataque, defesa,
experiência e nível. Mais para frente, o herói do jogador (Guerreiro, Mago,
Arqueiro) e os monstros vão APROVEITAR esse molde por meio de herança, em vez
de reescrever tudo de novo.
"""

from game.ui import Cor, colorir


class Character:
    """Molde base de um personagem (herói ou inimigo)."""

    def __init__(self, nome, hp_max, ataque, defesa, nivel=1):
        # O método __init__ é o "construtor": roda automaticamente quando
        # criamos um personagem novo. O 'self' representa o próprio objeto que
        # está sendo criado — é assim que guardamos os dados DENTRO dele.
        self.nome = nome
        self.nivel = nivel

        # Vida: hp_max é o máximo; hp é a vida atual (começa cheia).
        self.hp_max = hp_max
        self.hp = hp_max

        self.ataque = ataque
        self.defesa = defesa

        # Energia: recurso gasto para usar habilidades especiais (tipo "mana").
        # Começa cheia. Os monstros simples não usam, mas todo personagem tem.
        self.energia_max = 0
        self.energia = 0

        # Progressão: experiência acumulada e ouro coletado.
        self.xp = 0
        self.ouro = 0

    # -----------------------------------------------------------------
    # Estado de vida
    # -----------------------------------------------------------------
    def esta_vivo(self):
        """Retorna True se ainda tem vida. Usado no combate para saber se a
        luta acabou."""
        return self.hp > 0

    def receber_dano(self, dano):
        """Aplica dano ao personagem, descontando parte com a defesa.

        Regra simples: o dano real é o ataque do inimigo menos a defesa, mas
        nunca menos que 1 (sempre dói um pouquinho). Devolvemos o dano real
        para o combate poder mostrar na tela.
        """
        dano_real = max(1, dano - self.defesa)
        self.hp = max(0, self.hp - dano_real)  # não deixa a vida ficar negativa
        return dano_real

    def curar(self, quantidade):
        """Recupera vida, sem passar do máximo. Devolve quanto curou de fato."""
        cura_real = min(quantidade, self.hp_max - self.hp)
        self.hp += cura_real
        return cura_real

    def recuperar_energia(self, quantidade):
        """Recupera energia, sem passar do máximo. A cada turno de combate o
        personagem recupera um pouco, para poder usar habilidades de novo."""
        self.energia = min(self.energia_max, self.energia + quantidade)

    # -----------------------------------------------------------------
    # Progressão de nível
    # -----------------------------------------------------------------
    def xp_para_proximo_nivel(self):
        """Quanto de XP é preciso para subir do nível atual.

        Fórmula simples e crescente: 100 x nível. No nível 1 precisa de 100,
        no nível 2 precisa de 200, e assim por diante — cada nível fica mais
        difícil, como num RPG de verdade.
        """
        return 100 * self.nivel

    def ganhar_xp(self, quantidade):
        """Soma XP e sobe de nível quantas vezes for necessário.

        Usamos um 'while' (não um 'if') porque, se o personagem ganhar muito XP
        de uma vez, ele pode subir VÁRIOS níveis seguidos.
        """
        self.xp += quantidade
        while self.xp >= self.xp_para_proximo_nivel():
            self.xp -= self.xp_para_proximo_nivel()  # gasta o XP do nível
            self.subir_de_nivel()

    def subir_de_nivel(self):
        """Aumenta o nível e melhora os atributos. Também recupera toda a vida,
        como recompensa por evoluir."""
        self.nivel += 1
        self.hp_max += 20
        self.ataque += 5
        self.defesa += 2
        self.energia_max += 5
        self.hp = self.hp_max          # vida cheia ao subir de nível
        self.energia = self.energia_max  # energia cheia também

    # -----------------------------------------------------------------
    # Exibição
    # -----------------------------------------------------------------
    def barra_de_vida(self, largura=20):
        """Desenha uma barrinha visual de vida, tipo [#####-----].

        Calcula a proporção de vida atual e preenche essa fração da barra.
        A cor muda conforme a vida: verde (alta), amarela (média), vermelha (baixa).
        """
        proporcao = self.hp / self.hp_max if self.hp_max else 0
        preenchido = int(proporcao * largura)
        barra = "#" * preenchido + "-" * (largura - preenchido)

        if proporcao > 0.5:
            cor = Cor.VERDE
        elif proporcao > 0.25:
            cor = Cor.AMARELO
        else:
            cor = Cor.VERMELHO

        return colorir(f"[{barra}] {self.hp}/{self.hp_max}", cor)

    def ficha(self):
        """Devolve um texto com o resumo do personagem (usado no menu/combate)."""
        linhas = [
            f"{colorir(self.nome, Cor.NEGRITO)} (Nível {self.nivel})",
            f"  Vida:    {self.barra_de_vida()}",
        ]
        # Só mostramos a energia se o personagem realmente usa (herói).
        if self.energia_max > 0:
            linhas.append(
                colorir(f"  Energia: {self.energia}/{self.energia_max}", Cor.AZUL)
            )
        linhas.append(f"  Ataque: {self.ataque}   Defesa: {self.defesa}")
        linhas.append(
            f"  XP:     {self.xp}/{self.xp_para_proximo_nivel()}   Ouro: {self.ouro}"
        )
        return "\n".join(linhas)
