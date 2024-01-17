from raycaster.core import Settings


class Map:
    def __init__(self, level: list[list[int]] = None):
        self.level = (
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 3, 3, 3, 3, 0, 0, 0, 2, 2, 2, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 1],
                [1, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 3, 1, 3, 1, 1, 1, 4, 0, 0, 4, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 4, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 4, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 4, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 2, 0, 0, 0, 0, 0, 3, 2, 0, 2, 0, 0, 1],
                [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 1],
                [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 1],
                [1, 1, 3, 4, 0, 0, 4, 3, 1, 3, 3, 1, 3, 1, 1, 1],
                [1, 1, 1, 4, 0, 0, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 3, 4, 0, 0, 4, 3, 3, 3, 3, 3, 3, 3, 3, 1],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                [3, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 3],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                [3, 3, 3, 3, 3, 4, 0, 0, 0, 0, 4, 3, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 3, 3, 3, 3, 4, 0, 0, 0, 0, 4, 3, 3, 3, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
                [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
            if level is None
            else level
        )
        self.rows = len(self.level)
        self.cols = len(self.level[0])
        self._walls = self._locate_walls()
        self.settings = Settings()

    def _locate_walls(self) -> list[tuple[int, int]]:
        walls = []
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if cell != 0:
                    walls.append((x, y))
        return walls

    @property
    def walls(self) -> list[tuple[int, int]]:
        """
        Gets the coordinates of all walls in the level.

        :return: Walls coordinates
        """
        return self._walls

    def is_wall(self, x: int, y: int) -> bool:
        """
        Checks if the given coordinates are a wall.

        :param x: column index
        :param y: row index
        :return: True if the given coordinates are a wall, False otherwise
        """
        return (x, y) in self.walls

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        """
        Checks if the given coordinates are out of bounds of the level.

        ::param x: column index
        :param y: row index
        :return: True if the given coordinates are out of bounds of the level, False otherwise
        """
        return x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1

    def to_grid(self, x: float, y: float) -> tuple[int, int]:
        """
        Map x, y values to the map grid.
        """
        return int(x // self.settings.CELL_SIZE), int(y // self.settings.CELL_SIZE)
