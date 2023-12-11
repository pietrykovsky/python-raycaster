import math

from raycaster.core import Settings

# GAME RELATED
SCREEN_WIDTH = 1280  # Changes over time with resize
SCREEN_HEIGHT = 720

# PLAYER RELATED
DELTA_ANGLE = math.radians(Settings().FOV / Settings().RAY_COUNT)

# MAP RELATED
SCREEN_DISTANCE = (SCREEN_WIDTH // 2) / math.tan(math.radians(Settings().FOV // 2))
