import pygame

class HealingItem(pygame.sprite.Sprite):
    def __init__(self, name, health, width, height):
        super().__init__()
        self.name = name
        self.health = health
        self.width = width
        self.height = height

        self.image = pygame.image.load('assets/images/items/healing_potion/idle/01.png')
        self.rect = self.image.get_rect()

        collition_width = int(self.rect.width * 0.5)
        collision_height = int(self.rect.height * 0.5)

        self.collision_rect = pygame.Rect(0, 0, collition_width, collision_height)

        self.is_picked_up = False

        self.idle_animation = [pygame.image.load(f'assets/images/items/healing_potion/idle/0{i}.png') for i in range(1, 8)]
        #self.pickup_animation = [pygame.image.load(f'assets/images/items/healing_potion/pickup/0{i}.png') for i in range(1, 8)]

        for i in range (len(self.idle_animation)):
            self.idle_animation[i] = pygame.transform.scale(self.idle_animation[i], (self.width, self.height))

        self.frame_counter = 0
        self.animation_speed = 0.3
        self.current_frame = 0

    def update(self, *args):
        if not self.is_picked_up:
            self.animate_idle()
        if self.is_picked_up:
            self.animate_pickup()
            self.kill()

    def animate_idle(self):
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(self.idle_animation):
            self.frame_counter = 0
        self.image = self.idle_animation[int(self.frame_counter)]

    def animate_pickup(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def give_health(self):
        return self.health