"""Save and load progress as JSON."""

import json
import os

from game.classes import CLASSES_JOGAVEIS
from game.i18n import definir_idioma, idioma_atual
from game.inventory import Inventory
from game.items import criar_item

# "saves/" is gitignored, so saves stay local.
PASTA_SAVES = "saves"
ARQUIVO_SAVE = os.path.join(PASTA_SAVES, "savegame.json")

# Plain numeric attributes saved and restored as-is. The combat/enchantment
# stats are here too so enchantment bonuses survive a save/load.
_ATRIBUTOS = [
    "nivel", "hp_max", "hp", "ataque", "defesa",
    "energia_max", "energia", "xp", "ouro",
    "precisao", "chance_critico", "regen_por_turno", "veneno_no_ataque",
]


def existe_save():
    return os.path.exists(ARQUIVO_SAVE)


def _nome_da_classe(heroi):
    """Find the hero's class name in the catalog, needed to rebuild it on load."""
    for nome, classe in CLASSES_JOGAVEIS.items():
        if isinstance(heroi, classe):
            return nome
    raise ValueError("Classe do herói desconhecida")


def salvar(heroi):
    os.makedirs(PASTA_SAVES, exist_ok=True)

    inv = heroi.inventario
    dados = {
        "classe": _nome_da_classe(heroi),
        "nome": heroi.nome,
        "fase_atual": getattr(heroi, "fase_atual", 0),
        "dificuldade": getattr(heroi, "dificuldade", "Normal"),
        "idioma": idioma_atual(),
        # Items are stored by name and rebuilt on load.
        "itens": [item.nome for item in inv.itens],
        "arma_equipada": inv.arma_equipada.nome if inv.arma_equipada else None,
        "armadura_equipada": inv.armadura_equipada.nome if inv.armadura_equipada else None,
    }
    for atributo in _ATRIBUTOS:
        dados[atributo] = getattr(heroi, atributo)

    with open(ARQUIVO_SAVE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def carregar():
    with open(ARQUIVO_SAVE, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    # Restore the saved language (older saves default to Portuguese).
    definir_idioma(dados.get("idioma", "pt"))

    heroi = CLASSES_JOGAVEIS[dados["classe"]](dados["nome"])

    # Equipment bonuses are already baked into the saved numbers, so just restore
    # them (don't re-apply the bonuses). .get keeps the class default for keys
    # missing in older saves.
    for atributo in _ATRIBUTOS:
        setattr(heroi, atributo, dados.get(atributo, getattr(heroi, atributo)))
    heroi.fase_atual = dados["fase_atual"]
    heroi.dificuldade = dados.get("dificuldade", "Normal")

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
    if existe_save():
        os.remove(ARQUIVO_SAVE)
