from typing import TYPE_CHECKING
import pygame

from raycaster.core import Settings, Drawable
from raycaster.game import AssetLoader

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
        self.hud_textures = AssetLoader()._hud_face

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
            mini_map_height = self.settings.SCREEN_HEIGHT * self.settings.MINIMAP_RATIO
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

    def _draw_face_on_hud(
        self, hud_height: float, segment_width: float
    ) -> tuple[pygame.Surface, pygame.Rect]:
        # Load the face sprite
        face_sprite = self.hud_textures["face"]
        # Calculate the aspect ratio of the sprite
        face_aspect_ratio = face_sprite.get_width() / face_sprite.get_height()

        face_sprite_max_height = (
            hud_height * 0.8
        )
        face_sprite_max_width = face_sprite_max_height * face_aspect_ratio

        # If the width exceeds the width of one segment, scale it down further
        if face_sprite_max_width > segment_width:
            face_sprite_max_width = segment_width
            face_sprite_max_height = face_sprite_max_width / face_aspect_ratio

        # Scale the sprite to the calculated width and height
        face_sprite = pygame.transform.scale(
            face_sprite, (int(face_sprite_max_width), int(face_sprite_max_height))
        )

        # Get the new rect for the scaled sprite and set its position
        face_sprite_rect = face_sprite.get_rect(
            center=(segment_width * 3 + segment_width // 2, hud_height // 2)
        )

        return face_sprite, face_sprite_rect

    def _render_text_on_hud(
        self, font: pygame.font.Font, text: str, color: tuple[int, int, int]
    ) -> pygame.Surface:
        return font.render(text, True, color)

    def _calculate_position_on_hud(
        self,
        segment_width: int,
        text_width: int,
        text_height: int,
        hud_height: int,
        segment_index: int,
        is_label: bool,
    ) -> tuple[int, int]:
        x_position = segment_width * segment_index + (segment_width - text_width) / 2
        if is_label:
            y_position = hud_height - text_height - 10
        else:
            y_position = 10
        return x_position, y_position

    def _draw_hud(self):
        hud_width = self.settings.SCREEN_WIDTH
        hud_height = self.settings.SCREEN_HEIGHT * self.settings.HUD_RATIO_HEIGHT
        hud_position_x, hud_position_y = 0, self.settings.SCREEN_HEIGHT - hud_height

        hud_surface = pygame.Surface((hud_width, hud_height))
        hud_surface.fill((128, 128, 128))

        font_1 = pygame.font.SysFont("arial", 50)
        font_2 = pygame.font.SysFont("arial", 20)

        data = [("43", "AMMO", 0), ("100%", "HEALTH", 1), ("97%", "ARMOR", 4)]
        # later it will be
        # data = [(f"{self.player.ammo}", "AMMO", 0), (f"{self.player.health}%", "HEALTH", 1), (f"{self.player.armor}%", "ARMOR", 4)]

        segment_width = hud_width // 7

        for value, label, segment_index in data:
            value_text = self._render_text_on_hud(font_1, value, (255, 0, 0))
            label_text = self._render_text_on_hud(font_2, label, (255, 0, 0))

            value_pos = self._calculate_position_on_hud(
                segment_width,
                value_text.get_width(),
                value_text.get_height(),
                hud_height,
                segment_index,
                False,
            )
            label_pos = self._calculate_position_on_hud(
                segment_width,
                label_text.get_width(),
                label_text.get_height(),
                hud_height,
                segment_index,
                True,
            )

            hud_surface.blit(value_text, value_pos)
            hud_surface.blit(label_text, label_pos)

        face_sprite, face_sprite_rect = self._draw_face_on_hud(
            hud_height, segment_width
        )
        hud_surface.blit(face_sprite, face_sprite_rect)

        self.screen.blit(hud_surface, (hud_position_x, hud_position_y))

    def draw(self):
        if self.settings.MINIMAP_VISIBLE:
            self._draw_minimap()
        if self.settings.HUD_VISIBLE:
            self._draw_hud()
