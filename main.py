import random
from pygame import draw
import pygame
from pygame import sprite
import random
from framework.application import Application, Input
from framework.loader import Loader
from framework.renderer import Renderer, Entity
from framework.states import State, Trans, Transition
from framework.window import Window
from framework.map import Map, Platform, Facade, Door


class Player(Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(Loader.get_image("data/main_hero/chill.png"), (100, 100)), pygame.Vector2())
        self.rect = self.image.get_rect()

    def check(self, lst, pos):
        self.rect.x, self.rect.y = pos[0], pos[1]
        for p in lst:
            if self.rect.colliderect(p):
                return p


class Tree(Entity):
    def __init__(self, tree, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("data/trees/" + tree), (100, 400)), pygame.Vector2(x, y - 350))


class House(Entity):
    def __init__(self, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("data/house/house.png"), (500, 500)), pygame.Vector2(x, y))


class Ground(Entity):
    def __init__(self, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("grass.png"), (2000, 2000)), pygame.Vector2(x, y))


class Interior(Entity):
    def __init__(self, obj, size, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("data/house/inn/" + obj), size), pygame.Vector2(x, y))

# [Game] -> Push Pause
# [Game, Pause] -> Pop
# []
class MainMenu(State):
    def handle_event(self, event) -> Transition:
        pos = (270, 810), (100, 200)
        self.onbut = False
        if event.type == pygame.MOUSEMOTION:
            x2, y2 = event.pos
            if x2 > pos[0][0] and x2 < pos[0][1] and y2 > pos[1][0] and y2 < pos[1][1]:
                self.onbut = True
            else:
                self.onbut = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = event.pos
            if x1 > pos[0][0] and x1 < pos[0][1] and y1 > pos[1][0] and y1 < pos[1][1]:
                return Trans.Switch(GameState())
        if event.type == pygame.QUIT:
            return Trans.Quit
        return Trans.Pass

    def update(self) -> Transition:
        Renderer.clear_screen(0xffffff)
        if not self.onbut:
            pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), ((270, 100), (540, 100)))
        else:
            pygame.draw.rect(pygame.display.get_surface(), (150, 0, 0), ((270, 100), (540, 100)))

        return Trans.Pass


class PauseState(State):
    def handle_event(self, event) -> Transition:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return Trans.Pop

        if event.type == pygame.QUIT:
            return Trans.Quit
        return Trans.Pass

    def update(self) -> Transition:
        Renderer.clear_screen(0x000000)

        return Trans.Pass


