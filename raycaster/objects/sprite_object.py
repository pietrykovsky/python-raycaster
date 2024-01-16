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


class Corps(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("corps")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class Corps2(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("corps_2")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class GreenColumn(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("green_column")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class RedColumn(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("red_column")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class HangingCorpse(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("hanging_corpse")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class HangingCorpse2(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("hanging_corpse_2")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class HangingCorpse3(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("hanging_corpse_3")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class HangingCorpse4(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("hanging_corpse_4")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class StickWithHead(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("stick_with_head")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class StickWithHeads(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("stick_with_heads")
        super().__init__(position=position, shaded=True, player=player, texture=texture)


class EvilEye(SpriteObject):
    def __init__(self, position: tuple[float, float], player: "Player"):
        texture = AssetLoader().static_objects.get("evil_eye")
        super().__init__(position=position, shaded=True, player=player, texture=texture)
