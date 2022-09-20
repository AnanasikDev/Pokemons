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

    def choose_defencer(self, defencers):
        values = []
        for p in defencers:
            values.append(p.targety)
        defencer = self.active_box[values.index(max(values))]

        return defencer

    def pick_pokemon(self, poks):
        values = []
        for p in self.active_box:
            values.append(p.value)
        return self.active_box[values.index(max(values))]
