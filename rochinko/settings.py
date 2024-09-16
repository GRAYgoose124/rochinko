import arcade
import json
import os
from dataclasses import dataclass, field, asdict
from dataclass_wizard import JSONFileWizard
from typing import Tuple, List


@dataclass
class __GameSettings(JSONFileWizard):
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 720
    BALL_RADIUS: int = 10
    PEG_RADIUS: int = 15
    GRAVITY: Tuple[float, float] = (0, -500)
    BOUNCE_DAMPING: float = 0.9
    SHOOTER_Y: int = 660
    SHOOTER_X: int = 640
    INITIAL_BALL_SPEED: int = 10
    PEG_INFLUENCE: float = 0.5
    MIN_SHOOT_POWER: int = 0
    MAX_SHOOT_POWER: int = 1000
    ENABLE_TIMINGS: bool = True
    SHOW_HIT_COUNTS: bool = True


MODIFIER_PALETTE: List[arcade.types.Color] = [
    arcade.color.WHITE_SMOKE,
    arcade.color.RED,
    arcade.color.GREEN,
    arcade.color.BLUE,
    arcade.color.YELLOW,
    arcade.color.ORANGE,
    arcade.color.PURPLE,
    arcade.color.PINK,
    arcade.color.GRAY,
    arcade.color.BROWN,
    arcade.color.LIME,
    arcade.color.MAROON,
    arcade.color.OLIVE,
]


# Load settings from JSON or use defaults
GameSettings = None
if os.path.exists("rochinko-config.json"):
    print("Loading settings from JSON")
    GameSettings = __GameSettings.from_json_file("rochinko-config.json")
else:
    print("Creating new settings")
    GameSettings = __GameSettings()
    GameSettings.to_json_file("rochinko-config.json", indent=2)

print(GameSettings)

__all__ = ["GameSettings", "MODIFIER_PALETTE"]
