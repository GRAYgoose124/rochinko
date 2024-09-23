from pathlib import Path
import arcade
import logging

from dataclasses import dataclass
from dataclass_wizard import JSONFileWizard
from typing import Tuple, List


log = logging.getLogger(__name__)


@dataclass
class __GameSettings(JSONFileWizard):
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 720
    SCREEN_REFRESH_RATE: int = 60

    SPACE_STEPS: int = 1
    SPACE_STEP_MULTIPLIER: int = 2

    SHOOTER_Y: int = 660
    SHOOTER_X: int = 640

    BALL_RADIUS: int = 10
    INITIAL_BALL_SPEED: int = 10
    PEG_RADIUS: int = 15
    PEG_INFLUENCE: float = 0.5
    GRAVITY: Tuple[float, float] = (0, -500)
    BOUNCE_DAMPING: float = 0.9
    MIN_SHOOT_POWER: int = 0
    MAX_SHOOT_POWER: int = 1000

    ENABLE_TIMINGS: bool = True
    SHOW_HIT_COUNTS: bool = True
    LOG_LEVEL: int = logging.DEBUG
    LOG_TO_FILE: bool = False

    PARTICLE_COUNT: int = 300
    PARTICLE_LIFETIME: int = 1500
    MAX_FADE_TIME: int = 3
    MIN_FADE_TIME: int = 0.1


assets_path = Path(__file__).parent / "assets"


SOUND_PATHS = {path.stem: path for path in assets_path.glob("sounds/*.mp3")}
LOADED_SOUNDS = {name: arcade.load_sound(path) for name, path in SOUND_PATHS.items()}

SHADERS_PATH: str = assets_path / "shaders"

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
try:
    GameSettings = __GameSettings.from_json_file("rochinko-config.json")
    log.info("Settings loaded from file successfully")
except Exception as e:
    GameSettings = __GameSettings()
    GameSettings.to_json_file("rochinko-config.json", indent=2)
    log.info("Initialized default settings")


log.debug(GameSettings)

__all__ = ["GameSettings", "MODIFIER_PALETTE"]
