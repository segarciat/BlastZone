import pygame as pg

import src.utils.constants as constants
import src.input.input_manager as input_manager
import src.config as cfg
import src.services.text as text_renderer
import src.services.image_loader as image_loader
from src.input.input_state import InputState


# Player HUD constants.
_HP_X_OFFSET = 5
_HP_Y_OFFSET = 5
_HP_WIDTH = cfg.SCREEN_WIDTH / 4
_HP_HEIGHT = _HP_WIDTH // 8


class PlayerCtrl:
    """Class that represents the player's controls and actions for manipulating their sprite."""
    _ROT_SPEED = 75

    def __init__(self, tank):
        """Sets the PlayerCtrl's sprite object.

        :param tank: A Tank object that will be controlled by the player.
        """
        # Tank is assigned when level is created.
        self.tank = tank
        self._actions = {
            "fire": self._fire,
            "forward": self._forward,
            "reverse": self._reverse,
            "ccw_turn": self._ccw_turn,
            "cw_turn": self._cw_turn
        }

        # HUD attributes.
        # Ammo Icon
        self.ammo_surf = image_loader.get_image(f"bullet{tank.color}3_outline.png")
        self.ammo_rect = self.ammo_surf.get_rect()

        # Ammo text surface
        self.ammo_count_surf = pg.Surface((_HP_HEIGHT * 2, self.ammo_rect.height))
        self.ammo_count_rect = self.ammo_count_surf.get_rect()

    def handle_keys(self):
        """Consumes any key active key bindings and invokes the appropriate action on the PlayerCtrl's sprite."""
        # Reset acceleration if no press.
        self.tank.rot_speed = 0
        self.tank.acc.x, self.tank.acc.y = 0, 0
        for action_key, action in self._actions.items():
            if action_key in input_manager.active_bindings:
                action()  # i.e., self._forward()
                del input_manager.active_bindings[action_key]  # Consume the key binding.

    def handle_mouse(self, mouse_world_pos: pg.math.Vector2):
        """Processes the mouse state and invoke any appropriate action on the PlayerCtrl's sprite."""
        # Aim the barrel.
        pointing = mouse_world_pos - self.tank.pos
        aim_direction = pointing.angle_to(constants.UNIT_VEC)
        self.tank.rotate_barrel(aim_direction)

        # Fire bullet.
        if input_manager.mouse_state[InputState.MOUSE_LEFT] == InputState.JUST_PRESSED:
            self._fire()

    def _fire(self):
        """Causes the PlayerCtrl's tank to fire a bullet."""
        ammo = self.tank.ammo_count()
        if ammo > 0:
            self.tank.fire()

    def _forward(self):
        """Sets the acceleration of the PlayerCtrl's sprite to move forward."""
        self.tank.acc = pg.math.Vector2(self.tank.MAX_ACCELERATION, 0).rotate(-self.tank.rot)

    def _reverse(self):
        """Sets the acceleration of the PlayerCtrl's sprite to move backwards."""
        self.tank.acc = pg.math.Vector2(-self.tank.MAX_ACCELERATION, 0).rotate(-self.tank.rot)

    def _ccw_turn(self):
        """Sets the rotation speed of the PlayerCtrl's sprite to move backwards."""
        self.tank.rot_speed = PlayerCtrl._ROT_SPEED

    def _cw_turn(self):
        """Sets the rotation speed of the PlayerCtrl's sprite to move backwards."""
        self.tank.rot_speed = -PlayerCtrl._ROT_SPEED

    def draw_hud(self, surface, camera):
        """Draws the player's health and ammo count."""
        # Draw the health bar.
        hp_x, hp_y = camera.rect.x + _HP_X_OFFSET, camera.rect.y + _HP_Y_OFFSET
        bar_rect = pg.Rect(hp_x, hp_y, _HP_WIDTH, _HP_HEIGHT)
        self.tank.draw_health(surface, camera, bar_rect)

        hp_text_pos = camera.apply(bar_rect).center
        text_renderer.render_pos(surface, *hp_text_pos, f"HP: {self.tank.health} / {self.tank.MAX_HEALTH}", 16,
                                 cfg.WHITE)

        # Draw ammo icon.
        self.ammo_rect.x = bar_rect.left
        self.ammo_rect.y = bar_rect.bottom + 5
        surface.blit(self.ammo_surf, camera.apply(self.ammo_rect))

        # Ammo count
        self.ammo_count_rect.x = self.ammo_rect.right + 2
        self.ammo_count_rect.y = self.ammo_rect.y
        self.ammo_count_surf.fill(cfg.BLACK)

        ammo_text = f"Ammo: {self.tank.ammo_count()}"
        text_renderer.render(self.ammo_count_surf, ammo_text, 12, cfg.WHITE)
        surface.blit(self.ammo_count_surf, camera.apply(self.ammo_count_rect))