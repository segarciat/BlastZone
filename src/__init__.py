import pygame as pg
import src.config as cfg

print("Initializing pygame")
pg.init()
# Init video subsystems
pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
