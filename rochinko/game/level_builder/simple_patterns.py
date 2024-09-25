import arcade
import random
import math

from ...settings import GameSettings
from ..gobjects import Peg, Bomb, Obstacle, Bin
from ..level import Level


class PegPatternBuilder:
    @staticmethod
    def create_triangle_pattern():
        pegs = arcade.SpriteList()
        for row in range(1, 20):
            for column in range(row):
                x = (GameSettings.SCREEN_WIDTH / 10) * (column + 1) + (row % 2) * (
                    GameSettings.SCREEN_WIDTH / 15
                )
                y = GameSettings.SCREEN_HEIGHT - (row * 30)
                if random.random() < 0.1:
                    peg = Bomb(x, y)
                else:
                    peg = Peg(x, y)
                pegs.append(peg)
        return pegs

    @staticmethod
    def create_diamond_pattern():
        pegs = arcade.SpriteList()
        for row in range(10):
            for column in range(10 - abs(row - 4)):
                x = (
                    GameSettings.SCREEN_WIDTH / 2
                    + (column - (9 - abs(row - 4)) / 2) * 50
                )
                y = GameSettings.SCREEN_HEIGHT - 100 - row * 50
                if random.random() < 0.1:
                    peg = Bomb(x, y)
                else:
                    peg = Peg(x, y)
                pegs.append(peg)
        return pegs

    @staticmethod
    def create_circular_pattern():
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
                    start_x + amplitude * math.cos(t * 4.5),
                    start_y + amplitude * math.sin(t * 4.5),
                )

            if random.random() < 0.1:
                peg = Bomb(x, y, movement_function=circular_movement)
            else:
                peg = Peg(x, y, movement_function=circular_movement)
            pegs.append(peg)
        return pegs

    @staticmethod
    def create_spiral_pattern():
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
                angle = -t * 0.75
                return (
                    center_x
                    + (start_x - center_x) * math.cos(angle)
                    - (start_y - center_y) * math.sin(angle),
                    center_y
                    + (start_x - center_x) * math.sin(angle)
                    + (start_y - center_y) * math.cos(angle),
                )

            if random.random() < 0.1:
                peg = Bomb(x, y, movement_function=rotating_movement)
            else:
                peg = Peg(x, y, movement_function=rotating_movement)
            pegs.append(peg)
        return pegs

    @staticmethod
    def create_random_pattern():
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

            if random.random() < 0.1:
                peg = Bomb(x, y, movement_function=random_movement)
            else:
                peg = Peg(x, y, movement_function=random_movement)
            pegs.append(peg)
        return pegs


class ObstaclePatternBuilder:
    @staticmethod
    def create_random_obstacles():
        obstacles = []
        for _ in range(3):
            x = random.randint(0, GameSettings.SCREEN_WIDTH)
            y = random.randint(
                GameSettings.SCREEN_HEIGHT // 2, GameSettings.SCREEN_HEIGHT
            )
            width = random.randint(50, 150)
            height = random.randint(10, 30)
            obstacle = Obstacle(width, height, x, y)
            obstacles.append(obstacle)
        return obstacles

    @staticmethod
    def create_horizontal_obstacles():
        obstacles = []
        for i in range(3):
            y = GameSettings.SCREEN_HEIGHT // 2 + i * 100
            width = random.randint(100, 200)
            height = 20
            x = random.randint(0, GameSettings.SCREEN_WIDTH - width)
            obstacle = Obstacle(width, height, x, y)
            obstacles.append(obstacle)
        return obstacles

    @staticmethod
    def create_vertical_obstacles():
        obstacles = []
        for i in range(2):
            x = GameSettings.SCREEN_WIDTH // 3 + i * (GameSettings.SCREEN_WIDTH // 3)
            width = 20
            height = random.randint(100, 200)
            y = random.randint(
                GameSettings.SCREEN_HEIGHT // 2, GameSettings.SCREEN_HEIGHT - height
            )
            obstacle = Obstacle(width, height, x, y)
            obstacles.append(obstacle)
        return obstacles

    @staticmethod
    def create_circular_obstacles():
        obstacles = []
        center_x, center_y = (
            GameSettings.SCREEN_WIDTH // 2,
            GameSettings.SCREEN_HEIGHT // 2,
        )
        radius = 250
        num_obstacles = 8
        for i in range(num_obstacles):
            angle = i * (2 * math.pi / num_obstacles)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            width = 30
            height = 30
            obstacle = Obstacle(width, height, x, y)
            obstacles.append(obstacle)
        return obstacles

    @staticmethod
    def create_spiral_obstacles():
        obstacles = []
        center_x, center_y = (
            GameSettings.SCREEN_WIDTH // 2,
            GameSettings.SCREEN_HEIGHT // 2,
        )
        for i in range(5):
            angle = i * 1.5
            radius = 100 + i * 30
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            width = 40
            height = 40
            obstacle = Obstacle(width, height, x, y)
            obstacles.append(obstacle)
        return obstacles
