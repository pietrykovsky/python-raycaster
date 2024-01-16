from typing import TYPE_CHECKING
import pygame

from raycaster.core import Settings
from raycaster.const import PLAYER_INIT_HEALTH
from raycaster.game import AssetLoader

if TYPE_CHECKING:
    from raycaster.game import Player, Map
    from raycaster.rendering.raycaster import Raycaster


GRAY = 96, 96, 96
RED = 200, 0, 0
WHITE = 255, 255, 255


class GuiRenderer:
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
        self.font = AssetLoader().load_doom_font(15)

    def _draw_walls_on_minimap(self, surface: pygame.Surface, minimap_scale: float):
        for x, y in self.map.walls:
            pygame.draw.rect(
                surface,
                (255, 255, 255, 255 * self.settings.MINIMAP_OPACITY_RATIO),
                (
                    (x * minimap_scale),
                    y * minimap_scale,
                    minimap_scale,
                    minimap_scale,
                ),
                2,
            )

    def _draw_player_on_minimap(self, surface: pygame.Surface, minimap_cell: float):
        pygame.draw.circle(
            surface,
            (0, 255, 0, 255 * self.settings.MINIMAP_OPACITY_RATIO),
            (
                self.player.x / minimap_cell,
                self.player.y / minimap_cell,
            ),
            5,
        )

    def _draw_rays_on_minimap(self, surface: pygame.Surface, minimap_cell: float):
        rays = self.raycaster.rays
        for ray in rays:
            pygame.draw.line(
                surface,
                (255, 255, 0, 255 * self.settings.MINIMAP_OPACITY_RATIO),
                (
                    ray.x_start / minimap_cell,
                    ray.y_start / minimap_cell,
                ),
                (ray.x_end / minimap_cell, ray.y_end / minimap_cell),
                1,
            )

    def _draw_minimap(self):
        if self.map.cols > self.map.rows:
            # Map is wider than it is tall
            mini_map_width = self.settings.SCREEN_WIDTH * self.settings.MINIMAP_RATIO
            mini_map_scale = mini_map_width / self.map.cols
            mini_map_height = mini_map_scale * self.map.rows
        else:
            # Map is taller than it is wide
            mini_map_height = self.settings.SCREEN_HEIGHT * self.settings.HUD_RATIO
            mini_map_scale = mini_map_height / self.map.rows
            mini_map_width = mini_map_scale * self.map.cols

        mini_map_cell = self.settings.CELL_SIZE / mini_map_scale

        mini_map_position_x = (
            0  # (self.settings.SCREEN_WIDTH - mini_map_width) --> right corner
        )
        mini_map_position_y = (
            0  # (self.settings.SCREEN_HEIGHT - mini_map_height) --> down corner
        )

        additional_surface = pygame.Surface(
            (mini_map_width, mini_map_height), pygame.SRCALPHA
        )
        additional_surface.fill((0, 0, 0, 0))

        self._draw_walls_on_minimap(additional_surface, mini_map_scale)
        self._draw_player_on_minimap(additional_surface, mini_map_cell)
        self._draw_rays_on_minimap(additional_surface, mini_map_cell)

        self.screen.blit(additional_surface, (mini_map_position_x, mini_map_position_y))

    def _draw_health_bar(self):
        bar_width, bar_height = 150, 20
        position_x = self.settings.SCREEN_WIDTH - bar_width - 10
        position_y = self.settings.SCREEN_HEIGHT - bar_height - 10

        health_percentage = self.player.health / PLAYER_INIT_HEALTH
        health_bar_width = int(bar_width * health_percentage)

        # Background
        background_bar_surface = pygame.Surface((bar_width, bar_height))
        background_bar_surface.fill(GRAY)
        self.screen.blit(background_bar_surface, (position_x, position_y))

        # Health bar
        pygame.draw.rect(
            self.screen,
            RED,
            (
                position_x,
                position_y,
                health_bar_width,
                bar_height,
            ),
        )

        health_text_content = f"HEALTH: {int(health_percentage * 100)}%"
        health_text = self.font.render(health_text_content, True, WHITE)
        text_width, text_height = self.font.size(health_text_content)

        text_pos_x = position_x + (bar_width // 2) - (text_width // 2)
        text_pos_y = position_y - text_height - 5

        self.screen.blit(health_text, (text_pos_x, text_pos_y))

    def _scale_element(self, element: pygame.Surface):
        element_width, element_height = element.get_size()
        return pygame.transform.scale(element, (element_width, element_height))

    def _draw_score(self):
        value = self.player.score
        score_text_content = f"SCORE: {value}"
        score_text = self.font.render(score_text_content, True, WHITE)
        text_width, _ = self.font.size(score_text_content)

        text_pos_x = self.settings.SCREEN_WIDTH - text_width - 10
        text_pos_y = 10

        self.screen.blit(score_text, (text_pos_x, text_pos_y))

    def _draw_weapon(self):
        weapon = self.player.weapon
        if not weapon:
            return
        gui_representation = weapon.gui_representation
        x = self.settings.SCREEN_WIDTH / 2 - gui_representation.get_width() / 2
        y = self.settings.SCREEN_HEIGHT - gui_representation.get_height()
        self.screen.blit(gui_representation, (x, y))

    def draw_hud(self):
        if self.settings.MINIMAP_VISIBLE:
            self._draw_minimap()

        self._draw_health_bar()
        self._draw_score()
        self._draw_weapon()

    def draw_game_over_cta(self):
        self._draw_cta_background(AssetLoader().game_over_cta)
        self._draw_center_text(
            "PRESS 'R' TO RESTART", 4 / 20 * self.screen.get_height()
        )
        self._draw_center_text(f"SCORE: {self.player.score}", 5 / 20 * self.screen.get_height())

    def draw_victory_cta(self):
        self._draw_cta_background(AssetLoader().victory_cta)
        self._draw_center_text(
            "PRESS 'R' TO RESTART", 17 / 20 * self.screen.get_height()
        )
        self._draw_center_text(f"SCORE: {self.player.score}", 18 / 20 * self.screen.get_height())

    def draw_start_cta(self):
        self._draw_cta_background(AssetLoader().start_game_cta)
        self._draw_center_text("PRESS 'F' TO START", 18 / 20 * self.screen.get_height())

    def _draw_cta_background(self, background_image: pygame.Surface):
        background_image = pygame.transform.scale(
            background_image, (self.screen.get_width(), self.screen.get_height())
        )
        self.screen.blit(background_image, (0, 0))

    def _draw_center_text(self, text: str, row: int):
        text = self.font.render(text, True, WHITE)
        text_x = (self.screen.get_width() - text.get_width()) // 2
        text_y = row
        self.screen.blit(text, (text_x, text_y))
