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
