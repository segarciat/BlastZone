import os
import pygame as pg
import pytmx

import src.config as cfg


class TiledMapLoader:
    """TiledMapLoader class for loading a TiledMap from a .tmx file. Credits to Chris Bradfield from KidsCanCode"""
    def __init__(self, filename):
        tm = pytmx.util_pygame.load_pygame(os.path.join(cfg.MAP_DIR, filename), pixelalpha=True)
        self._width = tm.width * tm.tilewidth
        self._height = tm.height * tm.tileheight
        self._tiled_map = tm

    @property
    def tiled_map(self) -> pytmx.TiledMap:
        return self._tiled_map

    def make_map(self) -> pg.Surface:
        """Creates a pygame surface from the visible layers of the TiledMap object loaded.

        :return: A pygame surface representing the map.
        """
        surf = pg.Surface((self._width, self._height))
        for layer in self._tiled_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self._tiled_map.get_tile_image_by_gid(gid)
                    if tile:
                        surf.blit(tile, (x * self._tiled_map.tilewidth, y * self._tiled_map.tileheight))
        surf.set_colorkey(cfg.COLOR_KEY)
        if surf.get_alpha() is None:
            surf = surf.convert()
        else:
            surf = surf.convert_alpha()
        return surf
