import pygame as pg

import src.config as cfg
from src.utils.helpers import clamp


class Camera:
    """The Camera class follows a target in the game world."""
    def __init__(self, map_width, map_height, target=None):
        """Sets the target and creates a rectangle with the same size as the game's screen.

        :param map_width: The width of the map in pixels.
        :param map_height: The height of the map in pixels.
        :param target: The sprite used to clamp the position of the camera.
        """
        self.target = target
        self.rect = pg.Rect(0, 0, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
        self.map_width = map_width
        self.map_height = map_height

    def follow(self, target: pg.sprite.Sprite) -> None:
        """Sets the target that the camera will follow.

        :param target: Sprite whose position will be used to clamp the camera's position.
        :return:
        """
        self.target = target

    def update(self) -> None:
        """Clamps the camera position using the target's position so that the target is always visible."""
        self.rect.center = self.target.pos

        self.rect.centerx = clamp(self.target.pos.x, cfg.SCREEN_WIDTH / 2, self.map_width - cfg.SCREEN_WIDTH / 2)
        self.rect.centery = clamp(self.target.pos.y, cfg.SCREEN_HEIGHT / 2, self.map_height - cfg.SCREEN_HEIGHT / 2)

    def apply(self, rect: pg.Rect) -> pg.Rect:
        """Returns a rectangle offset by the camera's position.

        :param rect: pygame rectangle whose position we wish to offset.
        :return: A rectangle whose coordinates are the input's, offset by the camera's.
        """
        return rect.move(-self.rect.x, -self.rect.y)
