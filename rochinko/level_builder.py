import arcade
import random
import math

from .settings import *
from .lib import Peg


class LevelBuilder:
    @staticmethod
    def create_triangle_pattern():
        pegs = []
        for row in range(1, 10):
            for column in range(row):
                x = (Settings.SCREEN_WIDTH / 10) * (column + 1) + (row % 2) * (
                    Settings.SCREEN_WIDTH / 20
                )
                y = Settings.SCREEN_HEIGHT - (row * 50)
                peg = Peg(Settings.PEG_RADIUS, arcade.color.BLUE)
                peg.center_x = x
                peg.center_y = y
                pegs.append(peg)
        return pegs

    @staticmethod
    def create_diamond_pattern():
        pegs = []
        for row in range(10):
            for column in range(10 - abs(row - 4)):
                x = Settings.SCREEN_WIDTH / 2 + (column - (9 - abs(row - 4)) / 2) * 50
                y = Settings.SCREEN_HEIGHT - 100 - row * 50
                peg = Peg(Settings.PEG_RADIUS, arcade.color.BLUE)
                peg.center_x = x
                peg.center_y = y
                pegs.append(peg)
        return pegs

    @staticmethod
    def create_circular_pattern():
        pegs = []
        center_x, center_y = Settings.SCREEN_WIDTH / 2, Settings.SCREEN_HEIGHT / 2
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

            peg = Peg(Settings.PEG_RADIUS, arcade.color.BLUE, circular_movement)
            peg.center_x = x
            peg.center_y = y
            pegs.append(peg)
        return pegs

    @staticmethod
    def create_spiral_pattern():
        pegs = []
        center_x, center_y = Settings.SCREEN_WIDTH / 2, Settings.SCREEN_HEIGHT / 2
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

            peg = Peg(Settings.PEG_RADIUS, arcade.color.BLUE, rotating_movement)
            peg.center_x = x
            peg.center_y = y
            pegs.append(peg)
        return pegs

    @staticmethod
    def create_random_pattern():
        pegs = []
        for _ in range(50):
            x = random.randint(
                Settings.PEG_RADIUS, Settings.SCREEN_WIDTH - Settings.PEG_RADIUS
            )
            y = random.randint(
                Settings.PEG_RADIUS + 100, Settings.SCREEN_HEIGHT - Settings.PEG_RADIUS
            )

            def random_movement(t, start_x=x, start_y=y, amplitude=40):
                return (
                    start_x + amplitude * math.sin(t * 0.003 + random.random()),
                    start_y + amplitude * math.cos(t * 0.004 + random.random()),
                )

            peg = Peg(Settings.PEG_RADIUS, arcade.color.BLUE, random_movement)
            peg.center_x = x
            peg.center_y = y
            pegs.append(peg)
        return pegs
