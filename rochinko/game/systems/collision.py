class CollisionSystem:
    def setup_collision_handlers(self):
        handler = self.space.add_collision_handler(1, 2)  # 1 for balls, 2 for pegs
        handler.begin = self.handle_peg_collision

        bin_handler = self.space.add_collision_handler(1, 3)  # 3 for bins
        bin_handler.begin = self.handle_bin_collision

        obstacle_handler = self.space.add_collision_handler(1, 4)  # 4 for obstacles
        obstacle_handler.begin = self.handle_obstacle_collision

    def handle_peg_collision(self, arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        peg_shape = arbiter.shapes[1]

        peg = peg_shape.body.sprite

        return peg.on_collision(arbiter, space, data)

    def handle_bin_collision(self, arbiter, space, data):
        ball_shape = arbiter.shapes[0]
        bin_shape = arbiter.shapes[1]

        ball = ball_shape.body.sprite
        bin_sprite = bin_shape.body.sprite
        self.trigger_bin_effect(ball, bin_sprite, delayed=True)
        ball.remove_from_sprite_lists()

        return True

    def handle_obstacle_collision(self, arbiter, space, data):
        return True
