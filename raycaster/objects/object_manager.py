from typing import TYPE_CHECKING

from raycaster.objects.object_factory import ObjectFactory
from raycaster.core import Settings

if TYPE_CHECKING:
    from raycaster.game import Player
    from raycaster.objects.sprite_object import SpriteObject
    from raycaster.objects.enemy import Enemy


class ObjectManager:
    _instance = None

    def __new__(cls, player: "Player"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            ObjectFactory.add_player(player)
            cls._initialize_objects()
            cls._register_event_handlers()
        return cls._instance

    @property
    def objects(self) -> tuple["SpriteObject"]:
        return tuple(self._objects)

    @property
    def enemies(self) -> tuple["Enemy"]:
        return tuple(self._enemies)

    @classmethod
    def _initialize_objects(cls):
        cell_size = Settings().CELL_SIZE
        cls._objects = [
            ObjectFactory.create("candlebra", (2.5 * cell_size, 2.5 * cell_size)),
            ObjectFactory.create("candlebra", (4.5 * cell_size, 4.5 * cell_size)),
            ObjectFactory.create("npc", (4.5 * cell_size, 5.5 * cell_size)),
            ObjectFactory.create("candlebra", (5.5 * cell_size, 5.5 * cell_size)),
            ObjectFactory.create("quagmire", (9.5 * cell_size, 2.5 * cell_size)),
        ]
        cls._enemies = [
            ObjectFactory.create("test", (7.5 * cell_size, 2.5 * cell_size)),
            ObjectFactory.create("test", (8.5 * cell_size, 2.5 * cell_size)),
            ObjectFactory.create("test", (7.5 * cell_size, 4.5 * cell_size)),
            ObjectFactory.create("test", (8.5 * cell_size, 3.5 * cell_size)),
        ]

    @classmethod
    def _register_event_handlers(cls):
        for enemy in cls._enemies:
            enemy.death_handler += cls._on_enemy_death

    @classmethod
    def _on_enemy_death(cls, enemy: "Enemy"):
        if enemy in cls._enemies:
            cls._enemies.remove(enemy)
