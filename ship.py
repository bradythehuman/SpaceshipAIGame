import pygame


class Ship:
    def __init__(self):
        self.hull = 50
        self.shield = 3
        self.hull_dmg = 20
        self.shield_dmg = 2
        self.background = pygame.image.load("bitmaps/orange_ship.bmp")

        floor_img = pygame.image.load("bitmaps/orangeShipFloor.bmp")
        self.floor = []
        for i in range(48):
            for j in range(48):
                if floor_img.get_at((i, j)) == (254, 254, 254, 255):
                    self.floor.append([i, j])


if __name__ == "__main__":
    my_ship = Ship()
    print("floor: " + str(my_ship.floor))
