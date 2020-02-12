import csv
from pygame import draw, sprite, Surface, Rect, Color
import pygame


class Map:
    def drawing(self, map, n):
        self.d = {}
        self.map = map
        self.platforms = []
        text = csv.reader(self.map, delimiter=';')
        self.data = []
        for row in text:
            self.data.append([int(i) for i in row])
        self.world_width = len(self.data)
        self.world_height = len(self.data[0])
        self.d[1] = []
        self.d[2] = []
        for i in range(self.world_width):
            for j in range(self.world_height):
                if self.data[i][j] != 0:
                    self.d[self.data[i][j]].append((i * n, j * n))
        print(self.d)
        return self.d


class Platform:
    def __init__(self, x, y, obj):
        if obj == 1:
            self.rect = Rect(x + 10, y + 10, 80, 40)
        if obj == 2:
            self.rect = Rect(x + 15, y + 100, 475, 285)

class Facade:
    def __init__(self, x, y):
        self.rect = Rect(x, y + 400, 500, 100)


class Door:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 150, 20)
