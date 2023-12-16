import math
from enum import Enum

from raycaster.core import Settings

# GAME RELATED
RESOLUTION = Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT

# PLAYER RELATED
DELTA_ANGLE = math.radians(Settings().FOV / Settings().RAY_COUNT)

# MAP RELATED
SCREEN_DISTANCE = (Settings().SCREEN_WIDTH // 2) / math.tan(
    math.radians(Settings().FOV // 2)
)

# SPRITES RELATED
class AnimationType(Enum):
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"
    DEATH = "death"
    HIT = "hit"
