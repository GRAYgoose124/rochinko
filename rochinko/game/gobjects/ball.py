import math
import arcade
import pymunk

from ...settings import GameSettings


class Ball(arcade.SpriteCircle):
    def __init__(self, x, y):
        # super().__init__("path/to/ball_image.png", scale=0.5)
        super().__init__(
            radius=GameSettings.BALL_RADIUS,
            color=arcade.color.WHITE,
            mass=1,
        )
        mass = 1
        radius = GameSettings.BALL_RADIUS
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0.9
        self.shape.friction = 0.1
        self.modifiers = []

    def update(self, delta_time):
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y
        self.angle = self.body.angle

        # Remove ball if it goes out of bounds
        if (
            self.center_y < 0
            or self.center_x < 0
            or self.center_x > GameSettings.SCREEN_WIDTH
        ):
            self.body.space.remove(self.body, self.shape)
            self.remove_from_sprite_lists()

    @classmethod
    def shoot(cls, level, aim_angle, shoot_power):
        ball = cls(GameSettings.SHOOTER_X, GameSettings.SHOOTER_Y)
        ball.body.sprite = ball  # Store sprite reference in body
        ball.body.velocity = (
            math.cos(aim_angle) * (shoot_power),
            math.sin(aim_angle) * (shoot_power),
        )

        level.add_gobject(ball)

        if len(level.pending_modifiers) > 0:
            level.apply_modifier(ball, level.pending_modifiers.pop(0))
