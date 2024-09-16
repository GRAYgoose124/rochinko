import arcade
import pymunk
import math

from pyglet.graphics import Batch

from .settings import Settings
from .level_builder import LevelBuilder
from .draw_helpers import draw_ball_path_preview
from .objects import Ball, Peg, Obstacle
from .modifiers import SpeedUpModifier, SlowDownModifier, BounceMoreModifier


class Pachinko(arcade.Window):
    def __init__(self, enable_timings=True):
        super().__init__(
            Settings.SCREEN_WIDTH,
            Settings.SCREEN_HEIGHT,
            "Pachinko Game",
            resizable=True,
        )

        self.space = pymunk.Space()
        self.space.gravity = Settings.GRAVITY

        self.ball_list = arcade.SpriteList()
        self.peg_list = arcade.SpriteList()
        self.bin_list = arcade.SpriteList()

        self.score = 0
        self.current_level = 0
        self.levels = [
            LevelBuilder.create_triangle_pattern,
            LevelBuilder.create_diamond_pattern,
            LevelBuilder.create_circular_pattern,
            LevelBuilder.create_spiral_pattern,
            LevelBuilder.create_random_pattern,
        ]

        self.aim_angle = 0
        self.aiming = False
        self.shoot_power = 0
        self.max_shoot_power = 200
        self.min_shoot_power = 0

        self.text_batch = None
        self.power_text = None
        self.score_text = None
        self.fps_text = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.enable_timings = enable_timings
        if self.enable_timings:
            arcade.enable_timings()

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def setup(self):
        self.load_level(self.current_level)
        self.setup_collision_handlers()

    def setup_collision_handlers(self):
        handler = self.space.add_collision_handler(1, 2)  # 1 for balls, 2 for pegs
        handler.begin = self.handle_collision

        bin_handler = self.space.add_collision_handler(1, 3)  # 3 for bins
        bin_handler.begin = self.handle_bin_collision

    def handle_collision(self, arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        peg_shape = arbiter.shapes[1]

        peg = peg_shape.body.sprite
        peg.hit_count += 1

        return True

    def handle_bin_collision(self, arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        bin_shape = arbiter.shapes[1]

        ball = ball_shape.body.sprite
        bin_sprite = bin_shape.body.sprite
        self.trigger_bin_effect(ball, bin_sprite)
        self.space.remove(ball.body, ball.shape)
        ball.remove_from_sprite_lists()

        return True

    def load_level(self, level):
        self.current_level = level
        self.space = pymunk.Space()
        self.space.gravity = Settings.GRAVITY
        self.ball_list = arcade.SpriteList()
        self.peg_list = arcade.SpriteList()
        self.bin_list = arcade.SpriteList()

        if level < len(self.levels):
            pegs = self.levels[level]()
            for peg in pegs:
                new_peg = Peg(peg.center_x, peg.center_y, peg.movement_function)
                new_peg.shape.collision_type = 2  # Assign collision type for pegs
                new_peg.body.sprite = new_peg  # Store sprite reference in body
                self.peg_list.append(new_peg)
                self.space.add(new_peg.body, new_peg.shape)
        else:
            print("No more levels available")

        # Create bins
        for i in range(10):
            bin = Obstacle(
                int(Settings.SCREEN_WIDTH / 10),
                20,
                (i + 0.5) * (Settings.SCREEN_WIDTH / 10),
                25,
            )
            self.space.add(bin.body, bin.shape)
            bin.shape.collision_type = 3  # Assign collision type for bins
            bin.body.sprite = bin  # Store sprite reference in body
            bin.color = Settings.PALETTE[i % len(Settings.PALETTE)]
            self.bin_list.append(bin)

        self.__init_texts()
        self.setup_collision_handlers()

    def __init_texts(self):
        self.text_batch = Batch()

        self.power_text = arcade.Text(
            f"Power: {self.shoot_power:.0f}",
            Settings.SHOOTER_X,
            Settings.SHOOTER_Y + 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_batch,
        )
        self.score_text = arcade.Text(
            f"Score: {self.score}",
            Settings.SHOOTER_X,
            Settings.SHOOTER_Y - 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_batch,
        )
        if self.enable_timings:
            self.fps_text = arcade.Text(
                f"FPS: {arcade.get_fps():.0f}",
                Settings.SHOOTER_X,
                Settings.SHOOTER_Y - 60,
                arcade.color.WHITE,
                12,
                anchor_x="center",
                batch=self.text_batch,
            )
        # Add hit count text to pegs
        for peg in self.peg_list:
            peg.text = arcade.Text(
                str(peg.hit_count),
                peg.center_x,
                peg.center_y,
                arcade.color.WHITE,
                10,
                anchor_x="center",
                anchor_y="center",
                batch=self.text_batch,
            )

    def on_draw(self):
        self.clear()
        self.peg_list.draw()
        self.ball_list.draw()
        self.bin_list.draw()
        self.text_batch.draw()
        if self.fps_text:
            self.fps_text.draw()

        # Draw shooter
        arcade.draw_circle_filled(
            Settings.SHOOTER_X,
            Settings.SHOOTER_Y,
            Settings.BALL_RADIUS,
            arcade.color.RED,
        )

        # Draw aim line with power indicator
        if self.aiming:
            arcade.draw_line(
                Settings.SHOOTER_X,
                Settings.SHOOTER_Y,
                self.mouse_x,
                self.mouse_y,
                arcade.color.WHITE,
                2,
            )
            self.power_text.text = f"Power: {self.shoot_power:.0f}"

        # Draw ball path preview
        draw_ball_path_preview(
            self.peg_list,
            Settings.SHOOTER_X,
            Settings.SHOOTER_Y,
            self.aim_angle,
            self.shoot_power,
        )

    def on_update(self, delta_time):
        for _ in range(5):
            self.space.step(delta_time * 3)
        self.peg_list.update()
        self.ball_list.update()

        # Remove balls that are out of bounds
        for ball in self.ball_list:
            if (
                ball.center_y < 0
                or ball.center_x < 0
                or ball.center_x > Settings.SCREEN_WIDTH
            ):
                self.space.remove(ball.body, ball.shape)
                ball.remove_from_sprite_lists()

        # Update peg hit counts
        for peg in self.peg_list:
            if peg.text:
                peg.text.text = str(peg.hit_count)
                peg.text.x = peg.center_x
                peg.text.y = peg.center_y
            if peg.hit_count >= peg.max_hit_count:
                self.space.remove(peg.body, peg.shape)
                peg.remove_from_sprite_lists()
                del peg.text

        self.score_text.text = f"Score: {self.score}"
        self.fps_text.text = f"FPS: {arcade.get_fps():.0f}"

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        self.aim_angle = math.atan2(y - Settings.SHOOTER_Y, x - Settings.SHOOTER_X)
        distance = math.sqrt(
            (x - Settings.SHOOTER_X) ** 2 + (y - Settings.SHOOTER_Y) ** 2
        )
        self.shoot_power = min(
            max(distance, self.min_shoot_power), self.max_shoot_power
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.aiming = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.load_level((self.current_level + 1) % len(self.levels))

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.aiming = False
            self.shoot_ball()

    def shoot_ball(self):
        ball = Ball(Settings.SHOOTER_X, Settings.SHOOTER_Y)
        self.space.add(ball.body, ball.shape)
        ball.shape.collision_type = 1  # Assign collision type for balls
        ball.body.sprite = ball  # Store sprite reference in body
        ball.body.velocity = (
            math.cos(self.aim_angle) * (self.shoot_power),
            math.sin(self.aim_angle) * (self.shoot_power),
        )
        self.ball_list.append(ball)

    def trigger_bin_effect(self, ball, bin_sprite):
        effects = {
            arcade.color.RED: lambda: self.apply_modifier(
                ball, SpeedUpModifier("speed_up", duration=5)
            ),
            arcade.color.GREEN: lambda: self.apply_modifier(
                ball, SlowDownModifier("slow_down", duration=5)
            ),
            arcade.color.BLUE: lambda: self.apply_modifier(
                ball, BounceMoreModifier("bounce_more", duration=5)
            ),
            arcade.color.YELLOW: lambda: self.add_score(100),
        }
        effect = effects.get(bin_sprite.color, lambda: None)
        effect()

    def apply_modifier(self, ball, modifier):
        modifier.apply(ball)
        ball.modifiers.append(modifier)
        arcade.schedule_once(
            lambda _: self.remove_modifier(ball, modifier), modifier.duration
        )

    def remove_modifier(self, ball, modifier):
        if modifier in ball.modifiers:
            modifier.remove(ball)
            ball.modifiers.remove(modifier)

    def add_score(self, score):
        self.score += score
        print(f"Score: {self.score}")


def main():
    window = Pachinko()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
