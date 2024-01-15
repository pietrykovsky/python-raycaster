import sys
import pygame

from raycaster.core import Settings, Drawable, Updatable
from raycaster.game.player import Player
from raycaster.game.map import Map
from raycaster.rendering import WorldRenderer, GuiRenderer, Raycaster
from raycaster.objects import ObjectManager
from raycaster import const
from raycaster.game.game_state_manager import GameStateManager


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
                cls._instance, cls.player, cls.object_manager, cls.gui_renderer
            )
            cls.game_state_manager.change_state("gameplay")

        return cls._instance

    def run(self):
        while True:
            self.game_state_manager.update(self.delta_time)
            self.game_state_manager.draw(self.screen)
            pygame.display.flip()
            self.delta_time = self.clock.tick(self.settings.FPS)

    def handle_events(self):
        """
        Handles all events.
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                self.settings.MINIMAP_VISIBLE = not self.settings.MINIMAP_VISIBLE

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.shoot_handler.invoke()

            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

    def update_game_state(self, delta_time):
        Updatable.update_all()
        self.delta_time = delta_time

    def draw_game_state(self, screen):
        Drawable.draw_all()
