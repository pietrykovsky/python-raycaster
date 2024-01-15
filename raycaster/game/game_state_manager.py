import pygame


class GameState:
    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen):
        pass


class GameplayState(GameState):
    def __init__(self, game, player, object_manager):
        self.game = game
        self.player = player
        self.object_manager = object_manager

    def update(self, delta_time):
        if self.game.player.is_dead():
            self.game.game_state_manager.change_state("game_over")
            return

        self.game.handle_events()
        self.game.update_game_state(delta_time)

    def draw(self, screen):
        self.game.draw_game_state(screen)


class GameOverState(GameState):
    def __init__(self, game, gui_renderer):
        self.game = game
        self.gui_renderer = gui_renderer

    def enter(self):
        self.gui_renderer.draw_game_over_screen()

    def update(self, delta_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.game_state_manager.reset_game()


class GameStateManager:
    def __init__(self, game, player, object_manager, gui_renderer):
        self.game = game
        self.player = player
        self.object_manager = object_manager
        self.gui_renderer = gui_renderer
        self.states = {
            "gameplay": GameplayState(game, player, object_manager),
            "game_over": GameOverState(game, gui_renderer),
        }
        self.current_state = None

    def change_state(self, new_state):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[new_state]
        self.current_state.enter()

    def update(self, delta_time):
        if self.current_state:
            self.current_state.update(delta_time)

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)

    def reset_game(self):
        self.player.reset()
        self.object_manager.reset()
        self.change_state("gameplay")
