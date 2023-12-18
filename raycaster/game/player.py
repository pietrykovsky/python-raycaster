import math
from typing import TYPE_CHECKING
import pygame

from raycaster.core import Updatable, Settings, Event

if TYPE_CHECKING:
    from raycaster.game.map import Map


class Player(Updatable):
    def __init__(self, clock: pygame.time.Clock, map: "Map"):
        self.map = map
        self.settings = Settings()
        self.clock = clock
        self.speed = self.settings.PLAYER_SPEED
        self.sensitivity = self.settings.PLAYER_SENSITIVITY
        self.x = 3.5 * self.settings.CELL_SIZE
        self.y = 3.5 * self.settings.CELL_SIZE
        self.angle = 0
        self.delta_time = 1

        self.weapon = None
        self.shoot_handler = Event()
        self.shoot_handler += self._shoot

    def handle_movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = self.speed * self.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        num_key_pressed = -1
        if keys[pygame.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos

        # diagonal move correction
        if num_key_pressed:
            dx *= 1 / math.sqrt(2)
            dy *= 1 / math.sqrt(2)

        self.check_wall_collision(dx, dy)

    def in_fov(self, angle: float) -> bool:
        """
        Checks if the given angle is in the player's field of view.

        :param angle: angle in radians
        :return: True if the angle is in the player's field of view, False otherwise
        """
        player_dir = math.degrees(self.angle) % 360
        angle_deg = math.degrees(angle) % 360

        fov_start = (player_dir - self.settings.FOV / 2) % 360
        fov_end = (player_dir + self.settings.FOV / 2) % 360

        if fov_start < fov_end:
            return fov_start <= angle_deg <= fov_end
        return angle_deg >= fov_start or angle_deg <= fov_end

    def check_wall_collision(self, dx: int, dy: int):
        if not self.map.is_wall(
            int((self.x + dx) / self.settings.CELL_SIZE),
            int(self.y / self.settings.CELL_SIZE),
        ):
            self.x += dx
        if not self.map.is_wall(
            int(self.x / self.settings.CELL_SIZE),
            int((self.y + dy) / self.settings.CELL_SIZE),
        ):
            self.y += dy

    def handle_camera(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= self.sensitivity * self.delta_time
            self.angle = self.angle % (2 * math.pi)
        if keys[pygame.K_RIGHT]:
            self.angle += self.sensitivity * self.delta_time
            self.angle = self.angle % (2 * math.pi)

    def _shoot(self):
        if self.weapon is not None and self.weapon.can_shoot():
            self.weapon.shoot()

    def update(self):
        self.delta_time = self.clock.get_time()
        self.handle_movement()
        self.handle_camera()
