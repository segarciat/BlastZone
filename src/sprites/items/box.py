import itertools
import random
import typing
import pygame as pg

import src.services.sound as sfx_loader
from src.sprites.base_sprite import BaseSprite
from src.sprites.items.health import HealthItem
from src.sprites.items.ammo import AmmoItem
from src.sprites.items.speed import SpeedItem


class ItemBox(BaseSprite):
    _DISAPPEAR_ALPHA = [alpha for alpha in range(175, 255, 15)]
    BOXES = [
        {'image': 'crateWood.png', 'durability': 2},
        {'image': 'crateMetal.png', 'durability': 4}
    ]
    SFX = 'box.wav'

    def __init__(self, x, y, max_durability, image, groups: typing.Dict[str, pg.sprite.Group]):
        BaseSprite.__init__(self, image, groups, groups['item_boxes'], groups['obstacles'], groups['all'])
        self.rect.center = (x, y)
        self._durability = max_durability
        self._disappear_alpha = itertools.chain(ItemBox._DISAPPEAR_ALPHA * 2)

    def wear_out(self) -> None:
        """Reduces the item's durability count and darkens the box's sprite image."""
        self._durability -= 1
        if self._durability > 0:
            for i in range(10):
                self._darken(255)
        else:
            self.kill()
        """alpha = next(self._disappear_alpha, None)
        if alpha:
            self._darken(alpha)"""

    def is_broken(self) -> bool:
        """Checks if the box's durability is 0, which means it can be broken."""
        return self._durability == 0

    def _darken(self, alpha) -> None:
        """Darkens the box's image in response to a decrease by 1 in durability."""
        self.image.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MULT)

    def update(self, dt) -> None:
        pass

    def kill(self) -> None:
        sfx_loader.play(ItemBox.SFX)
        item_type = random.choice([HealthItem, AmmoItem, SpeedItem])
        item_type(self.rect.centerx, self.rect.centery, self.all_groups)
        super().kill()

    @classmethod
    def spawn(cls, x: float , y: float, all_groups: typing.Dict[str, pg.sprite.Group]) -> None:
        """Creates a box object at the given location."""
        box = random.choice(cls.BOXES)
        cls(x, y, box['durability'], box['image'], all_groups)
