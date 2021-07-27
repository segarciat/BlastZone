import typing
import pygame as pg

# from src.settings import FONT_NAMES
import src.config as cfg


class TextRenderer:
    def __init__(self):
        # Load all fonts
        self._fonts = {font: pg.font.match_font(font) for font in cfg.FONT_NAMES}

    def _render_text_surface(self, text, size, color, font_name='arial') -> typing.Tuple[pg.Surface, pg.Rect]:
        # Create font object
        font_object = pg.font.Font(self._fonts[font_name], size)

        # Create a text surface
        text_surface = font_object.render(text, True, color)
        text_rect = text_surface.get_rect()
        return text_surface, text_rect

        # Render at specified (x, y) [overloaded below]
    def render_pos(self, surface, x, y, text, size, color, font_name='arial') -> None:
        text_surface, text_rect = self._render_text_surface(text, size, color, font_name)
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

        # Render at a relative cardinal location
    def render(self, surface, text, size, color, location='c', font_name='arial') -> None:
        text_surface, text_rect = self._render_text_surface(text, size, color, font_name)

        # Determine where to blit the text
        if location == 'nw':
            text_rect.topleft = surface.get_rect().topleft
        elif location == 'n':
            text_rect.midtop = surface.get_rect().midtop
        elif location == 'ne':
            text_rect.topright = surface.get_rect().topright
        elif location == 'w':
            text_rect.midleft = surface.get_rect().midleft
        elif location == 'c':
            text_rect.center = surface.get_rect().center
        elif location == 'e':
            text_rect.midright = surface.get_rect().midright
        elif location == 'sw':
            text_rect.bottomleft = surface.get_rect().bottomleft
        elif location == 's':
            text_rect.midbottom = surface.get_rect().midbottom
        elif location == 'se':
            text_rect.bottomright = surface.get_rect().bottomright

        surface.blit(text_surface, text_rect)


_text_renderer = TextRenderer()

render = _text_renderer.render
render_pos = _text_renderer.render_pos
