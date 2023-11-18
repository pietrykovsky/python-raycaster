import math
from typing import TYPE_CHECKING

from updatable import Updatable
from ray import Ray
from settings import Settings


if TYPE_CHECKING:
    from player import Player
    from map import Map


class Raycaster(Updatable):
    def __init__(self, map: "Map", player: "Player"):
        self.map = map
        self.player = player
        self.settings = Settings()
        self._rays = []

    @property
    def rays(self) -> list[Ray]:
        return self._rays

    def update(self):
        player_angle = self.player.angle
        fov = self.settings.FOV
        ray_count = self.settings.RAY_COUNT
        angle_offset = self.settings.DELTA_ANGLE
        self.rays.clear()
        for ray in range(ray_count + 1):
            angle = (
                math.degrees(player_angle)
                - (fov // 2)
                + (ray * math.degrees(angle_offset))
            )
            angle = math.radians(angle) % (2 * math.pi)
            self._rays.append(self._cast_ray(angle))

    def _cast_ray(self, angle: float) -> Ray:
        cell_size = self.settings.CELL_SIZE
        max_distance = self.settings.MAX_DISTANCE
        player_x, player_y = self.player.x, self.player.y
        player_angle = self.player.angle
        angle_diff = angle - player_angle
        angle_diff = (angle_diff + math.pi) % (
            2 * math.pi
        ) - math.pi  # Normalize angle_diff to be within -pi to pi

        tan_a = math.tan(angle)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        epsilon = 0.0001

        up = sin_a > 0
        right = cos_a < 0

        # Handle near-horizontal angles
        if abs(tan_a) < epsilon:
            tan_a = epsilon if tan_a >= 0 else -epsilon

        # Check horizontal intersection
        horizontal_ray = Ray(
            player_x,
            player_y,
            player_x + max_distance * cos_a,
            player_y + max_distance * sin_a,
        )
        if tan_a != 0:
            y_n = -(player_y - (player_y // cell_size) * cell_size)
            y_n = cell_size + y_n if up else y_n
            x_n = y_n / tan_a

            y_step = -cell_size if not up else cell_size
            x_step = y_step / tan_a

            x = player_x + x_n
            y = player_y + y_n

            while True:
                distance = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
                map_x = int(x // cell_size)
                map_y = int(y // cell_size) - 1 if not up else int(y // cell_size)

                if (
                    self.map.is_out_of_bounds(map_x, map_y)
                    or distance >= horizontal_ray.length
                ):
                    break

                if self.map.is_wall(map_x, map_y):
                    horizontal_ray.hit_wall = True
                    horizontal_ray.length = distance * math.cos(angle_diff)
                    horizontal_ray.x_end = x
                    horizontal_ray.y_end = y
                    break

                x += x_step
                y += y_step

        # Check vertical intersection
        vertical_ray = Ray(
            player_x,
            player_y,
            player_x + max_distance * cos_a,
            player_y + max_distance * sin_a,
        )
        if tan_a != 1:
            x_n = -(player_x - (player_x // cell_size) * cell_size)
            x_n = cell_size + x_n if not right else x_n
            y_n = x_n * tan_a

            x_step = cell_size if not right else -cell_size
            y_step = x_step * tan_a

            x = player_x + x_n
            y = player_y + y_n

            while True:
                distance = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
                map_x = int(x // cell_size) - 1 if right else int(x // cell_size)
                map_y = int(y // cell_size)

                if (
                    self.map.is_out_of_bounds(map_x, map_y)
                    or distance >= vertical_ray.length
                ):
                    break

                if self.map.is_wall(map_x, map_y):
                    vertical_ray.hit_wall = True
                    vertical_ray.length = distance * math.cos(angle_diff)
                    vertical_ray.x_end = x
                    vertical_ray.y_end = y
                    break

                x += x_step
                y += y_step

        if horizontal_ray.length < vertical_ray.length:
            return horizontal_ray
        return vertical_ray
