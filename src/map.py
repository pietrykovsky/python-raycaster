from typing import TYPE_CHECKING
import pygame

from drawable import Drawable


if TYPE_CHECKING:
    from game import Game


class Map(Drawable):
    def __init__(self, game: "Game"):
        self.level = [
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
        self.rows = len(self.level)
        self.cols = len(self.level[0])
        self.game = game
        self.cell_width = self.game.settings.SCREEN_WIDTH / self.cols
        self.cell_height = self.game.settings.SCREEN_HEIGHT / self.rows

    @property
    def walls(self) -> list[tuple[int, int]]:
        walls = []
        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                if cell != 0:
                    walls.append((x, y))
        return walls

    def draw(self):
        for x, y in self.walls:
            pygame.draw.rect(
                self.game.screen,
                "gray",
                (
                    x * self.cell_width,
                    y * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                ),
                2,
            )
