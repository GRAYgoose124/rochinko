import arcade
import random

from ..settings import GameSettings


class MapNode:
    def __init__(self, level_index, x, y, radius=20, **data):
        self.level_index = level_index
        self.x = x
        self.y = y
        self.radius = radius
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


class MapView(arcade.View):
    def __init__(self):
        super().__init__()
        self.root_node = None
        self.current_node = None
        self.generate_map()

    def generate_map(self, depth=5, branching_factor=2):
        self.root_node = MapNode(
            0, GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT - 100
        )
        self.current_node = self.root_node

        nodes = [self.root_node]
        level_index = 1

        for _ in range(depth):
            new_nodes = []
            for node in nodes:
                for _ in range(random.randint(1, branching_factor)):
                    x = random.randint(50, GameSettings.SCREEN_WIDTH - 50)
                    y = node.y - 100
                    child = MapNode(level_index, x, y)
                    node.add_child(child)
                    new_nodes.append(child)
                    level_index += 1
            nodes = new_nodes

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        self.clear()
        self.draw_map(self.root_node)

        # Draw selection indicator
        arcade.draw_circle_outline(
            self.current_node.x,
            self.current_node.y,
            self.current_node.radius + 5,
            arcade.color.YELLOW,
            3,
        )

    def draw_map(self, node):
        # Draw connections to children
        for child in node.children:
            arcade.draw_line(node.x, node.y, child.x, child.y, arcade.color.WHITE, 2)

        # Draw node
        color = arcade.color.GREEN if node == self.current_node else arcade.color.RED
        arcade.draw_circle_filled(node.x, node.y, node.radius, color)

        # Draw level number
        arcade.draw_text(
            str(node.level_index),
            node.x,
            node.y,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            anchor_y="center",
        )

        # Recursively draw children
        for child in node.children:
            self.draw_map(child)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.current_node.parent:
            self.current_node = self.current_node.parent
        elif key == arcade.key.DOWN and self.current_node.children:
            self.current_node = self.current_node.children[0]
        elif key == arcade.key.LEFT and self.current_node.parent:
            siblings = self.current_node.parent.children
            current_index = siblings.index(self.current_node)
            self.current_node = siblings[(current_index - 1) % len(siblings)]
        elif key == arcade.key.RIGHT and self.current_node.parent:
            siblings = self.current_node.parent.children
            current_index = siblings.index(self.current_node)
            self.current_node = siblings[(current_index + 1) % len(siblings)]
        elif key == arcade.key.ENTER:
            level_view = self.window.level_view
            level_view.setup(level_index=self.current_node.level_index)
            self.window.show_view(level_view)
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
