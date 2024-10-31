from entities.enemies.Enemy import Enemy

class Goblin(Enemy):
    def __init__(self, name, level):
        super().__init__(name, level)
        self.abilities = ["bash", "slash", "stab"]
