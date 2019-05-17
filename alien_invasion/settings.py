class Settings:
    """a class to store all the settings in alien invasion"""

    def __init__(self):
        """static settings to initialize game"""

        #screen displays
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        #settings for ships
        
        self.ship_limit = 2

        #settings for bullet
        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #settings for aliens
        
        self.fleet_drop_speed = 5
        

        #how much to speed up game
        self.speedup_scale = 1.1

        #how much to improve score
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """some settiongs varied with game"""
        self.ship_speed_factor = 0.25
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 0.2

        #scoring
        self.alien_points = 50

        #fleet_direction means move left for -1 and move right for 1
        self.fleet_direction = 1

    def increase_speed(self):
        """improve the settings for speed and score"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
