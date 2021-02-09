import pygame
from settings import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            'sprite_devil': {
                'sprite': [pygame.image.load(f'../spr/devil/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'../spr/devil/anim/{i}.png').convert_alpha() for i in range(9)]),
                'animation_dist': 300,
                'animation_speed': 10,
                'blocked': True,
            },
        }

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters['sprite_devil'], (7, 4)),
        ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_objects], default=(float('inf'), 0))


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.backup_animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.side = 30
        self.animation_count = 0
        self.animation_work_times = 0
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    @property
    def is_on_fire(self):
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.distance_to_sprite, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = CENTER_RAY + delta_rays
        self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance_to_sprite > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = self.proj_height // 2
            shift = half_proj_height * self.shift
            # выбор спрайта исходя из угла обзора
            if self.viewing_angles:
                if self.theta < 0:
                    self.theta += DOUBLE_PI
                self.theta = 360 - int(math.degrees(self.theta))

                for angles in self.sprite_angles:
                    if self.theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            # анимация спрайтов
            sprite_object = self.object
            if self.animation and self.distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0
                    self.animation_work_times += 1
            else:
                for i in range(9 - (self.animation_work_times % 9)):
                    self.animation.rotate()
                self.animation_work_times = 0

            # позиция спрайта
            sprite_pos = (self.current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (self.proj_height, self.proj_height))
            return (self.distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
