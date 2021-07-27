import abc
import pygame as pg

import src.utils.constants as constants


class AIMob(metaclass=abc.ABCMeta):
    """Abstract base class for a game AI."""
    def __init__(self, sprite, target):
        """Sets the sprite to be controlled by the AI and the sprite that the AI is targeting.

        :param sprite: pygame Sprite to be controlled by AI
        :param target: pygame Sprite to be targeted by AI
        """
        self._sprite = sprite
        self.target = target
        self._state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        """Transitions the AI from one state to another."""
        if self._state:
            self._state.exit()
        self._state = state
        self._state.enter()

    @property
    def sprite(self):
        return self._sprite

    @property
    def ray_to_target(self) -> pg.math.Vector2:
        return self.target.pos - self._sprite.pos

    def update(self, dt: float) -> None:
        """Updates the behavior of the AI based on the current state."""
        self._state.update(dt)

    def is_target_in_range(self) -> None:
        """Determines if the target is in range."""
        return self.target.alive() and \
            self.ray_to_target.length_squared() < self._sprite.range ** 2

    def angle_to_target(self) -> float:
        """Determines the direction of the target relative to AI's sprite."""
        return self.ray_to_target.angle_to(constants.UNIT_VEC)
