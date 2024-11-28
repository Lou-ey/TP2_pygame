import pygame
import os
from skimage import filters

from skimage.transform import rescale
from utils.Cursor import Cursor


class MainMenu:
    def __init__(self):
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Vampire Diaries")
        #Adaptar largura e altura ao tamanho das telas
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.options = ["Play", "Options", "Quit"]
        self.selected_option = 0
        self.running = True
        self.CURSOR_SIZE = (15, 23)

        self.TILE_SIZE = 60
        self.MAP_WIDTH = 2
        self.MAP_HEIGHT = 2
        # teste

        #self.boneco1 = pygame.image.load("../assets/images/player/player_idle/00.png").convert_alpha()

        self.foam_animation = [pygame.image.load("assets/images/map/water/00.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/01.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/01.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/03.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/04.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/05.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/06.png").convert_alpha(),
                               pygame.image.load("assets/images/map/water/07.png").convert_alpha()]

        self.animation_speed = 0.2
        self.frame_counter = 0
        self.current_frame = 0
        self.foam_image = self.foam_animation[0]
        self.sand_image = pygame.image.load("assets/images/map/ground/sand_tile.png").convert_alpha()

        self.background_image = self.load_and_scale_image('assets/images/menu/Background.png',(self.width, self.height))
        self.smooth_background = self.load_and_scale_image('assets/images/menu/Background_blur.png',(self.width, self.height))
        self.banner_menu = self.load_and_scale_image('assets/images/menu/Banner_Vertical.png', (350, 450))
        self.banner_menu_options = self.load_and_scale_image('assets/images/menu/Banner_Vertical.png', (800, 1000))
        self.banner_image = self.load_and_scale_image('assets/images/menu/Ribbon_Red_3Slides.png', (350, 80))
        self.button_image = self.load_and_scale_image('assets/images/menu/Button_Red_3Slides.png', (150, 50))


        # Custom cursor instance
        self.cursor = Cursor('assets/images/UI/pointer/01.png', self.CURSOR_SIZE)
        # Track mouse position dynamically
        self.mouse_position = (0, 0)  # Initial position
        self.checkbox_rect = pygame.Rect(self.width // 2 - 20, self.height * 0.60, 40, 40)
        self.checkbox_checked = False

    def draw_checkbox(self):
        if self.checkbox_checked:
            pygame.draw.rect(self.screen, (0,0,0), self.checkbox_rect)  # Preenche a caixa com a cor
        else:
            pygame.draw.rect(self.screen, (255,255,255), self.checkbox_rect)  # Desenha a caixa sem preencher
        pygame.draw.rect(self.screen, (0,0,0), self.checkbox_rect, 2)  # Desenha a borda da caixa de seleção

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

    def animate_foam(self):
        foam_rescaled = []
        for i in self.foam_animation:
            foam_rescaled.append(pygame.transform.scale(i, (int(i.get_width() * 0.89), int(i.get_height() * 0.89))).convert_alpha())
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(foam_rescaled):
            self.frame_counter = 0
        self.foam_image = foam_rescaled[int(self.frame_counter)]

    def draw_text(self, text, color, x, y, font_size):
        self.font = pygame.font.Font(os.path.join('assets/fonts/DungeonFont.ttf'), font_size)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_slider(self, x, y, width, height, value):
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, width, height))  # Fundo da barra
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, value * width, height))  # Barra preenchida
        pygame.draw.circle(self.screen, (0, 0, 0), (x + int(value * width), y + height // 2), 10)

    def menuPrincipal(self):
        self.screen.blit(self.background_image, (0, 0))

        banner_x = (self.width - self.banner_menu.get_width()) // 2
        banner_y = (self.height - self.banner_menu.get_height()) // 2
        self.screen.blit(self.banner_menu, (banner_x, banner_y))
        self.screen.blit(self.banner_image, (banner_x, banner_y + 70))

        button_width, button_height = self.button_image.get_size()
        start_y = (self.height - (len(self.options) * button_height)) // 2

        self.button_rects = []

        for i, option in enumerate(self.options):
            if pygame.Rect((self.width - button_width) // 2, start_y + i * button_height, button_width, button_height).collidepoint(self.mouse_position):
                button_img = pygame.transform.scale(self.button_image,(int(button_width * 1.05), int(button_height * 1.05)))
                text_y = start_y + i * button_height + button_height - 60 // 2
                self.draw_text(option, (255, 255, 255), self.width // 2, text_y, 25)
                color = (255, 255, 255)
            else:
                button_img = self.button_image
                color = (0, 0, 0)

            button_x = (self.width - button_img.get_width()) // 2
            button_y = start_y + i * button_img.get_height()

            button_rect = pygame.Rect(button_x, button_y, button_img.get_width(), button_img.get_height())

            self.button_rects.append(button_rect)

            self.screen.blit(button_img, (button_x, button_y))
            text_x = button_x + button_img.get_width() // 2
            text_y = button_y + button_img.get_height() - 60 // 2
            self.draw_text(option, color, text_x, text_y, 25)

        self.animate_foam()

        foam_x = (self.width - self.foam_image.get_width()) // 2 - int(self.width * 0.1)
        foam_y = (self.height - self.foam_image.get_height()) // 2 - int(self.height * 0.4)
        self.screen.blit(self.foam_image, (foam_x, foam_y))

        sand_x = (self.width - self.sand_image.get_width()) // 2 - int(self.width * 0.1)
        sand_y = (self.height - self.sand_image.get_height()) // 2 - int(self.height * 0.4)
        self.screen.blit(self.sand_image, (sand_x, sand_y))
        '''boneco_x = (self.width - self.boneco1.get_width()) // 2 - int(self.width * 0.1)
        boneco_y = (self.height - self.boneco1.get_height()) // 2 - int(self.height * 0.4)
        self.screen.blit(self.boneco1, (boneco_x, boneco_y))'''

        foam_x = (self.width - self.foam_image.get_width()) // 2 + int(self.width * 0.1)
        foam_y = (self.height - self.foam_image.get_height()) // 2 + int(self.height * 0.4)
        self.screen.blit(self.foam_image, (foam_x, foam_y))

        sand_x = (self.width - self.sand_image.get_width()) // 2 + int(self.width * 0.1)
        sand_y = (self.height - self.sand_image.get_height()) // 2 + int(self.height * 0.4)
        self.screen.blit(self.sand_image, (sand_x, sand_y))
        self.cursor.draw(self.screen)
        pygame.display.flip()

    def options_menu(self):
        slider_width = 300
        self.screen.blit(self.smooth_background, (0, 0))
        banner_x = (self.width - self.banner_menu_options.get_width()) // 2
        banner_y = (self.height - self.banner_menu_options.get_height()) // 2
        self.screen.blit(self.banner_menu_options, (banner_x, banner_y))
        self.draw_text("Options Menu", (0, 0, 0), self.width // 2, self.height * 0.2, 60)
        self.draw_text("Sound", (0, 0, 0), self.width // 2, self.height * 0.35, 50)
        self.draw_slider(self.width // 2 - slider_width // 2, self.height * 0.4, slider_width, 20, self.volume)
        self.draw_text("FullScreen", (0, 0, 0), self.width // 2, self.height * 0.55, 50)
        self.draw_checkbox()
        self.cursor.draw(self.screen)
        pygame.display.flip()