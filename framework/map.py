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
        for i in range(5):
            self.d[i] = []
        for i in range(self.world_width):
            for j in range(self.world_height):
                if self.data[i][j] != 0:
                    self.d[self.data[i][j]].append((j * n, i * n))
        return self.d


class Platform:
    def __init__(self, x, y, obj):
        if obj == 1:
            self.rect = Rect(x + 10, y + 10, 80, 40)
        if obj == 4:
            self.rect = Rect(x + 10, y + 80, 50, 20)
        if obj == 'house':
            self.rect = Rect(x + 15, y + 100, 475, 285)
        if obj == 'chest':
            self.rect = Rect(x + 20, y + 10, 10, 5)
        if obj == 'bed':
            self.rect = Rect(x, y + 10, 100, 20)
        if obj == 'chair':
            self.rect = Rect(x + 20, y, 10, 5)
        if obj == 'table':
            self.rect = Rect(x + 20, y + 20, 100, 10)


class Facade:
    def __init__(self, x, y):
        self.rect = Rect(x, y + 400, 500, 100)


class Door:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 150, 20)


class Cutting:
    def __init__(self, x, y):
        self.rect = Rect(x + 30, y - 30, 40, 40)


class Cells:
    def __init__(self, pos):
        self.rect = Rect(pos[0], pos[1], 70, 95)


class Talking_area:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 175, 200)


class Btn:
    def __init__(self, x, y, btn):
        if btn == "Developer mode":
            self.rect = Rect(x - 10, y, 280, 50)
        if btn == "Exit":
            self.rect = Rect(x - 10, y, 100, 50)