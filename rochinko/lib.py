import arcade
import pymunk

from .settings import Settings


class Ball(arcade.SpriteCircle):
    def __init__(self, x, y, space):
        # super().__init__("path/to/ball_image.png", scale=0.5)
        super().__init__(
            radius=Settings.BALL_RADIUS,
            color=arcade.color.WHITE,
            mass=1,
            center_x=x,
            center_y=y,
        )
        mass = 1
        radius = Settings.BALL_RADIUS
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4
        space.add(self.body, self.shape)
        self.modifiers = []

    def update(self):
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y
        self.angle = self.body.angle


class Peg(arcade.SpriteCircle):
    def __init__(self, x, y, space, movement_function=None):
        # super().__init__("path/to/peg_image.png", scale=0.5)
        super().__init__(
            radius=Settings.PEG_RADIUS,
            color=arcade.color.BLUE,
            mass=1,
            center_x=x,
            center_y=y,
        )
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, Settings.PEG_RADIUS)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.4
        space.add(self.body, self.shape)
        self.movement_function = movement_function
        self.time = 0
        self.hit_count = 0
        self.max_hit_count = 10

    def update(self):
        if self.movement_function:
            self.time += 1
            self.body.position = self.movement_function(self.time)
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y


class Obstacle(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y, space):
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
        space.add(self.body, self.shape)

    def update(self):
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y
