from typing import TYPE_CHECKING
import math
import pygame

from raycaster.utils import calculate_distance
from raycaster.objects.sprite_object import SpriteObject
from raycaster.game import AssetLoader

if TYPE_CHECKING:
    from raycaster.game import Player


class AnimatedSpriteObject(SpriteObject):
    def __init__(
        self,
        position: tuple[int, int],
        player: "Player",
        frames: list[pygame.Surface],
        shaded: bool,
        animation_duration: float,
    ):
        self.frames = frames
        self.animation_duration = animation_duration  # in seconds
        self.current_frame_index = 0
        self.frame_time = animation_duration / len(self.frames)
        self.time_prev = pygame.time.get_ticks()
        super().__init__(
            position=position,
            texture=frames[self.current_frame_index],
            player=player,
            shaded=shaded,
        )

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
