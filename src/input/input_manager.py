import os
import json
import pygame as pg

import src.input.input_state as input_state


class InputManager:
    """Class that handles the active bindings in the game.

    Implementation based on the content in Chapter 5: Input of Game Programming Algorithms and Techniques by
    Sanjay Madhav.
    """
    def __init__(self):
        """Reads in key bindings from JSON file."""
        self._key_bindings = {}
        self._active_bindings = {}
        self._mouse_state = {}
        self.load_bindings()

    @property
    def active_bindings(self):
        return self._active_bindings

    @property
    def mouse_state(self):
        return self._mouse_state

    def load_bindings(self, filename='key_bindings.json'):
        """Loads the key bindings for the game from a json file.

        :param filename: The name of the file from which to load the keybindings.
        :return: None
        """
        bindings_path = os.path.join(os.path.dirname(__file__), filename)
        with open(bindings_path, 'r') as f:
            self._key_bindings = json.load(f)

        # Convert keycodes to ASCII codes (pygame enums).
        for bindings in self._key_bindings.values():
            for binding in bindings:
                binding['keycode'] = ord(binding['keycode'])

    def update_inputs(self):
        """Updates the input state since the last update, and stores any active key bindings."""
        # Update key and mouse state.
        input_state.update()

        # Clear bindings from last frame.
        self._mouse_state.clear()
        self._active_bindings.clear()

        # Store active key bindings.
        for button in pg.mouse.get_pressed(num_buttons=3):
            self._mouse_state[button] = input_state.get_mouse_state(button)

        for action, bindings in self._key_bindings.items():
            # Each action may have multiple bindings, i.e move with 'w' or 'up arrow'.
            for binding in bindings:
                if input_state.get_key_state(binding['keycode']) == binding['state_type']:
                    active_action_bindings = self._active_bindings.setdefault(action, [])
                    active_action_bindings.append(binding)


# Global object for input handling; loads the key bindings on-import.
_input_manager = InputManager()
# Interface method with the global input manager object.
update_inputs = _input_manager.update_inputs
load_bindings = _input_manager.load_bindings
active_bindings = _input_manager.active_bindings
mouse_state = _input_manager.mouse_state
