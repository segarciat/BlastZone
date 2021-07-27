import typing
import pygame as pg

import src.config as cfg
import src.services.sound as sfx_loader
import src.utils.helpers as helpers
from src.sprites.base_sprite import BaseSprite
from src.sprites.bullet import Bullet
from src.sprites.attributes.rotateable import RotateMixin
from src.sprites.effects.muzzle_flash import MuzzleFlash
from src.utils.timer import Timer

_STATS = {
    "standard": {"fire_delay": 350, "max_ammo": 20},
    "rapid": {"fire_delay": 250, "max_ammo": 20},
    "power": {"fire_delay": 400, "max_ammo": 20}
}


class Barrel(BaseSprite, RotateMixin):
    """Sprite class that models a Barrel object."""
    _FIRE_SFX = 'shoot.wav'

    def __init__(self, tank, offset: pg.math.Vector2, image: str, color: str,
                 category: str, all_groups: typing.Dict[str, pg.sprite.Group]):
        """Fills up the Barrel's ammo and centers its position on its parent."""
        self._layer = cfg.BARREL_LAYER
        BaseSprite.__init__(self, image, all_groups, all_groups['all'])
        RotateMixin.__init__(self)
        # Bullet parameters.
        self._category = category
        self._color = color
        self._ammo_count = _STATS[self._category]["max_ammo"]

        # Parameters used for barrel position.
        self._parent = tank
        self.rect.center = tank.rect.center
        self._offset = offset

        self._fire_delay = _STATS[self._category]["fire_delay"]
        self._fire_timer = Timer()

    @property
    def color(self) -> str:
        """Returns a string representing the barrel's color."""
        return self._color

    @property
    def ammo_count(self) -> int:
        """Returns the current ammo count for this barrel."""
        return self._ammo_count

    @property
    def range(self) -> float:
        """Returns the fire range of the barrel."""
        return Bullet.range(self._category)

    @property
    def fire_delay(self) -> float:
        """Returns the number of milliseconds until barrel can fire again."""
        return self._fire_delay

    def update(self, dt: float) -> None:
        """Updates the barrel's position by centering on the parent's position (accounting for the offset)."""
        vec = self._offset.rotate(-self.rot)
        self.rect.centerx = self._parent.rect.centerx + vec.x
        self.rect.centery = self._parent.rect.centery + vec.y

    def fire(self) -> None:
        """Fires a Bullet if enough time has passed and if there's ammo."""
        if self._ammo_count > 0 and self._fire_timer.elapsed() > self._fire_delay:
            self._spawn_bullet()
            sfx_loader.play(Barrel._FIRE_SFX)
            self._fire_timer.restart()

    def _spawn_bullet(self) -> None:
        """Spawns a Bullet object from the Barrel's nozzle."""
        fire_pos = pg.math.Vector2(self.hit_rect.height, 0).rotate(-self.rot)
        fire_pos.xy += self.rect.center
        Bullet(fire_pos.x, fire_pos.y, self.rot, self._color, self._category, self._parent, self.all_groups)
        MuzzleFlash(*fire_pos, self.rot, self.all_groups)
        self._ammo_count -= 1

    def reload(self) -> None:
        """Reloads the Barrel to have maximum ammo"""
        self._ammo_count = _STATS[self._category]["max_ammo"]

    def kill(self) -> None:
        self._parent = None
        super().kill()

    @classmethod
    def create_color_barrel(cls, tank, offset: pg.math.Vector2, color: str, category: str,
                            groups: typing.Dict[str, pg.sprite.Group]) -> 'Barrel':
        """Creates a color barrel object."""
        return cls(tank, offset, f"tank{color.capitalize()}_barrel{cfg.CATEGORY[category]}.png", color, category, groups)

    @classmethod
    def create_special(cls, tank, offset: pg.math.Vector2, color: str,
                       all_groups: typing.Dict[str, pg.sprite.Group], special) -> 'Barrel':
        """Creates a special barrel object."""
        barrel = cls(tank, offset, f"specialBarrel{special}.png", color, "standard", all_groups)
        helpers.flip(barrel, orig_image=barrel.image, x_reflect=True, y_reflect=False)
        return barrel
