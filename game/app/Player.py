from Character import Char

class Player(Char):
    
    def __init__(self, image, damage, hp, speed):
        super().__init__(image, damage, hp, speed)
    
    def draw(self, screen, x, y):
        return super().draw(screen, x, y)
    
    def attack(self, enemy):
        return super().attack(enemy)
    
    def get_speed(self):
        return super().get_speed()