Organização do código:

controller.py:

- Ponto de entrada do jogo.
- Instancia a cena do jogo (GameScene) e roda o loop principal.

game_scene.py:

Gere a lógica principal da cena (a movimentação, renderização e controle dos eventos).
Manipula a interação do jogador com o personagem e atualiza o estado da scene.

Character.py:

Define a classe Character.
A classe armazena as propriedades e o comportamento do personagem.


Fluxo do jogo:

O controller.py inicia o Pygame, configura a janela e chama o método run() da class GameScene().

A GameScene contém os métodos para:

- Eventos: Processa eventos do teclado e de saída.
- Atualização: Atualiza a posição do personagem com base nos inputs.
- Renderização: Desenha o personagem na scene e atualiza o display.

O Character.py fornece a classe do personagem com atributos vida, ataque, defesa, velocidade e posição inicial e tamanho(width/height).
