import arcade


class Peg(arcade.SpriteCircle):
    def __init__(self, radius=10, color=(0, 0, 255), movement_function=None):
        super().__init__(radius, color)
        self.hit_count = 0
        self.movement_function = movement_function
        self.time = 0

    def update(self):
        if self.movement_function:
            self.time += 1
            self.center_x, self.center_y = self.movement_function(self.time)


class Obstacle(arcade.SpriteSolidColor):
    pass
