import pygame


def img_to_pos(path):
    img = pygame.image.load(path)
    result = []
    for i in range(48):
        for j in range(48):
            if img.get_at((i, j)) != (0, 0, 0, 255):
                result.append([i, j])
    return result


def transform_up(pos, scalar=1):
    pos[1] -= scalar
    return pos


def transform_down(pos, scalar=1):
    pos[1] += scalar
    return pos


def transform_left(pos, scalar=1):
    pos[0] -= scalar
    return pos


def transform_right(pos, scalar=1):
    pos[0] += scalar
    return pos
