class Monster:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def attack(self, target):
        target.hp -= self.damage
        print(f"{self.name} attacks {target.name} for {self.damage} damage!")
