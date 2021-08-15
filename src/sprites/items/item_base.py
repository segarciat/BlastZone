import typing
import abc
import pygame as pg
import pytweening as tween

import src.services.sound as sfx_loader
from src.sprites.base_sprite import BaseSprite
from src.utils.timer import Timer


class Item(BaseSprite, metaclass=abc.ABCMeta):
    """An abstract base class for sprites that represent in-game items."""
    # Number of pixels up and down that item will bob.
    BOB_RANGE = 15
    BOB_SPEED = 0.2

    def __init__(self, x: float, y: float, image: str, sound: str, groups: typing.Dict[str, pg.sprite.Group]):
        BaseSprite.__init__(self, image, groups, groups['all'], groups['items'])
        self.rect.center = (x, y)
        self._sfx = sound
        self._spawn_pos = pg.math.Vector2(x, y)
        self._effect_timer = Timer()
        # Default duration is 0.
        self._duration = 0
        # Tween function maps integer steps to values between 0 and 1.
        self._tween = tween.easeInOutSine
        self._step = 0
        self._direction = 1

    @property
    def spawn_pos(self) -> pg.math.Vector2:
        return self._spawn_pos

    def update(self, dt: float) -> None:
        """Floating animation for an item that has spawned. Credits to Chris Bradfield from KidsCanCode."""
        # Shift bobbing y offset to bob about item's original center.
        offset = Item.BOB_RANGE * (self._tween(self._step / Item.BOB_RANGE) - 0.5)
        self.rect.centery = self._spawn_pos.y + offset * self._direction
        self._step += Item.BOB_SPEED
        # Reverse bobbing direction when item returns to center.
        if self._step > Item.BOB_RANGE:
            self._step = 0
            self._direction *= -1

    def activate(self, sprite: pg.sprite.Sprite) -> None:
        """Applies the item's effect upon pickup and causes it to be stop being drawn."""
        self._apply_effect(sprite)
        self._effect_timer.restart()
        # Applies to items with non-zero duration.
        sfx_loader.play(self._sfx)
        # Make sure it doesn't get drawn anymore after the effect has been applied.
        super().kill()

    def effect_subsided(self) -> bool:
        """Checks if the item's effect should subside."""
        return self._effect_timer.elapsed() > self._duration

    @abc.abstractmethod
    def _apply_effect(self, sprite) -> None:
        """Effect that is applied on item as long as the timer has not subsided."""
        pass

    def remove_effect(self, sprite) -> None:
        """Causes an item with a non-zero duration to have its effect removed from a sprite at the end."""
        pass
