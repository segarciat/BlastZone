import typing
import pygame as pg

import src.config as cfg
from src.sprites.base_sprite import BaseSprite
from src.sprites.barrel import Barrel
from src.sprites.effects.tracks import Tracks
from src.sprites.attributes.movable import MoveNonlinearMixin
from src.sprites.attributes.rotateable import RotateMixin
from src.sprites.attributes.damageable import DamageMixin
from src.utils.timer import Timer


class Tank(BaseSprite, MoveNonlinearMixin, RotateMixin, DamageMixin):
    """Sprite class that models a Tank object."""
    KNOCK_BACK = 100

    _SPEED_CUTOFF = 100
    _TRACK_DELAY = 100

    BIG = "big"
    LARGE = "large"
    HUGE = "huge"

    def __init__(self, x: float, y: float, img: str, all_groups: typing.Dict[str, pg.sprite.Group]):
        """Initializes the tank's sprite with no barrels to shoot from.

        :param x: x coordinate for centering the sprite's position.
        :param y: y coordinate for centering the sprite's position.
        :param img: filename for the sprite's tank image.
        :param all_groups: A dictionary of all of the game world's sprite groups.
        """
        self._layer = cfg.TANK_LAYER
        BaseSprite.__init__(self, img, all_groups, all_groups['all'],  all_groups['tanks'], all_groups['damageable'])
        MoveNonlinearMixin.__init__(self, x, y)
        RotateMixin.__init__(self)
        DamageMixin.__init__(self, self.hit_rect)
        self.rect.center = (x, y)
        self.MAX_ACCELERATION = 768
        self._barrels = []
        self._items = []
        self._track_timer = Timer()

    def update(self, dt: float) -> None:
        """Rotates, moves, and handles any active in-game items that have some effect.

        :param dt: Time elapsed since the tank's last update.
        :return: None
        """
        self.rotate(dt)
        self.move(dt)
        for item in self._items:
            if item.effect_subsided():
                item.remove_effect(self)
                self._items.remove(item)
        if self.vel.length_squared() > Tank._SPEED_CUTOFF and self._track_timer.elapsed() > Tank._TRACK_DELAY:
            self._spawn_tracks()

    @property
    def range(self) -> float:
        """The shooting distance of the tank, as given by the tank's barrels."""
        return self._barrels[0].range

    @property
    def color(self) -> str:
        """Returns a string representing the color of one of the tank's barrels."""
        return self._barrels[0].color

    def pickup(self, item) -> None:
        """Activates an item that this Tank object has picked up (collided with) and saves it.

        :param item: Item sprite that can be used to apply an effect on the Tank object.
        :return: None
        """
        item.activate(self)
        self._items.append(item)

    def equip_barrel(self, barrel: Barrel) -> None:
        """Equips a new barrel to this tank."""
        self._barrels.append(barrel)

    def _spawn_tracks(self) -> None:
        """Spawns track sprites as the tank object moves around the map."""
        Tracks(*self.pos, self.hit_rect.height, self.hit_rect.height, self.rot, self.all_groups)
        self._track_timer.restart()

    def rotate_barrel(self, aim_direction: float):
        """Rotates the all of the tank's barrels in a direction indicated by aim_direction."""
        for barrel in self._barrels:
            barrel.rot = aim_direction
            barrel.rotate()

    def ammo_count(self) -> int:
        """Returns the ammo count of the tank's barrels."""
        return self._barrels[0].ammo_count

    def fire(self) -> None:
        """Fires a bullet from the Tank's barrels."""
        for barrel in self._barrels:
            barrel.fire()

    def reload(self) -> None:
        """Reloads bullets for each of the bullets."""
        for barrel in self._barrels:
            barrel.reload()

    def kill(self) -> None:
        """Removes this sprite and its barrels from all sprite groups."""
        for barrel in self._barrels:
            barrel.kill()
        for item in self._items:
            item.kill()
        super().kill()

    @classmethod
    def color_tank(cls, x: float, y: float, color: str, category: str, groups: typing.Dict[str, pg.sprite.Group]):
        """Factory method for creating Tank objects."""
        tank = cls(x, y, f"tankBody_{color}_outline.png", groups)
        offset = pg.math.Vector2(tank.hit_rect.height // 3, 0)
        barrel = Barrel.create_color_barrel(tank, offset, color.capitalize(), category, groups)
        tank.equip_barrel(barrel)
        return tank

    @classmethod
    def enemy(cls, x: float, y: float, size: str, groups: typing.Dict[str, pg.sprite.Group]) -> 'Tank':
        """Returns a enemy tank class depending on the size parameter."""
        if size == cls.BIG:
            return cls.big_tank(x, y, groups)
        elif size == cls.LARGE:
            return cls.large_tank(x, y, groups)
        elif size == cls.HUGE:
            return cls.huge_tank(x, y, groups)
        raise ValueError(f"Invalid size attribute: {size}")

    @classmethod
    def big_tank(cls, x: float, y: float, groups: typing.Dict[str, pg.sprite.Group]) -> 'Tank':
        """Returns the a 'big' enemy tank."""
        tank = cls(x, y, "tankBody_bigRed.png", groups)
        for y_offset in (-10, 10):
            barrel = Barrel.create_special(tank, pg.math.Vector2(0, y_offset), "Dark", groups, special=1)
            tank.equip_barrel(barrel)
        return tank

    @classmethod
    def large_tank(cls, x: float, y: float, groups: typing.Dict[str, pg.sprite.Group]) -> 'Tank':
        """Returns the a 'large' enemy tank."""
        tank = cls(x, y, "tankBody_darkLarge.png", groups)
        tank.MAX_ACCELERATION *= 0.9
        for y_offset in (-10, 10):
            barrel = Barrel.create_special(tank, pg.math.Vector2(0, y_offset), "Dark", groups, special=4)
            tank.equip_barrel(barrel)
        return tank

    @classmethod
    def huge_tank(cls, x: float, y: float, groups: typing.Dict[str, pg.sprite.Group]) -> 'Tank':
        """Returns the a 'huge' enemy tank."""
        tank = cls(x, y, "tankBody_huge_outline.png", groups)
        tank.MAX_ACCELERATION *= 0.8
        for y_offset in (-10, 10):
            barrel = Barrel.create_special(tank, pg.math.Vector2(20, y_offset), "Dark", groups, special=4)
            tank.equip_barrel(barrel)
        barrel = Barrel.create_special(tank, pg.math.Vector2(-10, 0), "Dark", groups, special=1)
        tank.equip_barrel(barrel)
        return tank
