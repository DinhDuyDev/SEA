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
    Text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 144, "ENTER THE NAMES", "ADDING_NAMES")

    while Game.running:
        ######### Drawing block #########
        Game.draw_dest.fill((0, 0, 0))

        for button in Button.list_of_buttons:
            if button.scene == Game.curr_state:
                button.action()
                pygame.draw.rect(Game.draw_dest, button.color, button.button_rect, 1)
                Game.draw_dest.blit(button.text_surf, button.text_surf.get_rect(center=(button.x, button.y)))

        for text in Text.list_of_text:
            if text.scene == Game.curr_state:
                #text.action()
                Game.draw_dest.blit(text.text_surf, text.text_rect)

        for ondemand in OnDemandText.list_of_text:
            ondemand.action()
            Game.draw_dest.blit(ondemand.text_surf, ondemand.text_rect)

        Game.states[Game.curr_state]()

        #pygame.draw.rect(Game.draw_dest, (255, 0, 0), (100, 100, 25, 25))
        Game.screen.blit(pygame.transform.scale(Game.draw_dest, Game.screen.get_rect().size), (0, 0))

        ######## Pygame display update
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()