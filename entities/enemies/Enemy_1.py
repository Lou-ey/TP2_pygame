from entities.Enemy import Enemy

class Enemy_1(Enemy):
    def __init__(self):
        super().__init__("Enemy 1", 100, 10, 5, 10)