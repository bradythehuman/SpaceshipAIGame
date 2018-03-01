import os
import pygame

import positional


class Ship:
    base_hull = 50
    base_shield = 3

    def __init__(self):
        self.hull = self.base_hull
        self.shield = self.base_shield
        self.hull_dmg = 0
        self.shield_dmg = 0
        self.background = pygame.image.load("bitmaps/orange_ship.bmp")
        self.map = {}
        map_folder = "bitmaps\orange ship"
        for file in os.listdir(map_folder):
            self.map[file[4:len(file) - 4]] = positional.img_to_pos(map_folder + "\\" + file)
        # self.doors = [Door((list(x)[0], list(x)[1]-1), self.map["floor"], self.map["hull"]) for x in self.map["doors"]]
        self.doors = [Door(x, self.map["floor"], self.map["hull"]) for x in self.map["doors"]]
        door_bmps = pygame.image.load("bitmaps/doors.bmp").convert()
        door_tile_count = 8
        self.door_bmps = [''] * door_tile_count
        for i in range(door_tile_count):
            rect = pygame.Rect((12 * i, 0, 12, 12))
            self.door_bmps[i] = pygame.Surface(rect.size).convert()
            self.door_bmps[i].blit(door_bmps, (0, 0), rect)
            self.door_bmps[i].set_colorkey((0, 0, 0))

    def change_door_state(self, pos):
        for door in self.doors:
            if door.pos == pos:
                door.open_close()

    def get_available_roles(self):
        pass

    def query_map(self, pos, map_key):
        if pos in self.map[map_key]:
            return True
        else:
            return False


class Door:
    def __init__(self, pos, floor, hull):
        self.pos = pos
        if self.pos in floor:
            self.is_exterior = False
        else:
            self.is_exterior = True
        if self.is_exterior:
            self.is_closed = True
        else:
            self.is_closed = False
        if positional.transform_up(list(self.pos)) in hull:
            self.is_vertical = True
        else:
            self.is_vertical = False
        self.is_broken = False

    def open_close(self):
        if self.is_closed:
            self.is_closed = False
        else:
            self.is_closed = True
