import math
from settings import Settings


RESOLUTION = Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT

DELTA_ANGLE = math.radians(Settings().FOV / Settings().RAY_COUNT)

# MAP RELATED
SCREEN_DISTANCE = (Settings().SCREEN_WIDTH // 2) / math.tan(
    math.radians(Settings().FOV // 2)
)

# MINIMAP RELATED
MINIMAP_VISIBLE = True
MINIMAP_RATIO = 0.15
MINIMAP_SCALE = (
    Settings().SCREEN_WIDTH * MINIMAP_RATIO / 10
)  # just for now, to fix in next issue
MINIMAP_CELL = (
    Settings().CELL_SIZE / MINIMAP_SCALE
)  # just for now, to fix in next issue
