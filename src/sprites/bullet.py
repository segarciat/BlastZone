import typing
import pygame as pg

import src.config as cfg
from src.sprites.base_sprite import BaseSprite
from src.sprites.attributes.movable import MoveMixin
from src.sprites.attributes.rotateable import RotateMixin
from src.utils.timer import Timer


_IMAGES = {
    "standard": {color: f"bullet{color}1.png" for color in cfg.TANK_COLORS},
    "power": {color: f"bullet{color}2.png" for color in cfg.TANK_COLORS},
    "rapid": {color: f"bullet{color}3.png" for color in cfg.TANK_COLORS}
}
_STATS = {
    "standard": {"damage": 8, "speed": 500, "lifetime": 750},
    "rapid": {"damage": 6, "speed": 600, "lifetime": 750},
    "power": {"damage": 10, "speed": 400, "lifetime": 750}
}


# TODO: Consider implementing a humming bullet.
class Bullet(BaseSprite, MoveMixin):
    """Sprite class that models a Bullet object."""
    IMAGE_ROT = 90  # See sprite sheet.

    def __init__(self, x: float, y: float, angle: float, color: str, category: str, owner,
                 all_groups: typing.Dict[str, pg.sprite.Group]):
        """Creates a bullet object, rotating it to face the correct direction."""
        self._layer = cfg.ITEM_LAYER
        BaseSprite.__init__(self, _IMAGES[category][color], all_groups, all_groups['all'], all_groups['bullets'])
        MoveMixin.__init__(self, x, y)
        self.vel = pg.math.Vector2(_STATS[category]["speed"], 0).rotate(-angle)
        self._damage = _STATS[category]["damage"]
        self._lifetime = _STATS[category]["lifetime"]
        self._spawn_timer = Timer()
        self._owner = owner
        RotateMixin.rotate_image(self, self.image, angle - Bullet.IMAGE_ROT)

    @property
    def owner(self):
        """Returns the owner sprite that triggered the creation of this bullet, i.e., a Tank object.
        :return: A sprite that triggered the firing of this bullet.
        """
        return self._owner

    @classmethod
    def range(cls, category: str) -> float:
        """Returns the range that this bullet can travel before it vanishes."""
        return _STATS[category]["speed"] * (_STATS[category]["lifetime"] / 1000)

    @property
    def damage(self) -> int:
        """Returns the damage that this bullet can cause upon collision."""
        return self._damage

    def update(self, dt) -> None:
        """Moves the bullet until it's time for it to disappear."""
        if self._spawn_timer.elapsed() > self._lifetime:
            self.kill()
        else:
            self.move(dt)
