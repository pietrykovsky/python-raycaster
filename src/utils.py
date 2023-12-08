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


def calculate_shade_factor(
    distance: float
) -> float:
    """
    Calculates the shade of the color based on the distance.

    :param distance: length of the ray
    :return: shaded color with alpha channel
    """
    if distance <= Settings().MAX_DISTANCE:
        max_distance = Settings().MAX_DISTANCE
        shade_factor = (max_distance - distance) / max_distance
        return shade_factor
    return 0


def shade_surface(surface: pygame.Surface, shade_factor: float):
    """
    Shades the surface by darkening it.

    :param surface: Texture surface to be shaded.
    :param shade_factor: Factor to shade the surface with, ranging from 0 to 1.
    """
    # Create a shading surface with the same size as the original and with SRCALPHA to support alpha channel
    shading_surface = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)
    
    # Calculate the shade color, where alpha is determined by the shade_factor
    shade_color = (int(255*shade_factor), int(255*shade_factor), int(255*shade_factor), 255)

    # Fill the shading surface with the shade color
    shading_surface.fill(shade_color)

    # Blend the shading surface with the original surface using multiply blend mode
    surface.blit(shading_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
