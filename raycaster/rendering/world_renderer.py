import math
from typing import TYPE_CHECKING
import pygame

from raycaster.core import Drawable, Settings
from raycaster.game import AssetLoader
from raycaster.objects import ObjectManager, SpriteObject
from raycaster.rendering.object_renderer import ObjectRenderer
from raycaster.utils import calculate_shade_factor, shade_surface
from raycaster.rendering.ray import Ray
from raycaster import const


if TYPE_CHECKING:
    from raycaster.rendering.raycaster import Raycaster
    from raycaster.game import Map, Player


class WorldRenderer(Drawable):
    def __init__(
        self,
        screen: pygame.Surface,
        raycaster: "Raycaster",
        map: "Map",
        player: "Player",
    ):
        self.screen = screen
        self.raycaster = raycaster
        self.player = player
        self.settings = Settings()
        self.wall_textures = AssetLoader().wall_textures
        self.map = map

    def _draw_background(self):
        """
        Draws the background with gradient shading in the centre.
        """
        for row in range(self.settings.SCREEN_HEIGHT // 2):
            shade_factor = (
                (self.settings.SCREEN_HEIGHT // 2 - row)
                / (self.settings.SCREEN_HEIGHT // 2)
            ) ** 2
            pygame.draw.line(
                self.screen,
                (
                    int(50) * shade_factor,
                    int(50) * shade_factor,
                    int(50) * shade_factor,
                ),
                (0, row),
                (self.settings.SCREEN_WIDTH, row),
                1,
            )
        for row in range(self.settings.SCREEN_HEIGHT // 2, self.settings.SCREEN_HEIGHT):
            shade_factor = (
                (row - self.settings.SCREEN_HEIGHT // 2)
                / (self.settings.SCREEN_HEIGHT // 2)
            ) ** 2
            pygame.draw.line(
                self.screen,
                (
                    int(30) * shade_factor,
                    int(30) * shade_factor,
                    int(30) * shade_factor,
                ),
                (0, row),
                (self.settings.SCREEN_WIDTH, row),
                1,
            )

    def _draw_wall(self, ray: "Ray"):
        """
        Draws a wall on the screen.

        :param ray: Ray dataclass instance
        :param ray_number: number of the ray
        """
        if not ray.hit_wall:
            return
        if ray.texture_id not in self.wall_textures:
            raise ValueError(f"Wall texture with id {ray.texture_id} not found")

        screen_dist = const.SCREEN_DISTANCE
        ray_count = self.settings.RAY_COUNT
        column_width = math.ceil(self.settings.SCREEN_WIDTH / ray_count)

        wall_texture = self.wall_textures[ray.texture_id]

        height = screen_dist * self.settings.CELL_SIZE / ray.length
        x_offset = (
            (ray.x_end % self.settings.CELL_SIZE)
            if ray.is_horizontal
            else (ray.y_end % self.settings.CELL_SIZE)
        )
        texture_height = wall_texture.get_height()

        if height <= self.settings.SCREEN_HEIGHT:
            column = wall_texture.subsurface(x_offset, 0, 1, texture_height)
            column = pygame.transform.scale(column, (column_width, height))
            y_pos = self.settings.SCREEN_HEIGHT / 2 - height / 2
        else:
            y_offset = height - self.settings.SCREEN_HEIGHT
            y_offset = y_offset / height * self.settings.CELL_SIZE
            column = wall_texture.subsurface(
                x_offset, y_offset / 2, 1, self.settings.CELL_SIZE - y_offset
            )
            column = pygame.transform.scale(
                column, (column_width, self.settings.SCREEN_HEIGHT)
            )
            y_pos = 0

        shade = calculate_shade_factor(ray.length)
        shade_surface(column, shade)
        x_pos = ray.index * column_width
        self.screen.blit(column, (x_pos, y_pos))

    def _draw_world(self):
        object_renderer = ObjectRenderer(screen=self.screen, player=self.player)
        object_manager = ObjectManager(player=self.player)
        objects = [
            *[ray for ray in self.raycaster.rays if ray.hit_wall],
            *object_manager.objects,
            *object_manager.enemies,
        ]
        objects.sort(
            key=lambda obj: obj.distance
            if isinstance(obj, SpriteObject)
            else obj.length,
            reverse=True,
        )

        for obj in objects:
            if isinstance(obj, Ray):
                self._draw_wall(obj)
            else:
                object_renderer.draw(obj)

    def draw(self):
        """
        TODO: Find out why sometimes(very often) screen turns black when player run into wall and fix this.
        (objection: isn't it because of the player's falling into the wall? perhaps we should check wall hitbox)
        """
        self._draw_background()
        self._draw_world()
