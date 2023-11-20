import math


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