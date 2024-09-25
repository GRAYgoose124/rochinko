import arcade
import random
import math

from ...settings import GameSettings, MODIFIER_PALETTE
from ..gobjects import Peg, Bomb, Obstacle, Bin
from ..level import Level
from .simple_patterns import PegPatternBuilder, ObstaclePatternBuilder


class LevelBuilder:
    @staticmethod
    def all_builders():
        return [
            LevelBuilder.create_triangle_level,
            LevelBuilder.create_diamond_level,
            LevelBuilder.create_circular_level,
            LevelBuilder.create_spiral_level,
            LevelBuilder.create_random_level,
        ]

    @staticmethod
    def create_level(pattern_func, obstacle_pattern_func=None):
        level = Level()

        # Add pegs
        pegs = pattern_func()
        level.add_gobjects(pegs, "peg")

        # Add bins
        bins = LevelBuilder.create_bins()
        level.add_gobjects(bins, "bin")

        # Add obstacles
        if obstacle_pattern_func:
            obstacles = obstacle_pattern_func()
        else:
            obstacles = ObstaclePatternBuilder.create_random_obstacles()
        level.add_gobjects(obstacles, "obstacle")

        return level

    @staticmethod
    def create_bins():
        bins = []
        for i in range(10):
            bin = Bin(
                int(GameSettings.SCREEN_WIDTH / 10),
                20,
                (i + 0.5) * (GameSettings.SCREEN_WIDTH / 10),
                25,
            )
            bin.color = MODIFIER_PALETTE[i % len(MODIFIER_PALETTE)]
            bins.append(bin)
        return bins

    @staticmethod
    def create_obstacles():
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
    def create_triangle_level():
        return LevelBuilder.create_level(
            PegPatternBuilder.create_triangle_pattern,
            ObstaclePatternBuilder.create_horizontal_obstacles,
        )

    @staticmethod
    def create_diamond_level():
        return LevelBuilder.create_level(
            PegPatternBuilder.create_diamond_pattern,
            ObstaclePatternBuilder.create_vertical_obstacles,
        )

    @staticmethod
    def create_circular_level():
        return LevelBuilder.create_level(
            PegPatternBuilder.create_circular_pattern,
            ObstaclePatternBuilder.create_circular_obstacles,
        )

    @staticmethod
    def create_spiral_level():
        return LevelBuilder.create_level(
            PegPatternBuilder.create_spiral_pattern,
            ObstaclePatternBuilder.create_spiral_obstacles,
        )

    @staticmethod
    def create_random_level():
        return LevelBuilder.create_level(
            PegPatternBuilder.create_random_pattern,
            ObstaclePatternBuilder.create_random_obstacles,
        )
