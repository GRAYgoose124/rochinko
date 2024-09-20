import arcade
import pymunk

from ...settings import GameSettings, LOADED_SOUNDS


class Peg(arcade.SpriteCircle):
    def __init__(self, x, y, color=arcade.color.BLUE, movement_function=None):
        # super().__init__("path/to/peg_image.png", scale=0.5)
        super().__init__(
            radius=GameSettings.PEG_RADIUS,
            color=color,
            mass=1,
        )
        self.center_x = x
        self.center_y = y
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, GameSettings.PEG_RADIUS)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4

        self.movement_function = movement_function

        self.time = 0
        self.hit_count = 0
        self.max_hit_count = 10
        self.text = None

    def update(self, delta_time):
        if self.movement_function:
            self.time += 1
            self.body.position = self.movement_function(self.time)
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y

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
