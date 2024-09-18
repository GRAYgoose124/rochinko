import arcade
import math
import logging

from .settings import GameSettings
from .level.manager import LevelManager
from .game_systems import TextManagementSystem
from .draw_helpers import update_ball_path_preview
from .game_helpers import shoot_ball


log = logging.getLogger(__name__)


class RochinkoApp(arcade.Window, TextManagementSystem):
    def __init__(self):
        super().__init__(
            GameSettings.SCREEN_WIDTH,
            GameSettings.SCREEN_HEIGHT,
            "Pachinko Game",
            resizable=True,
        )
        TextManagementSystem.__init__(self)

        self.level_manager = LevelManager()

        self.shoot_power = 0
        self.aim_angle = 0
        self.aiming = False
        self.aim_preview_list = arcade.SpriteList()

        self.mouse_xy = (0, 0)

        if GameSettings.ENABLE_TIMINGS:
            arcade.enable_timings()

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def setup(self, level_index=0, next_level=False):
        self.aim_preview_list.clear()
        self.level_manager.setup(level_index, next_level)
        self.setup_texts()

    def on_draw(self):
        self.clear()
        self.level_manager.active_level.draw()
        self.text_list.draw()
        # Aim preview
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
        # Draw shooter
        arcade.draw_circle_filled(
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y,
            GameSettings.BALL_RADIUS,
            arcade.color.RED,
        )

    def on_update(self, delta_time):
        self.level_manager.active_level.on_update(delta_time)
        self.score_text.text = f"Score: {self.level_manager.active_level.score}, total: {self.level_manager.score}"
        if self.fps_text:
            self.fps_text.text = f"FPS: {arcade.get_fps():.0f}"

        # TODO: this is slowish
        self.aim_preview_list = update_ball_path_preview(
            self.level_manager.active_level.peg_list,
            self.aim_angle,
            self.shoot_power,
        )

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
        self.power_text.text = f"Power: {self.shoot_power:.0f}"

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
                shoot_ball(
                    self.level_manager.active_level, self.aim_angle, self.shoot_power
                )

    def on_resize(self, width, height):
        GameSettings.SCREEN_WIDTH = width
        GameSettings.SCREEN_HEIGHT = height
        GameSettings.SHOOTER_X = width / 2
        GameSettings.SHOOTER_Y = height - 60
        self.setup()


def main():
    logging.basicConfig(
        level=GameSettings.LOG_LEVEL,
        filename="rochinko.log" if GameSettings.LOG_TO_FILE else None,
        format="%(levelname)s - %(message)s",
    )
    logging.getLogger("arcade").setLevel(logging.WARNING)
    logging.getLogger("pymunk").setLevel(logging.WARNING)

    RochinkoApp().setup()
    arcade.run()


if __name__ == "__main__":
    main()
