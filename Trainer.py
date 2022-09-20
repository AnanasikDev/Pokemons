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
        self.update_title()
        self.update_wins()
        self.title_local_pos = (0, -16)
        self.wins_local_pos = (0, -36)
        # objects.append(self)
        trainers.append(self)

    def update_title(self):
        self.title_text = f"{self.name} owns {len(self.box)} p"

    def update_wins(self):
        self.wins_text = f"Wins {self.wins}"

    def add(self, pokemon):
        self.box.append(pokemon)

    def add2active(self, pokemon):
        self.active_box.append(pokemon)

    def choose_attacker(self):
        return select_random(self.active_box)

    def choose_defencer(self, defencers):
        return select_random(defencers)

    def choose_target(self, enemy):
        return select_random(enemy.active_box)

    def pick_pokemon(self, poks, world):
        world.pick_pokemon(select_random(poks), self)

    def best_team(self, n):
        b = self.box[0:n]
        self.box = self.box[n:]
        return b

    def set_position(self, pos):
        self.pos = pos

    def render(self):
        self.update_title()
        self.update_wins()
        screen.blit(self.image, self.pos)
        drawText(screen, contentColor, self.title_text, [self.pos[0] + self.title_local_pos[0], self.pos[1] + self.title_local_pos[1]])
        drawText(screen, contentColor, self.wins_text, [self.pos[0] + self.wins_local_pos[0], self.pos[1] + self.wins_local_pos[1]], font_size=20)
