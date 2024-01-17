from typing import TYPE_CHECKING
import pygame

from raycaster.objects.animated_sprite_object import Animation
from raycaster.objects.sprite_object import SpriteObject
from raycaster.game import AssetLoader
from raycaster.const import WeaponRepresentation, WeaponState

if TYPE_CHECKING:
    from raycaster.game import Player


class Weapon(SpriteObject):
    def __init__(
        self,
        player: "Player",
        shooting_animation: "Animation",
        sounds: dict[WeaponState, pygame.mixer.Sound],
        sprite_representation: pygame.Surface,
        damage: float,
        attack_range: float,
        attack_cooldown: float,
        shaded: bool,
        position: tuple[float, float] | None = None,
    ):
        self.gui_representation = shooting_animation.current_frame
        self.damage = damage
        self._equipped = False
        self._shooting_animation = shooting_animation
        self._sounds = sounds
        self._attack_range = attack_range
        self._attack_cooldown = attack_cooldown
        self._attack_timer = 0
        self._is_shooting = False
        self.can_be_picked_up = True
        super().__init__(
            position=position if position is not None else (player.x, player.y),
            shaded=shaded,
            player=player,
            texture=sprite_representation,
        )
        self.PICKUP_RADIUS = self.texture.get_width() / 2

    @property
    def equipped(self) -> bool:
        return self._equipped

    def equip(self):
        self._equipped = True
        self.player.weapon = self
        self._sounds.get(WeaponState.EQUIP).play()

    def unequip(self):
        self.x, self.y = self.player.x, self.player.y
        self.player.weapon = None
        self._equipped = False

    def can_shoot(self) -> bool:
        return pygame.time.get_ticks() >= self._attack_timer and self.equipped

    def shoot(self):
        self._is_shooting = True
        self._attack_timer = (
            pygame.time.get_ticks()
            + (self._shooting_animation.duration + self._attack_cooldown) * 1000
        )
        self._sounds.get(WeaponState.SHOOT).play()

    def update(self):
        if self._shooting_animation.finished:
            self._reset_shooting_animation()
        if self._is_shooting:
            self.gui_representation = self._shooting_animation.update_and_get_frame()
        if not self._equipped:
            super().update()
            self._check_pickup()
            if self.distance > self.PICKUP_RADIUS:
                self.can_be_picked_up = True

    def _reset_shooting_animation(self):
        self._shooting_animation.reset()
        self._is_shooting = False
        self.gui_representation = self._shooting_animation.current_frame

    def _check_pickup(self):
        if self.distance <= self.PICKUP_RADIUS and self.can_be_picked_up:
            if self.player.weapon:
                self.player.weapon.can_be_picked_up = False
                self.player.weapon.unequip()
            self.equip()


class Shotgun(Weapon):
    def __init__(
        self,
        position: tuple[float, float] | None = None,
        *,
        player: "Player",
    ):
        weapon_assets = AssetLoader().weapons.get("shotgun")
        animation = Animation(
            frames=weapon_assets.get(WeaponRepresentation.GUI.value),
            duration=0.75,
            repeat=False,
        )
        sprite_representation = weapon_assets.get(WeaponRepresentation.SPRITE.value)
        weapon_sounds = weapon_assets.get(WeaponRepresentation.SOUND.value)
        super().__init__(
            player=player,
            shooting_animation=animation,
            sounds=weapon_sounds,
            sprite_representation=sprite_representation,
            damage=10,
            attack_range=10,
            attack_cooldown=1.2,
            shaded=True,
            position=position,
        )


class Pistol(Weapon):
    def __init__(
        self,
        position: tuple[float, float] | None = None,
        *,
        player: "Player",
    ):
        weapon_assets = AssetLoader().weapons.get("pistol")
        animation = Animation(
            frames=weapon_assets.get(WeaponRepresentation.GUI.value),
            duration=0.5,
            repeat=False,
        )
        sprite_representation = weapon_assets.get(WeaponRepresentation.SPRITE.value)
        weapon_sounds = weapon_assets.get(WeaponRepresentation.SOUND.value)
        super().__init__(
            player=player,
            shooting_animation=animation,
            sounds=weapon_sounds,
            sprite_representation=sprite_representation,
            damage=5,
            attack_range=10,
            attack_cooldown=1,
            shaded=True,
            position=position,
        )
