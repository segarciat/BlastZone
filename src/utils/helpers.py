import pygame as pg


def clamp(x: float, lo: float, hi: float) -> float:
    """Returns x if it's between lo and hi; otherwise lo if x <lo or hi if x > hi.

    :param x: The value we are testing
    :param lo: The maximum value that x is allowed to be.
    :param hi: The minimum value that x is allowed to be.
    :return: Either lo, hi, or x, depending on how x compares with lo and hi.
    """
    if lo > hi:
        raise ValueError(f"lo:{lo}, hi:{hi}; invalid constraints.")
    if x < lo:
        return lo
    elif x > hi:
        return hi
    else:
        return x


def flip(sprite: pg.sprite.Sprite, orig_image, x_reflect: bool, y_reflect: bool):
    """Flips (reflects) the image for a sprite either horizontally, vertically, or both.

    :param sprite: The pygame Sprite whose image we're flipping.
    :param orig_image: A pygame Surface representing the image we will flip.
    :param x_reflect: A boolean indicating if the image should be flipped horizontally.
    :param y_reflect: A boolean indicating if the image should be flipped vertically.
    :return: None; operations done in-place.
    """
    old_center = sprite.rect.center
    sprite.image = pg.transform.flip(orig_image, x_reflect, y_reflect)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.center = old_center