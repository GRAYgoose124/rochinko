import arcade
import math

from .settings import Settings


def draw_ball_path_preview(peg_list, shooter_x, shooter_y, aim_angle, shoot_power):
    preview_list = arcade.SpriteList()
    x = shooter_x
    y = shooter_y
    dx = math.cos(aim_angle) * (shoot_power)
    dy = math.sin(aim_angle) * (shoot_power)

    done = False
    for _ in range(100):  # Limit the number of preview points
        preview_sprite = arcade.SpriteSolidColor(4, 4, color=arcade.color.YELLOW)
        preview_sprite.center_x = x
        preview_sprite.center_y = y
        preview_list.append(preview_sprite)
        x += dx * 0.1
        y += dy * 0.1
        dy += Settings.GRAVITY[1] * 0.1

        if x < 0 or x > Settings.SCREEN_WIDTH or y < 0:
            break

        for peg in peg_list:
            if (x - peg.center_x) ** 2 + (y - peg.center_y) ** 2 <= (
                Settings.BALL_RADIUS + Settings.PEG_RADIUS
            ) ** 2:
                done = True
                break
        if done:
            break

    preview_list.draw()
