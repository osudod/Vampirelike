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
    
    def move(self,target_rect):
        if target_rect.x > self.rect.x:
            print("down")
            self.rect.x += self.speed
        if target_rect.x < self.rect.x:
            print("up")
            self.rect.x -= self.speed
        if target_rect.y > self.rect.y:
            print("right")
            self.rect.y += self.speed
        if target_rect.y < self.rect.y:
            print("left")
            self.rect.y -= self.speed
    
