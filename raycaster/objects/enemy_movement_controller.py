import math

from typing import TYPE_CHECKING

from raycaster.core import Settings


if TYPE_CHECKING:
    from raycaster.objects.enemy import Enemy
    from raycaster.objects.sprite_object import SpriteObject
    from raycaster.game.map import Map


class EnemyMovementController:
    @classmethod
    def update_position(cls, enemy: "Enemy", map: "Map", objects: list["SpriteObject"]):
        """
        Updates the position of the enemy.

        :param enemy: Enemy to update position for
        """
        if not cls._collides_with_objects(
            enemy, objects
        ) and not cls._collides_with_player(enemy):
            new_position = cls._generate_new_position(enemy, map)
            enemy.x, enemy.y = new_position

    @staticmethod
    def _collides_with_objects(enemy: "Enemy", objects: list["SpriteObject"]) -> bool:
        """
        Checks if the enemy collides with any of the objects.

        :param enemy: Enemy to check collision for
        :return: True if the enemy collides with any of the objects, False otherwise
        """
        for object in objects:
            if object.distance < enemy.distance:
                dx = object.x - enemy.x
                dy = object.y - enemy.y
                distance = math.hypot(dx, dy)
                if distance < object.hitbox_radius + enemy.hitbox_radius:
                    return True
        return False

    def _collides_with_player(enemy: "Enemy") -> bool:
        """
        Checks if the enemy collides with the player.

        :param enemy: Enemy to check collision for
        :return: True if the enemy collides with the player, False otherwise
        """
        dx = enemy.player.x - enemy.x
        dy = enemy.player.y - enemy.y
        distance = math.hypot(dx, dy)
        return distance < enemy.player.hitbox_radius + enemy.hitbox_radius

    @classmethod
    def _generate_new_position(cls, enemy: "Enemy", map: "Map") -> tuple[float, float]:
        """
        Generates a new position for the enemy.

        :param enemy: Enemy to generate new position for
        :return: New position for the enemy
        """
        speed = enemy.speed * enemy.player.delta_time
        dx = -speed * math.cos(enemy.angle)
        dy = -speed * math.sin(enemy.angle)
        new_x, new_y = enemy.x, enemy.y

        if not cls._collides_with_wall(new_x + dx, new_y, enemy.hitbox_radius, map):
            new_x += dx
        if not cls._collides_with_wall(new_x, new_y + dy, enemy.hitbox_radius, map):
            new_y += dy

        return new_x, new_y

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
