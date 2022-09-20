from Trainer import *
from Render import *


class SmartTrainer(Trainer):
    def __init__(self, pos, name):
        super().__init__(pos, name)

    def choose_attacker(self):
        values = []
        for p in self.active_box:
            values.append(p.value)
        attacker = self.active_box[values.index(max(values))]

        return attacker

    def choose_target(self, player):
        values = []
        for p in player.active_box:
            values.append(p.targety)
        print("VALUES ", values)
        defencer = player.active_box[values.index(max(values))]

        return defencer

    def pick_pokemon(self, poks, world):
        values = []
        for p in poks:
            values.append(p.value)

        world.pick_pokemon(poks[values.index(max(values))], self)
