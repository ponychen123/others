import pygame.font

class Button():

    def __init__(self, ai_settings, screen, msg):
        """initialize the property of button"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #set the size of button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #set the rect object of button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #the lable of button only need to be creatived once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """reder the msg as image, and put it at the center of button"""
        self.msg_image = self.font.render(msg, True, self.text_color, 
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw a button filled by a specific color and then draw a button
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
