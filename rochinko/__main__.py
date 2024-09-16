import arcade
import pymunk
import math

from pyglet.graphics import Batch

from .settings import GameSettings, MODIFIER_PALETTE
from .level_builder import LevelBuilder
from .draw_helpers import update_ball_path_preview
from .objects import Ball, Peg, Obstacle
from .modifiers import *


class Pachinko(arcade.Window):
    def __init__(self):
        super().__init__(
            GameSettings.SCREEN_WIDTH,
            GameSettings.SCREEN_HEIGHT,
            "Pachinko Game",
            resizable=True,
        )

        self.space = None
        self.ball_list = None
        self.peg_list = None
        self.bin_list = None
        self.obstacle_list = None
        self.aim_preview_list = None

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
        self.old_shoot_power = None

        self.text_list = None
        self.power_text = None
        self.score_text = None
        self.fps_text = None

        self.mouse_x = 0
        self.mouse_y = 0

        if GameSettings.ENABLE_TIMINGS:
            arcade.enable_timings()

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def setup(self, level=0):
        self.__reset_state()
        self.load_level(level)
        self.__init_texts()
        self.__setup_collision_handlers()

    def __reset_state(self):
        self.space = pymunk.Space()
        self.space.gravity = GameSettings.GRAVITY
        self.ball_list = arcade.SpriteList()
        self.peg_list = arcade.SpriteList()
        self.bin_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.aim_preview_list = arcade.SpriteList()

        self.score = 0
        self.current_level = 0
        self.aim_angle = 0
        self.aiming = False
        self.shoot_power = 0
        self.old_shoot_power = None

    def __setup_collision_handlers(self):
        handler = self.space.add_collision_handler(1, 2)  # 1 for balls, 2 for pegs
        handler.begin = self.handle_peg_collision

        bin_handler = self.space.add_collision_handler(1, 3)  # 3 for bins
        bin_handler.begin = self.handle_bin_collision

    def handle_peg_collision(self, arbiter, space, data):
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

        return True

    def load_level(self, level):
        if level < len(self.levels):
            pegs = self.levels[level]()
            for peg in pegs:
                new_peg = Peg(peg.center_x, peg.center_y, peg.movement_function)
                new_peg.shape.collision_type = 2  # Assign collision type for pegs
                new_peg.body.sprite = new_peg  # Store sprite reference in body
                self.peg_list.append(new_peg)
                self.space.add(new_peg.body, new_peg.shape)
            self.current_level = level
            print(f"Loaded level {level}")
        else:
            print("No more levels available")

        # Create bins
        for i in range(10):
            bin = Obstacle(
                int(GameSettings.SCREEN_WIDTH / 10),
                20,
                (i + 0.5) * (GameSettings.SCREEN_WIDTH / 10),
                25,
            )
            self.space.add(bin.body, bin.shape)
            bin.shape.collision_type = 3  # Assign collision type for bins
            bin.body.sprite = bin  # Store sprite reference in body
            bin.color = MODIFIER_PALETTE[i % len(MODIFIER_PALETTE)]
            self.bin_list.append(bin)

    def __init_texts(self):
        self.text_list = Batch()

        self.power_text = arcade.Text(
            f"Power: {self.shoot_power:.0f}",
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y + 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_list,
        )
        self.score_text = arcade.Text(
            f"Score: {self.score}",
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y - 30,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            batch=self.text_list,
        )
        if GameSettings.ENABLE_TIMINGS:
            self.fps_text = arcade.Text(
                f"FPS: {arcade.get_fps():.0f}",
                GameSettings.SHOOTER_X,
                GameSettings.SHOOTER_Y - 60,
                arcade.color.WHITE,
                12,
                anchor_x="center",
                batch=self.text_list,
            )
        # Add hit count text to pegs
        if GameSettings.SHOW_HIT_COUNTS:
            for peg in self.peg_list:
                peg.text = arcade.Text(
                    str(peg.hit_count),
                    peg.center_x,
                    peg.center_y,
                    arcade.color.WHITE,
                    10,
                    anchor_x="center",
                    anchor_y="center",
                    batch=self.text_list,
                )

    def on_draw(self):
        self.clear()
        self.peg_list.draw()
        self.ball_list.draw()
        self.bin_list.draw()
        self.text_list.draw()
        self.aim_preview_list.draw()

        # Draw shooter
        arcade.draw_circle_filled(
            GameSettings.SHOOTER_X,
            GameSettings.SHOOTER_Y,
            GameSettings.BALL_RADIUS,
            arcade.color.RED,
        )

        # Draw aim line with power indicator
        if self.aiming:
            arcade.draw_line(
                GameSettings.SHOOTER_X,
                GameSettings.SHOOTER_Y,
                self.mouse_x,
                self.mouse_y,
                arcade.color.WHITE,
                1,
            )

    def on_update(self, delta_time):
        self.space.step(delta_time)
        self.peg_list.update(delta_time)
        self.ball_list.update(delta_time)

        self.score_text.text = f"Score: {self.score}"
        if self.fps_text:
            self.fps_text.text = f"FPS: {arcade.get_fps():.0f}"

        # TODO: this is slowish
        self.aim_preview_list = update_ball_path_preview(
            self.peg_list,
            self.aim_angle,
            self.shoot_power,
        )

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        self.aim_angle = math.atan2(
            y - GameSettings.SHOOTER_Y, x - GameSettings.SHOOTER_X
        )
        distance = math.sqrt(
            (x - GameSettings.SHOOTER_X) ** 2 + (y - GameSettings.SHOOTER_Y) ** 2
        )
        self.shoot_power = min(
            max(distance, GameSettings.MIN_SHOOT_POWER),
            GameSettings.MAX_SHOOT_POWER,
        )
        if self.old_shoot_power != self.shoot_power:
            self.power_text.text = f"Power: {self.shoot_power:.0f}"
            self.old_shoot_power = self.shoot_power

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.aiming = True
        elif button == arcade.MOUSE_BUTTON_RIGHT and not self.aiming:
            self.setup((self.current_level + 1) % len(self.levels))
        else:
            self.aiming = False

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.aiming:
            self.aiming = False
            self.shoot_ball()

    def shoot_ball(self):
        ball = Ball(GameSettings.SHOOTER_X, GameSettings.SHOOTER_Y)
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
                ball, SpeedUpModifier(duration=5)
            ),
            arcade.color.GREEN: lambda: self.apply_modifier(
                ball, SlowDownModifier(duration=5)
            ),
            arcade.color.BLUE: lambda: self.apply_modifier(
                ball, BounceMoreModifier(duration=5)
            ),
            arcade.color.YELLOW: lambda: self.add_score(100),
            arcade.color.ORANGE: lambda: self.apply_modifier(
                ball, InvertGravityModifier(duration=5)
            ),
            arcade.color.WHITE: lambda: self.apply_modifier(
                ball, NoBounceModifier(duration=5)
            ),
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


def main():
    window = Pachinko()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
