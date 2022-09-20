from Pokemons import *
from random import randint
from Render import *

from World import *
from Battle import *
from Trainer import *

world = World(4)
effects = Effects()
battle = Battle(world, effects)


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
