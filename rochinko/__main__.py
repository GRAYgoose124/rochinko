import arcade
import random
import math

from .settings import *
from .level_builder import LevelBuilder


class Pachinko(arcade.Window):
    def __init__(self):
        super().__init__(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, "Pachinko Game")
        self.ball_list = None
        self.peg_list = None
        self.bin_list = None
        self.current_level = 0
        self.levels = [
            LevelBuilder.create_triangle_pattern,
            LevelBuilder.create_diamond_pattern,
            LevelBuilder.create_circular_pattern,
            LevelBuilder.create_spiral_pattern,
            LevelBuilder.create_random_pattern,
        ]
        self.shooter_x = Settings.SCREEN_WIDTH // 2
        self.aim_angle = 0
        self.aiming = False
        self.shoot_power = 0
        self.max_shoot_power = 1000
        self.min_shoot_power = 200

    def setup(self):
        self.ball_list = arcade.SpriteList()
        self.peg_list = arcade.SpriteList()
        self.bin_list = arcade.SpriteList()
        self.load_level(self.current_level)

    def load_level(self, level):
        self.peg_list = arcade.SpriteList()

        if level < len(self.levels):
            self.peg_list.extend(self.levels[level]())
        else:
            print("No more levels available")

        # Create bins
        palette = [
            (255, 255, 255),
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
            (255, 128, 0),
            (0, 128, 255),
            (128, 0, 255),
        ]
        for i in range(10):
            bin_sprite = arcade.SpriteSolidColor(
                int(Settings.SCREEN_WIDTH / 10), 50, palette[i % len(palette)]
            )
            bin_sprite.center_x = (i + 0.5) * (Settings.SCREEN_WIDTH / 10)
            bin_sprite.center_y = 25
            self.bin_list.append(bin_sprite)

    def on_draw(self):
        self.clear()
        self.peg_list.draw()
        self.ball_list.draw()
        self.bin_list.draw()

        for peg in self.peg_list:
            arcade.draw_text(
                str(peg.hit_count),
                peg.center_x,
                peg.center_y,
                arcade.color.WHITE,
                10,
                anchor_x="center",
                anchor_y="center",
            )

        # Draw shooter
        arcade.draw_circle_filled(
            self.shooter_x, Settings.SHOOTER_Y, Settings.BALL_RADIUS, arcade.color.RED
        )

        # Draw aim line with power indicator
        if self.aiming:
            end_x = self.shooter_x + math.cos(self.aim_angle) * self.shoot_power / 5
            end_y = Settings.SHOOTER_Y + math.sin(self.aim_angle) * self.shoot_power / 5
            arcade.draw_line(
                self.shooter_x, Settings.SHOOTER_Y, end_x, end_y, arcade.color.WHITE, 2
            )
            # Draw power indicator
            arcade.draw_text(
                f"Power: {self.shoot_power:.0f}",
                self.shooter_x,
                Settings.SHOOTER_Y + 30,
                arcade.color.WHITE,
                12,
                anchor_x="center",
            )

        # Draw ball path preview
        if self.aiming:
            self.draw_ball_path_preview()

    def draw_ball_path_preview(self):
        preview_list = arcade.SpriteList()
        x = self.shooter_x
        y = Settings.SHOOTER_Y
        dx = math.cos(self.aim_angle) * (self.shoot_power / 50)
        dy = math.sin(self.aim_angle) * (self.shoot_power / 50)

        done = False
        for _ in range(100):  # Limit the number of preview points
            preview_sprite = arcade.SpriteSolidColor(4, 4, arcade.color.YELLOW)
            preview_sprite.center_x = x
            preview_sprite.center_y = y
            preview_list.append(preview_sprite)
            x += dx
            y += dy
            dy -= Settings.GRAVITY

            if x < 0 or x > Settings.SCREEN_WIDTH or y < 0:
                break

            for peg in self.peg_list:
                if (x - peg.center_x) ** 2 + (y - peg.center_y) ** 2 <= (
                    Settings.BALL_RADIUS + Settings.PEG_RADIUS
                ) ** 2:
                    done = True
                    break
            if done:
                break

        preview_list.draw()

    def on_update(self, delta_time):
        self.peg_list.update()
        self.ball_list.update()

        for ball in self.ball_list:
            ball.change_y -= Settings.GRAVITY

            hit_list = arcade.check_for_collision_with_list(ball, self.peg_list)

            if hit_list:
                for peg in hit_list:
                    peg.hit_count += 1
                    if peg.hit_count >= 3:
                        peg.remove_from_sprite_lists()

                    # Calculate bounce vector
                    normal_x = ball.center_x - peg.center_x
                    normal_y = ball.center_y - peg.center_y
                    normal_length = math.sqrt(normal_x**2 + normal_y**2)
                    normal_x /= normal_length
                    normal_y /= normal_length

                    # Calculate dot product
                    dot_product = (
                        ball.change_x * normal_x + ball.change_y * normal_y
                    ) * 2

                    # Update ball velocity
                    ball.change_x = (
                        ball.change_x - dot_product * normal_x
                    ) * Settings.BOUNCE_DAMPING
                    ball.change_y = (
                        ball.change_y - dot_product * normal_y
                    ) * Settings.BOUNCE_DAMPING

            # Check for collisions with bins
            bin_hit = arcade.check_for_collision_with_list(ball, self.bin_list)
            if bin_hit:
                bin_sprite = bin_hit[0]
                self.trigger_bin_effect(ball, bin_sprite)

            if ball.top < 0 or ball.left < 0 or ball.right > Settings.SCREEN_WIDTH:
                ball.remove_from_sprite_lists()

    def on_mouse_motion(self, x, y, dx, dy):
        self.aim_angle = math.atan2(y - Settings.SHOOTER_Y, x - self.shooter_x)
        distance = math.sqrt((x - self.shooter_x) ** 2 + (y - Settings.SHOOTER_Y) ** 2)
        self.shoot_power = min(
            max(distance * 2, self.min_shoot_power), self.max_shoot_power
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.aiming = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.current_level = (self.current_level + 1) % len(self.levels)
            self.load_level(self.current_level)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.aiming = False
            self.shoot_ball()

    def shoot_ball(self):
        ball = arcade.SpriteCircle(Settings.BALL_RADIUS, arcade.color.RED)
        ball.center_x = self.shooter_x
        ball.center_y = Settings.SHOOTER_Y
        ball.change_x = math.cos(self.aim_angle) * (self.shoot_power / 50)
        ball.change_y = math.sin(self.aim_angle) * (self.shoot_power / 50)
        ball.modifiers = []
        self.ball_list.append(ball)

    def trigger_bin_effect(self, ball, bin_sprite):
        # Example bin effects
        effects = {
            arcade.color.WHITE: lambda: None,  # No effect
            arcade.color.RED: lambda: ball.modifiers.append("speed_up"),
            arcade.color.GREEN: lambda: ball.modifiers.append("slow_down"),
            arcade.color.BLUE: lambda: ball.modifiers.append("bounce_more"),
            arcade.color.YELLOW: lambda: self.add_score(100),
            # Add more effects for other colors
        }
        effect = effects.get(bin_sprite.color, lambda: None)
        effect()
        self.apply_ball_modifiers(ball)

    def apply_ball_modifiers(self, ball):
        for modifier in ball.modifiers:
            if modifier == "speed_up":
                ball.change_x *= 1.5
                ball.change_y *= 1.5
            elif modifier == "slow_down":
                ball.change_x *= 0.75
                ball.change_y *= 0.75
            elif modifier == "bounce_more":
                global BOUNCE_DAMPING
                BOUNCE_DAMPING = 1.1  # Temporarily increase bounce
        ball.modifiers.clear()


def main():
    window = Pachinko()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
