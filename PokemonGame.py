import pygame.draw

from Pokemons import *
from random import randint
from Render import *


class Trainer(pygame.sprite.Sprite):

    size = (150, 326)

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/trainer.png").convert_alpha()
        self.box = []
        self.wins = 0
        self.pos = pos
        self.scoreText = f"Trainer [{len(self.box)}]"
        self.text_local_pos = (0, -18)
        # objects.append(self)
        trainers.append(self)

    def add(self, pokemon):
        self.box.append(pokemon)

    def best_team(self, n):
        b = self.box[0:n]
        self.box = self.box[n:]
        return b

    def set_position(self, pos):
        self.pos = pos

    def render(self):
        self.scoreText = f"Trainer [{len(self.box)}]"
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
        if k == 0:
            return WaterPokemon("W", randint(5, 50), randint(5, 50), pos)
        if k == 1:
            return FirePokemon("F", randint(5, 50), randint(5, 50), pos)
        if k == 2:
            return GrassPokemon("G", randint(5, 50), randint(5, 50), pos)
        if k == 3:
            return ElectricPokemon("E", randint(5, 50), randint(5, 50), pos)

    def generate_pokemons(self):
        print("generate")
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

        print(pokemons)

    def catch_pokemon(self):
        return pokemons[randint(0, len(pokemons))]

    def add_pokemon(self):
        x, y = self._get_pos()
        self._generate_pokemon((x, y))


class Battle:
    def __init__(self):
        self.trainer1 = Trainer((50, 50))
        self.trainer2 = Trainer((50, screenSize[1] - 450))

        self.trainers = [self.trainer1, self.trainer2]
        self.poke = 5

        self.i_trainers_points = ((50, 50), (50, screenSize[1] - 450))
        self.b_trainers_points = ((50, screenSize[1] // 2 - Trainer.size[1] // 2), (screenSize[0] - 50 - Trainer.size[0], screenSize[1] // 2 - Trainer.size[1] // 2))

        self.pokes_graphical = { "shift" : (175, Pokemon.size[0] + 150, 0), "step" : Pokemon.size[1] }

    def start(self):
        global pokemons

        i = randint(0, 1)
        assault = self.trainers[i]
        defence = self.trainers[1 - i]

        a_team = assault.best_team(self.poke)
        d_team = defence.best_team(self.poke)

        assault.set_position(self.b_trainers_points[0])
        defence.set_position(self.b_trainers_points[1])

        print(len(pokemons), pokemons)
        clear_pokemons()

        for i, p1 in enumerate(a_team):
            pokemons.append(p1)
            p1.set_position((self.pokes_graphical["shift"][0], self.pokes_graphical["shift"][2] + i * self.pokes_graphical["step"]))
            p1.scale_image(0.75)

        for i, p2 in enumerate(d_team):
            pokemons.append(p2)
            p2.set_position((screenSize[0] - self.pokes_graphical["shift"][1], self.pokes_graphical["shift"][2] + i * self.pokes_graphical["step"]))
            p2.scale_image(0.75)

    def finish(self):
        global pokemons
        self.trainer1.set_position(self.i_trainers_points[0])
        self.trainer2.set_position(self.i_trainers_points[1])

        clear_pokemons()


world = World(4)
battle = Battle()


def dmg():
    for p in pokemons:
        p.hp -= 10


while True:
    for event in pygame.event.get():
        pre_update()

        for p in pokemons:
            mouse_presses = pygame.mouse.get_pressed()
            cursor = pygame.mouse.get_pos()
            if p.overlap(cursor[0], cursor[1]):
                if mouse_presses[0]:
                    # print("Left Mouse Key is being pressed [First trainer]")
                    battle.trainer1.add(p)
                    p.destroy()
                    world.add_pokemon()

                if mouse_presses[2]:
                    # print("Right Mouse Key is being pressed [Second trainer]")
                    battle.trainer2.add(p)
                    p.destroy()
                    world.add_pokemon()

            p.render()

        for t in trainers:
            t.render()

        update()

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

        # timer.tick(FPS)
