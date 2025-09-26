import pygame
from game_setup import *
from Fighter import *



def main():

    clock = pygame.time.Clock()
    Game.running = True

    Button(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+32, 128, 32, "START GAME", "MENU")
    Button(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+64, 128, 32, "EXIT GAME", "MENU")
    Button(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+90, 128, 32, "Add Name", "ADDING_NAMES")
    Button(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+122, 128, 32, "Delete Name", "ADDING_NAMES")
    Button(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+154, 128, 32, "Proceed to fight!", "ADDING_NAMES")

    Text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 128, "AI SUPER SHOWDOWN", "MENU")
    Text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 128, "ENTER THE NAMES", "ADDING_NAMES")

    while Game.running:
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