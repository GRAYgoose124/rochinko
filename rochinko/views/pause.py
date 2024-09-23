import arcade
from ..settings import GameSettings


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.text_items = ["Paused", "1. Resume", "2. Return to Menu", "3. Quit"]

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        for i, item in enumerate(self.text_items):
            arcade.draw_text(
                item,
                GameSettings.SCREEN_WIDTH / 2,
                GameSettings.SCREEN_HEIGHT / 2 + (len(self.text_items) / 2 - i) * 50,
                arcade.color.WHITE,
                font_size=30,
                anchor_x="center",
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1:
            self.window.show_view(self.game_view)
        elif key == arcade.key.KEY_2:
            self.window.show_view(self.window.menu_view)
        elif key == arcade.key.KEY_3:
            arcade.close_window()
