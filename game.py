import sys
import pygame

import crew
import ship


class Game:
    # Color constants
    black = [0, 0, 0]
    hull_bar_light = [232, 235, 147]
    hull_bar_dark = [128, 133, 16]
    shield_bar_light = [184, 240, 255]
    shield_bar_dark = [17, 129, 126]
    crew_color = [0, 46, 112]
    invader_color = [148, 3, 3]
    door_color = [197, 124, 34]

    # Display settings
    scale = 12
    resolution = [576, 672]
    fullscreen = False

    def __init__(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

        # Run level variables
        self.cursor_pos = [20, 20]
        self.my_ship = ship.Ship()
        self.loop_type = 'main'
        self.selected_crew = False
        self.shortest_path_tree = {}
        self.path = []

        self.bar_gui = pygame.image.load("bitmaps/bar_gui.bmp")
        self.cursor = pygame.image.load("bitmaps/cursor.bmp").convert()
        self.cursor.set_colorkey(self.black)
        paths_red_img = pygame.image.load("bitmaps/pathsRed.bmp").convert()
        self.pathsRed = [''] * 6
        for i in range(6):
            rect = pygame.Rect((12 * i, 0, 12, 12))
            self.pathsRed[i] = pygame.Surface(rect.size).convert()
            self.pathsRed[i].blit(paths_red_img, (0, 0), rect)
            self.pathsRed[i].set_colorkey((0, 0, 0))

    def render_frame(self):
        self.screen.fill(self.black)
        self.screen.blit(self.bar_gui, (0, 0))
        self.screen.blit(self.my_ship.background, (0, 8 * self.scale))
        for crew_member in self.my_ship.crew:
            pos = crew_member.pos
            pygame.draw.rect(self.screen, self.crew_color, (pos[0] * 12 + 2, pos[1] * 12 + 98, 8, 8))
        self.screen.blit(self.cursor, (self.cursor_pos[0] * 12, self.cursor_pos[1] * 12 + 96))

        if self.path:
            for i in range(1, len(self.path) - 1):
                previous_pos = self.path[i - 1]
                current_pos = self.path[i]
                next_pos = self.path[i + 1]
                previous_next_pos = [get_relative_direction(current_pos, previous_pos),
                                     get_relative_direction(current_pos, next_pos)]
                print(previous_next_pos)
                if 'left' in previous_next_pos and 'right' in previous_next_pos:
                    self.screen.blit(self.pathsRed[0], ship_to_screen_pos(current_pos))
                elif 'up' in previous_next_pos and 'down' in previous_next_pos:
                    self.screen.blit(self.pathsRed[1], ship_to_screen_pos(current_pos))
                elif 'down' in previous_next_pos and 'right' in previous_next_pos:
                    self.screen.blit(self.pathsRed[2], ship_to_screen_pos(current_pos))
                elif 'right' in previous_next_pos and 'up' in previous_next_pos:
                    self.screen.blit(self.pathsRed[3], ship_to_screen_pos(current_pos))
                elif 'up' in previous_next_pos and 'left' in previous_next_pos:
                    self.screen.blit(self.pathsRed[4], ship_to_screen_pos(current_pos))
                elif 'left' in previous_next_pos and 'down' in previous_next_pos:
                    self.screen.blit(self.pathsRed[5], ship_to_screen_pos(current_pos))

        pygame.display.flip()

    def unit_selected_loop(self, event):
        self.try_quit(event)
        self.try_move_cursor(event)
        self.try_select_crew(event)

    def try_quit(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def try_move_cursor(self, event):
        if event.key == pygame.K_UP and self.cursor_pos[1] > 0:
            self.cursor_pos[1] -= 1
        elif event.key == pygame.K_DOWN and self.cursor_pos[1] < 48:
            self.cursor_pos[1] += 1
        elif event.key == pygame.K_LEFT and self.cursor_pos[0] > 0:
            self.cursor_pos[0] -= 1
        elif event.key == pygame.K_RIGHT and self.cursor_pos[0] < 48:
            self.cursor_pos[0] += 1

    def try_select_crew(self, event):
        if event.key == pygame.K_RETURN and self.cursor_pos in [x.pos for x in self.my_ship.crew] and not self.selected_crew:
            for x in self.my_ship.crew:
                if self.cursor_pos == x.pos:
                    selected_crew = x
                    self.shortest_path_tree = selected_crew.pathing(self.my_ship.tiles["floor"])
        elif event.key == pygame.K_RETURN and self.selected_crew:

            if self.path:
                print(self.path)
                self.selected_crew.pos = list(self.cursor_pos)
                self.selected_crew = False
                self.shortest_path_tree = {}
            else:
                print("pathing failed")

    def update_path(self):
        if tuple(self.cursor_pos) in self.shortest_path_tree:
            self.path = self.shortest_path_tree[tuple(self.cursor_pos)]
        else:
            self.path = []


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
    return pos[0] * 12, pos[1] * 12 + 96
