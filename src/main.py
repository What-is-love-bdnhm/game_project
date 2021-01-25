import pygame
from settings import *
from player import Player
import math
from map import world_map
from ray_casting import ray_casting
from drawing import Drawing

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
map_screen = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(screen, map_screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    player.movement()
    screen.fill(BLACK)

    drawing.background(player.angle)
    drawing.world(player.pos(), player.angle)
    drawing.fps(clock)
    drawing.mini_map(player)

    pygame.display.flip()
    clock.tick(FPS)
