import sys
import pygame

import game

my_game = game.Game()
my_game.update()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            my_game.unit_selected_loop(event)

    my_game.update_path()
    my_game.render_frame()
