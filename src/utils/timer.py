import pygame as pg


class Timer:
    """Simulates a timer for the game."""
    _all_timers = []

    def __init__(self):
        """Starts running the timer."""
        self._elapsed_time = 0
        self._paused = False
        self._unpause_time = pg.time.get_ticks()
        Timer._all_timers.append(self)

    def pause(self) -> None:
        """Pauses the timer."""
        self._paused = True
        self._elapsed_time += time_since(self._unpause_time)

    def unpause(self) -> None:
        """Unpauses the timer."""
        self._paused = False
        self._unpause_time = pg.time.get_ticks()

    def restart(self) -> None:
        """Restarts the timer."""
        self._elapsed_time = 0
        self._unpause_time = pg.time.get_ticks()

    def elapsed(self) -> float:
        """Returns the number of milliseconds that have passed since the timer started."""
        ms = self._elapsed_time
        if not self._paused:
            ms += time_since(self._unpause_time)
        return ms

    @classmethod
    def pause_timers(cls) -> None:
        """Pauses all of the timers in the game. Should be called only when the game is paused."""
        for timer in cls._all_timers:
            timer.pause()

    @classmethod
    def unpause_timers(cls) -> None:
        """Unpauses all of the timers in the game. Should be called only when the game is paused."""
        for timer in cls._all_timers:
            timer.unpause()

    @classmethod
    def restart_timers(cls) -> None:
        """Restarts all timers in the game"""
        for timer in cls._all_timers:
            timer.restart()

    @classmethod
    def clear_timers(cls) -> None:
        """Removes all timers in the game."""
        while cls._all_timers:
            cls._all_timers.pop()


def time_since(t0: int) -> int:
    """ Returns number of milliseconds since t0 """
    return pg.time.get_ticks() - t0
