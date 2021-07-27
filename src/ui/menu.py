import pygame as pg

import src.config as cfg
import src.services.text as text_renderer
from src.sprites.base_sprite import BaseSprite
from src.ui.button import Button


_BTN_IMAGES = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]


class Menu(BaseSprite):
    """General menu class with buttons to handle each action."""
    _BUTTON_PADDING = 15
    IMAGE = "blue_panel.png"

    def __init__(self, title, size, color, buttons, ui_group):
        BaseSprite.__init__(self, Menu.IMAGE, ui_group)
        self.buttons = [Button(b['action'], b['text'], b['size'], b['color'],
                               _BTN_IMAGES, ui_group) for b in buttons]
        self._make(title, size, color)

    def update(self, dt: float) -> None:
        pass

    def _make(self, title, size, color) -> None:
        """Resizes the menu to the appropriate size and relocates the menu on top of it."""
        # Resize menu surface
        width = (self.buttons[0].rect.w + Menu._BUTTON_PADDING * 2)
        height = (self.buttons[0].rect.h + Menu._BUTTON_PADDING) * (len(self.buttons) + 1)
        self.image = pg.transform.scale(self.image, (width, height))
        self.image.set_colorkey(cfg.BLACK)

        # Recenter menu surface
        self.rect = self.image.get_rect()
        self.rect.center = (cfg.SCREEN_WIDTH / 2, cfg.SCREEN_HEIGHT / 2)

        # Render menu title
        text_renderer.render_pos(self.image, x=self.rect.w/2, y=2 * Menu._BUTTON_PADDING,
                                 text=title, size=size, color=color)

        # Position buttons
        menu_offset = size * 2 + self.rect.top
        for i in range(len(self.buttons)):
            # 36 Points to pixels conversion multiply by 4/3
            self.buttons[i].rect.top = menu_offset + i * (self.buttons[i].rect.h + Menu._BUTTON_PADDING)
            self.buttons[i].rect.centerx = cfg.SCREEN_WIDTH / 2

    def handle_mouse(self) -> None:
        """Handles mouse by delegating to its buttons."""
        for button in self.buttons:
            button.handle_mouse()

    def draw(self, surface: pg.Surface) -> None:
        """Draws the menu onto the surface provided."""
        surface.blit(self.image, self.rect)
        for button in self.buttons:
            surface.blit(button.image, button.rect)

    def kill(self) -> None:
        """Stop drawing all of the buttons and the menu itself."""
        for button in self.buttons:
            button.kill()
        super().kill()
