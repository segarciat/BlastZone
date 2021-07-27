"""Loads sprite sheet from top-level config.py file upon import"""
import sys
import os
import xml.etree.ElementTree as ElementTree
import pygame as pg

import src.config as cfg


class _ImageLoader:
    """Provides a simple interface for getting a sprite surface."""
    def __init__(self, *sprite_sheets):
        """ Loads all sprite sheets and saves each sprite's rectangle data.

        :param sprite_sheets: Tuple of dictionaries, with keys 'img' and 'xml', corresponding
                              to a sheet's image and corresponding XML file.
        """
        self._sprite_sheets = []
        self._extra_images = {}
        print("Loading images...")
        for sheet in sprite_sheets:
            try:
                surf = pg.image.load(os.path.join(cfg.IMG_DIR, 'spritesheets', sheet['img']))
                if not surf.get_alpha():
                    surf = surf.convert()
                else:
                    surf = surf.convert_alpha()
                tree = ElementTree.parse(os.path.join(cfg.IMG_DIR, 'spritesheets', sheet['xml']))
                rectangles = {}
                for node in tree.getroot():
                    name = node.attrib['name']
                    rectangles[name] = [int(node.attrib[val]) for val in ('x', 'y', 'width', 'height')]
                self._sprite_sheets.append({'surf': surf, 'rectangles': rectangles})
            except pg.error as err:
                print(err, file=sys.stderr)
                raise SystemExit
        for filename in os.listdir(os.path.join(cfg.IMG_DIR, 'png')):
            if filename.lower().endswith(".png"):
                surf = pg.image.load(os.path.join(cfg.IMG_DIR, 'png', filename))
                if not surf.get_alpha():
                    surf = surf.convert()
                else:
                    surf = surf.convert_alpha()
                self._extra_images[filename] = surf

    def get_image(self, name: str) -> pg.Surface:
        """ Returns a surface corresponding with the given name

        :param name: Name of image as listed in the sprite sheet.
        :return: Pygame surface corresponding to the image name 'name'
        """
        for sprite_sheet in self._sprite_sheets:
            if name in sprite_sheet['rectangles']:
                return _ImageLoader._create_surface(sprite_sheet['surf'], sprite_sheet['rectangles'][name])
        return self._extra_images[name]

    @classmethod
    def _create_surface(cls, sheet_surf: pg.Surface, rect: tuple) -> pg.Surface:
        """ Creates a pygame surface corresponding to an image on a sprite sheet.

        :param sheet_surf: Sprite sheet surface from which to render image.
        :param rect: Portion of sprite sheet surface to render into new surface.
        :return: pygame surface corresponding to an image in the sprite sheet.
        """
        x, y, w, h = rect
        image = pg.Surface((w, h))
        image.blit(sheet_surf, (0, 0), pg.Rect(x, y, w, h))
        return image


# Loads all of the images for the game.
_img_loader = _ImageLoader(*cfg.SPRITE_SHEETS)
# Globally available method for getting a loaded image.
get_image = _img_loader.get_image
