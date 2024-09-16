import json
import os

import arcade


if os.path.exists("rochinko-config.json"):
    with open("rochinko-config.json", "r") as f:
        config = json.load(f)
else:
    config = {
        "SCREEN_WIDTH": 1280,
        "SCREEN_HEIGHT": 720,
        "BALL_RADIUS": 10,
        "PEG_RADIUS": 15,
        "GRAVITY": (0, -9.8),
        "BOUNCE_DAMPING": 0.9,
        "SHOOTER_Y": 660,
        "SHOOTER_X": 640,
        "INITIAL_BALL_SPEED": 10,
        "PEG_INFLUENCE": 0.5,
    }
    with open("rochinko-config.json", "w") as f:
        json.dump(config, f, indent=2)


class GameSettings:
    SCREEN_WIDTH = config["SCREEN_WIDTH"]
    SCREEN_HEIGHT = config["SCREEN_HEIGHT"]
    BALL_RADIUS = config["BALL_RADIUS"]
    PEG_RADIUS = config["PEG_RADIUS"]
    GRAVITY = config["GRAVITY"]
    BOUNCE_DAMPING = config["BOUNCE_DAMPING"]
    SHOOTER_Y = config["SHOOTER_Y"]
    SHOOTER_X = config["SHOOTER_X"]
    INITIAL_BALL_SPEED = config["INITIAL_BALL_SPEED"]
    PEG_INFLUENCE = config["PEG_INFLUENCE"]

    PALETTE = [
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


__all__ = [
    "GameSettings",
]
