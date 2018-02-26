import os

import pygame


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
            self.map[file[4:len(file) - 4]] = img_to_pos(map_folder + "\\" + file)

    def get_available_roles(self):
        pass


def img_to_pos(path):
    img = pygame.image.load(path)
    result = []
    for i in range(48):
        for j in range(48):
            if img.get_at((i, j)) != (0, 0, 0, 255):
                result.append([i, j])
    return result
