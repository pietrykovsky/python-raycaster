from typing import TYPE_CHECKING

from raycaster.objects import sprite_object, animated_sprite_object, enemy, weapons


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
            return cls._class_map.get(name)(position=position, player=cls.player)
        else:
            raise ValueError(f"Unknown object name: {name}")


class StaticObjectFactory(BaseObjectFactory):
    _class_map = {
        "corps": sprite_object.Corps,
        "corps_2": sprite_object.Corps2,
        "green_column": sprite_object.GreenColumn,
        "red_column": sprite_object.RedColumn,
        "hanging_corpse": sprite_object.HangingCorpse,
        "hanging_corpse_2": sprite_object.HangingCorpse2,
        "hanging_corpse_3": sprite_object.HangingCorpse3,
        "hanging_corpse_4": sprite_object.HangingCorpse4,
        "stick_with_head": sprite_object.StickWithHead,
        "stick_with_heads": sprite_object.StickWithHeads,
        "evil_eye": sprite_object.EvilEye,
    }


class AnimatedObjectFactory(BaseObjectFactory):
    _class_map = {
        "green_torch": animated_sprite_object.Green_Torch,
    }


class EnemyFactory(BaseObjectFactory):
    _class_map = {
        "lost_soul": enemy.Lost_Soul,
        "caco_demon": enemy.Caco_Demon,
        "cyber_demon": enemy.Cyber_Demon,
        "soldier": enemy.Soldier,
    }


class WeaponFactory(BaseObjectFactory):
    _class_map = {
        "shotgun": weapons.Shotgun,
        "pistol": weapons.Pistol,
    }


class ObjectFactory:
    @classmethod
    def add_player(cls, player: "Player"):
        StaticObjectFactory.add_player(player)
        AnimatedObjectFactory.add_player(player)
        EnemyFactory.add_player(player)
        WeaponFactory.add_player(player)

    @classmethod
    def create(
        cls, name: str, position: tuple[float, float] | None
    ) -> sprite_object.SpriteObject:
        if StaticObjectFactory.object_exists(name):
            return StaticObjectFactory.create(name, position)
        elif AnimatedObjectFactory.object_exists(name):
            return AnimatedObjectFactory.create(name, position)
        elif EnemyFactory.object_exists(name):
            return EnemyFactory.create(name, position)
        elif WeaponFactory.object_exists(name):
            return WeaponFactory.create(name, position)
        else:
            raise ValueError(f"Unknown object name: {name}")
