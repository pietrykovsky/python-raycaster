import math

from typing import TYPE_CHECKING

from raycaster.movement_controllers.base_movement_controller import (
    BaseMovementController,
)


if TYPE_CHECKING:
    from raycaster.objects.enemy import Enemy
    from raycaster.objects.sprite_object import SpriteObject
    from raycaster.game.map import Map


class EnemyMovementController(BaseMovementController):
    @classmethod
    def update_position(cls, enemy: "Enemy", map: "Map", objects: list["SpriteObject"]):
        """
        Updates the position of the enemy.

        :param enemy: Enemy to update position for
        :param map: Game map for collision detection
        :param objects: List of objects to check for collisions
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
        :param objects: List of objects to check against
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

    @staticmethod
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
        :param map: Game map for collision detection
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
