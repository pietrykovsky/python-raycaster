import math
from typing import TYPE_CHECKING
from raycaster.core import Settings


if TYPE_CHECKING:
    from raycaster.game.map import Map


class BaseMovementController:
    @staticmethod
    def _collides_with_wall(x: float, y: float, radius: float, map: "Map") -> bool:
        """
        Checks if the position is valid (not colliding with walls).

        :param x: X-coordinate of the position to check
        :param y: Y-coordinate of the position to check
        :param radius: The radius of the hitbox to consider
        :param map: The map to check against
        :return: True if the position is valid, False otherwise
        """
        for angle in [0, math.pi / 2, math.pi, 3 * math.pi / 2]:
            check_x = x + radius * math.cos(angle)
            check_y = y + radius * math.sin(angle)
            if map.is_wall(
                int(check_x / Settings().CELL_SIZE), int(check_y / Settings().CELL_SIZE)
            ):
                return True
        return False
