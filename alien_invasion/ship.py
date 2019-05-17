import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """initialize the space ship and set its position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load ship image and gain the circumscribed rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #put each ship in the middle of sreen bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #store floating distance
        self.center = float(self.rect.centerx)

        #sign for movement
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """draw the ship in specific position in the screen"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """adjust the ship position according to the sign"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        #adjust rect accoding to self.center
        self.rect.centerx = self.center

    def center_ship(self):
        """align center of ships after hit"""
        self.center = self.screen_rect.centerx
