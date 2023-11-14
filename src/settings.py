import math


class Settings:
    _instance = None

    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    RESOLUTION = SCREEN_WIDTH, SCREEN_HEIGHT

    CAPTION = "DOOM - demo"
    FPS = 60

    FOV = 90
    RAY_COUNT = 60
    DELTA_ANGLE = math.radians(FOV / RAY_COUNT)

    SCREEN_DISTANCE = (SCREEN_WIDTH // 2) / math.tan(math.radians(FOV // 2))
    CELL_SIZE = 16

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
