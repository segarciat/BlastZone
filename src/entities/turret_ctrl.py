from src.utils.timer import Timer
from src.entities.ai_mob import AIMob
from src.entities.tank_ctrl import AIPursueState


class AITurretCtrl(AIMob):
    """Class that represents an AI that controls a Turret sprite."""
    def __init__(self, sprite, ai_boss, target):
        """Initializes the AI in AttackState.

        :param sprite: turret sprite controlled by AI.
        :param ai_boss: Tank AI controller that the target is facing.
        :param target: The target that this AI will attack.
        """
        AIMob.__init__(self, sprite, target)
        self._ai_boss = ai_boss
        self._attack_state = AIAttackState(self)
        self._reload_state = AIReloadState(self)
        self._state = self._attack_state
        self._state.enter()

    @property
    def turret(self):
        return self._sprite

    @property
    def attack_state(self) -> 'AIAttackState':
        return self._attack_state

    @property
    def reload_state(self) -> 'AIReloadState':
        return self._reload_state

    def is_tank_pursuing(self) -> bool:
        """Checks if the boss' AI tank is pursuing the target."""
        return self._ai_boss.tank.alive() and type(self._ai_boss.state) == AIPursueState


class AITurretCtrlState:
    """Base class for AITurretCtrl state."""
    def __init__(self, ai):
        self._ai = ai

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass


class AIAttackState(AITurretCtrlState):
    """State class for AITankCtrl for attacking the player."""
    def __init__(self, ai):
        AITurretCtrlState.__init__(self, ai)

    def update(self, dt) -> None:
        """Attacks the T=target as long as they're in range and the AI's turret has ammo."""
        if self._ai.is_target_in_range():
            turret = self._ai.turret
            if turret.barrel.ammo_count > 0:
                if not self._ai.is_tank_pursuing():
                    aim_direction = self._ai.angle_to_target()
                    turret.fire(aim_direction)
            else:
                self._ai.state = self._ai.reload_state


class AIReloadState(AITurretCtrlState):
    """ State class for AITankCtrl for reloading the AI's turret."""
    _RELOAD_TIME = 10000

    def __init__(self, ai):
        AITurretCtrlState.__init__(self, ai)
        self._reload_timer = None

    def enter(self) -> None:
        """Initiates the reload timer for the AI's turret."""
        self._reload_timer = Timer()

    def update(self, dt: float) -> None:
        """Switches back to attack state once it's time to reload."""
        if self._reload_timer.elapsed() > AIReloadState._RELOAD_TIME:
            self._ai.turret.barrel.reload()
            self._ai.state = self._ai.attack_state
