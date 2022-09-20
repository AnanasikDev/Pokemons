from Render import *
from pygame import sprite
from time import time


class Pokemon(sprite.Sprite):

    size = (pokesize, pokesize)
    id = 0

    def __init__(self, name, atk, df, pos):
        super().__init__()
        self.name = name
        self.hp = 100
        self.atk = atk
        self.df = df
        self.pos = pos
        self.text_local_pos = (0, -4)
        self.hp_local_pos = (0, -14)
        self.scoreText = f"atk: {self.atk} | def: {self.df}"
        self.id = Pokemon.id + 1
        Pokemon.id += 1
        # objects.append(self)
        pokemons.append(self)

        self.init_sprite()
        self.calculate_center()

        self.value = self.atk * self.df
        self.update_targety()

    def update_targety(self):
        self.targety = self.value / (self.hp + 0.1)

    def calculate_center(self):
        # self.center = self.image.get_rect().center
        width, height = self.image.get_rect().size
        self.center = (self.pos[0] + width // 2, self.pos[1] + height // 2)

    def init_sprite(self):
        self.image = self.image_origin
        self.rect = self.image.get_rect()

    def set_position(self, pos):
        self.pos = pos
        self.calculate_center()

    def import_image(self, path):
        self.image_origin = pygame.image.load(path).convert_alpha()

    def scale_image(self, scale):
        self.image = pygame.transform.scale(self.image_origin, (int(self.size[0] * scale), int(self.size[1] * scale)))

    def render(self):
        image_size = self.image.get_rect().size
        pygame.draw.rect(screen, backgroundColor, (self.pos[0], self.pos[1] + self.text_local_pos[1], 64, 32))

        # pygame.draw.rect(screen, (250, 40, 40), (self.pos[0], self.pos[1], image_size[0], image_size[1]))

        hp = (self.hp + 1) / 100
        bar_color = (250 - hp * 200, hp * 180, 15)

        pygame.draw.rect(screen, bar_color, (self.pos[0], self.pos[1] + self.hp_local_pos[1], image_size[0] * self.hp / 100, 12))

        screen.blit(self.image, self.pos)
        self.update_targety()
        drawText(screen, contentColor, self.scoreText, [self.pos[0] + self.text_local_pos[0], self.pos[1] + self.text_local_pos[1]], font_size=14)
        drawText(screen, contentColor, str(self.hp), [self.pos[0] + self.hp_local_pos[0], self.pos[1] + self.hp_local_pos[1]], font_size=14)

    def translate(self, deltax, deltay):
        self.pos = (self.pos[0] + deltax, self.pos[1] + deltay)

    def overlap(self, x, y):
        return self.pos[0] <= x <= self.pos[0] + self.size[0] and \
               self.pos[1] <= y <= self.pos[1] + self.size[1]

    def destroy(self):
        pokemons.remove(self)
        # objects.remove(self)

    def attack(self, enemy):
        if self.hp <= 0 or enemy.hp <= 0:
            return

        damage = self.atk - enemy.df
        if damage <= 0:
            damage = 1
        enemy.hp -= damage
        if enemy.hp < 0:
            enemy.hp = 0

        enemy.update_targety()

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.atk

    def get_def(self):
        return self.df

    def __str__(self):
        return f"Pokemon {self.id} with attack = {self.atk}; defence = {self.df}; hp = {self.hp}"


class WaterPokemon(Pokemon):
    def __init__(self, name, atk, df, pos):
        self.import_image("images/poke2.png")
        super().__init__(name, atk, df, pos)
        self.value = self.atk * self.df * 1.15

    def attack(self, enemy):
        if self.hp <= 0 or enemy.hp <= 0:
            return

        if type(enemy) == FirePokemon:
            damage = self.atk * 3 - enemy.df
        else:
            damage = self.atk - enemy.df

        if damage <= 0:
            damage = 1
        enemy.hp -= damage
        if enemy.hp < 0:
            enemy.hp = 0


class FirePokemon(Pokemon):
    def __init__(self, name, atk, df, pos):
        self.import_image("images/poke3.png")
        super().__init__(name, atk, df, pos)
        self.value = self.atk * self.df * 0.75


class GrassPokemon(Pokemon):
    def __init__(self, name, atk, df, pos):
        self.import_image("images/poke4.png")
        super().__init__(name, atk, df, pos)
        self.value = self.atk * self.df * 1.1

    def attack(self, enemy):
        if self.hp <= 0 or enemy.hp <= 0:
            return

        if type(enemy) == FirePokemon:
            damage = self.atk - enemy.df // 2
        else:
            damage = self.atk - enemy.df

        if damage <= 0:
            damage = 1
        enemy.hp -= damage
        if enemy.hp < 0:
            enemy.hp = 0


class ElectricPokemon(Pokemon):
    def __init__(self, name, atk, df, pos):
        self.import_image("images/poke1.png")
        super().__init__(name, atk, df, pos)

    def attack(self, enemy):
        if self.hp <= 0 or enemy.hp <= 0:
            return

        if type(enemy) == WaterPokemon:
            damage = self.atk
        else:
            damage = self.atk - enemy.df

        if damage <= 0:
            damage = 1
        enemy.hp -= damage
        if enemy.hp < 0:
            enemy.hp = 0
