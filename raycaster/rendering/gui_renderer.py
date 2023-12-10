from typing import TYPE_CHECKING
import pygame

from raycaster.core import Settings, Drawable

if TYPE_CHECKING:
    from raycaster.game import Player, Map
    from raycaster.rendering.raycaster import Raycaster


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

    def _draw_walls(self, surface: pygame.Surface):
        scale_mini_map = self.settings.MINIMAP_SCALE

        for x, y in self.map.walls:
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                (
                    (x * scale_mini_map),
                    y * scale_mini_map,
                    scale_mini_map,
                    scale_mini_map,
                ),
                2,
            )

    def _draw_player(self, surface: pygame.Surface):
        scale_player_position = self.settings.MINIMAP_CELL
        pygame.draw.circle(
            surface,
            "green",
            (
                self.player.x / scale_player_position,
                self.player.y / scale_player_position,
            ),
            5,
        )

    def _draw_rays(self, surface: pygame.Surface):
        scale_player_position = self.settings.MINIMAP_CELL
        rays = self.raycaster.rays

        for ray in rays:
            pygame.draw.line(
                surface,
                "yellow",
                (
                    ray.x_start / scale_player_position,
                    ray.y_start / scale_player_position,
                ),
                (ray.x_end / scale_player_position, ray.y_end / scale_player_position),
                1,
            )

    def draw(self):
        if self.settings.MINIMAP_VISIBLE:
            mini_map_width = self.settings.MINIMAP_WIDTH
            mini_map_height = self.settings.MINIMAP_HEIGHT
            mini_map_position_x = (
                0  # (self.settings.SCREEN_WIDTH - mini_map_width) --> right corner
            )
            mini_map_position_y = (
                0  # (self.settings.SCREEN_HEIGHT - mini_map_height) --> down corner
            )

            additional_surface = pygame.Surface((mini_map_width, mini_map_height))
            additional_surface.fill((0, 0, 0))

            self._draw_walls(additional_surface)
            self._draw_player(additional_surface)
            self._draw_rays(additional_surface)

            additional_surface.set_alpha(50)
            self.screen.blit(
                additional_surface, (mini_map_position_x, mini_map_position_y)
            )
