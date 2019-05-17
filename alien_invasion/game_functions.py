import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """response to keydown"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """if allowed, fire a bullet"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def check_keyup_events(event, ship):
    """response to keyup"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets):
    """response to keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                    aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, mouse_x, mouse_y):
    """start the game while click on the play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reset some settings
        ai_settings.initialize_dynamic_settings()
        #hide the cursor
        pygame.mouse.set_visible(False)

        #reset game
        stats.reset_stats()
        stats.game_active = True

        #reset all scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #empty alien and bullets lists
        aliens.empty()
        bullets.empty()

        #create a new fleet of aliens and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    """update the image on screen, and turn to new screen"""
    #redraw the screen in each loop
    screen.fill(ai_settings.bg_color)

    #redraw all bullets after aliens and ships
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)

    #display score
    sb.show_score()

    #draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    #display the latest screen
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """update the positions of bullets and remove the vanished ones"""
    #update the positions of bullets
    bullets.update()

    #remove the vanished bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
   
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
            aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
        aliens, bullets):
    if len(aliens) == 0:
        #remove current bullets, speed up and create a fleet of new aliens
        bullets.empty()
        ai_settings.increase_speed()

        #upgrade while killed all aliens
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

    #check whether the bullet hit the alien
    #if so, delete corrosponding aliens and bullets
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

def get_number_aliens_x(ai_settings, alien_width):
    """calculate the numbers that this row can contain"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width ))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """determin how much rows can this display contain"""
    available_space_y = (ai_settings.screen_height -
            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #create a row of aliens
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """build a fleet of aliens"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
            alien.rect.height)
    
    #create the rows of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                    row_number)

def check_fleet_edges(ai_settings, aliens):
    """take some actions while aliens meet edges"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """move downforward the aliens and change relative directions"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """ship response to the hit aliens"""
    if stats.ships_left > 0:
        #ships_left minus 1
        stats.ships_left -= 1

        #update scoreboard
        sb.prep_ships()

        #wipe lists of alines and bullets
        aliens.empty()
        bullets.empty()

        #create a new fleet of aliens and put ship on the middle bottom
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """check if some aliens hit the bottom of screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #do same as ships hitted by aliens
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """update the positions of all aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #check the hit between aliens and ships
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    #check if any alien meet the botom
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """check whether exists high_score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
