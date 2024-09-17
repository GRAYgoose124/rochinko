from pathlib import Path
import arcade

assets_path = Path(__file__).parent / "assets"


SOUND_PATHS = {
    "clang": assets_path / "sounds" / "clang.mp3",
}

LOADED_SOUNDS = {name: arcade.load_sound(path) for name, path in SOUND_PATHS.items()}
