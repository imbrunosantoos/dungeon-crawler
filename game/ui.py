"""Terminal helpers: colors, screen handling and input."""

import os
import time


# ANSI escape codes, kept here with readable names.
class Cor:
    RESET = "\033[0m"
    NEGRITO = "\033[1m"
    VERMELHO = "\033[31m"
    VERDE = "\033[32m"
    AMARELO = "\033[33m"
    AZUL = "\033[34m"
    MAGENTA = "\033[35m"
    CIANO = "\033[36m"
    CINZA = "\033[90m"


def colorir(texto, cor):
    """Wrap text in a color and always reset afterwards."""
    return f"{cor}{texto}{Cor.RESET}"


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def titulo(texto):
    """Print a title inside a simple framed box."""
    largura = len(texto) + 4
    linha = "=" * largura
    print(colorir(linha, Cor.CIANO))
    print(colorir(f"= {texto} =", Cor.CIANO + Cor.NEGRITO))
    print(colorir(linha, Cor.CIANO))


def pausar(mensagem="\nPressione ENTER para continuar..."):
    input(colorir(mensagem, Cor.CINZA))


def digitar(texto, velocidade=0.02):
    """Print text with a typewriter effect. velocidade=0 prints instantly."""
    for caractere in texto:
        print(caractere, end="", flush=True)
        if velocidade:
            time.sleep(velocidade)
    print()


def ler_texto(pergunta):
    return input(colorir(pergunta, Cor.AMARELO)).strip()


def ler_opcao(pergunta, opcoes):
    """Keep asking until the player types one of the valid options."""
    while True:
        escolha = input(colorir(pergunta, Cor.AMARELO)).strip()
        if escolha in opcoes:
            return escolha
        print(colorir(f"Opção inválida. Escolha uma de: {', '.join(opcoes)}", Cor.VERMELHO))
