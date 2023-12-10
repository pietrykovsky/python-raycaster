import math


class Settings:
    _instance = None

    # GAME RELATED
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    RESOLUTION = SCREEN_WIDTH, SCREEN_HEIGHT

    CAPTION = "DOOM - demo"
    FPS = 60

    # PLAYER RELATED
    FOV = 60
    RAY_COUNT = 150
    DELTA_ANGLE = math.radians(FOV / RAY_COUNT)
    PLAYER_SPEED = 0.5
    PLAYER_SENSITIVITY = 0.001

    # MAP RELATED
    SCREEN_DISTANCE = (SCREEN_WIDTH // 2) / math.tan(math.radians(FOV // 2))
    CELL_SIZE = 256
    MAX_DISTANCE = 8 * CELL_SIZE

    # MINIMAP RELATED
    MINIMAP_VISIBLE = True
    MINIMAP_RATIO = 0.25
    MINIMAP_OPACITY_RATIO = 0.33

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
