from src.sprites.items.item_base import Item


class AmmoItem(Item):
    """Models an ammo-reload item."""
    IMAGE = 'ammo_item.png'
    SFX = 'reload.wav'

    def __init__(self, x, y, groups):
        Item.__init__(self, x, y, AmmoItem.IMAGE, AmmoItem.SFX, groups)
        self._duration = 10000

    def _apply_effect(self, tank) -> None:
        """Reloads a tank's ammo account."""
        tank.reload()
