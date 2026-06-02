# Dungeon Crawler ⚔️

Um RPG de terminal feito em Python. Você cria um herói, escolhe uma classe,
enfrenta monstros em fases cada vez mais difíceis, ganha experiência, sobe de
nível, coleta itens e equipamentos — até derrotar o chefe final.

## Como rodar

Você precisa do Python 3 instalado. Então, dentro da pasta do projeto:

```bash
python3 main.py
```

## Funcionalidades (em construção)

- [x] Estrutura do projeto e utilitários de terminal
- [ ] Personagem com vida, ataque, defesa, XP e nível
- [ ] Classes jogáveis: Guerreiro, Mago e Arqueiro
- [ ] Monstros e um chefe (boss)
- [ ] Combate por turnos
- [ ] Recompensas e evolução de nível
- [ ] Itens e poções
- [ ] Inventário e equipamentos
- [ ] Fases com dificuldade crescente
- [ ] Menu e loop principal do jogo
- [ ] Salvar e carregar progresso

## Estrutura do código

```
main.py          # ponto de entrada do jogo
game/            # módulos do jogo
  ui.py          # utilitários de terminal (cores, telas, input)
  character.py   # classe base do personagem
  classes.py     # classes jogáveis
  monster.py     # monstros e boss
  items.py       # itens, poções e equipamentos
  inventory.py   # inventário
  combat.py      # sistema de combate
  stages.py      # fases do jogo
```
