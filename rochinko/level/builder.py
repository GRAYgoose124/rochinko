import arcade
import random
import math

from ..settings import GameSettings
from ..gobjects import Peg, Bomb


class LevelBuilder:
    @staticmethod
    def all_builders():
        return [
            LevelBuilder.create_triangle_pattern,
            LevelBuilder.create_diamond_pattern,
            LevelBuilder.create_circular_pattern,
            LevelBuilder.create_spiral_pattern,
            LevelBuilder.create_random_pattern,
        ]

    @staticmethod
    def create_triangle_pattern(window):
        pegs = arcade.SpriteList()
        for row in range(1, 20):
            for column in range(row):
                x = (GameSettings.SCREEN_WIDTH / 10) * (column + 1) + (row % 2) * (
                    GameSettings.SCREEN_WIDTH / 15
                )
                y = GameSettings.SCREEN_HEIGHT - (row * 30)
                if random.random() < 0.1:
                    peg = Bomb(x, y, window)
                else:
                    peg = Peg(x, y)
                pegs.append(peg)
        return pegs

    @staticmethod
    def create_diamond_pattern(window):
        pegs = arcade.SpriteList()
        for row in range(10):
            for column in range(10 - abs(row - 4)):
                x = (
                    GameSettings.SCREEN_WIDTH / 2
                    + (column - (9 - abs(row - 4)) / 2) * 50
                )
                y = GameSettings.SCREEN_HEIGHT - 100 - row * 50
                peg = Peg(x, y)
                pegs.append(peg)
        return pegs

    @staticmethod
    def create_circular_pattern(window):
        pegs = arcade.SpriteList()
        center_x, center_y = (
            GameSettings.SCREEN_WIDTH / 2,
            GameSettings.SCREEN_HEIGHT / 2,
        )
        for i in range(50):
            angle = i * (2 * math.pi / 50)
            radius = 200
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            def circular_movement(t, start_x=x, start_y=y, amplitude=30):
                return (
                    start_x + amplitude * math.cos(t * 0.05),
                    start_y + amplitude * math.sin(t * 0.05),
                )

            peg = Peg(x, y, movement_function=circular_movement)
            pegs.append(peg)
        return pegs

    @staticmethod
    def create_spiral_pattern(window):
        pegs = arcade.SpriteList()
        center_x, center_y = (
            GameSettings.SCREEN_WIDTH / 2,
            GameSettings.SCREEN_HEIGHT / 2,
        )
        for i in range(100):
            angle = i * 0.5
            radius = 10 + i * 3
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            # TODO better and more consistent movement function
            def rotating_movement(t, start_x=x, start_y=y, amplitude=20):
                # rotate the pegs as a group around the center
                angle = -t * 0.1
                return (
                    center_x
                    + (start_x - center_x) * math.cos(angle)
                    - (start_y - center_y) * math.sin(angle),
                    center_y
                    + (start_x - center_x) * math.sin(angle)
                    + (start_y - center_y) * math.cos(angle),
                )

            peg = Peg(x, y, movement_function=rotating_movement)
            pegs.append(peg)
        return pegs

    @staticmethod
    def create_random_pattern(window):
        pegs = arcade.SpriteList()
        for _ in range(50):
            x = random.randint(
                GameSettings.PEG_RADIUS,
                GameSettings.SCREEN_WIDTH - GameSettings.PEG_RADIUS,
            )
            y = random.randint(
                GameSettings.PEG_RADIUS + 100,
                GameSettings.SCREEN_HEIGHT - GameSettings.PEG_RADIUS,
            )

            def random_movement(t, start_x=x, start_y=y, amplitude=40):
                return (
                    start_x + amplitude * math.sin(t * 0.003 + random.random()),
                    start_y + amplitude * math.cos(t * 0.004 + random.random()),
                )

            peg = Peg(x, y, movement_function=random_movement)
            pegs.append(peg)
        return pegs
