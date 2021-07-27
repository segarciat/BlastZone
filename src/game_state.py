import sys
import abc
import pygame as pg

import src.config as cfg
import src.input.input_manager as input_manager
import src.services.image_loader as image_loader
from src.world.level import Level
from src.utils.timer import Timer


class GameState(metaclass=abc.ABCMeta):
    """Abstract the state of the Game class."""
    def __init__(self, game):
        """Creates a GameState object.

        :param game: Game class whose behavior is driven by this class.
        """
        self._game = game

    @abc.abstractmethod
    def enter(self) -> None:
        """Performs any initial work to transition into this state."""
        pass

    def exit(self) -> None:
        """Performs any necessary clean-up before having the game transition to a new state."""
        pass

    @abc.abstractmethod
    def process_inputs(self) -> None:
        """Fetches any inputs in the queue since last frame and processes them."""
        pass

    @abc.abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        pass


class GameMainMenuState(GameState):
    """Main menu behavior for the Game class."""
    def __init__(self, game):
        """Creates the splash image for the main menu."""
        GameState.__init__(self, game)
        self._menu_splash = pg.transform.scale(image_loader.get_image('blast_zone_splash.png'),
                                               (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))

    def _play(self) -> None:
        """Enters the main gameplay state."""
        self._game.state = self._game.play_state

    def enter(self) -> None:
        """Clears the UI and makes the main menu available."""
        self._game.ui.clear()
        buttons = [
            {'action': self._play, 'text': 'Play', 'size': 16, 'color': cfg.WHITE},
            {'action': sys.exit, 'text': 'Exit', 'size': 16, 'color': cfg.WHITE},
        ]
        self._game.ui.make_menu("Main Menu", 24, cfg.WHITE, buttons)

    def process_inputs(self) -> None:
        """Allows the user to quit out of the game or click on menu options."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        input_manager.update_inputs()
        self._game.ui.process_inputs()

    def update(self, dt: float) -> None:
        """Does nothing."""
        pass

    def draw(self, screen: pg.Surface) -> None:
        """Draws the game splash and the menu on top of it."""
        screen.blit(self._menu_splash, self._menu_splash.get_rect())
        self._game.ui.draw(screen)


class GamePlayingState(GameState):
    """Controls the main in-game (gameplay) behavior of the Game class."""
    def __init__(self, game):
        GameState.__init__(self, game)
        self._level = None
        self._paused = False

    def enter(self) -> None:
        """Creates the game world."""
        # Clear the UI.
        self._game.ui.clear()
        Timer.clear_timers()
        self._level = Level('level_1.tmx')
        self._paused = False

    def _main_menu(self) -> None:
        """Sets the game's state to MainMenu, thus exiting the current state."""
        self._game.state = self._game.main_menu_state

    def _pause(self) -> None:
        """Toggles the pause mode of the game."""
        if self._paused:
            self._game.ui.pop_menu()
            Timer.unpause_timers()
        else:
            buttons = [
                {'action': self._pause, 'text': 'Resume', 'size': 16, 'color': cfg.WHITE},
                {'action': self.enter, 'text': 'Restart', 'size': 16, 'color': cfg.WHITE},
                {'action': self._main_menu, 'text': 'Main Menu', 'size': 16, 'color': cfg.WHITE}
            ]
            self._game.ui.make_menu("Game Paused", 24, cfg.WHITE, buttons)
            Timer.pause_timers()
        self._paused = not self._paused

    def process_inputs(self) -> None:
        """Processes any key and clicks since the last frame."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p and not self._is_game_over():
                    self._pause()
        input_manager.update_inputs()
        self._game.ui.process_inputs()
        if not self._paused:
            self._level.process_inputs()

    def _is_game_over(self):
        """Checks if the player has been defeated or if all mobs have been defeated."""
        return not self._level.is_player_alive() or self._level.mob_count() == 0

    def update(self, dt: float) -> None:
        """Updates the state of the game world and determines if game is over.

        :param dt: Time since last frame.
        :return: None
        """
        if not self._paused:
            self._level.update(dt)
            # If game is over, show game-over menu.
            if self._is_game_over():
                if self._level.is_player_alive():
                    title = "Victory!"
                else:
                    title = "Defeat"
                buttons = [
                    {'action': self.enter, 'text': 'Play Again', 'size': 16, 'color': cfg.WHITE},
                    {'action': self._main_menu, 'text': 'Main Menu', 'size': 16, 'color': cfg.WHITE},
                    {'action': sys.exit, 'text': 'Exit', 'size': 16, 'color': cfg.WHITE}
                ]
                self._game.ui.make_menu(title, 24, cfg.WHITE, buttons)
                Timer.pause_timers()
                self._paused = True

    def draw(self, screen: pg.Surface) -> None:
        """Draws the game's world and UI onto the screen.
        :param screen: pygame Surface object representing the game's screen.
        :return: None
        """
        if not self._paused:
            screen.fill(cfg.WHITE)
            self._level.draw(screen)
        self._game.ui.draw(screen)
