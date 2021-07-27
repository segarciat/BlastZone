import pygame as pg
import typing

import src.world.collisions as collision_handler
from src.sprites.base_sprite import BaseSprite

_FRICTION_MU = 4
_EPSILON = 1


class MoveMixin:
    """Mix-in class that an object whose class derives from BaseSprite would subclass to obtain move behavior."""
    def __init__(self: typing.Union[BaseSprite, 'MoveMixin'], x: float, y: float):
        """Assigns a position and velocity vector to """
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0, 0)
        self._hit_wall = False

    @property
    def hit_wall(self) -> bool:
        """Boolean that indicates if this object has collided with a 'wall' (obstacle)."""
        return self._hit_wall

    def move(self: typing.Union[BaseSprite, 'MoveMixin'], dt: float) -> None:
        """Updates this object's position based on the elapsed time, and updates its rectangles' positions"""
        # By default, Movable objects like bullets ignore colliders.
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.hit_rect.center = self.pos


class MoveNonlinearMixin(MoveMixin):
    """Mixin that derives from MoveMixin to also add acceleration to the move behavior."""
    def __init__(self: typing.Union[BaseSprite, 'MoveNonlinearMixin'], x: float, y: float):
        """Assigns a default 0 magnitude acceleration."""
        MoveMixin.__init__(self, x, y)
        self.acc = pg.math.Vector2(0, 0)

    def move(self: typing.Union[BaseSprite, 'MoveNonlinearMixin'], dt: float) -> None:
        """Updates the acceleration, velocity, and position of this object, and handles collisions."""
        # Simulate friction.
        self.acc -= _FRICTION_MU * self.vel

        # Effect kinematic equations.
        self.vel += self.acc * dt
        if self.vel.length_squared() < _EPSILON:
            self.vel.x = 0
            self.vel.y = 0
            displacement = pg.math.Vector2(0, 0)
        else:
            displacement = (self.vel * dt) + (0.5 * self.acc * dt**2)
        self._hit_wall = collision_handler.handle_obstacle_collisions(self, displacement)
