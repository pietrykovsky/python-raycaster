import math


class Settings:
    _instance = None

    CAPTION = "DOOM - demo"
    
    # GAME RELATED
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    FPS = 60

    CELL_SIZE = 256

    # PLAYER RELATED
    FOV = 60
    RAY_COUNT = 150

    PLAYER_SPEED = 0.5
    PLAYER_SENSITIVITY = 0.001

    MAX_DISTANCE = 8 * CELL_SIZE

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
