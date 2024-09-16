import arcade


class Modifier:
    def __init__(self, name, duration=None):
        self.name = name
        self.duration = duration  # Duration in seconds
        self.elapsed_time = 0

    def apply(self, ball):
        pass

    def update(self, ball, delta_time):
        if self.duration:
            self.elapsed_time += delta_time
            if self.elapsed_time >= self.duration:
                self.remove(ball)
                return True  # Indicates that the modifier should be removed
        return False

    def remove(self, ball):
        pass


class SpeedUpModifier(Modifier):
    def __init__(self, duration=None):
        super().__init__("speed_up", duration)

    def apply(self, ball):
        ball.change_x *= 1.5
        ball.change_y *= 1.5
        ball.color = arcade.color.RED  # Visual indication

    def remove(self, ball):
        ball.change_x /= 1.5
        ball.change_y /= 1.5
        ball.color = arcade.color.WHITE  # Reset color


class SlowDownModifier(Modifier):
    def __init__(self, duration=None):
        super().__init__("slow_down", duration)

    def apply(self, ball):
        ball.change_x *= 0.75
        ball.change_y *= 0.75
        ball.color = arcade.color.GREEN  # Visual indication

    def remove(self, ball):
        ball.change_x /= 0.75
        ball.change_y /= 0.75
        ball.color = arcade.color.WHITE  # Reset color


class BounceMoreModifier(Modifier):
    def __init__(self, duration=None):
        super().__init__("bounce_more", duration)

    def apply(self, ball):
        ball.color = arcade.color.BLUE  # Visual indication
        ball.shape.elasticity = 1.1

    def remove(self, ball):
        ball.color = arcade.color.WHITE  # Reset color


class NoBounceModifier(Modifier):
    def __init__(self, duration=None):
        super().__init__("no_bounce", duration)

    def apply(self, ball):
        ball.color = arcade.color.WHITE  # Visual indication
        ball.shape.elasticity = 0.0

    def remove(self, ball):
        ball.color = arcade.color.WHITE  # Reset color
        ball.shape.elasticity = 1.0


class InvertGravityModifier(Modifier):
    def __init__(self, duration=None):
        super().__init__("invert_gravity", duration)

    def apply(self, ball):
        ball.color = arcade.color.ORANGE  # Visual indication


__all__ = [
    "SpeedUpModifier",
    "SlowDownModifier",
    "BounceMoreModifier",
    "InvertGravityModifier",
    "NoBounceModifier",
]
