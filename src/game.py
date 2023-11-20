import sys
import pygame

from settings import Settings
from drawable import Drawable
from updatable import Updatable
from player import Player
from map import Map
from raycaster import Raycaster
from world_renderer import WorldRenderer
from object_renderer import ObjectRenderer
from gui_renderer import GuiRenderer


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
            cls.map = Map()
            cls.player = Player(cls._instance)
            cls.raycaster = Raycaster(cls.map, cls.player)
            cls.world_renderer = WorldRenderer(cls.screen, cls.raycaster, cls.map)
            cls.object_renderer = ObjectRenderer(cls.screen, cls.player)
            cls.gui_renderer = GuiRenderer(
                cls.screen, cls.map, cls.player, cls.raycaster
            )

        return cls._instance

    def run(self):
        """
        The main loop of the game.
        """
        while True:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        """
        Handles all events.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                self.settings.MINIMAP_VISIBLE = not self.settings.MINIMAP_VISIBLE

            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

    def update(self):
        """
        Updates the game state.
        """
        Updatable.update_all()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.settings.FPS)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        """
        Renders the game.
        """
        Drawable.draw_all()
