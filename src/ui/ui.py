import pygame as pg

from src.ui.menu import Menu


class UI:
    def __init__(self):
        self._ui_sprites = pg.sprite.Group()
        self._menus = []

    def make_menu(self, title, size, color, buttons):
        """Creates a menu and presents it as the UI's topmost element."""
        self._menus.append(Menu(title, size, color, buttons, self._ui_sprites))

    def process_inputs(self):
        """Handles the mouse by delegating to the topmost menu."""
        if self._menus:
            self._menus[-1].handle_mouse()

    def pop_menu(self):
        """Removes the topmost menu."""
        menu = self._menus.pop()
        menu.kill()

    def clear(self):
        """Clears all menus from the UI."""
        while self._menus:
            self.pop_menu()

    def draw(self, surface: pg.Surface):
        """Draw all menus from bottom to top."""
        for menu in self._menus:
            menu.draw(surface)
