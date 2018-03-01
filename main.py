import sys
import pygame

import crew
import ship
import mood


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


DIRECTION_TO_PATH = {('left', 'right'): 0,
                     ('right', 'left'): 0,
                     ('up', 'down'): 1,
                     ('down', 'up'): 1,
                     ('down', 'right'): 2,
                     ('right', 'down'): 2,
                     ('right', 'up'): 3,
                     ('up', 'right'): 3,
                     ('up', 'left'): 4,
                     ('left', 'up'): 4,
                     ('left', 'down'): 5,
                     ('down', 'left'): 5,
                     }


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
    font_scale = 16
    font_color = (255, 255, 255)
    resolution = [1576, 672]  # Origionally [576, 672]
    fullscreen = False

    def __init__(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)
        pygame.font.init()
        # RUN LEVEL VARIABLES
        self.my_ship = ship.Ship()
        self.crew = [crew.Crew()]
        self.mood = mood.Mood()
        self.states = [SelectAction()]
        # LOAD GRAPHICS
        self.myfont = pygame.font.SysFont('Courier New', self.font_scale)
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
        for crew_member in self.crew:
            pos = crew_member.pos
            pygame.draw.rect(self.screen, self.crew_color, (pos[0] * 12 + 2, pos[1] * 12 + 98, 8, 8))
        self.screen.blit(self.cursor, (self.states[-1].cursor_pos[0] * 12, self.states[-1].cursor_pos[1] * 12 + 96))
        if self.states[-1].path:
            path = self.states[-1].path
            for i in range(1, len(path) - 1):
                previous_pos = path[i - 1]
                current_pos = path[i]
                next_pos = path[i + 1]
                previous_next_pos = (get_relative_direction(current_pos, previous_pos),
                                     get_relative_direction(current_pos, next_pos))
                self.screen.blit(self.pathsRed[DIRECTION_TO_PATH[previous_next_pos]], ship_to_screen_pos(current_pos))
        for i in range(len(self.states[-1].console)):
            self.screen.blit(self.myfont.render(self.states[-1].console[i], False, self.font_color),
                             (576, (i*self.font_scale)))
        pygame.display.flip()

    def update(self):
        for member in self.crew:
            member.update(self)

    def is_empty_floor(self, pos):
        if pos not in self.my_ship.map["floor"]:
            return False
        for member in self.crew:
            if tuple(member.pos) == pos:
                return False
        return True


class State:
    console = ["Warning. This is the default state.", "Warning. This is the default state."]

    def __init__(self):
        self.cursor_pos = [20, 20]
        self.path = []

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


class SelectAction(State):
    console = ["(M)ove unit.", "(S)pawn unit.", "(K)ill unit."]

    def check_event(self, event):
        self.try_quit(event)
        self.try_move_cursor(event)
        if event.key == pygame.K_m:
            game.states.append(SelectUnit(self.cursor_pos))
        elif event.key == pygame.K_s:
            pass
        elif event.key == pygame.K_k:
            pass


class SelectUnit(State):
    console = ["Select unit..."]

    def __init__(self, cursor_pos):
        self.cursor_pos = cursor_pos
        self.path = []

    def check_event(self, event):
        # Event Processing
        self.try_quit(event)
        self.try_move_cursor(event)
        if event.key == pygame.K_RETURN and self.cursor_pos in [x.pos for x in game.crew]:
            for x in game.crew:
                if self.cursor_pos == x.pos:
                    game.states.append(SelectSpace(x))


class SelectSpace(State):
    console = ["Select space..."]

    def __init__(self, selected_crew):
        self.cursor_pos = list(selected_crew.pos)
        self.selected_crew = selected_crew
        self.shortest_path_tree = selected_crew.pathing(game.my_ship.map["floor"])
        self.path = []

    def check_event(self, event):
        # Event Processing
        self.try_quit(event)
        self.try_move_cursor(event)
        if event.key == pygame.K_RETURN and self.path:
            self.selected_crew.pos = list(self.cursor_pos)
            game.states[-3].cursor_pos = list(self.cursor_pos)
            game.states = game.states[:-2]
        # Update
        if tuple(self.cursor_pos) in self.shortest_path_tree:
            self.path = self.shortest_path_tree[tuple(self.cursor_pos)]
        else:
            self.path = []


class Encounter:
    def __init__(self):
        pass


if __name__ == "__main__":
    # game is being used as a global variable because there is only ever one instance of Game() and it is constantly mutated
    game = Game()
    game.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event == pygame.K_m:
                    print("That's an m alright")
                game.states[-1].check_event(event)
        game.render_frame()
