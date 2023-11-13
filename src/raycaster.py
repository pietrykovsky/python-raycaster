import math
from typing import TYPE_CHECKING
import pygame

from drawable import Drawable


if TYPE_CHECKING:
    from game import Game


class Raycaster(Drawable):
    def __init__(self, game: "Game"):
        self.game = game

    def draw(self):
        player_x, player_y = self.game.player.x, self.game.player.y
        player_angle = self.game.player.angle
        player_fov = self.game.player.fov
        for ray in range(player_fov):
            angle = (math.degrees(player_angle) - player_fov / 2) + ray
            angle = math.radians(angle) % (2 * math.pi)
            print(player_angle)
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
        cell_height = self.game.map.cell_height
        cell_width = self.game.map.cell_width
        player_x, player_y = self.game.player.x, self.game.player.y

        tan_a = math.tan(angle)

        up = not (0 < angle < math.pi)
        right = not (math.pi / 2 < angle < 3 * math.pi / 2)

        DEPTH = 10

        # Check horizontal intersection
        horizontal_distance = 0
        horizontal_intersection = 0, 0
        has_horizontal_intersection = False
        if tan_a != 0:
            y_n = -(player_y - (player_y // cell_height) * cell_height)
            y_n = cell_height + y_n if not up else y_n
            x_n = y_n / tan_a

            y_step = -cell_height if up else cell_height
            x_step = y_step / tan_a

            x = player_x + x_n
            y = player_y + y_n

            for _ in range(DEPTH + 1):
                map_x = int(x // cell_width)
                map_y = int(y // cell_height) - 1

                if not up:
                    map_y += 1

                if self.game.map.is_wall(map_x, map_y):
                    has_horizontal_intersection = True
                    horizontal_distance = math.sqrt(
                        (x - player_x) ** 2 + (y - player_y) ** 2
                    )
                    horizontal_intersection = x, y
                    break

                x += x_step
                y += y_step

        # Check vertical intersection
        vertical_distance = 0
        vertical_intersection = player_x, player_y
        has_vertical_intersection = False
        if tan_a != 1:
            x_n = -(player_x - (player_x // cell_width) * cell_width)
            x_n = cell_width + x_n if right else x_n
            y_n = x_n * tan_a

            x_step = cell_width if right else -cell_width
            y_step = x_step * tan_a

            x = player_x + x_n
            y = player_y + y_n

            for _ in range(DEPTH + 1):
                map_x = int(x // cell_width) - 1
                map_y = int(y // cell_height)

                if right:
                    map_x += 1

                if self.game.map.is_wall(map_x, map_y):
                    has_vertical_intersection = True
                    vertical_distance = math.sqrt(
                        (x - player_x) ** 2 + (y - player_y) ** 2
                    )
                    vertical_intersection = x, y
                    break

                x += x_step
                y += y_step

        if has_horizontal_intersection and not has_vertical_intersection:
            return horizontal_intersection
        elif has_vertical_intersection and not has_horizontal_intersection:
            return vertical_intersection
        else:
            if horizontal_distance < vertical_distance:
                return horizontal_intersection
            return vertical_intersection
