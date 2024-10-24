from entities.Enemy import Enemy

class Character:
    def __init__(self, name, health, attack, defense, speed):
        name = "Player"
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed

    def attack(self, target):
        target.health -= self.attack - target.defense
        print(f"{Enemy.name} attacked {target.name} for {self.attack - target.defense} damage!")
