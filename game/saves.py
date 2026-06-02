"""
saves.py — salvar e carregar o progresso do jogo.

Computadores guardam dados em arquivos. Aqui usamos o formato JSON (texto
simples, parecido com dicionários do Python) para gravar o estado do herói:
seus atributos, inventário, equipamentos e em que fase ele está.

Salvar  = transformar o objeto herói em um dicionário e escrever no arquivo.
Carregar = ler o arquivo e reconstruir o objeto herói a partir do dicionário.
"""

import json
import os

from game.classes import CLASSES_JOGAVEIS
from game.inventory import Inventory
from game.items import criar_item

# Pasta e arquivo onde o jogo é salvo. A pasta "saves/" está no .gitignore,
# então os saves ficam só na sua máquina.
PASTA_SAVES = "saves"
ARQUIVO_SAVE = os.path.join(PASTA_SAVES, "savegame.json")

# Atributos numéricos simples do herói que são salvos/restaurados diretamente.
_ATRIBUTOS = [
    "nivel", "hp_max", "hp", "ataque", "defesa",
    "energia_max", "energia", "xp", "ouro",
]


def existe_save():
    """Diz se já existe um jogo salvo (para mostrar a opção 'Continuar')."""
    return os.path.exists(ARQUIVO_SAVE)


def _nome_da_classe(heroi):
    """Descobre o nome da classe do herói ('Guerreiro', 'Mago'...) procurando
    no catálogo qual classe ele é. Precisamos disso para recriá-lo ao carregar."""
    for nome, classe in CLASSES_JOGAVEIS.items():
        if isinstance(heroi, classe):
            return nome
    raise ValueError("Classe do herói desconhecida")


def salvar(heroi):
    """Grava o estado atual do herói no arquivo de save (em JSON)."""
    os.makedirs(PASTA_SAVES, exist_ok=True)  # cria a pasta se ainda não existir

    inv = heroi.inventario
    dados = {
        "classe": _nome_da_classe(heroi),
        "nome": heroi.nome,
        "fase_atual": getattr(heroi, "fase_atual", 0),
        # Inventário: guardamos só os NOMES dos itens (recriados ao carregar).
        "itens": [item.nome for item in inv.itens],
        "arma_equipada": inv.arma_equipada.nome if inv.arma_equipada else None,
        "armadura_equipada": inv.armadura_equipada.nome if inv.armadura_equipada else None,
    }
    # Junta os atributos numéricos ao dicionário.
    for atributo in _ATRIBUTOS:
        dados[atributo] = getattr(heroi, atributo)

    # ensure_ascii=False mantém acentos legíveis; indent=2 deixa o arquivo bonito.
    with open(ARQUIVO_SAVE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def carregar():
    """Lê o arquivo de save e reconstrói o objeto herói."""
    with open(ARQUIVO_SAVE, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    # Recria o herói da classe certa (com os atributos-base da classe).
    heroi = CLASSES_JOGAVEIS[dados["classe"]](dados["nome"])

    # Sobrescreve os atributos com os valores salvos. Os bônus de equipamento já
    # estão embutidos nesses números, então NÃO reaplicamos os bônus aqui.
    for atributo in _ATRIBUTOS:
        setattr(heroi, atributo, dados[atributo])
    heroi.fase_atual = dados["fase_atual"]

    # Reconstrói o inventário a partir dos nomes dos itens.
    inv = Inventory(heroi)
    for nome_item in dados["itens"]:
        inv.adicionar(criar_item(nome_item))
    if dados["arma_equipada"]:
        inv.arma_equipada = criar_item(dados["arma_equipada"])
    if dados["armadura_equipada"]:
        inv.armadura_equipada = criar_item(dados["armadura_equipada"])
    heroi.inventario = inv

    return heroi


def apagar_save():
    """Remove o arquivo de save (ao terminar o jogo, em vitória ou derrota)."""
    if existe_save():
        os.remove(ARQUIVO_SAVE)
