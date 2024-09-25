import arcade
import pymunk

from ...settings import GameSettings, LOADED_SOUNDS
from .mixins.moving_body import MovingBody


class Target(arcade.SpriteCircle, MovingBody):
    # non-phys moving object that can be shot to produce various effects.
    def __init__(
        self,
        x,
        y,
        level=None,
        color=arcade.color.BLUE,
        movement_function=None,
    ):
        arcade.SpriteCircle.__init__(
            self,
            radius=GameSettings.PEG_RADIUS,
            color=color,
        )
        MovingBody.__init__(self, movement_function=movement_function)
        self.shape = pymunk.Circle(self.body, GameSettings.PEG_RADIUS - 10)

    def update(self, delta_time):
        self.update_position(delta_time)

    def on_collision(self, arbiter, space, data):

        self.remove_from_sprite_lists()
        return False
