from typing import TYPE_CHECKING
import pygame

from updatable import Updatable
from settings import Settings
from utils import calculate_distance

if TYPE_CHECKING:
    from player import Player


class SpriteObject(Updatable):
    def __init__(self, x: float, y: float, texture: pygame.Surface, player: "Player"):
        self.x = x
        self.y = y
        self.settings = Settings()
        self.player = player
        self.texture = texture
        self.distance = calculate_distance(x, y, player.x, player.y)

    def update(self):
        self.distance = calculate_distance(self.x, self.y, self.player.x, self.player.y)
