from typing import List, Tuple, Union
from framework.map import Platform
import pygame
from pygame import draw


class Entity:
    Alive: bool = True

    def __init__(self, image: pygame.Surface, position: pygame.Vector2):
        self.image: pygame.Surface = image
        self._pos: pygame.Vector2 = position

    @property
    def pos(self) -> pygame.Vector2:
        return self._pos

    @pos.setter
    def pos(self, a: Union[pygame.Vector2, float], y: float = 0):
        if isinstance(a, pygame.Vector2):
            self._pos = a
        else:
            self._pos = pygame.Vector2(a, y)

    @property
    def x(self):
        return self._pos.x

    @x.setter
    def x(self, v):
        self._pos.x = v

    @property
    def y(self):
        return self._pos.y

    @y.setter
    def y(self, v):
        self._pos.y = v


class Renderer:
    entities: List[Tuple[pygame.Surface, Tuple[int, int]]] = []
    cameraTranslation: Tuple[int, int] = (0, 0)
    windowSurface: pygame.Surface = pygame.display.get_surface()

    @staticmethod
    def start_frame():
        Renderer.entities.clear()

    @staticmethod
    def clear_screen(color):
        pygame.display.get_surface().fill(color)

    @staticmethod
    def begin_scene(camera_position: Tuple[int, int] = None):
        if camera_position is not None:
            Renderer.cameraTranslation = camera_position


    @staticmethod
    def submit(entity: Union[Entity, Tuple[pygame.Surface, Tuple[int, int]]], camera_affect: bool = True):
        if isinstance(entity, Entity):
            ent_pos = tuple(entity.pos)
            ent_img = entity.image
        else:
            ent_pos = entity[1]
            ent_img = entity[0]
        if camera_affect:
            tp = (int(ent_pos[0] + Renderer.cameraTranslation[0]),
                  int(ent_pos[1] + Renderer.cameraTranslation[1]))
            Renderer.entities.append((ent_img, tp))
        else:
            Renderer.entities.append((ent_img, ent_pos))


    @staticmethod
    def return_platforms(platforms):
        return platforms

    @staticmethod
    def present():
        pygame.display.get_surface().blits(Renderer.entities, doreturn=False)

    @staticmethod
    def check(lst):
        for i in lst:
            if i[1] == 1:
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0] + 10, i[0][1] + 10), (80, 40)), 1)
            elif i[1] == 2 or i[1] == 3:
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0], i[0][1] + 100), (500, 285)), 1)
            elif i[1] == 4:
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0] + 10, i[0][1] + 80), (50, 20)), 1)
            elif i[1] == 'door':
                draw.rect(pygame.display.get_surface(), (255, 255, 255), ((i[0][0], i[0][1]), (150, 20)), 1)
            elif i[1] == 'wool_hor':
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0], i[0][1]), (500, 10)), 1)
            elif i[1] == 'wool_ver':
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0], i[0][1]), (10, 410)), 1)
            elif i[1] == 'room':
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0], i[0][1]), (50, 50)), 1)
            elif i[1] == 'chest':
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0] + 20, i[0][1] + 10), (10, 5)), 1)
            elif i[1] == 'bed':
                draw.rect(pygame.display.get_surface(), (255, 0, 0), ((i[0][0], i[0][1] + 10), (100, 20)), 1)
            elif i[1] == 'cut':
                draw.rect(pygame.display.get_surface(), (255, 255, 255), ((i[0][0] + 10, i[0][1] - 30), (80, 40)), 1)