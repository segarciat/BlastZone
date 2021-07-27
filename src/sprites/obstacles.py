import pygame as pg

import src.config as cfg
from src.sprites.base_sprite import BaseSprite


class BoundaryWall(pg.sprite.Sprite):
    """Pygame sprite representing a rectangle/wall; meant to be used to make boundaries for the game world."""
    def __init__(self, x: float, y: float, width: float, height: float, all_groups):
        pg.sprite.Sprite.__init__(self, all_groups['all'], all_groups['obstacles'])
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = self.rect


class Tree(BaseSprite):
    """Tree sprite that other sprites can collide with."""
    _IMAGE = 'treeGreen_small.png'

    def __init__(self, x: float, y: float, all_groups):
        self._layer = cfg.ITEM_LAYER
        BaseSprite.__init__(self, Tree._IMAGE, all_groups, all_groups['all'], all_groups['obstacles'])
        self.rect.center = (x, y)

    def update(self, dt: float) -> None:
        """Trees stay in-place and don't move."""
        pass


class Barricade(BaseSprite):
    """Barricade sprite that other sprites can collide with."""
    _IMAGE = 'barricadeMetal.png'

    def __init__(self, x: float, y: float, all_groups):
        BaseSprite.__init__(self, Barricade._IMAGE, all_groups, all_groups['all'], all_groups['obstacles'])
        # Shrink hit-box and recenter.
        self.image = pg.transform.scale(self.image, (4 * self.rect.w // 5, 4 * self.rect.h // 5))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = (x, y)

    def update(self, dt: float) -> None:
        """Barricades stay in-place and don't move."""
        pass
