import arcade
import pymunk
from .mixins.moving_body import MovingBody


class Obstacle(arcade.SpriteSolidColor, MovingBody):
    def __init__(self, width, height, x, y, movement_function=None):
        arcade.SpriteSolidColor.__init__(
            self,
            width=width,
            height=height,
            color=arcade.color.RED,
            center_x=x,
            center_y=y,
        )
        MovingBody.__init__(
            self,
            x,
            y,
            movement_function=movement_function,
        )
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4

    def update(self, delta_time):
        self.update_position(delta_time)


class Bin(Obstacle):
    def __init__(self, width, height, x, y, movement_function=None):
        super().__init__(width, height, x, y, movement_function)
        self.color = arcade.color.RED

    def trigger_effect(self, ball):
        pass
