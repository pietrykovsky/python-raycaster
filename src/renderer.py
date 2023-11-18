import math
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from raycaster import Raycaster
    
from drawable import Drawable
from settings import Settings

class Renderer(Drawable):
    def __init__(self, screen: pygame.Surface, raycaster: "Raycaster"):
        self.screen = screen
        self.raycaster = raycaster
        self.settings = Settings()
        self.wall_textures = self.load_wall_textures()

    # def _calculate_shade(
    #     self, color: tuple[int, int, int], distance: float
    # ) -> tuple[int, int, int]:
    #     if distance != float("inf"):
    #         max_distance = self.settings.MAX_DISTANCE
    #         shade_factor = (max_distance - distance) / max_distance
    #         return (
    #             int(color[0] * shade_factor),
    #             int(color[1] * shade_factor),
    #             int(color[2] * shade_factor),
    #         )
    #     return color

    @staticmethod
    def get_texture(path, res=(64, 64)):
        texture = pygame.image.load(path).convert_alpha()
        return texture

    def load_wall_textures(self):
        return {
            1: self.get_texture("src/textures/C1.png"),
            # 2: self.get_texture('resources/textures/2.png'),
            # 3: self.get_texture('resources/textures/3.png'),
            # 4: self.get_texture('resources/textures/4.png'),
            # 5: self.get_texture('resources/textures/5.png'),
        }

    def draw(self):
        screen_dist = self.settings.SCREEN_DISTANCE
        ray_count = self.settings.RAY_COUNT
        rays = self.raycaster.rays

        for col, ray in enumerate(rays):
            if ray.hit_wall:
                height = screen_dist * self.settings.CELL_SIZE / ray.length
                col_scale = self.settings.SCREEN_WIDTH // ray_count

                # Determine the texture to use
                texture_key = "1"
                if ray.is_horizontal:
                    offset = int(ray.x_end) % self.settings.CELL_SIZE
                else:
                    offset = int(ray.y_end) % self.settings.CELL_SIZE

                width = self.wall_textures[1].get_width()

                wall_column = self.wall_textures[1].subsurface(
                    offset * 2, 0, col_scale / 4, 64
                )

                wall_column = pygame.transform.scale(wall_column, (col_scale, height))

                self.screen.blit(
                    wall_column,
                    (
                        math.ceil(col * col_scale),
                        self.settings.SCREEN_HEIGHT // 2 - height // 2,
                    ),
                )
