from pyglet.graphics import Batch
import arcade

from ...settings import GameSettings


class TextManagementSystem:
    def __init__(self):
        self.text_list = None
        self.texts = {
            "power": None,
            "score": None,
            "fps": None,
            "space_steps": None,
        }

    def setup_texts(self):
        self.text_list = Batch()

        self.texts["power"] = arcade.Text(
            f"Power: {self.shoot_power:.0f}",
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y - 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_list,
        )
        self.texts["score"] = arcade.Text(
            f"Score: {self.level_manager.active_level.score}",
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y + 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_list,
        )
        self.texts["space_steps"] = arcade.Text(
            f"{GameSettings.SPACE_STEPS}x",
            20,
            GameSettings.SCREEN_HEIGHT - 20,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_list,
        )

        if GameSettings.ENABLE_TIMINGS:
            self.texts["fps"] = arcade.Text(
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

    def draw_texts(self):
        self.text_list.draw()
