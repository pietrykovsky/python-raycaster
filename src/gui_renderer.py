from typing import TYPE_CHECKING
import pygame
from settings import Settings
from drawable import Drawable

if TYPE_CHECKING:
    from player import Player
    from map import Map
    from raycaster import Raycaster


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

    def _draw_minimap_walls(self, surface: pygame.Surface, minimap_scale: float):
        for x, y in self.map.walls:
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                (
                    (x * minimap_scale),
                    y * minimap_scale,
                    minimap_scale,
                    minimap_scale,
                ),
                2,
            )

    def _draw_minimap_player(self, surface: pygame.Surface, minimap_cell: float):
        pygame.draw.circle(
            surface,
            "green",
            (
                self.player.x / minimap_cell,
                self.player.y / minimap_cell,
            ),
            5,
        )

    def _draw_minimap_rays(self, surface: pygame.Surface, minimap_cell: float):
        rays = self.raycaster.rays
        for ray in rays:
            pygame.draw.line(
                surface,
                "yellow",
                (
                    ray.x_start / minimap_cell,
                    ray.y_start / minimap_cell,
                ),
                (ray.x_end / minimap_cell, ray.y_end / minimap_cell),
                1,
            )

    def _draw_minimap(self):
        # Check if the map is wider or taller
        if self.map.cols > self.map.rows:
            # Map is wider than it is tall
            mini_map_width = (
                self.settings.SCREEN_WIDTH * self.settings.MINIMAP_RATIO_WIDTH
            )
            mini_map_scale = mini_map_width / self.map.cols
            mini_map_height = mini_map_scale * self.map.rows
        else:
            # Map is taller than it is wide
            mini_map_height = (
                self.settings.SCREEN_HEIGHT * self.settings.MINIMAP_RATIO_HEIGHT
            )
            mini_map_scale = mini_map_height / self.map.rows
            mini_map_width = mini_map_scale * self.map.cols

        mini_map_cell = self.settings.CELL_SIZE / mini_map_scale

        mini_map_position_x = (
            0  # (self.settings.SCREEN_WIDTH - mini_map_width) --> right corner
        )
        mini_map_position_y = (
            0  # (self.settings.SCREEN_HEIGHT - mini_map_height) --> down corner
        )

        additional_surface = pygame.Surface((mini_map_width, mini_map_height))
        additional_surface.fill((0, 0, 0))

        self._draw_minimap_walls(additional_surface, mini_map_scale)
        self._draw_minimap_player(additional_surface, mini_map_cell)
        self._draw_minimap_rays(additional_surface, mini_map_cell)

        additional_surface.set_alpha(50)
        self.screen.blit(additional_surface, (mini_map_position_x, mini_map_position_y))

    def draw(self):
        if self.settings.MINIMAP_VISIBLE:
            self._draw_minimap()
