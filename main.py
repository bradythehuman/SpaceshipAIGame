import sys
import pygame

import game

game = game.Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            game.unit_selected_loop(event)

    game.update_path()
    game.render_frame()
