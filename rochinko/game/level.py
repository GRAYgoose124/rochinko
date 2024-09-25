import pymunk
import arcade
import logging

from ..settings import MODIFIER_PALETTE, GameSettings
from .gobjects import Obstacle, Ball, Peg, Bin
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

        self.gobjects = {
            "ball": arcade.SpriteList(),
            "peg": arcade.SpriteList(),
            "bin": arcade.SpriteList(),
            "obstacle": arcade.SpriteList(),
        }

    def on_update(self, delta_time):
        """Use like an arcade method"""
        # Game physics update
        for _ in range(GameSettings.SPACE_STEPS * GameSettings.SPACE_STEP_MULTIPLIER):
            self.space.step(delta_time)

        # Sprite updates
        for sprite_list in self.gobjects.values():
            sprite_list.update(delta_time)

    def add_gobject(self, gobject, collide=True):
        gtype = None
        collision_type = None
        if isinstance(gobject, Ball):
            collision_type = 1
            gtype = "ball"
        elif isinstance(gobject, Peg):
            collision_type = 2
            gtype = "peg"
        elif isinstance(gobject, Bin):
            collision_type = 3
            gtype = "bin"
        elif isinstance(gobject, Obstacle):
            collision_type = 4
            gtype = "obstacle"
        else:
            raise ValueError(f"Invalid gtype: {type(gobject)}")

        if collide:
            if gtype is None:
                raise ValueError(f"Invalid gtype: {type(gobject)}")
            gobject.shape.collision_type = collision_type
            gobject.body.sprite = gobject
            self.space.add(gobject.body, gobject.shape)

        self.gobjects.setdefault(gtype, arcade.SpriteList()).append(gobject)

    def add_gobjects(self, gobjects, collide=False):
        for p in gobjects:
            self.add_gobject(p, collide)

    def draw(self):
        for sprite_list in self.gobjects.values():
            sprite_list.draw()
