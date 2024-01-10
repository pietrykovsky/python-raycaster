from typing import TYPE_CHECKING
import math

from raycaster.core import Settings
from raycaster import const


if TYPE_CHECKING:
    from raycaster.objects import SpriteObject


class SpriteProjectionProcessor:
    @classmethod
    def get_screen_position(cls, obj: "SpriteObject") -> tuple[int, int]:
        """
        Calculates the position of the object on the screen.

        :param obj: Object to calculate position for
        :return: Object's position on the screen
        """
        screen_dist = const.SCREEN_DISTANCE
        rel_angle = obj.angle - obj.player.angle - math.pi
        spatial_width, spatial_height = cls.get_spatial_dimensions(obj)
        screen_y = (
            Settings().SCREEN_HEIGHT // 2 - spatial_height // 2
            if spatial_height <= Settings().SCREEN_HEIGHT
            else 0
        )
        screen_x = (
            (
                math.tan(rel_angle) * screen_dist
                + Settings().SCREEN_WIDTH // 2
                - spatial_width // 2
            )
            if spatial_width <= Settings().SCREEN_WIDTH
            else math.tan(rel_angle) * screen_dist
        )
        return int(screen_x), int(screen_y)

    @classmethod
    def get_screen_dimensions(cls, obj: "SpriteObject") -> tuple[int, int]:
        """
        Returns the size of the object on the screen.

        :param obj: Object to calculate size for
        :return: Object's size on the screen
        """
        spatial_width, spatial_height = cls.get_spatial_dimensions(obj)
        if cls.smaller_than_screen(spatial_width, spatial_height):
            return (spatial_width, spatial_height)
        else:
            return cls._scale_dimensions(spatial_width, spatial_height)

    @staticmethod
    def get_spatial_dimensions(obj: "SpriteObject") -> tuple[int, int]:
        """
        Calculates the dimensions of the object based on object distance.

        :param obj: Object to calculate dimensions for
        :return: Object's spatial dimensions
        """
        screen_dist = const.SCREEN_DISTANCE
        texture_width, texture_height = obj.texture.get_size()
        height = screen_dist * texture_height / obj.distance
        width = screen_dist * texture_width / obj.distance
        return int(width), int(height)

    @staticmethod
    def smaller_than_screen(width: float | int, height: float | int) -> bool:
        """
        Checks if the dimensions are smaller than the screen.
        """
        return height <= Settings().SCREEN_HEIGHT and width <= Settings().SCREEN_WIDTH

    @classmethod
    def intersects_screen_center(cls, obj: "SpriteObject") -> bool:
        """
        Checks if the object's screen projection intersects the center of the screen.
        """
        screen_x, screen_y = cls.get_screen_position(obj)
        screen_width, screen_height = cls.get_screen_dimensions(obj)
        return (
            screen_x <= Settings().SCREEN_WIDTH // 2 <= screen_x + screen_width
            and screen_y <= Settings().SCREEN_HEIGHT // 2 <= screen_y + screen_height
        )

    @staticmethod
    def _scale_dimensions(width: int | float, height: int | float) -> tuple[int, int]:
        """
        Returns the scaled dimensions of the object based on the spatial dimensions.
        """
        width = Settings().SCREEN_WIDTH if width > Settings().SCREEN_WIDTH else width
        height = (
            Settings().SCREEN_HEIGHT if height > Settings().SCREEN_HEIGHT else height
        )
        return int(width), int(height)
