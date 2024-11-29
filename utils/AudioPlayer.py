import pygame
import os
import random

class AudioPlayer:
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.music_playing = False
        self.music_tracks = []

    def load_sounds(self):
        pass
        # Carrega todos os sons
        #self.sounds["attack"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "attack.wav"))
        #self.sounds["die"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "die.wav"))
        #self.sounds["hit"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "hit.wav"))
        #self.sounds["pickup"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "pickup.wav"))

    def play_sound(self, sound_name):
        # Toca um som
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def load_music(self):
        # Carrega todas as músicas de fundo disponíveis
        music_files = [f for f in os.listdir("assets/sounds/game/musics") if f.endswith(".mp3") or f.endswith(".wav")]
        self.music_tracks = [os.path.join("assets", "sounds", "game", "musics", music) for music in music_files]

    def play_music(self):
        # Toca uma música de fundo aleatória
        if not self.music_playing and self.music_tracks:
            self.music = random.choice(self.music_tracks)
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(0.1)  # Ajuste o volume aqui
            pygame.mixer.music.play(-1)  # Reproduz a música em loop
            self.music_playing = True
            print(f"Playing music: {self.music}")  # Para debugar

    def stop_music(self):
        # Para a música de fundo
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def pause_music(self):
        # Pausa a música de fundo
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False

    def unpause_music(self):
        # Despausa a música de fundo
        if not self.music_playing and self.music:
            pygame.mixer.music.unpause()
            self.music_playing = True