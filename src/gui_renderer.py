import math
from typing import TYPE_CHECKING
import pygame

from drawable import Drawable
from settings import Settings

if TYPE_CHECKING:
    from player import Player
    from map import Map


class GuiRenderer(Drawable):
    def __init__(
        self,
        screen: pygame.Surface,
        map: "Map",
        player: "Player",
        raycaster: "Raycaster",
    ):
        self.screen = screen
        self.settings = Settings()
        self.raycaster = raycaster
        self.player = player
        self.map = map

    def draw(self):
        mini_map_width = self.settings.SCREEN_WIDTH / 7
        mini_map_height = mini_map_width * 2
        mini_map_position_x = (
            0  # (self.settings.SCREEN_WIDTH - mini_map_width) --> right corner
        )
        mini_map_position_y = (
            0  # (self.settings.SCREEN_HEIGHT - mini_map_height) --> down corner
        )

        scale_mini_map = self.settings.SCREEN_WIDTH / 70
        scale_player_position = self.settings.CELL_SIZE / scale_mini_map

        additional_surface = pygame.Surface((mini_map_width, mini_map_height))
        additional_surface.fill((0, 0, 0))

        for x, y in self.map.walls:
            pygame.draw.rect(
                additional_surface,
                (255, 255, 255),
                (
                    (x * scale_mini_map),
                    y * scale_mini_map,
                    scale_mini_map,
                    scale_mini_map,
                ),
                2,
            )

        pygame.draw.circle(
            additional_surface,
            "green",
            (
                self.player.x / scale_player_position,
                self.player.y / scale_player_position,
            ),
            5,
        )

        rays = self.raycaster.rays

        for ray in rays:
            pygame.draw.line(
                additional_surface,
                "yellow",
                (
                    ray.x_start / scale_player_position,
                    ray.y_start / scale_player_position,
                ),
                (ray.x_end / scale_player_position, ray.y_end / scale_player_position),
                1,
            )

        additional_surface.set_alpha(50)
        self.screen.blit(additional_surface, (mini_map_position_x, mini_map_position_y))
