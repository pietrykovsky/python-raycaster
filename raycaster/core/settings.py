class Settings:
    _instance = None

    # GAME RELATED
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    FPS = 60

    # SOUND RELATED
    MASTER_VOLUME = 0.8
    MUSIC_VOLUME = 0.5
    EFFECTS_VOLUME = 0.5

    # MAP RELATED
    CELL_SIZE = 256
    MAX_DISTANCE = 8 * CELL_SIZE

    # PLAYER RELATED
    FOV = 60
    RAY_COUNT = 400
    PLAYER_SPEED = 0.5
    PLAYER_SENSITIVITY = 0.001
    PLAYER_HITBOX_RADIUS = CELL_SIZE // 8

    # MINIMAP RELATED
    MINIMAP_VISIBLE = True  # Press F4 to change
    MINIMAP_RATIO = 0.50
    MINIMAP_OPACITY_RATIO = 0.33

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance
