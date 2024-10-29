import pygame
import os
from utils.Cursor import Cursor


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Vampire Diaries")
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.options = ["Play", "Options", "Quit"]
        self.selected_option = 0
        self.running = True
        self.CURSOR_SIZE = (15, 23)

        # self.map_layout = self.generate_map()
        # self.sand_assets = self.load_sand_tiles()

        self.TILE_SIZE = 60
        self.MAP_WIDTH = 2
        self.MAP_HEIGHT = 2

        self.foam_animation = [pygame.image.load("../assets/images/map/water/00.png"),
                               pygame.image.load("../assets/images/map/water/01.png"),
                               pygame.image.load("../assets/images/map/water/01.png"),
                               pygame.image.load("../assets/images/map/water/03.png"),
                               pygame.image.load("../assets/images/map/water/04.png"),
                               pygame.image.load("../assets/images/map/water/05.png"),
                               pygame.image.load("../assets/images/map/water/06.png"),
                               pygame.image.load("../assets/images/map/water/07.png")]

        self.animation_speed = 0.2
        self.frame_counter = 0
        self.current_frame = 0

        self.background_image = self.load_and_scale_image('../assets/images/menu/Background.png',
                                                          (self.width, self.height))
        self.banner_menu = self.load_and_scale_image('../assets/images/menu/Banner_Vertical.png', (350, 450))
        self.banner_image = self.load_and_scale_image('../assets/images/menu/Ribbon_Red_3Slides.png', (350, 80))
        self.button_image = self.load_and_scale_image('../assets/images/menu/Button_Red_3Slides.png', (150, 50))
        self.font = pygame.font.Font(os.path.join('../assets/fonts/DungeonFont.ttf'), 25)

        # Custom cursor instance
        self.cursor = Cursor('../assets/images/UI/pointer/01.png', self.CURSOR_SIZE)

        # Track mouse position dynamically
        self.mouse_position = (0, 0)  # Initial position

    def load_and_scale_image(self, path, size):
        try:
            image = pygame.image.load(path)
            return pygame.transform.scale(image, size)
        except FileNotFoundError:
            print(f"Error: File {path} not found.")
            return pygame.Surface(size)

    def animate_foam(self):
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.foam_animation):
            self.frame_counter = 0
        self.image = self.foam_animation[int(self.frame_counter)]


    '''def generate_map(self):
        empty_map = [[0 for _ in range(self.MAP_WIDTH)] for _ in range(self.MAP_HEIGHT)]
        return empty_map

    def load_sand_tiles(self):
        sand_tile = pygame.image.load("assets/images/map/ground/sand_tile.png")
        return {0: sand_tile}'''

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(self.mouse_position):
                            return self.options[i]

    def render(self):
        self.screen.blit(self.background_image, (0, 0))

        '''for row in range(self.MAP_HEIGHT):
            for col in range(self.MAP_WIDTH):
                tile = self.map_layout[row][col]
                tile_asset = self.sand_assets[tile]
                self.screen.blit(tile_asset, (100, 200))'''

        # Draw background and banner
        banner_x = (self.width - self.banner_menu.get_width()) // 2
        banner_y = (self.height - self.banner_menu.get_height()) // 2
        self.screen.blit(self.banner_menu, (banner_x, banner_y))
        self.screen.blit(self.banner_image, (590, 275))

        # Button rendering
        button_width, button_height = self.button_image.get_size()
        start_y = (self.height - (len(self.options) * button_height)) // 2
        self.button_rects = []

        for i, option in enumerate(self.options):
            if pygame.Rect((self.width - button_width) // 2, start_y + i * button_height, button_width,
                           button_height).collidepoint(self.mouse_position):
                button_img = pygame.transform.scale(self.button_image,
                                                    (int(button_width * 1.05), int(button_height * 1.05)))
                text_y = start_y + i * button_height + button_height - 60 // 2
                self.draw_text(option, (255, 255, 255), self.width // 2, text_y)
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
            self.draw_text(option, color, text_x, text_y)

        self.cursor.draw(self.screen)
        pygame.display.flip()

    def update(self):
        # Update mouse position
        self.mouse_position = pygame.mouse.get_pos()
        self.cursor.update()

    def run(self):
        while self.running:
            selected_action = self.handle_events()
            if selected_action == "Quit":
                self.running = False
            self.update()
            self.render()
            self.clock.tick(60)


menu = MainMenu()
menu.run()
