from enum import Enum
from typing import TYPE_CHECKING
import pygame
from raycaster.core import Updatable, Drawable, Settings
from raycaster.const import PlayerState


if TYPE_CHECKING:
    from raycaster.game.player import Player
    from raycaster.objects import ObjectManager
    from raycaster.rendering.gui_renderer import GuiRenderer


class GameState(Enum):
    START = 0
    GAMEPLAY = 1
    GAME_OVER = 2
    VICTORY = 3


class GameStateManager:
    _instance = None

    def __new__(
        cls,
        player: "Player",
        object_manager: "ObjectManager",
        gui_renderer: "GuiRenderer",
    ):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.player = player
            cls.object_manager = object_manager
            cls.gui_renderer = gui_renderer
            cls.settings = Settings()
            cls.current_state = GameState.START
        return cls._instance

    @classmethod
    def handle_events(cls, event: pygame.event.Event):
        if cls.current_state == GameState.START:
            cls._handle_start_game_events(event)
        elif cls.current_state == GameState.GAMEPLAY:
            cls._handle_gameplay_events(event)
        elif (
            cls.current_state == GameState.GAME_OVER
            or cls.current_state == GameState.VICTORY
        ):
            cls._handle_restart_game_events(event)
        else:
            raise ValueError("Unknown state")

    @classmethod
    def update(cls):
        if cls.current_state == GameState.GAMEPLAY:
            cls._update_gameplay()

    @classmethod
    def draw(cls):
        if cls.current_state == GameState.GAMEPLAY:
            Drawable.draw_all()
            cls.gui_renderer.draw_hud()
        elif cls.current_state == GameState.GAME_OVER:
            cls.gui_renderer.draw_game_over_cta()
        elif cls.current_state == GameState.VICTORY:
            cls.gui_renderer.draw_victory_cta()
        elif cls.current_state == GameState.START:
            cls.gui_renderer.draw_start_cta()
        else:
            raise ValueError("Unknown state")

    @classmethod
    def _reset_game(cls):
        cls.player.reset()
        cls.object_manager.reset()

    @classmethod
    def _handle_gameplay_events(cls, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
            cls.settings.MINIMAP_VISIBLE = not cls.settings.MINIMAP_VISIBLE
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if cls.player.weapon is not None and cls.player.weapon.can_shoot():
                cls.player.shoot_handler.invoke()

    @classmethod
    def _handle_start_game_events(cls, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            cls.current_state = GameState.GAMEPLAY

    @classmethod
    def _handle_restart_game_events(cls, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            cls.current_state = GameState.GAMEPLAY
            cls._reset_game()

    @classmethod
    def _update_gameplay(cls):
        Updatable.update_all()
        if cls.player.is_dead():
            cls.current_state = GameState.GAME_OVER
            cls.player.sounds.get(PlayerState.DEATH).play()
        elif len(cls.object_manager.enemies) == 0:
            cls.current_state = GameState.VICTORY
            cls.player.sounds.get(PlayerState.VICTORY).play()
