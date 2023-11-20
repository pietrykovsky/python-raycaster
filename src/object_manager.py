from typing import TYPE_CHECKING

from settings import Settings
from asset_loader import AssetLoader
from sprite_object import SpriteObject
from updatable import Updatable

if TYPE_CHECKING:
    from player import Player


class ObjectManager(Updatable):
    _instance = None

    def __new__(cls, player: "Player"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.player = player
            cls._initialize_objects()
        return cls._instance

    @classmethod
    def _initialize_objects(cls):
        candlebra_texture = AssetLoader().static_objects.get("candlebra")
        cell_size = Settings().CELL_SIZE
        cls._objects = [
            SpriteObject(
                2.5 * cell_size, 2.5 * cell_size, candlebra_texture, cls.player
            ),
            SpriteObject(
                4.5 * cell_size, 4.5 * cell_size, candlebra_texture, cls.player
            ),
            SpriteObject(
                4.5 * cell_size, 5.5 * cell_size, candlebra_texture, cls.player
            ),
            SpriteObject(
                5.5 * cell_size, 5.5 * cell_size, candlebra_texture, cls.player
            ),
            SpriteObject(
                7.5 * cell_size, 2.5 * cell_size, candlebra_texture, cls.player
            )
        ]

    @property
    def objects(self) -> list[SpriteObject]:
        return self._objects
    
    def update(self):
        self._objects.sort(key=lambda obj: obj.distance, reverse=True)
