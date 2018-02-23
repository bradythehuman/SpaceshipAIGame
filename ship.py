import os

import pygame


class Ship:
    def __init__(self):
        self.hull = 50
        self.shield = 3
        self.hull_dmg = 20
        self.shield_dmg = 2
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


if __name__ == "__main__":
    my_ship = Ship()
    for i in my_ship.map:
        print(i + ": " + str(len(my_ship.map[i])))
