from typing import TYPE_CHECKING
import pygame

from raycaster.core import Settings
from raycaster.utils import calculate_shade_factor, shade_surface
from raycaster.rendering.sprite_projection_processor import SpriteProjectionProcessor

if TYPE_CHECKING:
    from raycaster.game import Player
    from raycaster.objects import SpriteObject


class ObjectRenderer:
    _instance = None

    def __new__(cls, screen: pygame.Surface, player: "Player"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.player = player
            cls.screen = screen
        return cls._instance

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
        (
            spatial_width,
            spatial_height,
        ) = SpriteProjectionProcessor.get_spatial_dimensions(obj)

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

    def draw(self, obj: "SpriteObject"):
        """
        Draws the object on the screen.

        :param obj: Object to draw
        """
        if not self._can_be_drawn(obj):
            return

        (
            spatial_width,
            spatial_height,
        ) = SpriteProjectionProcessor.get_spatial_dimensions(obj)
        sprite = obj.texture.copy()

        if obj.shaded:
            shade_factor = calculate_shade_factor(obj.distance)
            shade_surface(sprite, shade_factor)

        if not SpriteProjectionProcessor.smaller_than_screen(
            spatial_width, spatial_height
        ):
            sprite = self._get_subsurface(obj, sprite)

        width, height = SpriteProjectionProcessor.get_screen_dimensions(obj)
        scaled_texture = pygame.transform.scale(sprite, (width, height))
        screen_x, screen_y = SpriteProjectionProcessor.get_screen_position(obj)
        self.screen.blit(scaled_texture, (screen_x, screen_y))

    def _can_be_drawn(self, obj: "SpriteObject") -> bool:
        """
        Checks if the object can be drawn on the screen.

        :param obj: Object to check
        :return: True if the object can be drawn, False otherwise
        """
        return (
            obj.distance <= Settings().MAX_DISTANCE
            and self.player.in_fov(obj.angle)
            and obj.distance > 0
        )
