import pygame.draw

from Pokemons import *
from random import randint
from Render import *


class Trainer(pygame.sprite.Sprite):

    size = (150, 326)

    def __init__(self, pos, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/trainer.png").convert_alpha()

        self.box = []
        self.active_box = []

        self.wins = 0
        self.pos = pos
        self.name = name
        self.scoreText = f"Trainer {self.name} [{len(self.box)}]"
        self.text_local_pos = (0, -18)
        # objects.append(self)
        trainers.append(self)

    def add(self, pokemon):
        self.box.append(pokemon)

    def add2active(self, pokemon):
        self.active_box.append(pokemon)

    def best_team(self, n):
        b = self.box[0:n]
        self.box = self.box[n:]
        return b

    def set_position(self, pos):
        self.pos = pos

    def render(self):
        self.scoreText = f"Trainer {self.name} [{len(self.box)}]"
        screen.blit(self.image, self.pos)
        drawText(screen, contentColor, self.scoreText, [self.pos[0] + self.text_local_pos[0], self.pos[1] + self.text_local_pos[1]])


class World:
    def __init__(self, amount):
        self.amount = amount
        self.generate_pokemons()

    def _get_pos(self):
        i = randint(0, gridsize * gridsize - 1)
        x, y = (i % gridsize * cell_size + cell_size, i // gridsize * cell_size + upper_padding)

        for p in pokemons:
            if p.pos == (x, y):
                return self._get_pos()

        return x, y

    def _generate_pokemon(self, pos):
        k = randint(0, 3)

        def_min = 5
        def_max = 15

        atk_min = 5
        atk_max = 60

        if k == 0:
            return WaterPokemon("W", randint(atk_min, atk_max), randint(def_min, def_max), pos)
        if k == 1:
            return FirePokemon("F", randint(atk_min, atk_max), randint(def_min, def_max), pos)
        if k == 2:
            return GrassPokemon("G", randint(atk_min, atk_max), randint(def_min, def_max), pos)
        if k == 3:
            return ElectricPokemon("E", randint(atk_min, atk_max), randint(def_min, def_max), pos)

    def generate_pokemons(self):
        _poss = [i for i in range(gridsize * gridsize - 1)]
        iposs = []

        for i in range(self.amount):
            k = gridsize * gridsize - i - 1 - 1
            j = randint(0, k)
            iposs.append(_poss[j])
            _poss.pop(j)

        poss = []
        for i in iposs:
            poss.append((i % gridsize * cell_size + cell_size, i // gridsize * cell_size + upper_padding))

        for i in range(self.amount):
            self._generate_pokemon(poss[i])

    def catch_pokemon(self):
        return pokemons[randint(0, len(pokemons))]

    def add_pokemon(self):
        x, y = self._get_pos()
        self._generate_pokemon((x, y))


class Battle:
    def __init__(self):
        self.running = False

        self.trainer1 = Trainer((50, 50), "Player")
        self.trainer2 = Trainer((50, screenSize[1] - 450), "Enemy")

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
        world.generate_pokemons()

    def win(self):
        self.trainer1.wins += 1
        self.finish()
        world.generate_pokemons()

    def draw_attack(self, attacker, defencer, color, width = 5):
        pygame.draw.line(screen, color, attacker.center, defencer.center, width)

    def assault(self):
        if self.selected_ally is None or self.selected_enemy is None:
            return False

        self.selected_ally.attack(self.selected_enemy)
        effects.add(Effect(self.draw_attack, [self.selected_ally, self.selected_enemy, (20, 240, 35), 7]), 1)

        if self.selected_enemy.hp <= 0:
            self.trainer2.active_box.remove(self.selected_enemy)
            pokemons.remove(self.selected_enemy)

        if len(self.trainer2.active_box) == 0:
            self.win()

        return True

    def response(self):
        if len(self.trainer2.active_box) == 0:
            return

        enemy = select_random(self.trainer2.active_box)
        ally = select_random(self.trainer1.active_box)

        enemy.attack(ally)
        effects.add(Effect(self.draw_attack, [ally, enemy, (200, 10, 10)]), 1)

        if self.selected_ally.hp <= 0:
            self.trainer1.active_box.remove(self.selected_ally)
            pokemons.remove(self.selected_ally)

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


world = World(4)
battle = Battle()


effects = Effects()

def dmg():
    for p in pokemons:
        p.hp -= 10


while True:
    for event in pygame.event.get():
        pre_update()

        for p in pokemons:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                cursor = pygame.mouse.get_pos()
                if p.overlap(cursor[0], cursor[1]):
                    if battle.running:
                        if mouse_presses[1]:
                            battle.clear_selection()

                        elif mouse_presses[0]:
                            print("A", p.id)
                            if p in battle.trainer1.active_box:
                                battle.selected_ally = p
                            elif p in battle.trainer2.active_box:
                                battle.selected_enemy = p
                                print("enemy selected", battle.selected_enemy)

                            if battle.selected_ally is not None and battle.selected_enemy is not None:
                                print("selection was: ", battle.selected_ally, battle.selected_enemy)
                                battle.assault()
                                battle.response()
                                battle.clear_selection()
                            print("selection: ", battle.selected_ally, battle.selected_enemy)

                    else:  # pokemons picking mode
                        if mouse_presses[0]:
                            print("Left Mouse Key is being pressed [First trainer]")
                            battle.trainer1.add(p)
                            p.destroy()
                            world.add_pokemon()

                        if mouse_presses[2]:
                            print("Right Mouse Key is being pressed [Second trainer]")
                            battle.trainer2.add(p)
                            p.destroy()
                            world.add_pokemon()

            p.render()

        for t in trainers:
            t.render()

        effects.render_all()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                dmg()
            if event.key == pygame.K_s:
                battle.start()
            if event.key == pygame.K_f:
                battle.finish()
                world.generate_pokemons()
            if event.key == pygame.K_r:
                clear_pokemons()
                world.generate_pokemons()

        if event.type == pygame.QUIT:
            pygame.quit()
            break

    update()
