from typing import TYPE_CHECKING
import math
import pygame

from raycaster.utils import calculate_distance
from raycaster.objects.sprite_object import SpriteObject
from raycaster.game import AssetLoader

if TYPE_CHECKING:
    from raycaster.game import Player


class Animation:
    def __init__(
        self, frames: list[pygame.Surface], duration: float, repeat: bool = True
    ):
        self.frames = frames
        self.duration = duration
        self.repeat = repeat
        self._finished = False
        self._frame_time = duration / len(self.frames)
        self._start_time = None
        self._finish_time = None
        self._frame_index = 0
        self._time_prev = pygame.time.get_ticks()

    @property
    def finished(self) -> bool:
        if self._finish_time is not None:
            self._finished = pygame.time.get_ticks() >= self._finish_time
        return self._finished

    @property
    def current_frame(self) -> pygame.Surface:
        return self.frames[self._frame_index]

    def update_and_get_frame(self) -> pygame.Surface:
        self._update()
        return self.current_frame

    def reset(self):
        self._frame_index = 0
        self._finished = False
        self._finish_time = None
        self._start_time = None
        self._time_prev = pygame.time.get_ticks()

    def _update_frame_index(self):
        if self._frame_index == 0:
            self._start_time = pygame.time.get_ticks()
            self._finish_time = self._start_time + self.duration * 1000
        if self._frame_index == len(self.frames) - 1 and not self.repeat:
            self._finished = True
        else:
            self._frame_index = (self._frame_index + 1) % len(self.frames)

    def _update(self):
        time_now = pygame.time.get_ticks()
        if time_now - self._time_prev > self._frame_time * 1000:  # convert to ms
            self._time_prev = time_now
            self._update_frame_index()

class AnimatedSpriteObject(SpriteObject):
    def __init__(
        self,
        position: tuple[int, int],
        player: "Player",
        frames: list[pygame.Surface],
        shaded: bool,
        animation_duration: float,
    ):
        self.animation = Animation(frames, animation_duration)
        super().__init__(
            position=position,
            texture=self.animation.current_frame,
            player=player,
            shaded=shaded,
        )

    def update(self):
        self.texture = self.animation.update_and_get_frame()
        self.distance = calculate_distance(self.x, self.y, self.player.x, self.player.y)
        self.angle = math.atan2(self.y - self.player.y, self.x - self.player.x)


class Quagmire(AnimatedSpriteObject):
    def __init__(self, position: tuple[int, int], player: "Player"):
        frames = AssetLoader().animated_objects.get("quagmire")
        super().__init__(
            position=position,
            player=player,
            frames=frames,
            shaded=True,
            animation_duration=5,
        )
