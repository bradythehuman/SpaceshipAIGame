import pygame


class Ship:
    def __init__(self):
        self.hull = 50
        self.shield = 3
        self.hull_dmg = 20
        self.shield_dmg = 2
        self.background = pygame.image.load("bitmaps/orange_ship.bmp")
        self.tiles = {"floor": img_to_pos("bitmaps/orangeShipFloor.bmp"),
                      # "cockpit": img_to_pos(),
                      # "turret": img_to_pos(),
                      # "bed": img_to_pos(),
                      # "engine": img_to_pos()
                      }

        self.crew = []

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
    print("floor: " + str(my_ship.floor))
