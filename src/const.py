import math
from settings import Settings


RESOLUTION = Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT

DELTA_ANGLE = math.radians(Settings().FOV / Settings().RAY_COUNT)

# MAP RELATED
SCREEN_DISTANCE = (Settings().SCREEN_WIDTH // 2) / math.tan(
    math.radians(Settings().FOV // 2)
)
