from entities.Character import Character

class Enemy:
    def __init__(self, name, health, attack, defense, speed):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed

    def attack(self, target):
        target.health -= self.attack - target.defense
        print(f"{self.name} attacked {target.name} for {self.attack - target.defense} damage!")