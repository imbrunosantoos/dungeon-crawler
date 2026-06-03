"""Base class shared by heroes and monsters."""

from game.i18n import nome as traduzir_nome, t
from game.ui import Cor, colorir


# Status effect names and the damage poison deals each turn.
VENENO = "veneno"
ATORDOADO = "atordoado"
VENENO_DANO = 8


class Character:
    def __init__(self, nome, hp_max, ataque, defesa, nivel=1):
        self.nome = nome
        self.nivel = nivel

        self.hp_max = hp_max
        self.hp = hp_max

        self.ataque = ataque
        self.defesa = defesa

        # Combat rolls: hit chance and critical hits.
        self.precisao = 0.9
        self.chance_critico = 0.1
        self.multiplicador_critico = 2.0

        # Bonuses granted by item enchantments while equipped.
        self.regen_por_turno = 0
        self.veneno_no_ataque = 0

        # Energy spent on special abilities (mana-like). Monsters leave it at 0.
        self.energia_max = 0
        self.energia = 0

        # Active status effects: name -> remaining turns.
        self.efeitos = {}

        self.xp = 0
        self.ouro = 0

    # -----------------------------------------------------------------
    # Health
    # -----------------------------------------------------------------
    def nome_exibicao(self):
        """Name shown on screen. Heroes use their given name; monsters override
        this to return the translated name."""
        return self.nome

    def esta_vivo(self):
        return self.hp > 0

    def receber_dano(self, dano):
        """Take damage reduced by defense (always at least 1). Returns the hit."""
        dano_real = max(1, dano - self.defesa)
        self.hp = max(0, self.hp - dano_real)
        return dano_real

    def curar(self, quantidade):
        """Heal without going over the max. Returns how much was healed."""
        cura_real = min(quantidade, self.hp_max - self.hp)
        self.hp += cura_real
        return cura_real

    def recuperar_energia(self, quantidade):
        self.energia = min(self.energia_max, self.energia + quantidade)

    # -----------------------------------------------------------------
    # Status effects (poison, stun)
    # -----------------------------------------------------------------
    def aplicar_efeito(self, nome, turnos):
        # Refresh to the longer duration instead of stacking.
        self.efeitos[nome] = max(self.efeitos.get(nome, 0), turnos)

    def tem_efeito(self, nome):
        return self.efeitos.get(nome, 0) > 0

    def processar_veneno(self):
        """Apply poison damage for the turn. Returns a message or None."""
        if not self.tem_efeito(VENENO):
            return None
        self.hp = max(0, self.hp - VENENO_DANO)
        self.efeitos[VENENO] -= 1
        return colorir(t("combate.dano_veneno", nome=self.nome_exibicao(),
                         dano=VENENO_DANO, barra=self.barra_de_vida()), Cor.VERDE)

    def consumir_atordoamento(self):
        """Spend a stun turn. Returns True if the character is stunned now."""
        if not self.tem_efeito(ATORDOADO):
            return False
        self.efeitos[ATORDOADO] -= 1
        return True

    def limpar_efeitos(self):
        # Effects don't carry over between fights.
        self.efeitos.clear()

    # -----------------------------------------------------------------
    # Leveling
    # -----------------------------------------------------------------
    def xp_para_proximo_nivel(self):
        # Each level costs more: 100 * level.
        return 100 * self.nivel

    def ganhar_xp(self, quantidade):
        # while (not if) so a big XP gain can grant several levels at once.
        self.xp += quantidade
        while self.xp >= self.xp_para_proximo_nivel():
            self.xp -= self.xp_para_proximo_nivel()
            self.subir_de_nivel()

    def subir_de_nivel(self):
        self.nivel += 1
        self.hp_max += 20
        self.ataque += 5
        self.defesa += 2
        self.energia_max += 5
        # Full heal and energy refill as a level-up reward.
        self.hp = self.hp_max
        self.energia = self.energia_max

    # -----------------------------------------------------------------
    # Display
    # -----------------------------------------------------------------
    def barra_de_vida(self, largura=20):
        """Health bar like [#####-----], colored by how much HP is left."""
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
        """One-block summary used in menus and combat."""
        linhas = [
            f"{colorir(self.nome, Cor.NEGRITO)} ({t('ficha.nivel')} {self.nivel})",
            f"  {t('ficha.vida')}: {self.barra_de_vida()}",
        ]
        # Energy only shows for characters that actually use it (heroes).
        if self.energia_max > 0:
            linhas.append(
                colorir(f"  {t('ficha.energia')}: {self.energia}/{self.energia_max}", Cor.AZUL)
            )
        linhas.append(f"  {t('ficha.ataque')}: {self.ataque}   {t('ficha.defesa')}: {self.defesa}")
        linhas.append(
            f"  XP: {self.xp}/{self.xp_para_proximo_nivel()}   {t('ficha.ouro')}: {self.ouro}"
        )
        ativos = [f"{traduzir_nome(ef)} ({turnos})" for ef, turnos in self.efeitos.items() if turnos > 0]
        if ativos:
            linhas.append(colorir(f"  {t('ficha.efeitos')}: {', '.join(ativos)}", Cor.MAGENTA))
        return "\n".join(linhas)
