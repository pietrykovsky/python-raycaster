from typing import TYPE_CHECKING
import pygame

from settings import Settings
from drawable import Drawable
from object_manager import ObjectManager

if TYPE_CHECKING:
    from player import Player
    from sprite_object import SpriteObject


class ObjectRenderer(Drawable):
    _instance = None
    def __new__(cls, player: "Player"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.player = player
            cls.object_manager = ObjectManager(player)
        return cls._instance
    
    def draw_object(self, obj: "SpriteObject"):
        max_distance = Settings().MAX_DISTANCE
        if obj.distance > max_distance:
            return

    def draw(self):
        objects = self.object_manager.objects
        for obj in objects:
            self.draw_object(obj)