import src.config as cfg
from src.sprites.base_sprite import BaseSprite
from src.sprites.attributes.rotateable import RotateMixin
from src.utils.timer import Timer


class MuzzleFlash(BaseSprite, RotateMixin):
    """Sprite that models the flash (or explosion) at the barrel's nozzle upon firing a bullet."""
    FLASH_DURATION = 25
    IMAGE = 'shotLarge.png'

    def __init__(self, x: float, y: float, rot: float, all_groups):
        """Aligns the MuzzleFlash so that it starts at the tip of the Barrel nozzle."""
        self._layer = cfg.EFFECTS_LAYER
        BaseSprite.__init__(self, MuzzleFlash.IMAGE, all_groups, all_groups['all'])
        RotateMixin.__init__(self)
        self.rect.center = (x, y)
        self.rot = rot
        self.rotate()
        self._spawn_timer = Timer()

    def update(self, dt: float) -> None:
        """Remove the flash from screen after a short duration."""
        if self._spawn_timer.elapsed() > MuzzleFlash.FLASH_DURATION:
            self.kill()
