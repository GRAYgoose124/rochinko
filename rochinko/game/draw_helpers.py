import array
from dataclasses import dataclass
import arcade
import math

from ..settings import GameSettings


def update_ball_path_preview(peg_list, aim_angle, shoot_power):
    preview_list = arcade.SpriteList()
    x = GameSettings.SHOOTER_X
    y = GameSettings.SHOOTER_Y
    dx = math.cos(aim_angle) * (shoot_power)
    dy = math.sin(aim_angle) * (shoot_power)

    done = False
    for _ in range(100):  # Limit the number of preview points
        preview_sprite = arcade.SpriteSolidColor(4, 4, color=arcade.color.YELLOW)
        preview_sprite.center_x = x
        preview_sprite.center_y = y
        preview_list.append(preview_sprite)
        x += dx * 0.05
        y += dy * 0.05
        dy += GameSettings.GRAVITY[1] * 0.05

        if x < 0 or x > GameSettings.SCREEN_WIDTH or y < 0:
            break

        for peg in peg_list:
            if (x - peg.center_x) ** 2 + (y - peg.center_y) ** 2 <= (
                GameSettings.BALL_RADIUS + GameSettings.PEG_RADIUS
            ) ** 2:
                done = True
                break
        if done:
            break

    return preview_list


@dataclass
class Burst:
    """Track for each burst."""

    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float
    time: float = 0
