from typing import TYPE_CHECKING
import pygame
import math

from settings import Settings
from object_manager import ObjectManager
from utils import calculate_shade_factor, shade_surface

if TYPE_CHECKING:
    from player import Player
    from sprite_object import SpriteObject


class ObjectRenderer:
    _instance = None

    def __new__(cls, screen: pygame.Surface, player: "Player"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.player = player
            cls.screen = screen
            cls.object_manager = ObjectManager(player)
        return cls._instance

    def _calculate_spatial_dimensions(self, obj: "SpriteObject") -> tuple[int, int]:
        """
        Calculates the dimensions of the object based on object distance.

        :param obj: Object to calculate dimensions for
        :return: Object's spatial dimensions
        """
        screen_dist = Settings().SCREEN_DISTANCE
        texture_width, texture_height = obj.texture.get_size()
        height = screen_dist * texture_height / obj.distance
        width = screen_dist * texture_width / obj.distance
        return int(width), int(height)

    def _calculate_position_on_screen(self, obj: "SpriteObject") -> tuple[int, int]:
        """
        Calculates the position of the object on the screen.

        :param obj: Object to calculate position for
        :return: Object's position on the screen
        """
        screen_dist = Settings().SCREEN_DISTANCE
        rel_angle = obj.angle - self.player.angle - math.pi
        spatial_width, spatial_height = self._calculate_spatial_dimensions(obj)
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

    def _smaller_than_screen(self, width: float | int, height: float | int) -> bool:
        """
        Checks if the dimensions are smaller than the screen.
        """
        return height <= Settings().SCREEN_HEIGHT and width <= Settings().SCREEN_WIDTH

    def _get_subsurface(
        self, obj: "SpriteObject", sprite: pygame.Surface
    ) -> pygame.Surface:
        """
        Returns a subsurface of the given sprite based on the spatial dimensions of the object.

        :param obj: Object to calculate subsurface for
        :param sprite: Sprite to calculate subsurface from
        :return: Subsurface of the sprite
        """
        texture_width, texture_height = obj.texture.get_size()
        spatial_width, spatial_height = self._calculate_spatial_dimensions(obj)

        if spatial_width > Settings().SCREEN_WIDTH:
            x_offset = (
                (spatial_width - Settings().SCREEN_WIDTH)
                / spatial_width
                * texture_width
            )
            x_start = x_offset / 2
            surface_width = texture_width - x_offset
        else:
            x_start = 0
            surface_width = texture_width

        if spatial_height > Settings().SCREEN_HEIGHT:
            y_offset = (
                (spatial_height - Settings().SCREEN_HEIGHT)
                / spatial_height
                * texture_height
            )
            y_start = y_offset / 2
            surface_height = texture_height - y_offset
        else:
            y_start = 0
            surface_height = texture_height

        return sprite.subsurface(x_start, y_start, surface_width, surface_height)

    def _get_scaling_dimensions(
        self, width: int | float, height: int | float
    ) -> tuple[int, int]:
        """
        Returns the scaled dimensions of the object based on the spatial dimensions.
        """
        width = Settings().SCREEN_WIDTH if width > Settings().SCREEN_WIDTH else width
        height = (
            Settings().SCREEN_HEIGHT if height > Settings().SCREEN_HEIGHT else height
        )
        return int(width), int(height)

    def draw(self, obj: "SpriteObject"):
        """
        Draws the object on the screen.

        :param obj: Object to draw
        """
        max_distance = Settings().MAX_DISTANCE
        if obj.distance > max_distance or not self.player.in_fov(obj.angle):
            return
        spatial_width, spatial_height = self._calculate_spatial_dimensions(obj)
        sprite = obj.texture.copy()

        if obj.shaded:
            shade_factor = calculate_shade_factor(obj.distance)
            shade_surface(sprite, shade_factor)

        if self._smaller_than_screen(spatial_width, spatial_height):
            obj_texture_scaled = pygame.transform.scale(
                sprite, (spatial_width, spatial_height)
            )
        else:
            subsurface = self._get_subsurface(obj, sprite)
            scaled_width, scaled_height = self._get_scaling_dimensions(
                spatial_width, spatial_height
            )
            obj_texture_scaled = pygame.transform.scale(
                subsurface, (scaled_width, scaled_height)
            )

        screen_x, screen_y = self._calculate_position_on_screen(obj)
        self.screen.blit(obj_texture_scaled, (screen_x, screen_y))
