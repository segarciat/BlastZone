import pygame as pg
import itertools
import random

import src.utils.constants as constants
from src.utils.timer import Timer
from src.entities.ai_mob import AIMob


class AITankCtrl(AIMob):
    """Class for an AI that controls a tank object."""
    def __init__(self, tank, path_data: list, target):
        """Initiates the AI in a patrol state.

        :param tank: The tank sprite controlled by this AI.
        :param path_data: The points that the sprite navigates to during its patrol state.
        :param target: The sprite that the target is targeting.
        """
        AIMob.__init__(self, tank, target)
        random.shuffle(path_data)
        # Iterator that cycles the destination points of the tank's destination points.
        self._path_points = itertools.cycle([pg.math.Vector2(p.x, p.y) for p in path_data])
        self._patrol_state = AIPatrolState(self)
        self._pursue_state = AIPursueState(self)
        self._flee_state = AIFleeState(self)
        self.state = self._patrol_state
        self.state.enter()

    @property
    def tank(self):
        return self._sprite

    @property
    def patrol_state(self) -> 'AIPatrolState':
        return self._patrol_state

    @property
    def pursue_state(self) -> 'AIPursueState':
        return self._pursue_state

    @property
    def flee_state(self) -> 'AIFleeState':
        return self._flee_state

    def rotate_to(self, aim_direction: float) -> None:
        """Rotates the tank controlled by the AI, as well as its barrels.

        :param aim_direction: Angle in which to rotate the sprite.
        :return: None
        """
        tank = self._sprite
        tank.rot = aim_direction
        tank.rotate()
        tank.rotate_barrel(aim_direction)

    def move(self, acc_pct=1.0) -> None:
        """Sets the acceleration of the tank sprite controlled by the AI

        :param acc_pct: modifier for the tank's acceleration; must be non-negative.
        :return: None
        """
        if acc_pct < 0:
            raise ValueError(f"Expected non-negative acc_pct value, but received {acc_pct}")
        tank = self._sprite
        tank.acc = pg.math.Vector2(tank.MAX_ACCELERATION * acc_pct, 0).rotate(-self._sprite.rot)

    def get_next_destination(self) -> pg.math.Vector2:
        """Gets the next path point that the AI's tank sprite should patrol to."""
        return next(self._path_points)


class AITankCtrlState:
    """Based class for the tank controller's state behavior."""
    WALL_AVOID_DURATION = 1000
    WALL_TURN_ANGLE = 15
    _crash_timer = Timer()

    def __init__(self, ai: AITankCtrl):
        self._ai = ai

    def check_for_walls(self) -> None:
        """Rotates the AI's tank sprite upon hitting a wall and causes to move away from it for a small duration."""
        if self._ai.tank.hit_wall:
            AITankCtrlState._crash_timer.restart()
            self._ai.rotate_to(self._ai.tank.rot + AITankCtrlState.WALL_TURN_ANGLE)

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    @staticmethod
    def is_avoiding_wall() -> bool:
        """Checks to see if the AI's tank sprite is still avoiding the a wall."""
        return AITankCtrlState._crash_timer.elapsed() < AITankCtrlState.WALL_AVOID_DURATION


class AIPatrolState(AITankCtrlState):
    """Simulates an idle, patrolling state for the AITankCtrl"""
    _EPSILON = 100

    def __init__(self, ai: AITankCtrl):
        AITankCtrlState.__init__(self, ai)
        self._destination = None

    def enter(self) -> None:
        """Sets the starting destination that the AI's sprite will patrol to."""
        self._destination = self._ai.get_next_destination()
        aim_direction = (self._destination - self._ai.tank.pos).angle_to(constants.UNIT_VEC)
        self._ai.rotate_to(aim_direction)

    def update(self, dt: float) -> None:
        """Marches on to the next path point, or pursues the target if it is in-range."""
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._ai.is_target_in_range():
                self._ai.state = self._ai.pursue_state
            else:
                if self.arrived():
                    self._destination = self._ai.get_next_destination()

                aim_direction = (self._destination - self._ai.tank.pos).angle_to(constants.UNIT_VEC)
                self._ai.rotate_to(aim_direction)
        self._ai.move(acc_pct=0.75)

    def arrived(self) -> bool:
        """Determines whether the target has reached its current destination."""
        dist = (self._destination - self._ai.tank.pos).length_squared()
        return dist < AIPatrolState._EPSILON


class AIPursueState(AITankCtrlState):
    """Class that simulates the AITankCtrl's pursue behavior."""
    def __init__(self, ai):
        AITankCtrlState.__init__(self, ai)

    def update(self, dt) -> None:
        """Chases and fires at the target while the AI's tank has ammo and is in range; flees when out of ammo."""
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._ai.tank.ammo_count() > 0:
                if self._ai.is_target_in_range():
                    aim_direction = self._ai.angle_to_target()
                    self._ai.rotate_to(aim_direction)
                    self._ai.tank.fire()
                else:
                    self._ai.state = self._ai.patrol_state
            else:
                self._ai.state = self._ai.flee_state
        self._ai.move(acc_pct=0.9)


class AIFleeState(AITankCtrlState):
    """Class that simulates the AITankCtrl's flee behavior."""
    # 180 to go opposite to player, and 30 for slight turn.
    FLEE_ANGLE = 210
    _RELOAD_TIME = 5000

    def __init__(self, ai):
        AITankCtrlState.__init__(self, ai)
        self._reload_timer = Timer()

    def enter(self) -> None:
        """Sets the time when the AI started fleeing."""
        self._reload_timer.restart()

    def update(self, dt: float) -> None:
        """Flees for a certain duration, switching back to patrol once the AI's tank ammo is reloaded."""
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._reload_timer.elapsed() > AIFleeState._RELOAD_TIME:
                self._ai.tank.reload()
                self._ai.state = self._ai.patrol_state  # Causes exit to be called by the AI.
            else:
                # Run away from target.
                aim_direction = self._ai.angle_to_target() + AIFleeState.FLEE_ANGLE
                self._ai.rotate_to(aim_direction)
        self._ai.move()
