from typing import TYPE_CHECKING

from raycaster.objects import sprite_object, animated_sprite_object, enemy


if TYPE_CHECKING:
    from raycaster.game import Player


class BaseObjectFactory:
    player: "Player" = None
    _class_map: dict[str, "sprite_object.SpriteObject"] = {}

    @classmethod
    def object_exists(cls, name: str) -> bool:
        return name in cls._class_map

    @classmethod
    def add_player(cls, player: "Player"):
        cls.player = player

    @classmethod
    def create(
        cls, name: str, position: tuple[float, float]
    ) -> sprite_object.SpriteObject:
        if cls.object_exists(name):
            return cls._class_map.get(name)(position, cls.player)
        else:
            raise ValueError(f"Unknown object name: {name}")


class StaticObjectFactory(BaseObjectFactory):
    _class_map = {
        "candlebra": sprite_object.Candlebra,
        "npc": sprite_object.NPC,
    }


class AnimatedObjectFactory(BaseObjectFactory):
    _class_map = {
        "quagmire": animated_sprite_object.Quagmire,
    }


class EnemyFactory(BaseObjectFactory):
    _class_map = {
        "test": enemy.Test,
    }


class ObjectFactory:
    @classmethod
    def add_player(cls, player: "Player"):
        StaticObjectFactory.add_player(player)
        AnimatedObjectFactory.add_player(player)
        EnemyFactory.add_player(player)

    @classmethod
    def create(
        cls, name: str, position: tuple[float, float]
    ) -> sprite_object.SpriteObject:
        if StaticObjectFactory.object_exists(name):
            return StaticObjectFactory.create(name, position)
        elif AnimatedObjectFactory.object_exists(name):
            return AnimatedObjectFactory.create(name, position)
        elif EnemyFactory.object_exists(name):
            return EnemyFactory.create(name, position)
        else:
            raise ValueError(f"Unknown object name: {name}")
