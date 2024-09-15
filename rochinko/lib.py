import arcade


class Peg(arcade.SpriteCircle):
    def __init__(self, radius=10, color=(0, 0, 255), movement_function=None):
        super().__init__(radius, color)
        self.hit_count = 0
        self.movement_function = movement_function
        self.time = 0
        self.text = None

    def update(self):
        if self.movement_function:
            self.time += 1
            self.center_x, self.center_y = self.movement_function(self.time)

        if self.text:
            self.text.text = str(self.hit_count)
            self.text.x = self.center_x
            self.text.y = self.center_y


class Obstacle(arcade.SpriteSolidColor):
    pass
