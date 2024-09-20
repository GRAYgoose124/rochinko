import arcade
import pymunk


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
