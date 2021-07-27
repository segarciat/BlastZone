import pygame as pg


class InputState:
    """Class used to updating and probing the state of the mouse and key presses.

    The class stores the inputs of the current frame and the previous to distinguish between four different input
    states.

    Implementation based on the content in Chapter 5: Input of Game Programming Algorithms and Techniques by
    Sanjay Madhav.
    """
    STILL_RELEASED, JUST_PRESSED, STILL_PRESSED, JUST_RELEASED = 0, 1, 2, 3
    MOUSE_LEFT, MOUSE_CENTER, MOUSE_RIGHT = 0, 1, 2

    def __init__(self):
        # Keyboard state boolean list.
        self._current_keys = pg.key.get_pressed()
        self._prev_keys = None

        # Mouse state boolean list.
        self.current_mouse = pg.mouse.get_pressed(num_buttons=3)
        self.prev_mouse = None

    def update(self):
        """Stores the previous mouse and key states, and sets their new states."""
        self._prev_keys = self._current_keys
        self._current_keys = pg.key.get_pressed()

        self.prev_mouse = self.current_mouse
        self.current_mouse = pg.mouse.get_pressed(num_buttons=3)

    def get_key_state(self, keycode: int) -> int:
        """Returns the current state of the keyboard whose keycode has been specified."""
        return self._get_state(self._prev_keys, self._current_keys, keycode)

    def get_mouse_state(self, button: int) -> int:
        """Returns the current state of the mouse button specified."""
        return self._get_state(self.prev_mouse, self.current_mouse, button)

    @classmethod
    def _get_state(cls, prev, current, keycode):
        """Gets the current state of the keycode specified."""
        if prev[keycode]:
            if current[keycode]:
                return InputState.STILL_PRESSED
            else:
                return InputState.JUST_RELEASED
        else:
            if current[keycode]:
                return InputState.JUST_PRESSED
            else:
                return InputState.STILL_RELEASED


# Global object for checking input states.
_input_state = InputState()
# Interface methods for the global InputState object.
get_key_state = _input_state.get_key_state
get_mouse_state = _input_state.get_mouse_state
update = _input_state.update
