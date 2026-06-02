"""
ui.py — utilitários de interface no terminal.

A ideia deste módulo é concentrar tudo que tem a ver com "mostrar coisas na tela"
e "ler o que o jogador digita". Assim, o resto do jogo não precisa se preocupar
com detalhes de cor, limpar tela, etc. — é só chamar estas funções.

Reaproveitar essas funções em todos os outros arquivos mantém o jogo consistente
e fácil de mudar (se um dia quisermos trocar as cores, mexemos só aqui).
"""

import os
import time


# ---------------------------------------------------------------------------
# CORES no terminal (códigos ANSI)
# ---------------------------------------------------------------------------
# O terminal entende uns "códigos de escape" especiais para mudar a cor do texto.
# Por exemplo, escrever \033[31m faz o texto ficar vermelho, e \033[0m volta ao
# normal. Guardamos esses códigos em constantes com nomes legíveis para não
# precisar decorar os números.
class Cor:
    RESET = "\033[0m"      # volta à cor padrão
    NEGRITO = "\033[1m"
    VERMELHO = "\033[31m"
    VERDE = "\033[32m"
    AMARELO = "\033[33m"
    AZUL = "\033[34m"
    MAGENTA = "\033[35m"
    CIANO = "\033[36m"
    CINZA = "\033[90m"


def colorir(texto, cor):
    """Envolve um texto com uma cor e garante o reset no final.

    Exemplo: colorir("Vitória!", Cor.VERDE) -> texto verde que depois volta
    ao normal, para não "vazar" a cor para as próximas linhas.
    """
    return f"{cor}{texto}{Cor.RESET}"


# ---------------------------------------------------------------------------
# Funções de TELA
# ---------------------------------------------------------------------------
def limpar_tela():
    """Limpa o terminal.

    No Windows o comando é "cls"; no Mac/Linux é "clear". O os.name nos diz em
    qual sistema estamos ("nt" = Windows) para escolher o comando certo.
    """
    os.system("cls" if os.name == "nt" else "clear")


def titulo(texto):
    """Imprime um título destacado, dentro de uma moldura simples."""
    largura = len(texto) + 4
    linha = "=" * largura
    print(colorir(linha, Cor.CIANO))
    print(colorir(f"= {texto} =", Cor.CIANO + Cor.NEGRITO))
    print(colorir(linha, Cor.CIANO))


def pausar(mensagem="\nPressione ENTER para continuar..."):
    """Espera o jogador apertar ENTER. Útil para ele ler o que aconteceu
    antes de a tela ser limpa ou o jogo seguir em frente."""
    input(colorir(mensagem, Cor.CINZA))


def digitar(texto, velocidade=0.02):
    """Imprime o texto letra por letra, dando um efeito de "máquina de escrever".

    Deixa as mensagens do jogo mais dramáticas. Se a velocidade for 0, imprime
    tudo de uma vez (útil para testes, onde não queremos esperar).
    """
    for caractere in texto:
        print(caractere, end="", flush=True)  # flush força aparecer na hora
        if velocidade:
            time.sleep(velocidade)
    print()  # quebra de linha no final


# ---------------------------------------------------------------------------
# Funções de ENTRADA (ler o que o jogador digita, com segurança)
# ---------------------------------------------------------------------------
def ler_texto(pergunta):
    """Lê um texto qualquer do jogador, removendo espaços sobrando nas pontas."""
    return input(colorir(pergunta, Cor.AMARELO)).strip()


def ler_opcao(pergunta, opcoes):
    """Lê uma escolha entre um número de opções válidas.

    'opcoes' é uma lista, por exemplo ["1", "2", "3"]. A função fica repetindo
    a pergunta até o jogador digitar algo que esteja nessa lista — assim o jogo
    nunca quebra por causa de uma digitação errada.
    """
    while True:
        escolha = input(colorir(pergunta, Cor.AMARELO)).strip()
        if escolha in opcoes:
            return escolha
        print(colorir(f"Opção inválida. Escolha uma de: {', '.join(opcoes)}", Cor.VERMELHO))
