"""Game configuration file specifying game constants and resource locations."""
import os


# Screen Settings.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TITLE = "Blast Zone"
FPS = 60

# Game directory and game assets directories.
GAME_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(GAME_DIR, 'assets', 'images')
SND_DIR = os.path.join(GAME_DIR, 'assets', 'sounds')
MAP_DIR = os.path.join(GAME_DIR, 'assets', 'maps')

# Color RGBs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANSPARENT = (255, 255, 255, 0)
COLOR_KEY = BLACK


# Sprite sheets.
SPRITE_SHEETS = (
    {"img": "onlyObjects_default.png", "xml": "onlyObjects_default.xml"},  # Game Object images.
    {"img": "blueSheet.png", "xml": "blueSheet.xml"}  # UI images.
)
TANK_COLORS = ["Blue", "Dark", "Green", "Red", "Sand"]
CATEGORY = {"standard": 1, "power": 2, "rapid": 3}
DEFAULT_IMAGE_ROT = -90  # See sprite sheet.

# Game font names.
FONT_NAMES = ('arial', 'calibri')


# Sprite Layers (smallest is topmost).
EFFECTS_LAYER = 5
BARREL_LAYER = 4
ITEM_LAYER = 3
TANK_LAYER = 2
TRACKS_LAYER = 1
