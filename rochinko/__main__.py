# main.py
import arcade
import logging

from .settings import GameSettings
from .views.level import LevelView
from .views.menu import MenuView  # We'll create this later


class RochinkoApp(arcade.Window):
    def __init__(self):
        super().__init__(
            GameSettings.SCREEN_WIDTH,
            GameSettings.SCREEN_HEIGHT,
            "Pachinko Game",
            resizable=True,
        )
        self.level_view = None
        self.menu_view = None

        if GameSettings.ENABLE_TIMINGS:
            arcade.enable_timings()

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def setup(self):
        self.level_view = LevelView()
        self.menu_view = MenuView()
        self.show_view(self.menu_view)

    def on_resize(self, width, height):
        super().on_resize(width, height)
        GameSettings.SCREEN_WIDTH = width
        GameSettings.SCREEN_HEIGHT = height
        GameSettings.SHOOTER_X = width / 2
        GameSettings.SHOOTER_Y = height - 60

        # Update the current view
        self.current_view.on_resize(width, height)


def main():
    logging.basicConfig(
        level=GameSettings.LOG_LEVEL,
        filename="rochinko.log" if GameSettings.LOG_TO_FILE else None,
        format="%(levelname)s - %(message)s",
    )
    logging.getLogger("arcade").setLevel(logging.WARNING)
    logging.getLogger("pymunk").setLevel(logging.WARNING)

    window = RochinkoApp()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
