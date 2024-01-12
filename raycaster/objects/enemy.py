from typing import TYPE_CHECKING
from enum import Enum

import pygame

from raycaster.objects.animated_sprite_object import AnimatedSpriteObject, Animation
from raycaster.game import AssetLoader
from raycaster.core import Settings, Event
from raycaster.const import AnimationType


if TYPE_CHECKING:
    from raycaster.game import Player


class EnemyState(Enum):
    IDLE = 0
    MOVE = 1
    ATTACK = 2
    HIT = 3
    DEATH = 4


class Enemy(AnimatedSpriteObject):
    def __init__(
        self,
        position: tuple[float, float],
        player: "Player",
        shaded: bool,
        animations: dict[AnimationType, Animation],
        damage: float,
        health: float,
        speed: float,
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
        self.speed = speed
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.attack_timer = 0
        self.state = EnemyState.IDLE
        self.death_handler = Event()
        self.position_update_handler = Event()

    def apply_damage(self, damage: float):
        self.health -= damage
        if self.health <= 0:
            self.state = EnemyState.DEATH
        else:
            self.state = EnemyState.HIT

    def update(self):
        self._update_state()
        super().update()

    def _update_state(self):
        if self._can_attack():
            self._attack()
        elif self._can_move():
            self._move()
        elif self._got_hit():
            self._hit()
        elif self._is_killed():
            self._die()
        else:
            self._idle()

    def _can_attack(self) -> bool:
        if self.state == EnemyState.ATTACK and not self._finished_attack():
            return True
        return (
            self._player_in_attack_range()
            and not self._attack_on_cooldown()
            and not self._got_hit()
            and not self._is_killed()
        )

    def _attack(self):
        self.attack_timer = (
            pygame.time.get_ticks()
            + self.animations.get(AnimationType.ATTACK).duration * 1000
        )
        self._change_animation(AnimationType.ATTACK)
        self.state = EnemyState.ATTACK

    def _can_move(self) -> bool:
        return (
            not self._player_in_attack_range()
            and not self._got_hit()
            and not self._is_killed()
            and not self.state == EnemyState.ATTACK
            and self._player_in_move_range()
        )

    def _move(self):
        self._change_animation(AnimationType.MOVE)
        self.state = EnemyState.MOVE
        self.position_update_handler.invoke(self)

    def _got_hit(self):
        return self.state == EnemyState.HIT

    def _hit(self):
        self._change_animation(AnimationType.HIT)
        if self.animation.finished:
            self._idle()

    def _is_killed(self):
        return self.state == EnemyState.DEATH

    def _die(self):
        self._change_animation(AnimationType.DEATH)
        if self.animation.finished:
            self.death_handler.invoke(self)

    def _idle(self):
        self._change_animation(AnimationType.IDLE)
        self.state = EnemyState.IDLE

    def _change_animation(self, animation_type: AnimationType):
        if self.animation == self.animations.get(animation_type):
            return
        self.animation = self.animations.get(animation_type)
        self.animation.reset()

    def _player_in_move_range(self) -> bool:
        return self.distance <= Settings().MAX_DISTANCE

    def _player_in_attack_range(self) -> bool:
        return self.distance <= self.attack_range

    def _attack_on_cooldown(self) -> bool:
        if self.attack_timer == 0:
            return False
        return pygame.time.get_ticks() - self.attack_timer < self.attack_cooldown * 1000

    def _finished_attack(self) -> bool:
        return (
            self.animation == self.animations.get(AnimationType.ATTACK)
            and self.animation.finished
        )


class Test(Enemy):
    def __init__(self, position: tuple[float, float], player: "Player"):
        assets = AssetLoader().enemies.get("test")
        animations = {
            AnimationType.IDLE: Animation(
                frames=assets.get(AnimationType.IDLE),
                duration=3,
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
                duration=3,
                repeat=False,
            ),
            AnimationType.DEATH: Animation(
                frames=assets.get(AnimationType.DEATH),
                duration=2,
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
            speed=0.1,
            attack_range=Settings().CELL_SIZE * 2,
            attack_cooldown=5,
        )
