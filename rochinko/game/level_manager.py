import pymunk
import arcade
import logging

from .level_builder import LevelBuilder
from .systems.score import ScoreSystem
from .level import Level

log = logging.getLogger(__name__)


class LevelManager(ScoreSystem):
    def __init__(self, window):
        ScoreSystem.__init__(self)
        self.window = window

        self.level_index = 0
        self.active_level = None
        self.level_builders = LevelBuilder.all_builders()

    def setup(self, level_idx=0, next_level=False):
        if next_level:
            self.level_index = (self.level_index + 1) % len(self.level_builders)
        else:
            self.level_index = level_idx

        if self.active_level and self.active_level.score:
            log.info(f"Adding score: {self.active_level.score}")
            self.add_score(self.active_level.score)

        self.active_level = self.load_level(self.level_index)
        self.active_level.setup_collision_handlers()

    def load_level(self, level_idx):
        if level_idx < len(self.level_builders):
            log.info(f"Loaded level {level_idx}")
            return self.level_builders[level_idx](self.window)
        else:
            log.info("No more levels available")
