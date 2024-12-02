import pygame
import os
import random

class AudioPlayer:
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.music_playing = False
        self.music_tracks = []
        self.is_muted = False
        self.volume = 0.03

    def load_sounds(self):
        # Carrega todos os sons
        #self.sounds['select'] = pygame.mixer.Sound('assets/sounds/game/sfx/select.wav')
        self.sounds['hit'] = pygame.mixer.Sound('assets/sounds/game/sfx/hit.wav')
        self.sounds['level_up'] = pygame.mixer.Sound('assets/sounds/game/sfx/level_up.wav')
        self.sounds['game_over'] = pygame.mixer.Sound('assets/sounds/game/sfx/game_over.mp3')
        #self.sounds['enemy_die'] = pygame.mixer.Sound('assets/sounds/game/enemy_die.wav')
        #self.sounds['player_die'] = pygame.mixer.Sound('assets/sounds/game/player_die.wav')
        self.sounds['player_hit'] = pygame.mixer.Sound('assets/sounds/game/sfx/player_hit.wav')
        #self.sounds['player_walk'] = pygame.mixer.Sound('assets/sounds/game/sfx/player_walk.wav')
        self.sounds['heal'] = pygame.mixer.Sound('assets/sounds/game/sfx/heal.wav')

    def play_sound(self, sound_name, volume):
        # Toca um som
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            self.sounds[sound_name].set_volume(volume)

    def load_music(self):
        # Carrega todas as músicas de fundo disponíveis
        music_files = [f for f in os.listdir("assets/sounds/game/musics") if f.endswith(".mp3") or f.endswith(".wav")]
        self.music_tracks = [os.path.join("assets", "sounds", "game", "musics", music) for music in music_files]

    def menu_music(self):
        musica = 'assets/sounds/menu/Title_Theme .wav'
        return musica

    def play_music(self):
        # Toca uma música de fundo aleatória
        if not self.music_playing and self.music_tracks:
            self.music = random.choice(self.music_tracks)
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(0.03)  # Ajuste o volume aqui
            pygame.mixer.music.play(-1)  # Reproduz a música em loop
            self.music_playing = True
            print(f"Playing music: {self.music}")  # Para debugar

    def set_volume(self, volume):
        self.volume =  volume
        pygame.mixer.music.set_volume(self.volume)

    def mute_music(self):
        if not self.is_muted:
            self.set_volume(0)
            self.is_muted = True

    def unmute_music(self):
        if self.is_muted:
            self.set_volume(0.03)
            self.is_muted = False

    def pause_music(self):
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False

    def unpause_music(self):
        if not self.music_playing:
            pygame.mixer.music.unpause()
            self.music_playing = True

    def stop_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False