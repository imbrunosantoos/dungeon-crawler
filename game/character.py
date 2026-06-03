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


# Nomes dos efeitos de status e o dano que o veneno causa por turno.
# Usar constantes evita erros de digitação (ex.: "veneno" escrito errado).
VENENO = "veneno"
ATORDOADO = "atordoado"
VENENO_DANO = 8


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

        # Atributos de combate (v3):
        #  - precisao: chance (0 a 1) de o ataque ACERTAR. 0.9 = 90% de acerto.
        #  - chance_critico: chance de um ataque normal virar crítico.
        #  - multiplicador_critico: quanto o crítico multiplica o dano.
        self.precisao = 0.9
        self.chance_critico = 0.1
        self.multiplicador_critico = 2.0

        # Energia: recurso gasto para usar habilidades especiais (tipo "mana").
        # Começa cheia. Os monstros simples não usam, mas todo personagem tem.
        self.energia_max = 0
        self.energia = 0

        # Efeitos de status ativos (v3). É um dicionário nome -> turnos restantes.
        # Ex.: {"veneno": 3} significa "envenenado por mais 3 turnos".
        self.efeitos = {}

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
    # Efeitos de status (veneno, atordoamento)
    # -----------------------------------------------------------------
    def aplicar_efeito(self, nome, turnos):
        """Aplica (ou renova) um efeito por uma quantidade de turnos.

        Usamos max() para que reaplicar um efeito sempre fique com a MAIOR
        duração, em vez de somar infinitamente.
        """
        self.efeitos[nome] = max(self.efeitos.get(nome, 0), turnos)

    def tem_efeito(self, nome):
        """Diz se o personagem está sob um efeito (turnos restantes > 0)."""
        return self.efeitos.get(nome, 0) > 0

    def processar_veneno(self):
        """Se envenenado, perde vida e gasta um turno do veneno.

        Devolve uma mensagem para o combate exibir, ou None se não há veneno.
        """
        if not self.tem_efeito(VENENO):
            return None
        self.hp = max(0, self.hp - VENENO_DANO)
        self.efeitos[VENENO] -= 1  # passou um turno de veneno
        return colorir(f"{self.nome} sofre {VENENO_DANO} de dano de veneno! {self.barra_de_vida()}", Cor.VERDE)

    def consumir_atordoamento(self):
        """Se atordoado, gasta um turno do efeito e devolve True (perde a vez)."""
        if not self.tem_efeito(ATORDOADO):
            return False
        self.efeitos[ATORDOADO] -= 1
        return True

    def limpar_efeitos(self):
        """Remove todos os efeitos. Chamado ao fim do combate — eles não duram
        de uma luta para a outra."""
        self.efeitos.clear()

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
        # Mostra os efeitos de status ativos, se houver (ex.: "veneno (2), atordoado (1)").
        ativos = [f"{nome} ({turnos})" for nome, turnos in self.efeitos.items() if turnos > 0]
        if ativos:
            linhas.append(colorir(f"  Efeitos: {', '.join(ativos)}", Cor.MAGENTA))
        return "\n".join(linhas)
