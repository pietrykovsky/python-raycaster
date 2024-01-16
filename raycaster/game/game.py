import sys
import pygame

from raycaster.core import Settings, Drawable, Updatable
from raycaster.game.player import Player
from raycaster.game.map import Map
from raycaster.game.game_state_manager import GameStateManager
from raycaster.rendering import WorldRenderer, GuiRenderer, Raycaster
from raycaster.objects import ObjectManager
from raycaster import const


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
            cls.screen = pygame.display.set_mode(const.RESOLUTION)
            pygame.display.set_caption(cls.settings.CAPTION)
            cls.delta_time = 1
            cls.clock = pygame.time.Clock()
            cls.map = Map()
            cls.player = Player(cls.clock, cls.map)
            cls.raycaster = Raycaster(cls.map, cls.player)
            cls.object_manager = ObjectManager(cls.player, cls.raycaster, cls.map)
            cls.renderer = WorldRenderer(cls.screen, cls.raycaster, cls.map, cls.player)
            cls.gui_renderer = GuiRenderer(
                cls.screen, cls.map, cls.player, cls.raycaster
            )
            cls.game_state_manager = GameStateManager(
                cls.player, cls.object_manager, cls.gui_renderer
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
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

            self.game_state_manager.handle_events(event)

    def update(self):
        """
        Updates the game state.
        """
        self.game_state_manager.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.settings.FPS)
        pygame.display.set_caption(f"{self.clock.get_fps() :.1f}")

    def draw(self):
        """
        Renders the game.
        """
        self.game_state_manager.draw()
