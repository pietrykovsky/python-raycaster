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
        """
        TODO:
            - refactor
            - fix column height
            - add texture handling
        """
        player_angle = self.game.player.angle
        fov = self.game.settings.FOV
        ray_count = self.game.settings.RAY_COUNT
        angle_offset = self.game.settings.DELTA_ANGLE
        screen_dist = self.game.settings.SCREEN_DISTANCE
        for ray in range(ray_count + 1):
            angle = (
                math.degrees(player_angle)
                - (fov // 2)
                + (ray * math.degrees(angle_offset))
            )
            angle = math.radians(angle) % (2 * math.pi)
            ray_length, is_horizontal = self._cast_ray(angle)
            height = screen_dist * self.game.settings.CELL_SIZE / ray_length
            color = self._calculate_shade((0, 0, 255), ray_length)
            if ray_length != float("inf"):
                col_scale = self.game.settings.SCREEN_WIDTH / ray_count
                pygame.draw.rect(
                    self.game.screen,
                    color,
                    (
                        math.ceil(ray * col_scale),
                        self.game.settings.SCREEN_HEIGHT // 2 - height // 2,
                        math.ceil(col_scale),
                        height,
                    ),
                )

    def _calculate_shade(
        self, color: tuple[int, int, int], distance: float
    ) -> tuple[int, int, int]:
        max_distance = self.game.settings.MAX_DISTANCE
        if distance != float("inf"):
            shade_factor = (max_distance - distance) / max_distance
            return (
                int(color[0] * shade_factor),
                int(color[1] * shade_factor),
                int(color[2] * shade_factor),
            )
        return color

    def _cast_ray(self, angle: float) -> tuple[float, bool]:
        """
        TODO:
            - refactor
        """
        cell_size = self.game.settings.CELL_SIZE
        player_x, player_y = self.game.player.x, self.game.player.y
        player_angle = self.game.player.angle

        tan_a = math.tan(angle)
        epsilon = 0.0001

        up = math.sin(angle) > 0
        right = math.cos(angle) < 0

        # Handle near-horizontal angles
        if abs(tan_a) < epsilon:
            tan_a = epsilon if tan_a >= 0 else -epsilon

        # Check horizontal intersection
        horizontal_distance = float("inf")
        # horizontal_intersection = 0, 0
        if tan_a != 0:
            y_n = -(player_y - (player_y // cell_size) * cell_size)
            y_n = cell_size + y_n if up else y_n
            x_n = y_n / tan_a

            y_step = -cell_size if not up else cell_size
            x_step = y_step / tan_a

            x = player_x + x_n
            y = player_y + y_n

            while True:
                map_x = int(x // cell_size)
                map_y = int(y // cell_size) - 1 if not up else int(y // cell_size)

                if (
                    map_x < 0
                    or map_x >= self.game.map.cols
                    or map_y < 0
                    or map_y >= self.game.map.rows
                ):
                    break

                if (
                    math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
                    >= self.game.settings.MAX_DISTANCE
                ):
                    break

                if self.game.map.is_wall(map_x, map_y):
                    horizontal_distance = math.sqrt(
                        (x - player_x) ** 2 + (y - player_y) ** 2
                    )
                    # horizontal_intersection = x, y
                    break

                x += x_step
                y += y_step

        # Check vertical intersection
        vertical_distance = float("inf")
        # vertical_intersection = 0, 0
        if tan_a != 1:
            x_n = -(player_x - (player_x // cell_size) * cell_size)
            x_n = cell_size + x_n if not right else x_n
            y_n = x_n * tan_a

            x_step = cell_size if not right else -cell_size
            y_step = x_step * tan_a

            x = player_x + x_n
            y = player_y + y_n

            while True:
                map_x = int(x // cell_size) - 1 if right else int(x // cell_size)
                map_y = int(y // cell_size)

                if (
                    map_x < 0
                    or map_x >= self.game.map.cols
                    or map_y < 0
                    or map_y >= self.game.map.rows
                ):
                    break

                if (
                    math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
                    >= self.game.settings.MAX_DISTANCE
                ):
                    break

                if self.game.map.is_wall(map_x, map_y):
                    vertical_distance = math.sqrt(
                        (x - player_x) ** 2 + (y - player_y) ** 2
                    )
                    # vertical_intersection = x, y
                    break

                x += x_step
                y += y_step

        angle_diff = angle - player_angle
        # Normalize angle_diff to be within -pi to pi
        angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi
        horizontal_distance *= math.cos(angle_diff)
        vertical_distance *= math.cos(angle_diff)
        if horizontal_distance < vertical_distance:
            return horizontal_distance, True
            # return horizontal_intersection
        return vertical_distance, False
        # return vertical_intersection
