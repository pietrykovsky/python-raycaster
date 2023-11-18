import math
from typing import TYPE_CHECKING
import pygame

from drawable import Drawable
from settings import Settings

if TYPE_CHECKING:
    from raycaster import Raycaster


class Renderer(Drawable):
    def __init__(self, screen: pygame.Surface, raycaster: "Raycaster"):
        self.screen = screen
        self.raycaster = raycaster
        self.settings = Settings()

    def _calculate_shade(
        self, color: tuple[int, int, int], distance: float
    ) -> tuple[int, int, int]:
        if distance != float("inf"):
            max_distance = self.settings.MAX_DISTANCE
            shade_factor = (max_distance - distance) / max_distance
            return (
                int(color[0] * shade_factor),
                int(color[1] * shade_factor),
                int(color[2] * shade_factor),
            )
        return color

    def draw(self):
        screen_dist = self.settings.SCREEN_DISTANCE
        ray_count = self.settings.RAY_COUNT
        rays = self.raycaster.rays
        for col, ray in enumerate(rays):
            if ray.hit_wall:
                height = screen_dist * self.settings.CELL_SIZE / ray.length
                color = self._calculate_shade((0, 0, 255), ray.length)
                col_scale = self.settings.SCREEN_WIDTH / ray_count
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        math.ceil(col * col_scale),
                        self.settings.SCREEN_HEIGHT // 2 - height // 2,
                        math.ceil(col_scale),
                        height,
                    ),
                )
