import math
import random
import arcade
import array
import time

from ...settings import GameSettings, LOADED_SOUNDS
from ..draw_helpers import Burst
from .peg import Peg


class Bomb(Peg):
    def __init__(self, x, y, window):
        super().__init__(x, y, arcade.color.RED)
        self.window = window
        self.max_hit_count = 2

    def on_collision(self, arbiter, space, data):
        super().on_collision(arbiter, space, data)
        # trigger explosion
        if self.hit_count >= self.max_hit_count:
            ball = arbiter.shapes[0].body
            self.explode(ball)
            return False
        return True

    def explode(self, ball):
        dx = ball.position.x - self.center_x
        dy = ball.position.y - self.center_y

        length = math.sqrt(dx**2 + dy**2)
        dx, dy = dx / length, dy / length
        force = 35000
        self._start_explosion()
        ball.apply_force_at_local_point((dx * force, dy * force), (0, 0))
        arcade.play_sound(LOADED_SOUNDS["explosion"])

    def _start_explosion(self):
        """User clicks mouse"""

        def _gen_initial_data(initial_x, initial_y):
            """Generate data for each particle"""
            for i in range(GameSettings.PARTICLE_COUNT):
                angle = random.uniform(0, 2 * math.pi)
                speed = abs(random.gauss(0, 1)) * 0.5
                dx = math.sin(angle) * speed
                dy = math.cos(angle) * speed
                red = random.uniform(0.5, 1.0)
                green = random.uniform(0, red)
                blue = 0
                fade_rate = random.uniform(
                    1 / GameSettings.MAX_FADE_TIME, 1 / GameSettings.MIN_FADE_TIME
                )

                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        # Recalculate the coordinates from pixels to the OpenGL system with
        # 0, 0 at the center.
        x2 = self.center_x / GameSettings.SCREEN_WIDTH * 2.0 - 1.0
        y2 = self.center_y / GameSettings.SCREEN_HEIGHT * 2.0 - 1.0

        # Get initial particle data
        initial_data = _gen_initial_data(x2, y2)

        # Create a buffer with that data
        buffer = self.window.ctx.buffer(data=array.array("f", initial_data))

        # Create a buffer description that says how the buffer data is formatted.
        buffer_description = arcade.gl.BufferDescription(
            buffer, "2f 2f 3f f", ["in_pos", "in_vel", "in_color", "in_fade_rate"]
        )
        # Create our Vertex Attribute Object
        vao = self.window.ctx.geometry([buffer_description])

        # Create the Burst object and add it to the list of bursts
        burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
        self.window.level_view.burst_list.append(burst)

        self.text = None
