from src.sprites.items.item_base import Item


class SpeedItem(Item):
    """Models a speed item that increases the target's acceleration."""
    IMAGE = 'speed_item.png'
    SFX = 'speedup.wav'
    BOOST_PCT = 1.8
    DURATION = 10000

    def __init__(self, x, y, groups):
        Item.__init__(self, x, y, SpeedItem.IMAGE, SpeedItem.SFX, groups)
        self._duration = SpeedItem.DURATION

    def _apply_effect(self, tank) -> None:
        """Increases the tank's acceleration by a fixed multiplier."""
        tank.MAX_ACCELERATION *= SpeedItem.BOOST_PCT

    def remove_effect(self, tank) -> None:
        """Decreases the tank acceleration previously applied to the same sprite from before."""
        tank.MAX_ACCELERATION /= SpeedItem.BOOST_PCT
