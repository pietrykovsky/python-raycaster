import math


class Settings:
    _instance = None

    # GAME RELATED
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    RESOLUTION = SCREEN_WIDTH, SCREEN_HEIGHT

    CAPTION = "DOOM - demo"
    FPS = 60

    # PLAYER RELATED
    FOV = 60
    RAY_COUNT = 300
    DELTA_ANGLE = math.radians(FOV / RAY_COUNT)
    PLAYER_SPEED = 0.1
    PLAYER_SENSITIVITY = 0.001

    # MAP RELATED
    SCREEN_DISTANCE = (SCREEN_WIDTH // 2) / math.tan(math.radians(FOV // 2))
    CELL_SIZE = 64
    MAX_DISTANCE = 8 * CELL_SIZE

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
