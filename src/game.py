import sys
import pygame

from settings import Settings
from drawable import Drawable
from updatable import Updatable
from player import Player
from map import Map


class Game:
    _instance: "Game" = None
    settings: Settings
    clock: pygame.time.Clock
    screen: pygame.Surface
    delta_time: int

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # INITIALIZATION
            cls.settings = Settings()
            pygame.init()
            pygame.mouse.set_visible(False)
            cls.screen = pygame.display.set_mode(cls.settings.RESOLUTION)
            pygame.display.set_caption(cls.settings.CAPTION)
            cls.delta_time = 1
            cls.clock = pygame.time.Clock()
            cls.map = Map(cls._instance)
            cls.player = Player(cls._instance)

        return cls._instance

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

    def update(self):
        Updatable.update_all()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.settings.FPS)

    def draw(self):
        self.screen.fill("black")
        Drawable.draw_all()
