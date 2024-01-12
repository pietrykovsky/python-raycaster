import math

from typing import TYPE_CHECKING

from raycaster.core import Settings


if TYPE_CHECKING:
    from raycaster.objects.enemy import Enemy
    from raycaster.game.map import Map


class EnemyMovementController:
    @classmethod
    def update_position(cls, enemy: "Enemy", map: "Map"):
        """
        Updates the position of the enemy.

        :param enemy: Enemy to update position for
        """
        new_position = cls._generate_new_position(enemy, map)
        enemy.x, enemy.y = new_position

    @staticmethod
    def _generate_new_position(enemy: "Enemy", map: "Map") -> tuple[float, float]:
        """
        Generates a new position for the enemy.

        :param enemy: Enemy to generate new position for
        :return: New position for the enemy
        """
        speed = enemy.speed * enemy.player.delta_time
        dx = -speed * math.cos(enemy.angle)
        dy = -speed * math.sin(enemy.angle)
        new_x, new_y = enemy.x, enemy.y

        if not map.is_wall(
            int((new_x + dx) / Settings().CELL_SIZE),
            int(new_y / Settings().CELL_SIZE),
        ):
            new_x += dx
        if not map.is_wall(
            int(new_x / Settings().CELL_SIZE),
            int((new_y + dy) / Settings().CELL_SIZE),
        ):
            new_y += dy

        return new_x, new_y
