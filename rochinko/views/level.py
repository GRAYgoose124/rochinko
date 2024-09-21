import time
import arcade
import math

from ..game.systems.text_management import TextManagementSystem
from ..game.level_manager import LevelManager
from ..settings import GameSettings, SHADERS_PATH
from ..game.draw_helpers import update_ball_path_preview
from ..game.gobjects.ball import Ball


class LevelView(arcade.View, TextManagementSystem):
    def __init__(self):
        super().__init__()
        TextManagementSystem.__init__(self)

        self.level_manager = LevelManager(self.window)

        self.shoot_power = 0
        self.aim_angle = 0
        self.aiming = False
        self.aim_preview_list = arcade.SpriteList()

        self.mouse_xy = (0, 0)

        self.burst_program = self.window.ctx.load_program(
            vertex_shader=SHADERS_PATH / "burst.vert",
            fragment_shader=SHADERS_PATH / "burst.frag",
        )
        self.burst_list = []

        self.window.ctx.enable_only(
            self.window.ctx.BLEND,
        )

    def setup(self, level_index=0, next_level=False):
        self.aim_preview_list.clear()
        self.level_manager.setup(level_index, next_level)
        self.setup_texts()

    def on_draw(self):
        self.clear()
        self.window.ctx.point_size = 2 * self.window.get_pixel_ratio()

        self.level_manager.active_level.draw()
        self.text_list.draw()
        self.aim_preview_list.draw()
        if self.aiming:
            arcade.draw_line(
                GameSettings.SHOOTER_X,
                GameSettings.SHOOTER_Y,
                self.mouse_xy[0],
                self.mouse_xy[1],
                arcade.color.WHITE,
                1,
            )
        arcade.draw_circle_filled(
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y,
            GameSettings.BALL_RADIUS,
            arcade.color.RED,
        )

        # Render the bursts
        for burst in self.burst_list:
            self.burst_program["time"] = burst.time
            burst.vao.render(self.burst_program, mode=self.window.ctx.POINTS)

    def on_update(self, delta_time):
        self.level_manager.active_level.on_update(delta_time)
        self.texts["score"].text = (
            f"Score: {self.level_manager.active_level.score}, total: {self.level_manager.score}"
        )
        if self.texts["fps"]:
            self.texts["fps"].text = f"FPS: {arcade.get_fps():.0f}"

        self.aim_preview_list = update_ball_path_preview(
            self.level_manager.active_level.peg_list,
            self.aim_angle,
            self.shoot_power,
        )

        new_burst_list = []
        for burst in self.burst_list:
            burst.time = time.time() - burst.start_time
            if burst.time < 3:
                new_burst_list.append(burst)
        self.burst_list = new_burst_list

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_xy = (x, y)
        self.aim_angle = math.atan2(
            y - GameSettings.SHOOTER_Y, x - GameSettings.SHOOTER_X
        )
        distance = math.sqrt(
            (x - GameSettings.SHOOTER_X) ** 2 + (y - GameSettings.SHOOTER_Y) ** 2
        )
        self.shoot_power = min(
            max(distance, GameSettings.MIN_SHOOT_POWER),
            GameSettings.MAX_SHOOT_POWER,
        )
        self.texts["power"].text = f"Power: {self.shoot_power:.0f}"

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.aiming = True
        elif button == arcade.MOUSE_BUTTON_RIGHT and not self.aiming:
            self.setup(next_level=True)
        else:
            self.aiming = False

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.aiming:
            self.aiming = False

            if len(self.level_manager.active_level.ball_list) < 3:
                Ball.shoot(
                    self.level_manager.active_level, self.aim_angle, self.shoot_power
                )

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.level_manager.active_level.space_steps = (
                self.level_manager.active_level.space_steps + 1
            ) % 5

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.setup()
