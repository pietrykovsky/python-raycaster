from typing import TYPE_CHECKING

from raycaster.objects.object_factory import ObjectFactory
from raycaster.objects.enemy_movement_controller import EnemyMovementController
from raycaster.rendering.raycaster import Raycaster
from raycaster.core import Settings, Updatable

if TYPE_CHECKING:
    from raycaster.game import Player
    from raycaster.objects.sprite_object import SpriteObject
    from raycaster.objects.enemy import Enemy
    from raycaster.game.map import Map


class ObjectManager:
    _instance = None

    def __new__(cls, player: "Player", raycaster: "Raycaster", map: "Map"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.player = player
            cls.raycaster = raycaster
            cls.map = map
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
            enemy.position_update_handler += cls._on_enemy_position_update

    @classmethod
    def _on_enemy_death(cls, enemy: "Enemy"):
        if enemy in cls._enemies:
            cls._enemies.remove(enemy)
            Updatable.unregister(enemy)

    @classmethod
    def _on_enemy_position_update(cls, enemy: "Enemy"):
        EnemyMovementController.update_position(enemy, cls.map)
