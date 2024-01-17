from typing import TYPE_CHECKING
from enum import Enum
import random

import pygame

from raycaster.objects.animated_sprite_object import AnimatedSpriteObject, Animation
from raycaster.game import AssetLoader
from raycaster.core import Settings, Event
from raycaster.const import EnemyState, EFFECTS_VOLUME


if TYPE_CHECKING:
    from raycaster.game import Player


class Enemy(AnimatedSpriteObject):
    def __init__(
        self,
        position: tuple[float, float],
        player: "Player",
        shaded: bool,
        animations: dict[EnemyState, Animation],
        sounds: dict[EnemyState, pygame.mixer.Sound],
        damage: float,
        health: float,
        speed: float,
        attack_range: float,
        attack_cooldown: float,
        attack_chance: float,
        score: int,
    ):
        super().__init__(
            position=position,
            player=player,
            shaded=shaded,
            frames=animations.get(EnemyState.IDLE).frames,
            animation_duration=animations.get(EnemyState.IDLE).duration,
        )
        self.animations = animations
        self.sounds = sounds
        self.damage = damage
        self.health = health
        self.speed = speed
        self.score = score
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.attack_chance = attack_chance
        self.attack_timer = 0
        self.state = EnemyState.IDLE
        self.death_handler = Event()
        self.position_update_handler = Event()
        self.attack_handler = Event()

    def apply_damage(self, damage: float):
        self.health -= damage
        if self.health <= 0:
            self._play_sound(EnemyState.DEATH)
            self.state = EnemyState.DEATH
        else:
            self._play_sound(EnemyState.HIT)
            self.state = EnemyState.HIT

    def update(self):
        self._update_state()
        super().update()

    def _play_sound(self, state: EnemyState):
        sound = self.sounds.get(state)
        volume = max(0, 1 - self.distance / Settings().MAX_DISTANCE) * EFFECTS_VOLUME
        sound.set_volume(volume)
        sound.play()

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
        if not self.state == EnemyState.ATTACK:
            self._draw_hit()
            self._play_sound(EnemyState.ATTACK)
        self.attack_timer = (
            pygame.time.get_ticks()
            + self.animations.get(EnemyState.ATTACK).duration * 1000
        )
        self._change_animation(EnemyState.ATTACK)
        self.state = EnemyState.ATTACK

    def _draw_hit(self):
        """
        Draws a player hit based on the attack chance. If hit is successful, the attack handler is invoked.
        """
        if random.random() <= self.attack_chance:
            self.attack_handler.invoke(self)

    def _can_move(self) -> bool:
        return (
            not self._player_in_attack_range()
            and not self._got_hit()
            and not self._is_killed()
            and not self.state == EnemyState.ATTACK
            and self._player_in_move_range()
        )

    def _move(self):
        if self.state != EnemyState.MOVE:
            self._play_sound(EnemyState.MOVE)
        self._change_animation(EnemyState.MOVE)
        self.state = EnemyState.MOVE
        self.position_update_handler.invoke(self)

    def _got_hit(self):
        return self.state == EnemyState.HIT

    def _hit(self):
        self._change_animation(EnemyState.HIT)
        if self.animation.finished:
            self._idle()

    def _is_killed(self):
        return self.state == EnemyState.DEATH

    def _die(self):
        self._change_animation(EnemyState.DEATH)
        if self.animation.finished:
            self.death_handler.invoke(self)

    def _idle(self):
        if self.state != EnemyState.IDLE:
            self._play_sound(EnemyState.IDLE)
        self._change_animation(EnemyState.IDLE)
        self.state = EnemyState.IDLE

    def _change_animation(self, animation_type: EnemyState):
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
            self.animation == self.animations.get(EnemyState.ATTACK)
            and self.animation.finished
        )


