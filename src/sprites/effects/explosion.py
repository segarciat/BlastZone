import src.config as cfg
from src.sprites.animated_sprite import AnimatedSprite


_IMAGES = [f'explosion{i}.png' for i in range(1, 6)]


class Explosion(AnimatedSprite):
    """Explosion class for game explosion animation."""
    def __init__(self, x: float, y: float, all_groups):
        """

        :param x: x position where Explosion will be centered.
        :param y: y position where Explosion will be centered.
        :param all_groups: Dictionary of pygame sprites.
        """
        self._layer = cfg.EFFECTS_LAYER
        frame_info = [{'start_frame': 0, 'num_frames': len(_IMAGES)}]
        AnimatedSprite.__init__(self, _IMAGES, frame_info, all_groups, all_groups['all'],)
        self.anim_fps = 48.0
        self.rect.center = (x, y)

    def _handle_last_frame(self) -> None:
        """Upon reaching the last frame of the Explosion's animation, the sprite is killed (no longer drawn)."""
        self._current_frame = 0
        self.kill()
