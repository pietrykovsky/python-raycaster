import sys
import pygame

from raycaster.core import Settings, Drawable, Updatable
from raycaster.game.player import Player
from raycaster.game.map import Map
from raycaster.rendering import WorldRenderer, GuiRenderer, Raycaster


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
            Settings().ORIGINAL_SCREEN_HEIGHT = Settings().SCREEN_HEIGHT
            cls.screen = pygame.display.set_mode(
                (Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT), pygame.FULLSCREEN
            )
            pygame.display.set_caption(cls.settings.CAPTION)
            cls.delta_time = 1
            cls.clock = pygame.time.Clock()
            cls.map = Map()
            cls.player = Player(cls.clock, cls.map)
            cls.raycaster = Raycaster(cls.map, cls.player)
            cls.renderer = WorldRenderer(cls.screen, cls.raycaster, cls.map, cls.player)
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

    def _handle_window_resize(self, event: pygame.event.Event):
        Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT = event.w, event.h
        self.screen = pygame.display.set_mode(
            (Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT), pygame.RESIZABLE
        )

    def _change_screen_mode(self):
        Settings().FULLSCREEN_MODE = not Settings().FULLSCREEN_MODE
        if Settings().FULLSCREEN_MODE:
            self.screen = pygame.display.set_mode(
                (Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT), pygame.FULLSCREEN
            )
            Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT = self.screen.get_size()
        else:
            Settings().SCREEN_WIDTH = int(
                Settings().MINIMIZE_RATIO * Settings().SCREEN_WIDTH
            )
            Settings().SCREEN_HEIGHT = int(
                Settings().MINIMIZE_RATIO * Settings().SCREEN_HEIGHT
            )
            self.screen = pygame.display.set_mode(
                (Settings().SCREEN_WIDTH, Settings().SCREEN_HEIGHT), pygame.RESIZABLE
            )

    def handle_events(self):
        """
        Handling events and switch betwenn screen modes
        """
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE and not Settings().FULLSCREEN_MODE:
                self._handle_window_resize(event)

            elif event.type == pygame.KEYDOWN:
                # Toggle full screen mode
                if event.key == pygame.K_F11:
                    self._change_screen_mode()
                elif event.key == pygame.K_F4:
                    Settings().MINIMAP_VISIBLE = not Settings().MINIMAP_VISIBLE
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

            elif event.type == pygame.QUIT:
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
