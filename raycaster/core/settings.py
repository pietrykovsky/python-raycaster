class Settings:
    _instance = None

    # GAME RELATED

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    ORIGINAL_SCREEN_WIDTH = SCREEN_WIDTH
    ORIGINAL_SCREEN_HEIGHT = SCREEN_HEIGHT
    FULLSCREEN_MODE = True  # Press F11 to change
    MINIMIZE_RATIO = 0.5

    CAPTION = "DOOM - demo"
    FPS = 60

    # PLAYER RELATED
    FOV = 60
    RAY_COUNT = 150
    PLAYER_SPEED = 0.5
    PLAYER_SENSITIVITY = 0.001

    # MAP RELATED
    CELL_SIZE = 256
    MAX_DISTANCE = 8 * CELL_SIZE

    # MINIMAP RELATED
    MINIMAP_VISIBLE = True  # Press F4 to change
    MINIMAP_RATIO = 0.25
    MINIMAP_OPACITY_RATIO = 0.33

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
