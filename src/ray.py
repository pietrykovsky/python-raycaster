from dataclasses import dataclass

from settings import Settings


@dataclass
class Ray:
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    length: float = Settings().MAX_DISTANCE
    hit_wall: bool = False
