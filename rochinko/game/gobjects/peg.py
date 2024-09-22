import arcade
import pymunk

from ...settings import GameSettings, LOADED_SOUNDS
from .moving_body import MovingBody


class Peg(arcade.SpriteCircle, MovingBody):
    def __init__(self, x, y, color=arcade.color.BLUE, movement_function=None):
        arcade.SpriteCircle.__init__(
            self,
            radius=GameSettings.PEG_RADIUS,
            color=color,
            mass=1,
        )
        MovingBody.__init__(
            self,
            x,
            y,
            movement_function=movement_function,
        )
        self.shape = pymunk.Circle(self.body, GameSettings.PEG_RADIUS)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4

        self.hit_count = 0
        self.max_hit_count = 10
        self.text = None

    def update(self, delta_time):
        self.update_position(delta_time)

        if self.text:
            self.text.text = str(self.hit_count)
            self.text.x = self.center_x
            self.text.y = self.center_y

        if self.hit_count >= self.max_hit_count:
            self.body.space.remove(self.body, self.shape)
            self.remove_from_sprite_lists()
            del self.text

    def on_collision(self, arbiter, space, data):
        self.hit_count += 1
        arcade.play_sound(LOADED_SOUNDS["clang"], volume=0.5)
        return True
