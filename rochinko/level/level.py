import pymunk
import arcade
import logging

from ..settings import MODIFIER_PALETTE, GameSettings
from ..objects import Obstacle
from .systems import ScoreSystem, ModifierSystem, CollisionSystem


log = logging.getLogger(__name__)


class Level(CollisionSystem, ModifierSystem, ScoreSystem):
    def __init__(self):
        CollisionSystem.__init__(self)
        ModifierSystem.__init__(self)
        ScoreSystem.__init__(self)

        self.space = pymunk.Space()
        self.space.gravity = GameSettings.GRAVITY

        self.ball_list = arcade.SpriteList()
        self.peg_list = arcade.SpriteList()
        self.bin_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()

        self.space_steps = 1

        self.__init_bins()

    def __init_bins(self):
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

    def add_pegs(self, pegs):
        for p in pegs:
            p.shape.collision_type = 2  # Assign collision type for pegs
            p.body.sprite = p  # Store sprite reference in body
            self.peg_list.append(p)
            self.space.add(p.body, p.shape)

    def draw(self):
        self.peg_list.draw()
        self.ball_list.draw()
        self.bin_list.draw()
        # self.obstacle_list.draw()

    def on_update(self, delta_time):
        for _ in range(self.space_steps * 2):
            self.space.step(delta_time)
        self.peg_list.update(delta_time)
        self.ball_list.update(delta_time)
        # bin_list.update(delta_time)
        # self.obstacle_list.update(delta_time)
