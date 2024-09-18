import math

from .objects import Ball
from .settings import GameSettings


def shoot_ball(level, aim_angle, shoot_power):
    ball = Ball(GameSettings.SHOOTER_X, GameSettings.SHOOTER_Y)

    ball.shape.collision_type = 1  # Assign collision type for balls
    ball.body.sprite = ball  # Store sprite reference in body
    ball.body.velocity = (
        math.cos(aim_angle) * (shoot_power),
        math.sin(aim_angle) * (shoot_power),
    )

    level.space.add(ball.body, ball.shape)
    level.ball_list.append(ball)

    if len(level.pending_modifiers) > 0:
        level.apply_modifier(ball, level.pending_modifiers.pop(0))
