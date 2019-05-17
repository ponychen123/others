class GameStats():
    """tracking the statistics information"""

    def __init__(self, ai_settings):
        """initialize statistics information"""
        self.ai_settings = ai_settings
        self.reset_stats()

        #being steady on after run the game
        #self.game_active = True

        #set the game to be unactive
        self.game_active = False

        #you can't reset this value at any case
        self.high_score = 0

    def reset_stats(self):
        """initialize the statics information may changing iduring game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
