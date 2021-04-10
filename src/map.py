from settings import *
import pygame

_ = False
matrix_map = [
    [7, 1, 1, 1, 1, 1, 1, 1, 1, 7],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, 2, 2, _, _, 5, 5, _, 1],
    [1, _, 2, _, _, _, _, 5, _, 1],
    [1, _, _, _, 6, 6, _, _, _, 1],
    [1, _, _, _, 6, 6, _, _, _, 1],
    [1, _, 3, _, _, _, _, 4, _, 1],
    [1, _, 3, 3, _, _, 4, 4, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [7, 1, 1, 1, 1, 1, 1, 1, 1, 7]

]

WORLD_WIDTH = len(matrix_map[0]) * TILE
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = {}
mini_map = set()
collision_walls = []
free_place = []

# анализ карты(для возможности изменения карты свыше)
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4
            elif char == 5:
                world_map[(i * TILE, j * TILE)] = 5
            elif char == 6:
                world_map[(i * TILE, j * TILE)] = 6
            elif char == 7:
                world_map[(i * TILE, j * TILE)] = 7
        else:
            free_place.append((i, j))

