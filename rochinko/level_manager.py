from dataclasses import dataclass, field
import pymunk
import arcade

from .settings import MODIFIER_PALETTE, GameSettings
from .objects import Peg, Obstacle
from .level_builder import LevelBuilder
from .level_systems import ScoreSystem, ModifierSystem, CollisionSystem


@dataclass
class Level(CollisionSystem, ModifierSystem, ScoreSystem):
    space: pymunk.Space = field(default_factory=pymunk.Space)
    ball_list: arcade.SpriteList = field(default_factory=arcade.SpriteList)
    peg_list: arcade.SpriteList = field(default_factory=arcade.SpriteList)
    bin_list: arcade.SpriteList = field(default_factory=arcade.SpriteList)
    obstacle_list: arcade.SpriteList = field(default_factory=arcade.SpriteList)

    def __post_init__(self):
        ScoreSystem.__init__(self)

    def draw(self):
        self.peg_list.draw()
        self.ball_list.draw()
        self.bin_list.draw()
        # self.obstacle_list.draw()

    def on_update(self, delta_time):
        self.space.step(delta_time)
        self.peg_list.update(delta_time)
        self.ball_list.update(delta_time)
        # bin_list.update(delta_time)
        # self.obstacle_list.update(delta_time)


class LevelManager(ScoreSystem):
    def __init__(self):
        self.level_index = 0
        self.active_level = None
        self.levels = [
            LevelBuilder.create_triangle_pattern,
            LevelBuilder.create_diamond_pattern,
            LevelBuilder.create_circular_pattern,
            LevelBuilder.create_spiral_pattern,
            LevelBuilder.create_random_pattern,
        ]

    def setup(self, level=0, next_level=False):
        if next_level:
            self.level_index = (self.level_index + 1) % len(self.levels)
        else:
            self.level_index = level

        self.active_level = self.load_level(self.level_index)
        self.active_level.setup_collision_handlers()

    def load_level(self, level):
        new_level = Level()
        new_level.space.gravity = GameSettings.GRAVITY
        if level < len(self.levels):
            pegs = self.levels[level]()
            for peg in pegs:
                p = Peg(peg.center_x, peg.center_y, peg.movement_function)
                p.shape.collision_type = 2  # Assign collision type for pegs
                p.body.sprite = p  # Store sprite reference in body
                new_level.peg_list.append(p)
                new_level.space.add(p.body, p.shape)
            self.active_level = new_level
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
            new_level.space.add(bin.body, bin.shape)
            bin.shape.collision_type = 3  # Assign collision type for bins
            bin.body.sprite = bin  # Store sprite reference in body
            bin.color = MODIFIER_PALETTE[i % len(MODIFIER_PALETTE)]
            new_level.bin_list.append(bin)

        return new_level
