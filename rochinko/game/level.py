import pymunk
import arcade
import logging

from ..settings import MODIFIER_PALETTE, GameSettings
from .gobjects import Obstacle
from .systems.score import ScoreSystem
from .systems.modifier import ModifierSystem
from .systems.collision import CollisionSystem


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

        self.__init_bins()

    def __init_bins(self):
        for i in range(10):
            bin = Obstacle(
                int(GameSettings.SCREEN_WIDTH / 10),
                20,
                (i + 0.5) * (GameSettings.SCREEN_WIDTH / 10),
                25,
            )
            bin.color = MODIFIER_PALETTE[i % len(MODIFIER_PALETTE)]

            self.add_gobject(bin, gtype="bin", collision_type=3)

    def add_gobject(self, gobject, gtype=None, collision_type=None):
        if collision_type is not None:
            gobject.shape.collision_type = collision_type
            gobject.body.sprite = gobject  # Store sprite reference in body
            self.space.add(gobject.body, gobject.shape)

        if gtype == "peg":
            self.peg_list.append(gobject)
        elif gtype == "bin":
            self.bin_list.append(gobject)
        elif gtype == "ball":
            self.ball_list.append(gobject)
        elif gtype == "obstacle":
            self.obstacle_list.append(gobject)
        else:
            raise ValueError(f"Unknown gtype: {gtype}")

    def add_gobjects(self, gobjects, gtype=None, collision_type=None):
        for p in gobjects:
            self.add_gobject(p, gtype, collision_type)

    def draw(self):
        self.peg_list.draw()
        self.ball_list.draw()
        self.bin_list.draw()
        # self.obstacle_list.draw()

    def on_update(self, delta_time):
        for _ in range(GameSettings.SPACE_STEPS * GameSettings.SPACE_STEP_MULTIPLIER):
            self.space.step(delta_time)
        self.peg_list.update(delta_time)
        self.ball_list.update(delta_time)
        # bin_list.update(delta_time)
        # self.obstacle_list.update(delta_time)