class GameState(State):
    def do_some_cut(self, n, count):
        rects = []
        sheetImage = pygame.image.load('data/main_hero/hero.png').convert_alpha()
        spriteWidth = sheetImage.get_width() // 4
        spriteHeight = sheetImage.get_height() // 4

        for y in range(0, sheetImage.get_height(), spriteHeight):
            if y + spriteHeight > sheetImage.get_height():
                continue
            lst = []
            for x in range(0, sheetImage.get_width(), spriteWidth):
                if x + spriteWidth > sheetImage.get_width():
                    continue
                lst.append((x, y, spriteWidth, spriteHeight))
            rects.append(lst)
        returnedSurfaces = []
        for rect in rects:
            lst = []
            for i in rect:
                surf = pygame.Surface((i[2], i[3]), 0, sheetImage)
                surf.blit(sheetImage, (0, 0), i, pygame.BLEND_RGBA_ADD)
                lst.append(surf)
            returnedSurfaces.append(lst)
        self.player.image = pygame.transform.scale(returnedSurfaces[n][count // 10], (100, 100))

    def on_start(self):
        with open('map.csv', newline='') as csvfile:
            m = Map()
            self.coords = m.drawing(csvfile, 100)
        self.in_home = False
        self.on_facade = False
        self.count = 0

        self.entities = []
        self.building = []
        self.player = Player()
        self.ground = Ground(0, 0)
        self.pos = pygame.Vector2()
        self.player.pos = (1000, 500)
        for i in self.coords[2]:
            x, y = i[0], i[1]
            self.building.append(House(x, y))

        for i in self.coords[1]:
            x, y = i[0], i[1]
            self.entities.append(Tree("tree" + str(random.randint(1, 3)) + ".png", x, y))

    def handle_event(self, event) -> Transition:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                if self.player.check(self.doors, (self.player.x, self.player.y) + Renderer.cameraTranslation):
                    self.coord_of_house = self.player.check(self.doors, (
                    self.player.x, self.player.y) + Renderer.cameraTranslation).rect.topleft
                    if not self.in_home:
                        self.camera_pos = Renderer.cameraTranslation
                        self.in_home = True
                    else:
                        self.in_home = False
            if event.key == pygame.K_ESCAPE:
                return Trans.Push(PauseState())

        if event.type == pygame.QUIT:
            return Trans.Quit
        return Trans.Pass

    def slerp(self, p0, p1, t):
        return p0 + (p1 - p0) * t

    def room(self, coords, room):
        self.platforms = []
        Renderer.cameraTranslation = self.camera_pos + (0, 100)
        x, y = coords[0] - self.camera_pos[0] - 175, coords[1] - self.camera_pos[1] - 300
        Renderer.clear_screen((0, 0, 0))
        Renderer.submit(Interior("floor.png", (500, 411), x, y))
        with open('room_1.csv', newline='') as csvfile:
            m = Map()
            self.interior = m.drawing(csvfile, 50)
        for i in sorted(self.interior, reverse=True):
            for j in self.interior[i]:
                a, b = x + j[0], y + j[1]
                if i == 1:
                    pf = Platform(a, b, 'chest')
                    self.platforms.append(pf)
                    self.furniture.append(Interior("chest.png", (50, 50), a, b))
                elif i == 2:
                    pf = Platform(a, b, 'bed')
                    self.platforms.append(pf)
                    self.furniture.append(Interior("bed.png", (100, 160), a, b))
        for f in self.furniture:
            Renderer.submit(f)
        Renderer.submit(self.player)

    def move(self):
        if Input.is_key_held(pygame.K_a):
            self.player.x -= 5
            if self.player.check(self.platforms, (self.player.x, self.player.y) + Renderer.cameraTranslation) or \
                    self.player.x < 0:
                self.player.x += 5
            self.do_some_cut(0, self.count)
        if Input.is_key_held(pygame.K_d):
            self.player.x += 5
            if self.player.check(self.platforms, (self.player.x, self.player.y) + Renderer.cameraTranslation) or \
                    self.player.x > 1900:
                self.player.x -= 5
            self.do_some_cut(1, self.count)
        if Input.is_key_held(pygame.K_w):
            self.player.y -= 5
            if self.player.check(self.platforms, (self.player.x, self.player.y) + Renderer.cameraTranslation) or \
                    self.player.y < 0:
                self.player.y += 5
            self.do_some_cut(2, self.count)
        if Input.is_key_held(pygame.K_s):
            self.player.y += 5
            if self.player.check(self.platforms, (self.player.x, self.player.y) + Renderer.cameraTranslation) or \
                    self.player.y > 1900:
                self.player.y -= 5
            self.do_some_cut(3, self.count)
        self.count += 1
        if self.count == 40:
            self.count = 0

    def create_map(self):
        for i in self.coords:
            for j in self.coords[i]:
                if i == 1:
                    if not self.in_home:
                        x, y = j[0] + Renderer.cameraTranslation[0], j[1] + Renderer.cameraTranslation[1]
                        pf = Platform(x, y, i)
                        self.platforms.append(pf)
                        self.posit.append(((x, y), i))
                if i == 2:
                    x, y = j[0] + Renderer.cameraTranslation[0], j[1] + Renderer.cameraTranslation[1]
                    if not self.in_home:
                        pf = Platform(x, y, i)
                        self.platforms.append(pf)
                        f = Facade(x, y)
                        self.facade.append(f)
                        self.posit.append(((x, y), i))
                    else:
                        self.platforms.append(pygame.Rect(x, y + 170, 500, 10))
                        self.platforms.append(pygame.Rect(x, y + 590, 500, 10))
                        self.platforms.append(pygame.Rect(x - 10, y + 180, 10, 500))
                        self.platforms.append(pygame.Rect(x + 500, y + 180, 10, 500))
                        self.posit.append(((x, y + 170), 'wool_hor'))
                        self.posit.append(((x, y + 590), 'wool_hor'))
                        self.posit.append(((x - 10, y + 180), 'wool_ver'))
                        self.posit.append(((x + 500, y + 180), 'wool_ver'))
                    d = Door(x + 175, y + 480)
                    self.doors.append(d)
                    self.posit.append(((x + 175, y + 480), 'door'))

    def update(self) -> Transition:
        self.furniture = []
        if not self.in_home:
            self.platforms = []
        self.doors = []
        self.facade = []
        self.posit = []
        self.do_some_cut(3, 15)

        self.create_map()

        self.move()
        if self.player.check(self.facade, (self.player.x, self.player.y) + Renderer.cameraTranslation):
            self.on_facade = True
        else:
            self.on_facade = False

        self.pos.x = self.slerp(self.pos.x, self.player.x, 0.1)
        self.pos.y = self.slerp(self.pos.y, self.player.y, 0.1)

        Renderer.begin_scene(-(self.pos - ((Window.Instance.width - self.player.image.get_width()) / 2,
                                                  (Window.Instance.height - self.player.image.get_height()) / 2)))
        Renderer.clear_screen(0xffffff)

        if self.pos.y < 320:
            Renderer.cameraTranslation[1] = 0
        if self.pos.x < 490:
            Renderer.cameraTranslation[0] = 0
        if self.pos.y > 1580:
            Renderer.cameraTranslation[1] = -1280
        if self.pos.x > 1410:
            Renderer.cameraTranslation[0] = -920
        if self.in_home:
            self.room(self.coord_of_house, 'inn')
        else:
            if not self.on_facade:
                Renderer.submit(self.ground)
                Renderer.submit(self.player)
                for b in self.building:
                    Renderer.submit(b)
                for ent in self.entities:
                    Renderer.submit(ent)
            else:
                Renderer.submit(self.ground)
                for b in self.building:
                    Renderer.submit(b)
                Renderer.submit(self.player)
                for ent in self.entities:
                    Renderer.submit(ent)

        Renderer.present()
        # Renderer.check(self.posit)

        return Trans.Pass


if __name__ == "__main__":
    app = Application(MainMenu(), "Game", 1080, 720)
    app.run()
