import math
from typing import TYPE_CHECKING
import pygame

from updatable import Updatable
from drawable import Drawable


if TYPE_CHECKING:
    from game import Game


class Raycaster(Updatable, Drawable):
    def __init__(self, game: "Game"):
        self.game = game

    def update(self):
        pass

    def draw(self):
        player_x, player_y = self.game.player.x, self.game.player.y
        player_angle = self.game.player.angle
        player_fov = self.game.player.fov
        for ray in range(player_fov):
            angle = math.degrees(player_angle) - player_fov / 2 + ray
            ray_x, ray_y = self._calculate_ray_endpoint(angle)
            pygame.draw.line(
                self.game.screen,
                "yellow",
                (player_x, player_y),
                (
                    ray_x,
                    ray_y,
                ),
                2,
            )

    def _calculate_ray_endpoint(self, angle: float) -> tuple[int, int]:
        # kąt w radianach i krok dla DDA
        ray_angle = math.radians(angle)
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # DDA initialization
        x = self.game.player.x
        y = self.game.player.y
        while True:
            if not self.game.map.is_wall(
                int(x / self.game.map.cell_width), int(y / self.game.map.cell_height)
            ):
                return x, y

            x += cos_a
            y += sin_a
