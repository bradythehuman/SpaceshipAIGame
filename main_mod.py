import sys
import pygame

import crew
import ship

black = [0, 0, 0]
hull_bar_light = [232, 235, 147]
hull_bar_dark = [128, 133, 16]
shield_bar_light = [184, 240, 255]
shield_bar_dark = [17, 129, 126]
crew_color = [0, 46, 112]
invader_color = [148, 3, 3]
door_color = [197, 124, 34]

resolution = [576, 672]
fullscreen = False
pygame.init()
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(resolution)

bar_gui = pygame.image.load("bitmaps/bar_gui.bmp")
cursor = pygame.image.load("bitmaps/cursor.bmp").convert()
cursor.set_colorkey(black)

scale = 12


# def open_window(resolution=[576, 672], fullscreen=False):
#     pygame.init()
#     if fullscreen:
#         screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#     else:
#         screen = pygame.display.set_mode(resolution)
#     return screen


def render_frame(cursor_pos, my_ship, my_crew):
    screen.fill(black)
    screen.blit(bar_gui, (0, 0))
    screen.blit(my_ship.background, (0, 8 * scale))
    for crew_member in my_crew:
        pos = crew_member.pos
        pygame.draw.rect(screen, crew_color, (pos[0] * 12 + 2, pos[1] * 12 + 98, 8, 8))
    screen.blit(cursor, (cursor_pos[0] * 12, cursor_pos[1] * 12 + 96))

    pygame.display.flip()


def unit_selected_loop(cursor_pos, my_ship, my_crew):
    pass


def try_move_cursor():
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_UP and cursor_pos[1] > 0:
        cursor_pos[1] -= 1
    elif event.key == pygame.K_DOWN and cursor_pos[1] < 48:
        cursor_pos[1] += 1
    elif event.key == pygame.K_LEFT and cursor_pos[0] > 0:
        cursor_pos[0] -= 1
    elif event.key == pygame.K_RIGHT and cursor_pos[0] < 48:
        cursor_pos[0] += 1