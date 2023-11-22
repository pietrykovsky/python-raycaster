import math
from typing import TYPE_CHECKING
import pygame

from drawable import Drawable
from settings import Settings
from asset_loader import AssetLoader

if TYPE_CHECKING:
    from raycaster import Raycaster
    from map import Map


class WorldRenderer(Drawable):
    def __init__(self, screen: pygame.Surface, raycaster: "Raycaster", map: "Map"):
        self.screen = screen
        self.raycaster = raycaster
        self.settings = Settings()
        self.wall_textures = AssetLoader().wall_textures
        self.map = map

    def _calculate_shade(
        self, color: tuple[int, int, int], distance
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

    def _draw_column(
        self,
        column: pygame.Surface,
        col: int,
        y_pos: int,
        ray_length: float,
        column_width: int,
    ):
        """
        Draws a column on the screen.
        """
        col_x = col * column_width
        self.screen.blit(column, (col_x, y_pos))

        shade_color = self._calculate_shade((255, 255, 255), ray_length)
        shading_surface = pygame.Surface(column.get_size()).convert_alpha()
        shading_surface.fill(shade_color + (128,))
        self.screen.blit(
            shading_surface, (col_x, y_pos), special_flags=pygame.BLEND_RGBA_MULT
        )

    def _prepare_column(
        self,
        wall_texture: dict[int, pygame.Surface],
        offset: float,
        height: float,
        column_width: int,
    ):
        """
        Prepares a wall texture column for drawing.
        """
        texture_height = wall_texture.get_height()

        if height < self.settings.SCREEN_HEIGHT:
            column = wall_texture.subsurface(offset, 0, 1, texture_height)
            column = pygame.transform.scale(column, (column_width, height))
            y_pos = self.settings.SCREEN_HEIGHT // 2 - height // 2
        else:
            scaled_texture_height = (
                texture_height * self.settings.SCREEN_HEIGHT / height
            )
            column = wall_texture.subsurface(
                offset,
                texture_height / 2 - scaled_texture_height / 2,
                1,
                scaled_texture_height,
            )
            column = pygame.transform.scale(
                column, (column_width, self.settings.SCREEN_HEIGHT)
            )
            y_pos = 0

        return column, y_pos

    def draw(self):
        """
        TODO: Find out why sometimes(very often) screen turns black when player run into wall and fix this.
        """

        self._draw_background()
        screen_dist = self.settings.SCREEN_DISTANCE
        ray_count = self.settings.RAY_COUNT
        column_width = math.ceil(self.settings.SCREEN_WIDTH / ray_count)

        for col, ray in enumerate(self.raycaster.rays):
            if ray.hit_wall:
                if ray.texture_id not in self.wall_textures:
                    raise ValueError(f"Wall texture with id {ray.texture_id} not found")

                wall_texture = self.wall_textures[ray.texture_id]
                height = screen_dist * self.settings.CELL_SIZE / ray.length
                offset = (
                    (ray.x_end % self.settings.CELL_SIZE)
                    if ray.is_horizontal
                    else (ray.y_end % self.settings.CELL_SIZE)
                )
                column, y_pos = self._prepare_column(
                    wall_texture, offset, height, column_width
                )

                self._draw_column(column, col, y_pos, ray.length, column_width)
