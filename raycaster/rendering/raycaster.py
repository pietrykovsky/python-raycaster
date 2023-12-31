import math
from typing import TYPE_CHECKING

from raycaster.core import Updatable, Settings
from raycaster.rendering.ray import Ray
from raycaster.utils import calculate_distance
from raycaster import const

if TYPE_CHECKING:
    from raycaster.game import Player, Map


class Raycaster(Updatable):
    def __init__(self, map: "Map", player: "Player"):
        self.map = map
        self.player = player
        self.settings = Settings()
        self._rays = []

    @property
    def rays(self) -> list[Ray]:
        """
        Gets the list of rays casted by the raycaster.

        :return: List of rays
        """
        return self._rays

    def update(self):
        player_angle = self.player.angle
        fov = self.settings.FOV
        ray_count = self.settings.RAY_COUNT
        angle_offset = const.DELTA_ANGLE
        self.rays.clear()
        for ray_number in range(ray_count + 1):
            angle = (
                math.degrees(player_angle)
                - (fov // 2)
                + (ray_number * math.degrees(angle_offset))
            )
            angle = math.radians(angle) % (2 * math.pi)
            ray = self.cast_ray(angle)
            ray.index = ray_number
            self._rays.append(ray)

    def cast_ray(self, angle: float) -> Ray:
        """
        Casts a ray from the player's position at the given angle.

        :param angle: angle in radians from 0 to 2pi
        :return: Returns information about the casted ray
        """
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

        x_max = player_x + max_distance * cos_a
        y_max = player_y + max_distance * sin_a

        up = sin_a > 0
        right = cos_a < 0

        # Handle near-horizontal angles
        if abs(tan_a) < epsilon:
            tan_a = epsilon if tan_a >= 0 else -epsilon

        # Helper functions
        def _map_coords(x: float, y: float, horizontal: bool = True) -> tuple[int, int]:
            """
            Map x, y values to the map grid.
            """
            if horizontal:
                return int(x // cell_size), int(y // cell_size) - 1 if not up else int(
                    y // cell_size
                )
            return int(x // cell_size) - 1 if right else int(x // cell_size), int(
                y // cell_size
            )

        def _check_intersections(ray: Ray, x: float, y: float, horizontal: bool):
            """Check for intersections with walls."""
            distance = calculate_distance(x, y, player_x, player_y)
            map_x, map_y = _map_coords(x, y, horizontal)
            while distance <= max_distance and not self.map.is_out_of_bounds(
                map_x, map_y
            ):
                if self.map.is_wall(map_x, map_y):
                    ray.hit_wall = True
                    ray.length = distance * math.cos(angle_diff)
                    ray.texture_id = self.map.level[map_y][map_x]
                    ray.is_horizontal = horizontal
                    ray.x_end = x
                    ray.y_end = y
                    break

                x += x_step
                y += y_step
                distance = calculate_distance(x, y, player_x, player_y)
                map_x, map_y = _map_coords(x, y, horizontal)

        # Check horizontal intersection
        horizontal_ray = Ray(player_x, player_y, x_max, y_max)
        if tan_a != 0:
            y_n = -(player_y - (player_y // cell_size) * cell_size)
            y_n = cell_size + y_n if up else y_n
            x_n = y_n / tan_a

            y_step = -cell_size if not up else cell_size
            x_step = y_step / tan_a

            x = player_x + x_n
            y = player_y + y_n

            _check_intersections(horizontal_ray, x, y, horizontal=True)

        # Check vertical intersection
        vertical_ray = Ray(player_x, player_y, x_max, y_max)
        if tan_a != 1:
            x_n = -(player_x - (player_x // cell_size) * cell_size)
            x_n = cell_size + x_n if not right else x_n
            y_n = x_n * tan_a

            x_step = cell_size if not right else -cell_size
            y_step = x_step * tan_a

            x = player_x + x_n
            y = player_y + y_n

            _check_intersections(vertical_ray, x, y, horizontal=False)

        if horizontal_ray.length < vertical_ray.length:
            return horizontal_ray
        return vertical_ray
