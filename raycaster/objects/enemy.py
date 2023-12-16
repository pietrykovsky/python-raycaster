from typing import TYPE_CHECKING

import pygame

from raycaster.objects.animated_sprite_object import AnimatedSpriteObject, Animation
from raycaster.game import AssetLoader
from raycaster.const import AnimationType


if TYPE_CHECKING:
    from raycaster.game import Player


class Enemy(AnimatedSpriteObject):
    def __init__(
        self,
        position: tuple[float, float],
        player: "Player",
        shaded: bool,
        animations: dict[AnimationType, Animation],
        damage: float,
        health: float,
        attack_range: float,
        attack_cooldown: float,
    ):
        super().__init__(
            position=position,
            player=player,
            shaded=shaded,
            frames=animations.get(AnimationType.IDLE).frames,
            animation_duration=animations.get(AnimationType.IDLE).duration,
        )
        self.animations = animations
        self.damage = damage
        self.health = health
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.attack_timer = 0

    def _player_in_range(self) -> bool:
        return self.distance <= self.attack_range

    def change_animation(self, animation_type: AnimationType):
        if self.animation == self.animations.get(animation_type):
            return
        self.animation = self.animations.get(animation_type)
        self.animation.reset()

    def _attack_on_cooldown(self) -> bool:
        if self.attack_timer == 0:
            return False
        return pygame.time.get_ticks() - self.attack_timer < self.attack_cooldown * 1000

    def _got_hit(self):
        return (
            self.animation == self.animations.get(AnimationType.HIT)
            and not self.animation.finished
        )

    def _can_attack(self) -> bool:
        return (
            self._player_in_range()
            and not self._attack_on_cooldown()
            and not self._got_hit()
        )

    def _finished_attack(self) -> bool:
        return (
            self.animation == self.animations.get(AnimationType.ATTACK)
            and self.animation.finished
        )

    def attack(self):
        self.attack_timer = (
            pygame.time.get_ticks()
            + self.animations.get(AnimationType.ATTACK).duration * 1000
        )
        self.change_animation(AnimationType.ATTACK)

    def _can_move(self) -> bool:
        return not self._player_in_range() and not self._got_hit()

    def move(self):
        self.animation = self.animations.get(AnimationType.MOVE)

    def update(self):
        if self._can_attack():
            self.attack()
        elif self._can_move():
            self.move()
        elif (
            not self._can_move() and not self._can_attack() and self._finished_attack()
        ):
            self.change_animation(AnimationType.IDLE)

        super().update()


class Test(Enemy):
    def __init__(self, position: tuple[float, float], player: "Player"):
        assets = AssetLoader().enemies.get("test")
        animations = {
            AnimationType.IDLE: Animation(
                frames=assets.get(AnimationType.IDLE),
                duration=0.5,
            ),
            AnimationType.MOVE: Animation(
                frames=assets.get(AnimationType.MOVE),
                duration=2.5,
            ),
            AnimationType.ATTACK: Animation(
                frames=assets.get(AnimationType.ATTACK),
                duration=4,
                repeat=False,
            ),
            AnimationType.HIT: Animation(
                frames=assets.get(AnimationType.HIT),
                duration=0.5,
                repeat=False,
            ),
        }
        super().__init__(
            position=position,
            player=player,
            shaded=True,
            animations=animations,
            damage=1,
            health=10,
            attack_range=256 * 2,
            attack_cooldown=5,
        )
