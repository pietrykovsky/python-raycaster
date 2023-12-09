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

    # MINIMAP RELATED
    MINIMAP_VISIBLE = True
    MINIMAP_RATIO = 0.15
    MINIMAP_SCALE = (
        Settings().SCREEN_WIDTH * MINIMAP_RATIO / 10
    )  # just for now, to fix in next issue
    MINIMAP_CELL = (
        Settings().CELL_SIZE / MINIMAP_SCALE
    )  # just for now, to fix in next issue

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
