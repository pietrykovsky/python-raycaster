import math
from typing import TYPE_CHECKING
import pygame

from updatable import Updatable
from drawable import Drawable


if TYPE_CHECKING:
    from game import Game


class Player(Updatable, Drawable):
    def __init__(self, game: "Game"):
        self.x = int(3.5) * game.map.cell_width
        self.y = int(3.5) * game.map.cell_height
        self.angle = 0
        self.fov = 60
        self.sensitivity = 0.001
        self.speed = 0.1
        self.game = game
        self.time_prev = pygame.time.get_ticks()

    def handle_movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = self.speed * self.game.delta_time
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

    def check_wall_collision(self, dx: int, dy: int):
        if self.game.map.is_wall(
            int((self.x + dx) / self.game.map.cell_width),
            int(self.y / self.game.map.cell_height),
        ):
            self.x += dx
        if self.game.map.is_wall(
            int(self.x / self.game.map.cell_width),
            int((self.y + dy) / self.game.map.cell_height),
        ):
            self.y += dy

    def handle_camera(self):
        num_key_pressed = -1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            num_key_pressed += 1
            self.angle -= self.sensitivity * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            num_key_pressed += 1
            self.angle += self.sensitivity * self.game.delta_time

    def update(self):
        self.handle_movement()
        self.handle_camera()

    def draw(self):
        pygame.draw.circle(self.game.screen, "green", (self.x, self.y), 15)
