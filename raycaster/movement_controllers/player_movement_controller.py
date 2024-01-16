import math

from typing import TYPE_CHECKING

from raycaster.movement_controllers.base_movement_controller import (
    BaseMovementController,
)

if TYPE_CHECKING:
    from raycaster.game import Map, Player
    from raycaster.objects.sprite_object import SpriteObject


class PlayerMovementController(BaseMovementController):
    @classmethod
    def update_position(
        cls,
        player: "Player",
        delta_position: tuple[float, float],
        map: "Map",
        objects: list["SpriteObject"],
    ):
        dx, dy = delta_position
        cls._apply_movement(player, dx, dy, map, objects)

    @classmethod
    def _apply_movement(
        cls,
        player: "Player",
        dx: float,
        dy: float,
        map: "Map",
        objects: list["SpriteObject"],
    ):
        """
        Apply movement to the player, checking for wall and object collisions.

        python
        Copy code
        :param player: Player to move
        :param dx: Delta X of the movement
        :param dy: Delta Y of the movement
        :param map: Game map for collision detection
        :param objects: List of objects to check for collisions
        """
        new_x = player.x + dx
        new_y = player.y + dy

        # Check for wall collision in X direction
        if not cls._collides_with_wall(
            new_x, player.y, player.hitbox_radius, map
        ) and not cls._collides_with_any_object(
            new_x, player.y, player.hitbox_radius, objects
        ):
            player.x = new_x

        # Check for wall collision in Y direction
        if not cls._collides_with_wall(
            player.x, new_y, player.hitbox_radius, map
        ) and not cls._collides_with_any_object(
            player.x, new_y, player.hitbox_radius, objects
        ):
            player.y = new_y

    @classmethod
    def _collides_with_any_object(
        cls, x: float, y: float, radius: float, objects: list["SpriteObject"]
    ) -> bool:
        """
        Checks if the position collides with any of the objects.

        :param x: X-coordinate of the position to check
        :param y: Y-coordinate of the position to check
        :param radius: The radius of the hitbox to consider
        :param objects: List of objects to check against
        :return: True if the position collides with any object, False otherwise
        """
        for obj in objects:
            dx = obj.x - x
            dy = obj.y - y
            distance = math.hypot(dx, dy)
            if distance < obj.hitbox_radius + radius:
                return True
        return False
