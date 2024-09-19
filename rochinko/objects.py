import array
import random
import time
import arcade
import pymunk
from dataclasses import dataclass

from .settings import GameSettings
from .sound import LOADED_SOUNDS
from .draw_helpers import Burst


class Ball(arcade.SpriteCircle):
    def __init__(self, x, y):
        # super().__init__("path/to/ball_image.png", scale=0.5)
        super().__init__(
            radius=GameSettings.BALL_RADIUS,
            color=arcade.color.WHITE,
            mass=1,
        )
        mass = 1
        radius = GameSettings.BALL_RADIUS
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4
        self.modifiers = []

    def update(self, delta_time):
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y
        self.angle = self.body.angle

        # Remove ball if it goes out of bounds
        if (
            self.center_y < 0
            or self.center_x < 0
            or self.center_x > GameSettings.SCREEN_WIDTH
        ):
            self.body.space.remove(self.body, self.shape)
            self.remove_from_sprite_lists()


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
        arcade.play_sound(LOADED_SOUNDS["clang"])
        return True


class Bomb(Peg):
    def __init__(self, x, y, window):
        super().__init__(x, y, arcade.color.RED)
        self.window = window
        self.max_hit_count = 2

    def on_collision(self, arbiter, space, data):
        super().on_collision(arbiter, space, data)
        # trigger explosion
        if self.hit_count >= self.max_hit_count:
            self.explode()
            return False
        return True

    def explode(self):
        """User clicks mouse"""

        def _gen_initial_data(initial_x, initial_y):
            """Generate data for each particle"""
            for i in range(GameSettings.PARTICLE_COUNT):
                dx = random.uniform(-0.2, 0.2)
                dy = random.uniform(-0.2, 0.2)
                yield initial_x
                yield initial_y
                yield dx
                yield dy

        # Get initial particle data
        initial_data = _gen_initial_data(self.center_x, self.center_y)

        # Create a buffer with that data
        buffer = self.window.ctx.buffer(data=array.array("f", initial_data))

        # Create a buffer description that says how the buffer data is formatted.
        buffer_description = arcade.gl.BufferDescription(
            buffer, "2f 2f", ["in_pos", "in_vel"]
        )
        # Create our Vertex Attribute Object
        vao = self.window.ctx.geometry([buffer_description])

        # Create the Burst object and add it to the list of bursts
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.window.level_view.burst_list.append(burst)

        self.text = None
        self.remove_from_sprite_lists()


class Obstacle(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y):
        super().__init__(
            width=width,
            height=height,
            color=arcade.color.RED,
            center_x=x,
            center_y=y,
        )
        self.width = width
        self.height = height
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4

    def update(self, delta_time):
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y


class Bin(Obstacle):
    def __init__(self, width, height, x, y):
        super().__init__(width, height, x, y)
        self.color = arcade.color.RED

    def trigger_effect(self, ball):
        pass
