class Settings:
    _instance = None

    FPS = 60
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    RESOLUTION = SCREEN_WIDTH, SCREEN_HEIGHT
    CAPTION = "DOOM - demo"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
