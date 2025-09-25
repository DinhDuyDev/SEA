import pygame
from game_setup import *
from Fighter import *



def main():

    clock = pygame.time.Clock()
    Game.running = True

    while Game.running:
        # for event in pg.event.get():
        #     if event.type == pygame.QUIT:
        #         Game.running = False
        #     elif event.type == pygame.KEYDOWN:
        #         get_keys(event)

            # elif event.type == pygame.VIDEORESIZE:
            #     Game.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         if not Game.giving_names:
            #             Game.giving_names = True
            #             TextBox.curr_name_string = ""
            #         else:
            #             running = False
            #     elif event.key == pygame.K_e:
            #         if len(Fighter.list_of_fighters) == 0 or len(Fighter.list_of_fighters) == 1:
            #             Fighter.list_of_fighters.clear()
            #             add_all_fighters_in_queue()
            #     elif event.key == pygame.K_p:
            #         if not Game.giving_names:
            #             Game.PAUSED = not Game.PAUSED
            #
            #     if Game.giving_names:
            #         get_name(event)

        ######### Drawing block #########
        Game.draw_dest.fill((0, 0, 0))

        Game.states[Game.curr_state]()

        #pygame.draw.rect(Game.draw_dest, (255, 0, 0), (100, 100, 25, 25))
        Game.screen.blit(pygame.transform.scale(Game.draw_dest, Game.screen.get_rect().size), (0, 0))

        ######## Pygame display update
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()