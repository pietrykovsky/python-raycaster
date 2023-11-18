import math
from typing import TYPE_CHECKING
import pygame

from updatable import Updatable


if TYPE_CHECKING:
    from game import Game


class Player(Updatable):
    def __init__(self, game: "Game"):
        self.game = game
        self.speed = game.settings.PLAYER_SPEED
        self.sensitivity = game.settings.PLAYER_SENSITIVITY
        self.x = 3.5 * game.settings.CELL_SIZE
        self.y = 3.5 * game.settings.CELL_SIZE
        self.angle = 0
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
        if not self.game.map.is_wall(
            int((self.x + dx) / self.game.settings.CELL_SIZE),
            int(self.y / self.game.settings.CELL_SIZE),
        ):
            self.x += dx
        if not self.game.map.is_wall(
            int(self.x / self.game.settings.CELL_SIZE),
            int((self.y + dy) / self.game.settings.CELL_SIZE),
        ):
            self.y += dy

    def handle_camera(self):
        num_key_pressed = -1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            num_key_pressed += 1
            self.angle -= self.sensitivity * self.game.delta_time
            self.angle = self.angle % (2 * math.pi)
        if keys[pygame.K_RIGHT]:
            num_key_pressed += 1
            self.angle += self.sensitivity * self.game.delta_time
            self.angle = self.angle % (2 * math.pi)

    def update(self):
        self.handle_movement()
        self.handle_camera()

    # def draw(self):
    #     pygame.draw.circle(self.game.screen, "green", (self.x, self.y), 15)
