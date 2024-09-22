import pymunk


class MovingBody:
    def __init__(self, x, y, shape=None, movement_function=None):
        if movement_function is None:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = shape
        self.movement_function = movement_function
        self.time = 0

    def update_position(self, delta_time):
        if self.movement_function:
            self.time += delta_time
            self.body.position = self.movement_function(self.time)
        self.center_x = self.body.position.x
        self.center_y = self.body.position.y
