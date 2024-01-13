import sys
import pygame

from raycaster.core import Settings, Drawable, Updatable
from raycaster.game.player import Player
from raycaster.game.map import Map
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

        return cls._instance

    def reset_game(self):
        """
        Reset the game state (e.g., player position, health, etc.)
        """
        self.player.reset()
        self.object_manager.reset()

    def wait_for_reset(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return

    def show_game_over_screen(self):
        """
        Displaing game over Screen with score.
        """
        self.gui_renderer.draw_game_over_screen()

        # Wait for reset
        self.wait_for_reset()

    def run(self):
        """
        The main loop of the game.
        """
        while True:
            if self.player.is_dead():
                self.show_game_over_screen()
            else:
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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.shoot_handler.invoke()

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
        pygame.display.set_caption(
            f"{self.clock.get_fps() :.1f} HEALTH: {self.player.health}"
        )

    def draw(self):
        """
        Renders the game.
        """
        Drawable.draw_all()
