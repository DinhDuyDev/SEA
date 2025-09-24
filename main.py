import pygame
from game_setup import *
from Fighter import *
from Smoke_And_Explosions import *
from Camera import *
def main():
    def mouse_coords():
        x = pygame.mouse.get_pos()[0] / (Game.screen.get_rect().width / Game.draw_dest.get_width())
        y = pygame.mouse.get_pos()[1] / (Game.screen.get_rect().height / Game.draw_dest.get_height())
        return x, y

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pg.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                Game.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    Game.level_editor = not Game.level_editor
                elif event.key == pygame.K_F4:
                    Game.FULLSCREEN = not Game.FULLSCREEN
                    if Game.FULLSCREEN:
                        set_full_screen()
                    else:
                        set_not_full_screen()
                elif event.key == pygame.K_e:
                    if len(Fighter.list_of_fighters) == 0 or len(Fighter.list_of_fighters) == 1:
                        Fighter.list_of_fighters.clear()
                        add_all_fighters_in_queue()
                elif event.key == pygame.K_p:
                   Game.PAUSED = not Game.PAUSED

        ######### Drawing block #########
        Game.draw_dest.fill((0, 0, 0))

        ######### Logic block #########
        c = cxy()
        if not Game.PAUSED:
            Camera.update(None)
        ######### Moving fighters

        for f in Fighter.list_of_fighters:
            if not Game.PAUSED:
                f.action()
        for b in Bullet.list_of_bullets:
            if not Game.PAUSED:
                b.action()
                for f in Fighter.list_of_fighters:
                    if point_distance(b.x, b.y, f.x, f.y) < b.hit_radius and b.spawner is not f:
                        f.take_damage(b.get_damage())

        print(len(Bullet.list_of_bullets))

        for b in Bullet.list_of_bullets:
            b_spr = pygame.transform.rotate(BULLET_SPRITES[b.get_type()], b.dir)
            Game.draw_dest.blit(b_spr, b_spr.get_rect(center=(b.x-c[0], b.y-c[1])))
            #pygame.draw.rect(Game.draw_dest, (255, 255, 255), (b.x - 2, b.y - 2, 2, 2))

        ######## Drawing block (cont) ########
        for f in Fighter.list_of_fighters:
            if f.hp > 0:
                col = f.color
                unique_tint = pygame.Surface((13, 13))
                unique_tint.fill(col)
                unique_tint.set_alpha(128)
                Game.draw_dest.blit(FIGHTER_SPRITE, FIGHTER_SPRITE.get_rect(center=(f.x-c[0], f.y-c[1])))
                Game.draw_dest.blit(unique_tint, unique_tint.get_rect(center=(f.x-c[0], f.y-c[1])))

                w = pygame.transform.rotate(WEAPONS[f.get_weapon_sprite()], f.get_weapon_direction())
                Game.draw_dest.blit(w, w.get_rect(center=(f.x-c[0], f.y+5-c[1])))

                text_surf = my_font.render(f.get_name(), False, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(f.x, f.y-16))
                Game.draw_dest.blit(text_surf, text_rect)

                pygame.draw.rect(Game.draw_dest, (255, 0, 0), (f.x-16-c[0], f.y+8-c[1], 32, 6))
                pygame.draw.rect(Game.draw_dest, (82, 14, 125), (f.x-16-c[0], f.y+8-c[1], (f.get_recovery_health()/Fighter.full_health) * 32, 6))
                pygame.draw.rect(Game.draw_dest, (0, 255, 0), (f.x-16-c[0], f.y+8-c[1], (f.get_health()/Fighter.full_health) * 32, 6))

        for s in Smoke.list_of_smoke:
            if not Game.PAUSED:
                s.action()
            pygame.draw.circle(Game.draw_dest, s.get_color(), (s.x-c[0], s.y-c[1]), s.radius)

        for st in SmokeTrail.list_of_smoke_trails:
            if not Game.PAUSED:
                st.action()

        for e in Explosion.list_of_explosion:
            if not Game.PAUSED:
                for fi in Fighter.list_of_fighters:
                    dist = point_distance(fi.x, fi.y, e.x, e.y)
                    if dist < e.radius:
                        fi.take_damage(e.radius - dist)
                        dir_to_player = point_direction(e.x, e.y, fi.x, fi.y)
                        fi.take_knockback(random.randrange(3, 6), dir_to_player)
                e.explode()

        #pygame.draw.rect(Game.draw_dest, (255, 0, 0), (100, 100, 25, 25))
        Game.screen.blit(pygame.transform.scale(Game.draw_dest, Game.screen.get_rect().size), (0, 0))

        ######## Pygame display update
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()