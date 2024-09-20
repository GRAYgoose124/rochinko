from pyglet.graphics import Batch
import arcade

from ..settings import GameSettings


class TextManagementSystem:
    def __init__(self):
        self.text_list = None
        self.power_text = None
        self.score_text = None
        self.fps_text = None

    def setup_texts(self):
        self.text_list = Batch()

        self.power_text = arcade.Text(
            f"Power: {self.shoot_power:.0f}",
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y - 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_list,
        )
        self.score_text = arcade.Text(
            f"Score: {self.level_manager.active_level.score}",
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y + 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_list,
        )
        if GameSettings.ENABLE_TIMINGS:
            self.fps_text = arcade.Text(
                f"FPS: {arcade.get_fps():.0f}",
                GameSettings.SCREEN_WIDTH - 40,
                GameSettings.SCREEN_HEIGHT - 20,
                arcade.color.WHITE,
                12,
                anchor_x="center",
                batch=self.text_list,
            )
        # Add hit count text to pegs
        if GameSettings.SHOW_HIT_COUNTS and self.level_manager.active_level:
            for peg in self.level_manager.active_level.peg_list:
                peg.text = arcade.Text(
                    str(peg.hit_count),
                    peg.center_x,
                    peg.center_y,
                    arcade.color.WHITE,
                    10,
                    anchor_x="center",
                    anchor_y="center",
                    batch=self.text_list,
                )