class Soldier(Enemy):
    def __init__(self, position: tuple[float, float], player: "Player"):
        assets = AssetLoader().enemies.get("soldier")
        animations = {
            EnemyState.IDLE: Animation(
                frames=assets.get(EnemyState.IDLE),
                duration=1.5,
            ),
            EnemyState.MOVE: Animation(
                frames=assets.get(EnemyState.MOVE),
                duration=2.5,
            ),
            EnemyState.ATTACK: Animation(
                frames=assets.get(EnemyState.ATTACK),
                duration=2,
                repeat=False,
            ),
            EnemyState.HIT: Animation(
                frames=assets.get(EnemyState.HIT),
                duration=0.3,
                repeat=False,
            ),
            EnemyState.DEATH: Animation(
                frames=assets.get(EnemyState.DEATH),
                duration=1,
                repeat=False,
            ),
        }
        super().__init__(
            position=position,
            player=player,
            shaded=True,
            animations=animations,
            sounds=assets.get("sound"),
            damage=5,
            health=15,
            speed=0.4,
            attack_range=Settings().CELL_SIZE * 4,
            attack_cooldown=1,
            attack_chance=0.7,
            score=100,
        )


class LostSoul(Enemy):
    def __init__(self, position: tuple[float, float], player: "Player"):
        assets = AssetLoader().enemies.get("lost_soul")
        animations = {
            EnemyState.IDLE: Animation(
                frames=assets.get(EnemyState.IDLE),
                duration=2,
            ),
            EnemyState.MOVE: Animation(
                frames=assets.get(EnemyState.MOVE),
                duration=2,
            ),
            EnemyState.ATTACK: Animation(
                frames=assets.get(EnemyState.ATTACK),
                duration=2,
                repeat=False,
            ),
            EnemyState.HIT: Animation(
                frames=assets.get(EnemyState.HIT),
                duration=0.3,
                repeat=False,
            ),
            EnemyState.DEATH: Animation(
                frames=assets.get(EnemyState.DEATH),
                duration=1,
                repeat=False,
            ),
        }
        super().__init__(
            position=position,
            player=player,
            shaded=True,
            animations=animations,
            sounds=assets.get("sound"),
            damage=20,
            health=90,
            speed=0.6,
            attack_range=Settings().CELL_SIZE * 2,
            attack_cooldown=0.5,
            attack_chance=0.8,
            score=200,
        )


class CacoDemon(Enemy):
    def __init__(self, position: tuple[float, float], player: "Player"):
        assets = AssetLoader().enemies.get("caco_demon")
        animations = {
            EnemyState.IDLE: Animation(
                frames=assets.get(EnemyState.IDLE),
                duration=2,
            ),
            EnemyState.MOVE: Animation(
                frames=assets.get(EnemyState.MOVE),
                duration=1.5,
            ),
            EnemyState.ATTACK: Animation(
                frames=assets.get(EnemyState.ATTACK),
                duration=2,
                repeat=False,
            ),
            EnemyState.HIT: Animation(
                frames=assets.get(EnemyState.HIT),
                duration=0.3,
                repeat=False,
            ),
            EnemyState.DEATH: Animation(
                frames=assets.get(EnemyState.DEATH),
                duration=1,
                repeat=False,
            ),
        }
        super().__init__(
            position=position,
            player=player,
            shaded=True,
            animations=animations,
            sounds=assets.get("sound"),
            damage=40,
            health=120,
            speed=0.3,
            attack_range=Settings().CELL_SIZE * 1.5,
            attack_cooldown=3,
            attack_chance=0.9,
            score=250,
        )


class CyberDemon(Enemy):
    def __init__(self, position: tuple[float, float], player: "Player"):
        assets = AssetLoader().enemies.get("cyber_demon")
        animations = {
            EnemyState.IDLE: Animation(
                frames=assets.get(EnemyState.IDLE),
                duration=3,
            ),
            EnemyState.MOVE: Animation(
                frames=assets.get(EnemyState.MOVE),
                duration=1.5,
            ),
            EnemyState.ATTACK: Animation(
                frames=assets.get(EnemyState.ATTACK),
                duration=1,
                repeat=False,
            ),
            EnemyState.HIT: Animation(
                frames=assets.get(EnemyState.HIT),
                duration=0.3,
                repeat=False,
            ),
            EnemyState.DEATH: Animation(
                frames=assets.get(EnemyState.DEATH),
                duration=1,
                repeat=False,
            ),
        }
        super().__init__(
            position=position,
            player=player,
            shaded=True,
            animations=animations,
            sounds=assets.get("sound"),
            damage=20,
            health=400,
            speed=0.8,
            attack_range=Settings().CELL_SIZE * 3.5,
            attack_cooldown=0.6,
            attack_chance=1,
            score=1000,
        )
