from Render import *


class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, atk, df, pos):
        super().__init__()
        self.name = name
        self.hp = 100
        self.atk = atk
        self.df = df
        self.pos = pos
        self.size = (pokesize, pokesize)
        print(f"Poke spawned on {self.pos}")
        self.text_local_pos = (0, -32)
        self.hp_local_pos = (0, -18)
        self.scoreText = f"{self.name} {self.atk} {self.df}"
        objects.append(self)
        pokemons.append(self)

    def import_image(self, path):
        self.image = pygame.image.load(path).convert_alpha()

    def render(self):
        screen.blit(self.image, self.pos)
        pygame.draw.rect(screen, backgroundColor, (self.pos[0], self.pos[1] + self.text_local_pos[1], 64, 32))
        drawText(screen, contentColor, self.scoreText, [self.pos[0] + self.text_local_pos[0], self.pos[1] + self.text_local_pos[1]])
        drawText(screen, contentColor, str(self.hp), [self.pos[0] + self.hp_local_pos[0], self.pos[1] + self.hp_local_pos[1]])

    def overlap(self, x, y):
        return self.pos[0] <= x <= self.pos[0] + self.size[0] and \
               self.pos[1] <= y <= self.pos[1] + self.size[1]

    def destroy(self):
        pokemons.remove(self)
        objects.remove(self)
        pygame.draw.rect(screen, backgroundColor, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

    def attack(self, enemy):
        if self.hp <= 0 or enemy.hp <= 0:
            return

        damage = self.atk - enemy.df
        if damage <= 0:
            damage = 1
        enemy.hp -= damage
        if enemy.hp < 0:
            enemy.hp = 0

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.atk

    def get_def(self):
        return self.df


class WaterPokemon(Pokemon):
    def __init__(self, name, atk, df, pos):
        self.import_image("images/poke2.png")
        super().__init__(name, atk, df, pos)

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


class GrassPokemon(Pokemon):
    def __init__(self, name, atk, df, pos):
        self.import_image("images/poke4.png")
        super().__init__(name, atk, df, pos)

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
