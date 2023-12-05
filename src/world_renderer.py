import math
from typing import TYPE_CHECKING
import pygame

from drawable import Drawable
from settings import Settings
from asset_loader import AssetLoader

if TYPE_CHECKING:
    from raycaster import Raycaster
    from map import Map
    from ray import Ray


class WorldRenderer(Drawable):
    def __init__(self, screen: pygame.Surface, raycaster: "Raycaster", map: "Map"):
        self.screen = screen
        self.raycaster = raycaster
        self.settings = Settings()
        self.wall_textures = AssetLoader().wall_textures
        self.map = map

    def _calculate_shade(
        self, color: tuple[int, int, int], distance: float
    ) -> tuple[int, int, int, int]:
        """
        Calculates the shade of the given color based on the distance.

        :param color: color to shade
        :param distance: length of the ray
        :return: shaded color with alpha channel
        """
        if distance <= self.settings.MAX_DISTANCE:
            max_distance = self.settings.MAX_DISTANCE
            shade_factor = (max_distance - distance) / max_distance
            return (
                int(color[0] * shade_factor),
                int(color[1] * shade_factor),
                int(color[2] * shade_factor),
            )
        return 0, 0, 0, 128

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

    def _shade_wall(
        self,
        column: pygame.Surface,
        position: tuple[int, int],
        shade_color: tuple[int, int, int, int],
    ):
        """
        Shades the column surface.

        :param column: Wall column surface
        :param position: Position of the column on the screen
        :param shade_color: Color to shade the column with in RGBA format
        """
        shading_surface = pygame.Surface(column.get_size()).convert_alpha()
        shading_surface.fill(shade_color)
        self.screen.blit(
            shading_surface, position, special_flags=pygame.BLEND_RGBA_MULT
        )

    def _draw_wall(self, ray: "Ray", ray_number: int):
        """
        Draws a wall on the screen.

        :param ray: Ray dataclass instance
        :param ray_number: number of the ray
        """
        screen_dist = self.settings.SCREEN_DISTANCE
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
            y_offset = height - Settings().SCREEN_HEIGHT
            y_offset = y_offset / height * Settings().CELL_SIZE
            column = wall_texture.subsurface(
                x_offset, y_offset / 2, 1, Settings().CELL_SIZE - y_offset
            )
            column = pygame.transform.scale(
                column, (column_width, self.settings.SCREEN_HEIGHT)
            )
            y_pos = 0

        x_pos = ray_number * column_width
        self.screen.blit(column, (x_pos, y_pos))

        shade_color = self._calculate_shade((255, 255, 255), ray.length)
        self._shade_wall(column, (x_pos, y_pos), shade_color)

    def _draw_walls(self):
        for col, ray in enumerate(self.raycaster.rays):
            if not ray.hit_wall:
                continue
            if ray.texture_id not in self.wall_textures:
                raise ValueError(f"Wall texture with id {ray.texture_id} not found")

            self._draw_wall(ray, col)

    def draw(self):
        """
        TODO: Find out why sometimes(very often) screen turns black when player run into wall and fix this.
        (objection: isn't it because of the player's falling into the wall? perhaps we should check wall hitbox)
        """
        self._draw_background()
        self._draw_walls()
