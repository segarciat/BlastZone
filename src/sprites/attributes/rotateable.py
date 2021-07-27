import pygame as pg
import typing

import src.config as cfg
from src.sprites.base_sprite import BaseSprite


class RotateMixin:
    """Mixin class that an object whose class derives from sprite can subclass to obtain rotation behavior."""
    def __init__(self: typing.Union[BaseSprite, 'RotateMixin'], rot_speed=0):
        """Sets the default rotation speed and default image for rotation transformations."""
        # Default rotation is 90 degrees CW
        self.rot = cfg.DEFAULT_IMAGE_ROT
        self.rot_speed = rot_speed
        self._orig_image = self.image

    def rotate(self: typing.Union[BaseSprite, 'RotateMixin'], dt=0) -> None:
        """Updates the rot attribute and rotates the image accordingly."""
        self.rot = (self.rot + self.rot_speed * dt) % 360
        self.rotate_image(self, self._orig_image, self.rot - cfg.DEFAULT_IMAGE_ROT)

    @staticmethod
    def rotate_image(sprite: BaseSprite, image: pg.Surface, angle: float) -> None:
        """Rotates the sprite's image while keeping it centered at the same center-coordinates."""
        old_center = sprite.rect.center
        sprite.image = pg.transform.rotate(image, angle)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = old_center
        sprite.hit_rect.center = sprite.rect.center
