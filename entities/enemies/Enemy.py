import pygame

class Enemy:
    def __init__(self, name, health, attack, defense, speed):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed


    def attack(self, target):
        # Calcula o dano considerando a defesa do alvo
        damage = max(0, self.attack - target.defense)
        target.health -= damage
        print(f"{self.name} atacou {target.name} e causou {damage} de dano!")

    def update(self):
        pass