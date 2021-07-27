import random

from src.sprites.items.item_base import Item


class HealthItem(Item):
    """Class that models a health item that a sprite can pick up to recover health."""
    _IMAGE = 'health_item.png'
    _SFX = 'heal.wav'
    MIN_HEAL_PCT = 0.1
    MAX_HEAL_PCT = 0.2

    def __init__(self, x, y, groups):
        Item.__init__(self, x, y, HealthItem._IMAGE, HealthItem._SFX, groups)

    def _apply_effect(self, tank) -> None:
        """Recovers a small percentage of the tank's health."""
        pct = HealthItem.MIN_HEAL_PCT + random.random() * (HealthItem.MAX_HEAL_PCT - HealthItem.MIN_HEAL_PCT)
        tank.heal(pct)
