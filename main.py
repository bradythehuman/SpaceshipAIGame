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
        # INITIALIZE
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)
        pygame.font.init()
        # RUN LEVEL VARIABLES
        self.my_ship = ship.Ship()
        self.crew = [crew.Crew()]
        self.mood = mood.Mood()
        self.states = [Encounter()]
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
        # UPDATE
        self.update()

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
        for door in self.my_ship.doors:
            if door.is_closed:
                if door.is_vertical:
                    self.screen.blit(self.my_ship.door_bmps[4], (door.pos[0] * 12, door.pos[1] * 12 + 96))
                else:
                    self.screen.blit(self.my_ship.door_bmps[0], (door.pos[0] * 12, door.pos[1] * 12 + 96))
            else:
                if door.is_vertical:
                    self.screen.blit(self.my_ship.door_bmps[5], (door.pos[0] * 12, (door.pos[1]-1) * 12 + 96))
                    self.screen.blit(self.my_ship.door_bmps[6], (door.pos[0] * 12, door.pos[1] * 12 + 96))
                    self.screen.blit(self.my_ship.door_bmps[7], (door.pos[0] * 12, (door.pos[1]+1) * 12 + 96))
                else:
                    self.screen.blit(self.my_ship.door_bmps[1], ((door.pos[0]-1) * 12, door.pos[1] * 12 + 96))
                    self.screen.blit(self.my_ship.door_bmps[2], (door.pos[0] * 12, door.pos[1] * 12 + 96))
                    self.screen.blit(self.my_ship.door_bmps[3], ((door.pos[0]+1) * 12, door.pos[1] * 12 + 96))
        pygame.display.flip()

    def initialize_round(self):
        for member in self.crew:
            member.initialize_round(self)

    def update(self):
        for member in self.crew:
            member.update(self)

    def get_empty_floor(self):
        floor = []
        for tile in self.my_ship.map["floor"]:
            if tile not in [member.pos for member in self.crew]:
                floor.append(tile)
        return floor

    def push_states(self, state):
        self.states.append(state)

    def pop_states(self, n):
        if n == 1:
            return self.states.pop()
        else:
            return [self.states.pop(-1) for i in range(n)]

    def get_state(self):
        return self.states[-1]


class State:
    console = ["Warning. This is the default state.", "Warning. This is the default state."]

    def __init__(self, cursor_pos=(20, 20)):
        self.cursor_pos = list(cursor_pos)
        self.path = []

    def process_event(self, event, game):
        self.try_quit(event)
        self.try_move_cursor(event)
        self.update()

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

    def update(self):
        pass


class Encounter(State):
    console = ["(M)ove unit.", "(O)pen or close doors.", "(R)equest action", ""]

    def process_event(self, event, game):
        if event.key == pygame.K_m:
            game.push_states(SelectUnit(self.cursor_pos))
        elif event.key == pygame.K_o:
            game.push_states(ChangeDoors(self.cursor_pos))
        super().process_event(event, game)


class SelectUnit(State):
    console = ["Select unit..."]

    def process_event(self, event, game):
        if event.key == pygame.K_RETURN and self.cursor_pos in [x.pos for x in game.crew]:
            for x in game.crew:
                if self.cursor_pos == x.pos:
                    game.push_states(SelectSpace(x))
        super().process_event(event, game)


class SelectSpace(State):
    console = ["Select space..."]

    def __init__(self, selected_crew):
        super().__init__(tuple(selected_crew.pos))
        self.selected_crew = selected_crew

    def process_event(self, event, game):

        if event.key == pygame.K_RETURN and self.path:
            self.selected_crew.move_unit(self.cursor_pos, game)
            game.states[-3].cursor_pos = list(self.cursor_pos)
            game.pop_states(2)
        super().process_event(event, game)

    def update(self):
        self.path = self.selected_crew.get_path(self.cursor_pos)


class ChangeDoors(State):
    console = ["Select a door to open/close it.", "Press 'O' to stop changing door states"]

    def process_event(self, event, game):
        if event.key == pygame.K_RETURN:
            if game.my_ship.query_map(self.cursor_pos, "doors"):
                game.my_ship.change_door_state(self.cursor_pos, game)
        if event.key == pygame.K_o:
            game.states[-2].cursor_pos = list(self.cursor_pos)
            game.pop_states(1)
        super().process_event(event, game)


if __name__ == "__main__":
    # game is being used as a global variable because there is only ever one instance of Game() and it is
    # constantly mutated
    game = Game()
    game.initialize_round()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game.get_state().process_event(event, game)
        game.render_frame()
