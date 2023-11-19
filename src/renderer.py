import math
from typing import TYPE_CHECKING
import pygame

from drawable import Drawable
from settings import Settings
from asset_loader import AssetLoader

if TYPE_CHECKING:
    from raycaster import Raycaster
    from map import Map


class Renderer(Drawable):
    def __init__(self, screen: pygame.Surface, raycaster: "Raycaster", map: "Map"):
        self.screen = screen
        self.raycaster = raycaster
        self.settings = Settings()
        self.wall_textures = AssetLoader().wall_textures
        self.map = map

    def _calculate_shade(
        self, color: tuple[int, int, int], distance: float
    ) -> tuple[int, int, int]:
        """
        Calculates the shade of the given color based on the distance.

        :param color: color to shade
        :param distance: length of the ray
        :return: shaded color
        """
        if distance <= self.settings.MAX_DISTANCE:
            max_distance = self.settings.MAX_DISTANCE
            shade_factor = (max_distance - distance) / max_distance
            return (
                int(color[0] * shade_factor),
                int(color[1] * shade_factor),
                int(color[2] * shade_factor),
            )
        return 0, 0, 0

    def _draw_background(self):
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

    def draw(self):
        self._draw_background()
        screen_dist = self.settings.SCREEN_DISTANCE
        ray_count = self.settings.RAY_COUNT
        rays = self.raycaster.rays
        for col, ray in enumerate(rays):
            if ray.hit_wall:
                if ray.texture_id not in self.wall_textures:
                    raise ValueError(f"Wall texture with id {ray.texture_id} not found")
                wall_texture = self.wall_textures[ray.texture_id]
                height = screen_dist * self.settings.CELL_SIZE / ray.length
                column_width = self.settings.SCREEN_WIDTH / ray_count
                texture_height = wall_texture.get_height()
                offset = (
                    ray.x_end % self.settings.CELL_SIZE
                    if ray.is_horizontal
                    else ray.y_end % self.settings.CELL_SIZE
                )

                column = wall_texture.subsurface(offset, 0, 1, texture_height)
                column = pygame.transform.scale(
                    column, (math.ceil(column_width), math.ceil(height))
                )
                self.screen.blit(
                    column,
                    (
                        math.ceil(col * column_width),
                        self.settings.SCREEN_HEIGHT // 2 - height // 2,
                    ),
                )
                shade_color = self._calculate_shade((255, 255, 255), ray.length)
                shading_surface = pygame.Surface(column.get_size()).convert_alpha()
                shading_surface.fill(shade_color + (128,))
                self.screen.blit(
                    shading_surface,
                    (
                        math.ceil(col * column_width),
                        self.settings.SCREEN_HEIGHT // 2 - height // 2,
                    ),
                    special_flags=pygame.BLEND_RGBA_MULT,
                )
