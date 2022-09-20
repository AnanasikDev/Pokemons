from Pokemons import *
from Render import *


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

    def add_pokemon(self):
        x, y = self._get_pos()
        self._generate_pokemon((x, y))

    def pick_pokemon(self, pokemon, trainer):
        trainer.add(pokemon)
        pokemon.destroy()
