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

resolution = [576, 672]  # (x, y)
scale = 12
fullscreen = False
pygame.init()
if fullscreen:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(resolution)

bar_gui = pygame.image.load("bitmaps/bar_gui.bmp")

myCrew = [crew.Crew([26, 16])]
myShip = ship.Ship()

cursor = pygame.image.load("bitmaps/cursor.bmp").convert()
cursor.set_colorkey(black)
cursor_pos = [0, 0]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
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

    screen.fill(black)
    screen.blit(bar_gui, (0, 0))
    screen.blit(myShip.background, (0, 8*scale))
    for crew_member in myCrew:
        pos = crew_member.pos
        pygame.draw.rect(screen, crew_color, (pos[0]*12 + 2, pos[1]*12 + 98, 8, 8))
    screen.blit(cursor, (cursor_pos[0]*12, cursor_pos[1]*12 + 96))

    pygame.display.flip()
