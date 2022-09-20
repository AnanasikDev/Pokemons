import pygame
from random import randint
import threading
from time import sleep

def pre_update():
    screen.fill(backgroundColor)


def update():
    pygame.display.flip()


def drawText(surface, color, text, where, font_name="Arial", font_size=16):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if type(where) is pygame.Rect:
        text_rect.center = where.center
    else:
        text_rect.topleft = where
    surface.blit(text_surface, text_rect)


def clear_pokemons():
    global pokemons
    pokemons.clear()


pokemons = []
objects = []
trainers = []

pygame.init()

FPS = 60

cell_size = 200
upper_padding = 80

pokesize = 175
gridsize = 4

backgroundColor = (150, 151, 155)
contentColor = (5, 5, 5)
screenSize = (1000, cell_size * gridsize + upper_padding)

margin = 0.8
contentBorder = (screenSize[0] * (1 - margin), screenSize[0] * margin, screenSize[1] * (1 - margin), screenSize[1] * margin)

screen = pygame.display.set_mode(screenSize)
screen.fill(backgroundColor)
pygame.display.set_caption("Pokemons")

timer = pygame.time.Clock()


def select_random(collection):
    return collection[randint(0, len(collection) - 1)]


class Effects:
    def __init__(self):
        self.effects = []

    def clear(self):
        self.effects.clear()

    def render_all(self):
        for effect in self.effects:
            effect.render()

    def add(self, effect, seconds = 0):
        self.effects.append(effect)
        if seconds > 0:
            t = threading.Thread(target=self.shoot, args=(effect, seconds))
            t.start()

    def shoot(self, effect, time):
        sleep(time)
        if effect in self.effects:
            self.remove(effect)

    def remove(self, effect):
        self.effects.remove(effect)


class Effect:
    def __init__(self, function, args):
        self.function = function
        self.args = args

    def render(self):
        self.function(*self.args)
