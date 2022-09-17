import pygame


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

objects = []
pokemons = []
trainers = []

pygame.init()

cell_size = 200
upper_padding = 100

backgroundColor = (150, 150, 150)
contentColor = (5, 5, 5)
screenSize = (1200, cell_size * 5 + upper_padding)
contentBorder = ((100, 1100), (100, 700))

screen = pygame.display.set_mode(screenSize)
screen.fill(backgroundColor)
pygame.display.set_caption("Pokemons")
