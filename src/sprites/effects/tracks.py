import typing
import pygame as pg

import src.config as cfg
from src.sprites.base_sprite import BaseSprite


class Tracks(BaseSprite):
    """Sprite that models the tracks that a tank leaves behind on the ground after moving."""
    IMAGE = 'tracksSmall.png'
    IMG_ROT = -90

    def __init__(self, x, y, scale_h, scale_w, rot, groups: typing.Dict[str, pg.sprite.Group]):
        """Sets the sprite's position and angle value so that it matches and trails the tank's path."""
        self._layer = cfg.TRACKS_LAYER
        BaseSprite.__init__(self, Tracks.IMAGE, groups, groups['all'])
        # Transform and recenter.
        self.image = pg.transform.rotate(self.image, rot - Tracks.IMG_ROT)
        self.image = pg.transform.scale(self.image, (scale_h, scale_w))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._alpha = 255

    def update(self, dt: float) -> None:
        """Increases the transparency of the tracks until it fades out, at which point we stop drawing."""
        # Fade effect.
        if self._alpha > 0:
            self._alpha -= 4
            self.image.set_alpha(self._alpha)
        else:
            self.kill()
