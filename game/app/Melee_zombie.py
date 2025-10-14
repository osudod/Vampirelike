from Character import Char

class Melee(Char):
    
    def __init__(self, image, damage, hp, speed, x, y):
        super().__init__(image, damage, hp, speed, x, y)
    
    def draw(self, screen, x, y):
        return super().draw(screen, x, y)
    
    def attack(self, enemy):
        return super().attack(enemy)
    
    def get_speed(self):
        return super().get_speed()
    
    def move(self, x, y):
        if x > self.x:
            self.x = self.x + self.speed
        elif x < self.x:
            self.x = self.x - self.speed
        if y > self.y:
            self.y = self.y + self.speed
        elif y < self.y:
            self.y = self.y - self.speed
    
