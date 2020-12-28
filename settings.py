class Settings:

    def __init__(self):
        """
        Initialize the setting of game and this block
        will execute first time after the object initilized
        """

        # screen setting
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # ship setting
        self.ship_speed = 1.5