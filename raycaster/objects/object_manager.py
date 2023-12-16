from typing import TYPE_CHECKING

from raycaster.objects.object_factory import ObjectFactory
from raycaster.core import Settings

if TYPE_CHECKING:
    from raycaster.game import Player
    from raycaster.objects.sprite_object import SpriteObject


class ObjectManager:
    _instance = None

    def __new__(cls, player: "Player"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            ObjectFactory.add_player(player)
            cls._initialize_objects()
        return cls._instance

    @classmethod
    def _initialize_objects(cls):
        cell_size = Settings().CELL_SIZE
        cls._objects = [
            ObjectFactory.create("candlebra", (2.5 * cell_size, 2.5 * cell_size)),
            ObjectFactory.create("candlebra", (4.5 * cell_size, 4.5 * cell_size)),
            ObjectFactory.create("npc", (4.5 * cell_size, 5.5 * cell_size)),
            ObjectFactory.create("candlebra", (5.5 * cell_size, 5.5 * cell_size)),
            ObjectFactory.create("test", (7.5 * cell_size, 2.5 * cell_size)),
            ObjectFactory.create("quagmire", (9.5 * cell_size, 2.5 * cell_size)),
        ]

    @property
    def objects(self) -> list["SpriteObject"]:
        return self._objects
