from settings import Settings


class Map:
    def __init__(self, level: list[list[int]] = None):
        self.level = (
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]
            if level is None
            else level
        )
        self.rows = len(self.level)
        self.cols = len(self.level[0])
        settings = Settings()
        self.cell_width = settings.SCREEN_WIDTH / self.cols
        self.cell_height = settings.SCREEN_HEIGHT / self.rows

    @property
    def walls(self) -> tuple[tuple[int, int]]:
        """
        Gets the coordinates of all walls in the map.

        :return: Walls coordinates
        """
        walls = ()
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if cell != 0:
                    walls.append((x, y))
        return walls

    # def draw(self):
    #     for x, y in self.walls:
    #         pygame.draw.rect(
    #             self.game.screen,
    #             "gray",
    #             (
    #                 x * self.cell_width,
    #                 y * self.cell_height,
    #                 self.cell_width,
    #                 self.cell_height,
    #             ),
    #             2,
    #         )

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
