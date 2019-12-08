from src.sprites.tanks.color_tank import ColorTank
import pygame as pg

class PlayerCtrl:
    # def __init__(self, tank)
    def __init__(self):
        # Load bindings from json file
        self.bindings = None

    def handle_input(self, input_state, dt):
        aim_vec = pg.math.Vector2(*pg.mouse.get_pos())
        self.tank.rotate_barrel(aim_vec)

    def set_tank(self, tank):
        self.tank = tank
