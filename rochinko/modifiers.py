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
    def apply(self, ball):
        ball.change_x *= 1.5
        ball.change_y *= 1.5
        ball.color = arcade.color.RED  # Visual indication

    def remove(self, ball):
        ball.change_x /= 1.5
        ball.change_y /= 1.5
        ball.color = arcade.color.WHITE  # Reset color


class SlowDownModifier(Modifier):
    def apply(self, ball):
        ball.change_x *= 0.75
        ball.change_y *= 0.75
        ball.color = arcade.color.GREEN  # Visual indication

    def remove(self, ball):
        ball.change_x /= 0.75
        ball.change_y /= 0.75
        ball.color = arcade.color.WHITE  # Reset color


class BounceMoreModifier(Modifier):
    def apply(self, ball):
        ball.color = arcade.color.BLUE  # Visual indication

    def remove(self, ball):
        ball.color = arcade.color.WHITE  # Reset color
