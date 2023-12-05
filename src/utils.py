import math
import pygame

from settings import Settings


def calculate_distance(start_x, start_y, end_x, end_y) -> float:
    """
    Calculate distance between 2 points.

    :param start_x: Starting x coordinate
    :param start_y: Starting y coordinate
    :param end_x: Ending x coordinate
    :param end_y: Ending y coordinate
    :return: calculated distance between 2 points
    """
    return math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)


def calculate_shade(
    color: tuple[int, int, int], distance: float
) -> tuple[int, int, int, int]:
    """
    Calculates the shade of the given color based on the distance.

    :param color: color to shade
    :param distance: length of the ray
    :return: shaded color with alpha channel
    """
    if distance <= Settings().MAX_DISTANCE:
        max_distance = Settings().MAX_DISTANCE
        shade_factor = (max_distance - distance) / max_distance
        return (
            int(color[0] * shade_factor),
            int(color[1] * shade_factor),
            int(color[2] * shade_factor),
        )
    return 0, 0, 0, 128


def shade_surface(
    screen: pygame.Surface,
    surface: pygame.Surface,
    position: tuple[int, int],
    shade_color: tuple[int, int, int, int],
):
    """
    Shades the surface.

    :param screen: Screen to blit the surface on
    :param surface: Texture surface
    :param position: Position of the surface on the screen
    :param shade_color: Color to shade the surface with in RGBA format
    """
    shading_surface = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
    shading_surface.blit(surface, (0, 0))
    shading_surface.fill(shade_color, special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(shading_surface, position)
