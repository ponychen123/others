import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """a class to control the bullets emitted by ships"""

    def __init__(self, ai_settings, screen, ship):
        """create a bullet in the same position of ship"""
        super().__init__()
        self.screen = screen
        
        #create a bullet rect on (0,0), and set the right position later
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #store the float position of bullet 
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """move the bullet upward"""
        #update the float position of bullet
        self.y -= self.speed_factor
        #update the ini position of rect
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullt on display"""
        pygame.draw.rect(self.screen, self.color, self.rect)

