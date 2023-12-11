from typing import TYPE_CHECKING
import math
import pygame

from raycaster.core import Settings
from raycaster.utils import calculate_distance
from raycaster.objects.sprite_object import SpriteObject

if TYPE_CHECKING:
    from raycaster.game import Player


class AnimatedSpriteObject(SpriteObject):
    def __init__(
        self,
        position: tuple[int, int],
        frames: list[pygame.Surface],
        player: "Player",
        shaded: bool = True,
        *,
        animation_duration: float,
    ):
        self.frames = frames
        self.current_frame_index = 0
        self.animation_duration = animation_duration  # in seconds
        self.frame_time = animation_duration / len(self.frames)
        self.time_prev = pygame.time.get_ticks()
        super().__init__(position, frames[self.current_frame_index], player, shaded)

    def _update_texture(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.time_prev > self.frame_time * 1000:  # convert to ms
            self.time_prev = time_now
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.texture = self.frames[self.current_frame_index]

    def update(self):
        self._update_texture()
        self.distance = calculate_distance(self.x, self.y, self.player.x, self.player.y)
        self.angle = math.atan2(self.y - self.player.y, self.x - self.player.x)
