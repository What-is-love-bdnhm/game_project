import pygame
import math
from settings import *
from map import world_map


def mapping(x, y):
    return (x // TILE) * TILE, (y // TILE) * TILE


def ray_casting(screen, player_pos, player_angle):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # вертикали
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * TILE

        # горизонтали
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, TILE):
            depth_g = (y - oy) / sin_a
            x = ox + depth_g * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * TILE

        # проектирование
        depth = depth_v if depth_v < depth_g else depth_g
        depth *= math.cos(player_angle - cur_angle)
        proj_height = PROJ_COEFF / depth
        c = 255 / (1 + depth * depth * 0.00002)
        color = (c, c // 2, c // 3)
        pygame.draw.rect(screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
        cur_angle += DELTA_ANGLE
