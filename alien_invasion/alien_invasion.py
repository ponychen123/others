import sys


import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    #initialize the game and build a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
            (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #create a ship
    ship = Ship(ai_settings, screen)

    #create a group to store bullets
    bullets = Group()
    
    #create a group to store aliens
    aliens = Group()

    #create a group of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #create an instance to store statistics information during game, and create
    #a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #create a play button
    play_button = Button(ai_settings, screen, 'Play')

    #start to the main loop in game
    while True:

        #monitor the keyboard and mouse events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
                aliens, bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, 
                    aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        #update the images in screen and switch on the latest screen
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,  bullets,
                play_button)

run_game()
