import pygame
import os
from utils.Cursor import Cursor
from utils.AudioPlayer import AudioPlayer

class MainMenu:
    def __init__(self):
        self.volume = 0.03
        self.audio = AudioPlayer()
        self.musica = self.audio.menu_music()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.musica)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Dungeon Crawler")
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.options = ["Play", "Options", "Quit"]
        self.selected_option = 0
        self.running = True
        self.CURSOR_SIZE = (15, 23)

        self.TILE_SIZE = 60
        self.MAP_WIDTH = 2
        self.MAP_HEIGHT = 2
        # teste

        self.boneco1_animation = [pygame.image.load(f"assets/images/player/knight/idle/0{i}.png").convert_alpha() for i in range(1, 6)]
        self.boneco2_animation = [pygame.image.load(f"assets/images/enemies/torch_goblin/idle/0{i}.png").convert_alpha() for i in range(1, 6)]

        self.foam_animation = [pygame.image.load("assets/images/map/water/00.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/01.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/01.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/03.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/04.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/05.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/06.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/07.png").convert_alpha()]

        self.boneco1_animation = [pygame.transform.scale(i, (int(i.get_width() * 0.7), int(i.get_height() * 0.7))).convert_alpha() for i in self.boneco1_animation]
        self.boneco2_animation = [pygame.transform.scale(i, (int(i.get_width() * 0.7), int(i.get_height() * 0.7))).convert_alpha() for i in self.boneco2_animation]

        self.animation_speed = 0.08
        self.frame_counter = 0
        self.current_frame = 0
        self.foam_image = self.foam_animation[0]
        self.boneco1_image = self.boneco1_animation[0]
        self.boneco2_image = self.boneco2_animation[0]
        self.sand_image = pygame.image.load("assets/images/map/ground/sand_tile.png").convert_alpha()

        self.background_image = self.load_and_scale_image('assets/images/menu/Background.png',(self.screen.get_width(), self.screen.get_height()))
        self.smooth_background = self.load_and_scale_image('assets/images/menu/Background_blur.png',(self.screen.get_width(), self.screen.get_height()))
        self.banner_menu = self.load_and_scale_image('assets/images/menu/Banner_Vertical.png', (350, 450))
        self.banner_menu_options = self.load_and_scale_image('assets/images/menu/Banner_Vertical.png', (self.screen.get_width() - self.screen.get_width() * 0.60, self.screen.get_height() - self.screen.get_height() * 0.25))
        self.banner_image = self.load_and_scale_image('assets/images/menu/Ribbon_Red_3Slides.png', (350, 80))
        self.button_image = self.load_and_scale_image('assets/images/menu/Button_Red_3Slides.png', (150, 50))
        self.back_button = self.load_and_scale_image('assets/images/UI/menuUI/voltar.png', (70, 70))
        self.back_button_rect = self.back_button.get_rect(center=(self.screen.get_width()// 2 - self.banner_menu_options.get_width() * 0.15,self.screen.get_height() // 2 - self.banner_menu_options.get_height() * 0.18))
        self.back_button_pressed = self.load_and_scale_image('assets/images/UI/menuUI/voltar_pressed.png', (70, 70))
        self.with_sound = self.load_and_scale_image('assets/images/UI/menuUI/with_Sound.png', (70, 70))
        self.with_sound_rect = self.with_sound.get_rect(center=(self.screen.get_width() // 2 , self.screen.get_height() * 0.45))
        self.sound_muted = self.load_and_scale_image('assets/images/UI/menuUI/Sound_mute.png', (70, 70))
        self.muted = False
        self.fullscreen_off = self.load_and_scale_image('assets/images/UI/menuUI/Fullscreen_off.png', (70, 70))
        self.fullscreen_off_rect = self.fullscreen_off.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() * 0.57))
        self.fullscreen_on = self.load_and_scale_image('assets/images/UI/menuUI/Fullscreen_on.png', (70, 70))
        self.fullscreened = False
        # Custom cursor instance
        self.cursor = Cursor('assets/images/UI/pointer/01.png', self.CURSOR_SIZE)
        # Track mouse position dynamically
        self.mouse_position = (0, 0)



    #função para mudar o tamanho de uma imagem
    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    #função para animar a espuma
    def animate_foam(self):
        # Cria uma lista para armazenar as imagens redimensionadas da animação de espuma
        foam_rescaled = []

        # Itera por cada frame na animação de espuma (lista de imagens em self.foam_animation)
        for i in self.foam_animation:
            # Converte a superfície para preservar transparência com .convert_alpha()
            foam_rescaled.append(
                pygame.transform.scale(i, (int(i.get_width() * 0.89), int(i.get_height() * 0.89))).convert_alpha())

        # Incrementa o contador de frames com base na velocidade da animação
        self.frame_counter += self.animation_speed

        # Reinicia o contador se ele ultrapassar o número total de frames na animação
        if self.frame_counter >= len(foam_rescaled):
            self.frame_counter = 0

        # Seleciona a imagem atual da animação com base no contador e define como `self.foam_image`
        self.foam_image = foam_rescaled[int(self.frame_counter)]

    def animate_boneco1(self):
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.boneco1_animation):
            self.frame_counter = 0
        self.boneco1_image = self.boneco1_animation[int(self.frame_counter)]

    def animate_boneco2(self):
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.boneco2_animation):
            self.frame_counter = 0
        self.boneco2_image = self.boneco2_animation[int(self.frame_counter)]

    #Função para desenhar texto
    def draw_text(self, text, color, x, y, font_size):
        self.font = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), font_size)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    #Função para desenhar o menu principal
    def menuPrincipal(self):
        self.screen.blit(self.background_image, (0, 0))

        # Define as posições do banner principal desenha no centro do ecrã
        banner_x = (self.width - self.banner_menu.get_width()) // 2
        banner_y = (self.height - self.banner_menu.get_height()) // 2
        self.screen.blit(self.banner_menu, (banner_x, banner_y))
        self.screen.blit(self.banner_image, (banner_x, banner_y + 70))

        # Obtém as dimensões do botão e calcula a posição inicial para centralizar verticalmente
        button_width, button_height = self.button_image.get_size()
        #start_y é usada para calcular a posição vertical inicial de onde os botões do menu devem começar a ser desenhados.
        start_y = (self.height - (len(self.options) * button_height)) // 2

        # Lista para armazenar os retângulos dos botões (usada para detectar cliques)
        self.button_rects = []

        # faz um ciclo sobre as opções do menu para desenhar os botões
        for i, option in enumerate(self.options):
            # Detecta se o rato está sobre o botão para aplicar um efeito de aumento
            if pygame.Rect((self.width - button_width) // 2, start_y + i * button_height, button_width,button_height).collidepoint(self.mouse_position):
                # Aumenta levemente o tamanho do botão e muda a cor do texto
                button_img = pygame.transform.scale(self.button_image,(int(button_width * 1.05), int(button_height * 1.05)))
                color = (255, 255, 255)
            else:
                # Mantém o botão no seu tamanho original
                button_img = self.button_image
                color = (0, 0, 0)

            # Calcula as posições X e Y para desenhar o botão e o texto
            button_x = (self.width - button_img.get_width()) // 2
            button_y = start_y + i * button_img.get_height()

            # Cria um retângulo correspondente ao botão para guardar
            button_rect = pygame.Rect(button_x, button_y, button_img.get_width(), button_img.get_height())
            self.button_rects.append(button_rect)

            # Desenha o botão e o texto no ecrã
            self.screen.blit(button_img, (button_x, button_y))
            text_x = button_x + button_img.get_width() // 2
            text_y = button_y + button_img.get_height() - 60 // 2
            self.draw_text(option, color, text_x, text_y, 25)

        # créditos
        self.draw_text("Made by Rodri & Louey", (255, 255, 255),self.screen.get_width() - self.screen.get_width() * 0.82, self.screen.get_height() * 0.92, 30)
        self.draw_text("Music by, xDeviruchi", (255, 255, 255),self.screen.get_width() - self.screen.get_width() * 0.1, self.screen.get_height() * 0.95, 18)
        # Animações para os elementos de fundo
        self.animate_foam()
        self.animate_boneco1()
        self.animate_boneco2()

        # Calcula posições e desenha elementos no ecrã
        foam_x = (self.width - self.foam_image.get_width()) // 2 - int(self.width * 0.1)
        foam_y = (self.height - self.foam_image.get_height()) // 2 - int(self.height * 0.4)
        self.screen.blit(self.foam_image, (foam_x, foam_y))

        sand_x = (self.width - self.sand_image.get_width()) // 2 - int(self.width * 0.1)
        sand_y = (self.height - self.sand_image.get_height()) // 2 - int(self.height * 0.4)
        self.screen.blit(self.sand_image, (sand_x, sand_y))

        boneco_x = (self.width - self.boneco1_image.get_width()) // 2 - int(self.width * 0.1)
        boneco_y = (self.height - self.boneco1_image.get_height()) // 2 - int(self.height * 0.4)
        self.screen.blit(self.boneco1_image, (boneco_x, boneco_y))

        foam_x = (self.width - self.foam_image.get_width()) // 2 + int(self.width * 0.1)
        foam_y = (self.height - self.foam_image.get_height()) // 2 + int(self.height * 0.4)
        self.screen.blit(self.foam_image, (foam_x, foam_y))

        sand_x = (self.width - self.sand_image.get_width()) // 2 + int(self.width * 0.1)
        sand_y = (self.height - self.sand_image.get_height()) // 2 + int(self.height * 0.4)
        self.screen.blit(self.sand_image, (sand_x, sand_y))

        boneco_2_x = (self.width - self.boneco2_image.get_width()) // 2 + int(self.width * 0.1)
        boneco_2_y = (self.height - self.boneco2_image.get_height()) // 2 + int(self.height * 0.4)
        self.screen.blit(self.boneco2_image, (boneco_2_x, boneco_2_y))

        # Desenha o cursor no ecrã
        self.cursor.draw(self.screen)

        pygame.display.flip()

    def options_menu(self):
        self.screen.blit(self.smooth_background, (0, 0))

        # Define e desenha o banner no centro do ecrã
        banner_x = (self.screen.get_width() - self.banner_menu_options.get_width()) // 2
        banner_y = (self.screen.get_height() - self.banner_menu_options.get_height()) // 2
        self.screen.blit(self.banner_menu_options, (banner_x, banner_y))

        self.draw_text("Options Menu", (0, 0, 0), self.screen.get_width() // 2, self.screen.get_height() * 0.30, 40)

        # Obtém a posição atual do rato
        mouse_position = pygame.mouse.get_pos()

        # Verifica se o rato está sobre o botão de voltar
        if self.back_button_rect.collidepoint(mouse_position):
            self.screen.blit(self.back_button_pressed, self.back_button_rect.topleft)
        else:
            self.screen.blit(self.back_button, self.back_button_rect.topleft)

        self.draw_text("Sound", (0, 0, 0), self.screen.get_width() // 2, self.screen.get_height() * 0.40, 30)

        if self.muted:
            self.screen.blit(self.sound_muted, self.with_sound_rect.topleft)
        else:
            self.screen.blit(self.with_sound, self.with_sound_rect.topleft)

        self.draw_text("FullScreen", (0, 0, 0), self.screen.get_width() // 2, self.screen.get_height() * 0.52, 30)
        if self.fullscreened:
            # Se o modo fullscreen estiver ativo, desenha o ícon correspondente
            self.screen.blit(self.fullscreen_on, self.fullscreen_off_rect.topleft)
        else:
            # Caso contrário, desenha o ícon de fullscreen  desativado
            self.screen.blit(self.fullscreen_off, self.fullscreen_off_rect.topleft)

        self.cursor.draw(self.screen)

        pygame.display.flip()



