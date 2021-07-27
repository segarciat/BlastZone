import pygame as pg

import src.config as cfg
# Loads all sprite sheet images and sounds upon import.
import src.services.image_loader
import src.services.sound
from src.game_state import GamePlayingState, GameMainMenuState, GameState
from src.ui.ui import UI


class Game:
    """Top-level game class for running the current pygame application."""
    def __init__(self):
        """Sets the game screen and clock."""
        self._screen = pg.display.get_surface()
        self._clock = pg.time.Clock()
        self._ui = UI()
        self._running = False

        self._play_state = GamePlayingState(self)
        self._main_menu_state = GameMainMenuState(self)
        self._state = None

    @property
    def ui(self) -> UI:
        return self._ui

    @property
    def play_state(self) -> GamePlayingState:
        return self._play_state

    @property
    def main_menu_state(self) -> GameMainMenuState:
        return self._main_menu_state

    @property
    def state(self) -> GameState:
        """Returns the Game object's state."""
        return self._state

    @state.setter
    def state(self, state: GameState) -> None:
        """Exits a game state and enters a new one.

        :param state: GameState which drives the behavior of the Game class.
        :return: None
        """
        if self._state:
            self._state.exit()
        self._state = state
        self._state.enter()

    def run(self) -> None:
        """Runs the game loop: processes inputs, updates, and draws at a frame rate specified in a config file."""
        self._running = True
        self.state = self._main_menu_state
        while self._running:
            dt = self._clock.tick(cfg.FPS) / 1000
            self._state.process_inputs()
            self._state.update(dt)
            self._state.draw(self._screen)
            pg.display.set_caption(f"{cfg.TITLE}: {int(self._clock.get_fps())} (FPS)")
            pg.display.flip()
