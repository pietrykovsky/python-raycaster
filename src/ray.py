from dataclasses import dataclass

from settings import Settings


@dataclass
class Ray:
    x_start: float
    y_start: float
    x_end: float | None = None
    y_end: float | None = None
    length: float = Settings().MAX_DISTANCE
    is_horizontal: bool = False
    hit_wall: bool = False
    texture_id: int | None = None
