import random
import pytmx
import pygame as pg


import src.world.collisions as collision_handler
from src.world.tiled_map import TiledMapLoader
from src.world.camera import Camera
from src.entities.player_ctrl import PlayerCtrl
from src.entities.tank_ctrl import AITankCtrl
from src.entities.turret_ctrl import AITurretCtrl
from src.sprites.tank import Tank
from src.sprites.turret import Turret
from src.sprites.obstacles import Tree
from src.sprites.obstacles import BoundaryWall
from src.sprites.items.box import ItemBox
from src.utils.timer import Timer


class Level:
    """Class that creates, draws, and updates the game world, including the map and all sprites."""
    _MAX_ITEMS = 1
    _ITEM_RESPAWN_TIME = 5000

    def __init__(self, level_file: str):
        """Creates a map and creates all of the sprites in it.

        :param level_file: Filename of level file to load from the configuration file's map folder.
        """
        # Create the tiled map surface.
        map_loader = TiledMapLoader(level_file)
        self.image = map_loader.make_map()
        self.rect = self.image.get_rect()
        self._groups = {
            'all': pg.sprite.LayeredUpdates(),
            'tanks': pg.sprite.Group(),
            'damageable': pg.sprite.Group(),
            'bullets': pg.sprite.Group(),
            'obstacles': pg.sprite.Group(),
            'items': pg.sprite.Group(),
            'item_boxes': pg.sprite.Group()
        }
        self._player = None
        self._camera = None
        self._ai_mobs = []
        self._item_spawn_positions = []
        self._item_spawn_timer = Timer()
        # Initialize all sprites in game world.
        self._init_sprites(map_loader.tiled_map.objects)

    def _init_sprites(self, objects: pytmx.TiledObjectGroup) -> None:
        """Initializes all of the pygame sprites in this level's map.

        :param objects: Iterator for accessing the properties of all game objects to be created.
        :return: None

        Expects to find a single 'player' and 'enemy_tank' object, and possible more than one
        of any other object. A sprite is created out of each object and added to the appropriate
        group. A boundary for the game world is also created to keep the sprites constrained.
        """
        game_objects = {}
        for t_obj in objects:
            # Expect single enemy tank and multiple of other objects.
            if t_obj.name == 'enemy_tank' or t_obj.name == "player":
                game_objects[t_obj.name] = t_obj
            else:
                game_objects.setdefault(t_obj.name, []).append(t_obj)

        # Create the player and world camera.
        p = game_objects.get('player')
        tank = Tank.color_tank(p.x, p.y, p.color, p.category, self._groups)  # Make a tank factory.
        self._player = PlayerCtrl(tank)
        self._camera = Camera(self.rect.width, self.rect.height, self._player.tank)

        # Spawn single enemy tank.
        t = game_objects.get('enemy_tank')
        tank = Tank.enemy(t.x, t.y, t.size, self._groups)  # Make a tank factory.
        ai_patrol_points = game_objects.get('ai_patrol_point')
        ai_boss = AITankCtrl(tank, ai_patrol_points, self._player.tank)
        self._ai_mobs.append(ai_boss)

        # Spawn turrets.
        for t in game_objects.get('turret'):
            turret = Turret(t.x, t.y, t.category, t.special, self._groups)
            self._ai_mobs.append(AITurretCtrl(turret, ai_boss, self._player.tank))

        # Spawn obstacles that one can collide with.
        for tree in game_objects.get('small_tree'):
            Tree(tree.x, tree.y, self._groups)

        # Spawn items boxes that can be destroyed to get an item.
        for box in game_objects.get('box_spawn'):
            self._item_spawn_positions.append((box.x, box.y))
            ItemBox.spawn(box.x, box.y, self._groups)

        # Creates the boundaries of the game world.
        BoundaryWall(x=0, y=0, width=self.rect.width, height=1, all_groups=self._groups)                 # Top
        BoundaryWall(x=0, y=self.rect.height, width=self.rect.width, height=1, all_groups=self._groups)  # Bottom
        BoundaryWall(x=0, y=0, width=1, height=self.rect.height, all_groups=self._groups)                # Left
        BoundaryWall(x=self.rect.width, y=0, width=1, height=self.rect.height, all_groups=self._groups)  # Right

    def _can_spawn_item(self) -> bool:
        """"Checks if a new item can be spawned."""
        return self._item_spawn_timer.elapsed() > Level._ITEM_RESPAWN_TIME and \
            len(self._groups['item_boxes']) < Level._MAX_ITEMS

    def is_player_alive(self) -> bool:
        """Checks if the player's tank has been defeated."""
        return self._player.tank.alive()

    def mob_count(self) -> int:
        """Checks if all the AI mobs have been defeated."""
        return len(self._ai_mobs)

    def process_inputs(self) -> None:
        """Handles keys and clicks that affect the game world."""
        self._player.handle_keys()
        # Convert mouse coordinates to world coordinates.
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_world_pos = pg.math.Vector2(mouse_x + self._camera.rect.x, mouse_y + self._camera.rect.y)
        self._player.handle_mouse(mouse_world_pos)

    def update(self, dt: float) -> None:
        """Updates the game world's AI, sprites, camera, and resolves collisions.

        :param dt: time elapsed since the last update of the game world.
        :return: None
        """
        for ai in self._ai_mobs:
            ai.update(dt)
        self._groups['all'].update(dt)
        # Update list of ai mobs.
        self._camera.update()
        collision_handler.handle_collisions(self._groups)
        for box in self._groups['item_boxes']:
            if box.is_broken():
                self._item_spawn_timer.restart()
        # See if it's time to spawn a new item.
        if self._can_spawn_item():
            x, y, = random.choice(self._item_spawn_positions)
            ItemBox.spawn(x, y, self._groups)

        # Filter out any AIs that have been defeated.
        self._ai_mobs = [ai for ai in self._ai_mobs if ai.sprite.alive()]

    def draw(self, screen: pg.Surface) -> None:
        """Draws every sprite in the game world, as well as heads-up display elements.

        :param screen: The screen surface that the world's elements will be drawn to.
        :return: None
        """
        # Draw the map.
        screen.blit(self.image, self._camera.apply(self.rect))
        # Draw all sprites.
        for sprite in self._groups['all']:
            screen.blit(sprite.image, self._camera.apply(sprite.rect))
            # pg.draw.rect(screen, (255, 255, 255), self._camera.apply(sprite.hit_rect), 1)

        # Draw HUD.
        for ai in self._ai_mobs:
            ai.sprite.draw_health(screen, self._camera)
        self._player.draw_hud(screen, self._camera)
