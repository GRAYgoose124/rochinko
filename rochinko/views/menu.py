import arcade

from ..settings import GameSettings


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.text_items = ["Rochinko", "1. Start Game", "2. Show Map", "3. Quit"]

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

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
            level_view = self.window.level_view
            level_view.setup()
            self.window.show_view(level_view)
        elif key == arcade.key.KEY_2:
            map_view = self.window.map_view
            self.window.show_view(map_view)
        elif key == arcade.key.KEY_3:
            arcade.close_window()
