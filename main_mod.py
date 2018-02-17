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

scale = 12
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
pathsRedImg = pygame.image.load("bitmaps/pathsRed.bmp").convert()
pathsRed = ['']*6
for i in range(6):
    rect = pygame.Rect((12*i, 0, 12, 12))
    pathsRed[i] = pygame.Surface(rect.size).convert()
    pathsRed[i].blit(pathsRedImg, (0, 0), rect)
    pathsRed[i].set_colorkey((0, 0, 0))


def render_frame(cursor_pos, my_ship, my_crew, path):
    screen.fill(black)
    screen.blit(bar_gui, (0, 0))
    screen.blit(my_ship.background, (0, 8 * scale))
    for crew_member in my_crew:
        pos = crew_member.pos
        pygame.draw.rect(screen, crew_color, (pos[0] * 12 + 2, pos[1] * 12 + 98, 8, 8))
    screen.blit(cursor, (cursor_pos[0] * 12, cursor_pos[1] * 12 + 96))

    if path:
        for i in range(1, len(path) - 1):
            previous_pos = path[i - 1]
            current_pos = path[i]
            next_pos = path[i + 1]
            previous_next_pos = [get_relative_direction(current_pos, previous_pos),
                                 get_relative_direction(current_pos, next_pos)]
            print(previous_next_pos)
            if 'left' in previous_next_pos and 'right' in previous_next_pos:
                screen.blit(pathsRed[0], ship_to_screen_pos(current_pos))
            elif 'up' in previous_next_pos and 'down' in previous_next_pos:
                screen.blit(pathsRed[1], ship_to_screen_pos(current_pos))
            elif 'down' in previous_next_pos and 'right' in previous_next_pos:
                screen.blit(pathsRed[2], ship_to_screen_pos(current_pos))
            elif 'right' in previous_next_pos and 'up' in previous_next_pos:
                screen.blit(pathsRed[3], ship_to_screen_pos(current_pos))
            elif 'up' in previous_next_pos and 'left' in previous_next_pos:
                screen.blit(pathsRed[4], ship_to_screen_pos(current_pos))
            elif 'left' in previous_next_pos and 'down' in previous_next_pos:
                screen.blit(pathsRed[5], ship_to_screen_pos(current_pos))

    pygame.display.flip()


def get_relative_direction(start, end):
    if start[0] == end[0]:
        if start[1] > end[1]:
            return 'up'
        else:
            return 'down'
    elif start[0] > end[0]:
        return 'left'
    else:
        return 'right'


def ship_to_screen_pos(pos):
    return (pos[0]*12, pos[1]*12 + 96)

# def unit_selected_loop(cursor_pos, my_ship, my_crew):
#     pass
#
#
# def try_move_cursor():
#     if event.key == pygame.K_ESCAPE:
#         sys.exit()
#     elif event.key == pygame.K_UP and cursor_pos[1] > 0:
#         cursor_pos[1] -= 1
#     elif event.key == pygame.K_DOWN and cursor_pos[1] < 48:
#         cursor_pos[1] += 1
#     elif event.key == pygame.K_LEFT and cursor_pos[0] > 0:
#         cursor_pos[0] -= 1
#     elif event.key == pygame.K_RIGHT and cursor_pos[0] < 48:
#         cursor_pos[0] += 1

if __name__ == "__main__":
    path = [(25, 17), (25, 16), (25, 15), (25, 14), (26, 14), (27, 14), (28, 14), (28, 13), (28, 12), (28, 11),
            (27, 11), (26, 11), (26, 10), (25, 10), (24, 10), (23, 10)]
    for i in range(1, len(path)-1):
        previous_pos = path[i-1]
        current_pos = path[i]
        next_pos = path[i+1]
        previous_next_pos = [get_relative_direction(current_pos, previous_pos),
                             get_relative_direction(current_pos, next_pos)]
        print(previous_next_pos)
