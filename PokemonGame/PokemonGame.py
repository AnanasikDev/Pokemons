import pygame.draw

from Pokemons import *
from random import randint
from Render import *


class Trainer(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/trainer.png").convert_alpha()
        self.box = []
        self.wins = 0
        self.pos = pos
        self.scoreText = f"Trainer [{len(self.box)}]"
        self.text_local_pos = (0, -18)
        objects.append(self)
        trainers.append(self)

    def add(self, pokemon):
        self.box.append(pokemon)

    def best_team(self, n):
        b = self.box[0:n]
        self.box = self.box[n:]
        return b

    def render(self):
        self.scoreText = f"Trainer [{len(self.box)}]"
        screen.blit(self.image, self.pos)
        drawText(screen, contentColor, self.scoreText, [self.pos[0] + self.text_local_pos[0], self.pos[1] + self.text_local_pos[1]])


class World:
    def __init__(self, amount):
        self.amount = amount
        self.generate_pokemons()

    def _get_pos(self):
        l = 25
        w = 5
        i = randint(0, l)
        x, y = (i % w * cell_size + cell_size, i // w * cell_size + upper_padding)

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
        l = 25
        w = 5
        _poss = [i for i in range(l)]
        iposs = []

        for i in range(self.amount):
            k = l - i - 1
            j = randint(0, k)
            iposs.append(_poss[j])
            _poss.pop(j)

        poss = []
        for i in iposs:
            poss.append((i % w * cell_size + cell_size, i // w * cell_size + upper_padding))

        for i in range(self.amount):
            self._generate_pokemon(poss[i])

    def catch_pokemon(self):
        return pokemons[randint(0, len(pokemons))]

    def add_pokemon(self):
        x, y = self._get_pos()
        self._generate_pokemon((x, y))


a = Trainer((50, 50))
b = Trainer((50, screenSize[1] - 450))

w = World(4)


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
                    print("Left Mouse Key is being pressed [First trainer]")
                    a.add(p)
                    p.destroy()
                    w.add_pokemon()

                if mouse_presses[2]:
                    print("Right Mouse Key is being pressed [Second trainer]")
                    b.add(p)
                    p.destroy()
                    w.add_pokemon()

            p.render()

        for t in trainers:
            t.render()

        update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                dmg()

        if event.type == pygame.QUIT:
            pygame.quit()
            break
