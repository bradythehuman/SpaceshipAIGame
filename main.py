import sys
import pygame

import main_mod
import crew
import ship

# screen = main_mod.open_window()

cursor_pos = [20, 20]
my_ship = ship.Ship()
my_crew = [crew.Crew([26, 16])]
loop_type = 'main'
selected_crew = False

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
            elif event.key == pygame.K_RETURN and cursor_pos in [x.pos for x in my_crew] and not selected_crew:
                for x in my_crew:
                    if cursor_pos == x.pos:
                        selected_crew = x
            elif event.key == pygame.K_RETURN and cursor_pos in my_ship.floor and selected_crew:
                path = selected_crew.pathing(my_ship.floor, cursor_pos)
                if path:
                    print(path)
                    selected_crew.pos = list(cursor_pos)
                    selected_crew = False
                else:
                    print("pathing failed")

    main_mod.render_frame(cursor_pos, my_ship, my_crew)
