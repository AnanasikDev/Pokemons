from Render import *
from Pokemons import *
from Trainer import *
from SmartTrainer import *


class Battle:
    def __init__(self, world, effects):
        self.running = False

        self.world = world
        self.effects = effects

        self.trainer1 = Trainer((50, 50), "Player")
        self.trainer2 = SmartTrainer((50, screenSize[1] - 450), "Enemy")

        self.trainers = [self.trainer1, self.trainer2]
        self.poke = 5

        self.idle_trainers_points = ((50, 50), (50, screenSize[1] - 450))
        self.battle_trainers_points = ((50, screenSize[1] // 2 - Trainer.size[1] // 2), (screenSize[0] - 50 - Trainer.size[0], screenSize[1] // 2 - Trainer.size[1] // 2))

        self.pokes_graphical = { "shift" : (200, Pokemon.size[0] + 150, 40), "step" : Pokemon.size[1] }

        self.selected_ally = None
        self.selected_enemy = None

    def lose(self):
        self.trainer2.wins += 1
        self.finish()
        self.world.generate_pokemons()
        self.effects.clear()

    def win(self):
        self.trainer1.wins += 1
        self.finish()
        self.world.generate_pokemons()
        self.effects.clear()

    def draw_attack(self, attacker, defencer, color, width = 5):
        pygame.draw.line(screen, color, attacker.center, defencer.center, width)

    def assault(self):
        if self.selected_ally is None or self.selected_enemy is None:
            return False

        self.selected_ally.attack(self.selected_enemy)
        self.effects.add(Effect(self.draw_attack, [self.selected_ally, self.selected_enemy, (20, 240, 35), 7]), 0.8)

        if self.selected_enemy.hp <= 0:
            self.trainer2.active_box.remove(self.selected_enemy)
            pokemons.remove(self.selected_enemy)

        if len(self.trainer2.active_box) == 0:
            self.win()

        return True

    def response(self):
        if len(self.trainer2.active_box) == 0:
            return

        enemy = self.trainer2.choose_attacker()
        ally = self.trainer2.choose_target(self.trainer1)

        enemy.attack(ally)
        self.effects.add(Effect(self.draw_attack, [ally, enemy, (200, 10, 10)]), 0.8)

        if ally.hp <= 0:
            self.trainer1.active_box.remove(ally)
            pokemons.remove(ally)

        if len(self.trainer1.active_box) == 0:
            self.lose()
            return

    def clear_selection(self):
        self.selected_ally = None
        self.selected_enemy = None

    def start(self):
        self.running = True

        i = randint(0, 1)
        assault = self.trainers[i]
        defence = self.trainers[1 - i]

        team_player = self.trainer1.best_team(self.poke)
        team_enemy = self.trainer2.best_team(self.poke)

        self.trainer1.set_position(self.battle_trainers_points[0])
        self.trainer2.set_position(self.battle_trainers_points[1])

        clear_pokemons()

        for i, p1 in enumerate(team_player):
            pokemons.append(p1)
            p1.set_position((self.pokes_graphical["shift"][0], self.pokes_graphical["shift"][2] + i * self.pokes_graphical["step"]))
            p1.scale_image(0.75)
            self.trainer1.add2active(p1)

        for i, p2 in enumerate(team_enemy):
            pokemons.append(p2)
            p2.set_position((screenSize[0] - self.pokes_graphical["shift"][1], self.pokes_graphical["shift"][2] + i * self.pokes_graphical["step"]))
            p2.scale_image(0.75)
            self.trainer2.add2active(p2)

    def finish(self):
        self.running = False

        self.trainer1.set_position(self.idle_trainers_points[0])
        self.trainer2.set_position(self.idle_trainers_points[1])

        clear_pokemons()
        self.trainer1.active_box.clear()
        self.trainer2.active_box.clear()
