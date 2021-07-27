import pygame as pg
import typing

import src.config as cfg
from src.sprites.base_sprite import BaseSprite


_MAX_HEALTH = 100


class DamageMixin:
    """Mixin class that an object whose class is BaseSprite can subclass to obtain health-related attributes."""
    MAX_HEALTH = 100

    def __init__(self: typing.Union[BaseSprite, 'DamageMixin'], hit_rect):
        """Assigns a maximum health dan a hit_rect attribute to the sprite."""
        self.health = self.MAX_HEALTH
        self.hit_rect = hit_rect

    def heal(self, pct: float) -> None:
        """Heals the sprite's health by a specified amount."""
        if pct < 0:
            raise ValueError(f"Expected non-negative percent value, but received {pct}")
        self.health += int(pct * self.MAX_HEALTH)
        if self.health > self.MAX_HEALTH:
            self.health = self.MAX_HEALTH

    def inflict_damage(self, amount: float) -> None:
        """Causes the sprite's health to be reduced by a specified amount."""
        if amount < 0:
            raise ValueError(f"Expected non-negative health recovery amount, but received {amount}")
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw_health(self, surface: pg.Surface, camera, outline_rect=None) -> None:
        """Draw's a health bar display on the sprite."""
        # surface is generally the screen we draw on.
        pct = self.health / self.MAX_HEALTH
        color = cfg.TRANSPARENT
        if pct > 0.7:
            color = cfg.GREEN
        elif pct > 0.3:
            color = cfg.YELLOW
        elif pct > 0:
            color = cfg.RED

        if outline_rect:
            fill_rect = outline_rect.copy()
        else:
            fill_rect = self.hit_rect.copy()
            fill_rect.height = fill_rect.height // 3
            outline_rect = fill_rect.copy()

        fill_rect.width *= pct

        pg.draw.rect(surface, color, camera.apply(fill_rect))
        pg.draw.rect(surface, cfg.BLACK, camera.apply(outline_rect), 2)
