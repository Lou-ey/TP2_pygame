# Projeto: Jogo em Pygame

Este é um jogo desenvolvido em Python utilizando a biblioteca Pygame. O jogo apresenta um personagem que pode se mover em um ambiente de mapa 2D. O objetivo deste projeto é proporcionar uma experiência interativa e divertida com elementos de RPG e Sobrevivência.

## Índice

- [Recursos](#recursos)
- [Instalação](#instalação)
- [Como Jogar](#como-jogar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuições](#contribuições)
- [Licença](#licença)

## Recursos

- **Movimentação do Personagem:** O personagem pode se mover em quatro direções.
- **Interação com o Ambiente:** Árvores que podem ser desenhadas no mapa, e o personagem pode passar atrás delas.
- **Animações:** O personagem e as árvores possuem animações para tornar a experiência mais envolvente.

## Instalação

Para executar o jogo, você precisará ter Python e Pygame instalados em seu sistema. Siga os passos abaixo:

1. Clone este repositório:
   ```bash
   git clone <URL_DO_REPOSITÓRIO>
   cd <NOME_DA_PASTA>

2. Instale o Pygame:
   ```bash
    pip install pygame
   
3. Execute o jogo:

    ```bash
    python controller.py
   
## Estrutura do Projeto

``` bash
project_directory/
│
├── controller.py               # Ficheiro principal para iniciar o jogo
├── scenes/                      # Contém as diferentes cenas do jogo
│   ├── game_scene.py            # Lógica da cena do jogo
│
├── entities/                    # Contém os diferentes sprites do jogo
│   ├── characters/              # Contém a classe do personagem
│   │   └── Character.py
│   ├── objects/                 # Contém objetos interativos como árvores
│   │   └── Tree.py
│   ├── enemies/                 # Contém inimigos do jogo
│   │   └── Enemy.py
│
├── utils/                       # Funções utilitárias
│   ├── CameraGroup.py           # Classe para gerenciar a câmera do jogo
│   ├── Cursor.py                # Classe para gerenciar o cursor do jogo
│   └── helpers.py             # Constantes do jogo
│
├── assets/                      # Imagens e sons do jogo
│   ├── images/
│   │   ├── map/
│   │   │   ├── grass_tile.png
│   │   │   ├── tree/
│   │   │   │   ├── 00.png
│   │   │   │   ├── 01.png
│   │   │   │   ├── 02.png
│   │   │   │   └── 03.png
│   │   └── ...
│   └── sound/
│
└── README.md                   # Este ficheiro
```

