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

    def draw(self, obj: "SpriteObject"):
        """
        TODO: refactor
        """
        max_distance = Settings().MAX_DISTANCE
        if obj.distance > max_distance or not self.player.in_fov(obj.angle):
            return
        s_width, s_height = obj.texture.get_size()
        screen_dist = Settings().SCREEN_DISTANCE
        height = screen_dist * s_height / obj.distance
        width = screen_dist * s_width / obj.distance
        rel_angle = obj.angle - self.player.angle - math.pi
        screen_y = Settings().SCREEN_HEIGHT // 2 - height // 2
        screen_x = (
            math.tan(rel_angle) * screen_dist
            + Settings().SCREEN_WIDTH // 2
            - width // 2
        )
        sprite = obj.texture.copy()

        if obj.shaded:
            shade = calculate_shade_factor(obj.distance)
            shade_surface(
                sprite, shade
            )

        if height <= Settings().SCREEN_HEIGHT and width <= Settings().SCREEN_WIDTH:
            obj_texture_scaled = pygame.transform.scale(
                sprite, (int(width), int(height))
            )

        elif height > Settings().SCREEN_HEIGHT and width <= Settings().SCREEN_WIDTH:
            y_offset = height - Settings().SCREEN_HEIGHT
            y_offset = y_offset / height * s_height

            subsurface = sprite.subsurface(
                0, y_offset / 2, s_width, s_height - y_offset
            )
            obj_texture_scaled = pygame.transform.scale(
                subsurface, (int(width), Settings().SCREEN_HEIGHT)
            )

            screen_y = 0

        elif width > Settings().SCREEN_WIDTH and height <= Settings().SCREEN_HEIGHT:
            x_offset = width - Settings().SCREEN_WIDTH
            x_offset = x_offset / width * s_width

            subsurface = sprite.subsurface(
                x_offset / 2, 0, s_width - y_offset, height
            )
            obj_texture_scaled = pygame.transform.scale(
                subsurface, (Settings().SCREEN_WIDTH, int(height))
            )

            screen_x = math.tan(rel_angle) * screen_dist

        else:
            x_offset = width - Settings().SCREEN_WIDTH
            x_offset = x_offset / width * s_width
            y_offset = height - Settings().SCREEN_HEIGHT
            y_offset = y_offset / height * s_height

            subsurface = sprite.subsurface(
                x_offset / 2, y_offset / 2, s_width - x_offset, s_height - y_offset
            )
            obj_texture_scaled = pygame.transform.scale(
                subsurface, (Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT)
            )

            screen_y = 0
            screen_x = math.tan(rel_angle) * screen_dist

        self.screen.blit(obj_texture_scaled, (int(screen_x), int(screen_y)))
