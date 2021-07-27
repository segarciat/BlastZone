import pygame as pg

from src.sprites.barrel import Barrel
from src.sprites.obstacles import Barricade
from src.sprites.attributes.damageable import DamageMixin


class Turret(Barricade, DamageMixin):
    """Represents a barrel at stands in one place, which can be controlled by others to attack,"""
    def __init__(self, x, y, category, special, all_groups):
        Barricade.__init__(self, x, y, all_groups)
        DamageMixin.__init__(self, self.hit_rect)
        all_groups['damageable'].add(self)
        img_file = f'specialBarrel{special}.png'
        offset = pg.math.Vector2(0, 0)
        self._barrel = Barrel(self, offset, img_file, "Dark", category, all_groups)
        self.pos = self.rect.center

    @property
    def barrel(self) -> Barrel:
        """Returns the barrel that belongs tot he barrel."""
        return self._barrel

    @property
    def range(self) -> float:
        """Returns the range of the Turret's barrel, i.e., how far its bullets reach."""
        return self._barrel.range

    def kill(self) -> None:
        self._barrel.kill()
        # kill the barricade?
        super().kill()

    def fire(self, angle: float) -> None:
        """Causes the Turret's barrel to turn in a certain direction and fire a bullet."""
        # TODO: Make it so that it rotates slowly?
        self._barrel.rot = angle
        self._barrel.rotate()
        self._barrel.fire()
