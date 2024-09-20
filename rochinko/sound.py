from pathlib import Path
import arcade

assets_path = Path(__file__).parent / "assets"


SOUND_PATHS = {path.stem: path for path in assets_path.glob("sounds/*.mp3")}
LOADED_SOUNDS = {name: arcade.load_sound(path) for name, path in SOUND_PATHS.items()}
