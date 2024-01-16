from typing import TYPE_CHECKING

from raycaster.objects.object_factory import ObjectFactory
from raycaster.rendering.sprite_projection_processor import SpriteProjectionProcessor
from raycaster.objects.enemy_movement_controller import EnemyMovementController
from raycaster.rendering.raycaster import Raycaster
from raycaster.core import Settings, Updatable

if TYPE_CHECKING:
    from raycaster.game import Player
    from raycaster.objects.sprite_object import SpriteObject
    from raycaster.objects.enemy import Enemy
    from raycaster.game.map import Map
    from raycaster.objects.weapons import Weapon
    from raycaster.rendering.ray import Ray


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

    @property
    def weapons(self) -> tuple["Weapon"]:
        return tuple(self._weapons)

    @classmethod
    def _initialize_objects(cls):
        cell_size = Settings().CELL_SIZE
        cls._objects = [
            ObjectFactory.create("green_torch", (1.5 * cell_size, 1.5 * cell_size)),
            ObjectFactory.create("green_torch", (1.5 * cell_size, 7.5 * cell_size)),
            ObjectFactory.create("green_torch", (13.5 * cell_size, 3.5 * cell_size)),
            ObjectFactory.create("green_torch", (1.5 * cell_size, 12.5 * cell_size)),
            ObjectFactory.create("green_torch", (14.5 * cell_size, 12.5 * cell_size)),
            ObjectFactory.create("green_torch", (4.5 * cell_size, 16.5 * cell_size)),
            ObjectFactory.create("green_torch", (14.5 * cell_size, 24.5 * cell_size)),
            ObjectFactory.create("green_torch", (1.5 * cell_size, 24.5 * cell_size)),
            ObjectFactory.create("green_torch", (14.5 * cell_size, 30.5 * cell_size)),
            ObjectFactory.create("green_torch", (1.5 * cell_size, 30.5 * cell_size)),
            ObjectFactory.create("corps", (5.5 * cell_size, 3.5 * cell_size)),
            ObjectFactory.create("corps_2", (5.5 * cell_size, 4.5 * cell_size)),
            ObjectFactory.create("corps", (1.5 * cell_size, 19.5 * cell_size)),
            ObjectFactory.create("corps_2", (2.5 * cell_size, 20.5 * cell_size)),
            ObjectFactory.create("corps", (7.5 * cell_size, 29.5 * cell_size)),
            ObjectFactory.create("corps_2", (8.5 * cell_size, 29.5 * cell_size)),
            ObjectFactory.create("corps", (7.5 * cell_size, 30.5 * cell_size)),
            ObjectFactory.create("corps_2", (8.5 * cell_size, 30.5 * cell_size)),
            ObjectFactory.create("green_column", (9.5 * cell_size, 7.5 * cell_size)),
            ObjectFactory.create("green_column", (12.5 * cell_size, 7.5 * cell_size)),
            ObjectFactory.create("red_column", (3.5 * cell_size, 20.5 * cell_size)),
            ObjectFactory.create("red_column", (6.5 * cell_size, 20.5 * cell_size)),
        ]
        cls._enemies = [
            ObjectFactory.create("soldier", (11.5 * cell_size, 3.5 * cell_size)),
            ObjectFactory.create("soldier", (14.5 * cell_size, 1.5 * cell_size)),
            ObjectFactory.create("soldier", (14.5 * cell_size, 7.5 * cell_size)),
            ObjectFactory.create("soldier", (7.5 * cell_size, 16.5 * cell_size)),
            ObjectFactory.create("caco_demon", (10.5 * cell_size, 12.5 * cell_size)),
            ObjectFactory.create("caco_demon", (1.5 * cell_size, 18.5 * cell_size)),
            ObjectFactory.create("caco_demon", (2.5 * cell_size, 18.5 * cell_size)),
            ObjectFactory.create("caco_demon", (4.5 * cell_size, 24.5 * cell_size)),
            ObjectFactory.create("caco_demon", (5.5 * cell_size, 24.5 * cell_size)),
            ObjectFactory.create("cyber_demon", (13.5 * cell_size, 19.5 * cell_size)),
            ObjectFactory.create("cyber_demon", (5.5 * cell_size, 29.5 * cell_size)),
            ObjectFactory.create("cyber_demon", (10.5 * cell_size, 29.5 * cell_size)),
        ]
        cls._weapons = [
            ObjectFactory.create("shotgun", (14.5 * cell_size, 20.5 * cell_size)),
            ObjectFactory.create("pistol", (4.5 * cell_size, 4.5 * cell_size)),
        ]

    @classmethod
    def _register_event_handlers(cls):
        cls.player.shoot_handler += cls._on_player_shot
        for enemy in cls._enemies:
            enemy.death_handler += cls._on_enemy_death
            enemy.position_update_handler += cls._on_enemy_position_update
            enemy.attack_handler += cls._on_enemy_attack

    @classmethod
    def _on_enemy_death(cls, enemy: "Enemy"):
        if enemy in cls._enemies:
            cls.player.add_score(enemy.score)
            cls._enemies.remove(enemy)
            Updatable.unregister(enemy)

    @classmethod
    def _on_enemy_position_update(cls, enemy: "Enemy"):
        EnemyMovementController.update_position(enemy, cls.map)

    @classmethod
    def _on_enemy_attack(cls, enemy: "Enemy"):
        ray = cls.raycaster.cast_ray(enemy.angle)
        if not (ray.hit_wall and ray.length < enemy.distance):
            cls.player.apply_damage(enemy.damage)

    @classmethod
    def _on_player_shot(cls):
        ray = cls.raycaster.cast_ray(cls.player.angle)
        if cls.player.weapon:
            for enemy in sorted(cls._enemies, key=lambda e: e.distance):
                if (
                    SpriteProjectionProcessor.intersects_screen_center(enemy)
                    and not (ray.hit_wall and ray.length < enemy.distance)
                    and cls.player.in_fov(enemy.angle)
                ):
                    enemy.apply_damage(cls.player.weapon.damage)
                    return

    @classmethod
    def reset(cls):
        cls._remove_all_objects()
        cls._initialize_objects()
        cls._register_event_handlers()

    @classmethod
    def _remove_all_objects(cls):
        for enemy in cls._enemies:
            cls._enemies.remove(enemy)
            Updatable.unregister(enemy)
