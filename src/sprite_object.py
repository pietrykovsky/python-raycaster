from typing import TYPE_CHECKING
import math
import pygame

from updatable import Updatable
from settings import Settings
from utils import calculate_distance

if TYPE_CHECKING:
    from player import Player


class SpriteObject(Updatable):
    def __init__(
        self,
        position: tuple[int, int],
        texture: pygame.Surface,
        player: "Player",
        shaded: bool = True,
    ):
        x, y = position
        self.x = x
        self.y = y
        self.settings = Settings()
        self.player = player
        self.texture = texture
        self.distance = calculate_distance(x, y, player.x, player.y)
        self.angle = math.atan2(y - player.y, x - player.x)
        self.shaded = shaded

    def update(self):
        self.distance = calculate_distance(self.x, self.y, self.player.x, self.player.y)
        self.angle = math.atan2(self.y - self.player.y, self.x - self.player.x)
