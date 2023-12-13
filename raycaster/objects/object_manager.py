from typing import TYPE_CHECKING

from raycaster.core import Settings
from raycaster.game import AssetLoader
from raycaster.objects.sprite_object import SpriteObject
from raycaster.objects.animated_sprite_object import AnimatedSpriteObject

if TYPE_CHECKING:
    from raycaster.game import Player


class ObjectManager:
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
        npc_texture = AssetLoader().static_objects.get("npc")
        test_animation = AssetLoader().animated_objects.get("test")
        quagmire = AssetLoader().animated_objects.get("quagmire")
        cell_size = Settings().CELL_SIZE
        cls._objects = [
            SpriteObject(
                (2.5 * cell_size, 2.5 * cell_size), candlebra_texture, cls.player, False
            ),
            SpriteObject(
                (4.5 * cell_size, 4.5 * cell_size), candlebra_texture, cls.player, False
            ),
            SpriteObject((4.5 * cell_size, 5.5 * cell_size), npc_texture, cls.player),
            SpriteObject(
                (5.5 * cell_size, 5.5 * cell_size), candlebra_texture, cls.player, False
            ),
            SpriteObject((7.5 * cell_size, 2.5 * cell_size), npc_texture, cls.player),
            AnimatedSpriteObject(
                (9.5 * cell_size, 2.5 * cell_size),
                quagmire,
                cls.player,
                animation_duration=5,
            ),
        ]

    @property
    def objects(self) -> list[SpriteObject]:
        return self._objects
