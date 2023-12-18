from typing import TYPE_CHECKING
import math
import pygame

from raycaster.core import Updatable, Settings
from raycaster.game import AssetLoader
from raycaster.utils import calculate_distance

if TYPE_CHECKING:
    from raycaster.game import Player


class SpriteObject(Updatable):
    def __init__(
        self,
        position: tuple[float, float],
        shaded: bool,
        player: "Player",
        texture: pygame.Surface,
    ):
        self.x, self.y = position
        self.shaded = shaded
        self.player = player
        self.texture = texture
        self.settings = Settings()
        self.distance = calculate_distance(self.x, self.y, self.player.x, self.player.y)
        self.angle = math.atan2(self.y - self.player.y, self.x - self.player.x)

    def update(self):
        self.distance = calculate_distance(self.x, self.y, self.player.x, self.player.y)
        self.angle = math.atan2(self.y - self.player.y, self.x - self.player.x)


class Candlebra(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("candlebra")
        super().__init__(
            position=position, shaded=False, player=player, texture=texture
        )


class NPC(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("npc")
        super().__init__(position=position, shaded=True, player=player, texture=texture)
