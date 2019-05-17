import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """create a class of an alien"""

    def __init__(self, ai_settings, screen):
        """initialize an alien and set its initial position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load the image of aliens and set relatice propertites of rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #put the initial alien adjent to  the top lrft corner 
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the accurate of alien
        self.x = float(self.rect.x)

    def blitme(self):
        """draw the alien at specific position"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """return true while aliens meet the edges"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """right or left  move the alien"""
        self.x += (self.ai_settings.alien_speed_factor *
                self.ai_settings.fleet_direction)
        self.rect.x = self.x
