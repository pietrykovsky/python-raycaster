from typing import TYPE_CHECKING
import pygame
import math

from settings import Settings
from drawable import Drawable
from object_manager import ObjectManager

if TYPE_CHECKING:
    from player import Player
    from sprite_object import SpriteObject
    from raycaster import Raycaster


class ObjectRenderer(Drawable):
    _instance = None

    def __new__(cls, screen: pygame.Surface, player: "Player", raycaster: "Raycaster"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.player = player
            cls.screen = screen
            cls.raycaster = raycaster
            cls.object_manager = ObjectManager(player)
        return cls._instance

    def draw_object(self, obj: "SpriteObject"):
        """
        TODO:
            - refactor
            - take walls into account (don't draw objects behind walls)
        """
        max_distance = Settings().MAX_DISTANCE
        ray = self.raycaster.cast_ray(obj.angle)
        if (
            ray.hit_wall
            and ray.length < obj.distance
            or obj.distance > max_distance
            or not self.player.in_fov(obj.angle)
        ):
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
        if height <= Settings().SCREEN_HEIGHT and width <= Settings().SCREEN_WIDTH:
            obj_texture_scaled = pygame.transform.scale(
                obj.texture, (int(width), int(height))
            )

        elif height > Settings().SCREEN_HEIGHT and width <= Settings().SCREEN_WIDTH:
            y_offset = height - Settings().SCREEN_HEIGHT
            y_offset = y_offset / height * s_height

            subsurface = obj.texture.subsurface(
                0, y_offset / 2, s_width, s_height - y_offset
            )
            obj_texture_scaled = pygame.transform.scale(
                subsurface, (int(width), Settings().SCREEN_HEIGHT)
            )

            screen_y = 0

        elif width > Settings().SCREEN_WIDTH and height <= Settings().SCREEN_HEIGHT:
            x_offset = width - Settings().SCREEN_WIDTH
            x_offset = x_offset / width * s_width

            subsurface = obj.texture.subsurface(
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

            subsurface = obj.texture.subsurface(
                x_offset / 2, y_offset / 2, s_width - x_offset, s_height - y_offset
            )
            obj_texture_scaled = pygame.transform.scale(
                subsurface, (Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT)
            )

            screen_y = 0
            screen_x = math.tan(rel_angle) * screen_dist

        self.screen.blit(obj_texture_scaled, (int(screen_x), int(screen_y)))

    def draw(self):
        objects = self.object_manager.objects
        for obj in objects:
            self.draw_object(obj)
