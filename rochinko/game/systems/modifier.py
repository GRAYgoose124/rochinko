import arcade

from ..modifiers import *
from ..modifiers import Modifier


DEFAULT_BIN_EFFECTS = {
    arcade.color.RED: SpeedUpModifier(duration=5),
    arcade.color.GREEN: SlowDownModifier(duration=5),
    arcade.color.BLUE: BounceMoreModifier(duration=5),
    arcade.color.YELLOW: 100,
    arcade.color.ORANGE: InvertGravityModifier(duration=5),
    arcade.color.WHITE: NoBounceModifier(duration=5),
}


class ModifierSystem:
    def __init__(self):
        self.pending_modifiers = []

    def trigger_bin_effect(self, ball, bin_sprite, effects=None, delayed=False):
        if effects is None:
            effects = DEFAULT_BIN_EFFECTS

        effect = effects.get(bin_sprite.color, lambda: None)
        if isinstance(effect, Modifier):
            if delayed:
                self.pending_modifiers.append(effect)
            else:
                self.apply_modifier(ball, effect)
        else:
            if isinstance(effect, int):
                self.add_score(effect)

    def apply_modifier(self, ball, modifier):
        modifier.apply(ball)
        ball.modifiers.append(modifier)
        arcade.schedule_once(
            lambda _: self.remove_modifier(ball, modifier), modifier.duration
        )

    def remove_modifier(self, ball, modifier):
        if modifier in ball.modifiers:
            modifier.remove(ball)
            ball.modifiers.remove(modifier)
