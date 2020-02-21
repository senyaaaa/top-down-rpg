import pygame
import random
from framework.application import Application, Input
from framework.loader import Loader
from framework.renderer import Renderer, Entity
from framework.states import State, Trans, Transition
from framework.window import Window
from framework.map import Map, Platform, Facade, Door, Cutting, Cells, Talking_area


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


class Houses(Entity):
    def __init__(self, house, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("data/houses/" + house + ".png"), (500, 500)), pygame.Vector2(x, y))


class Ground(Entity):
    def __init__(self, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("grass.png"), (2000, 2000)), pygame.Vector2(x, y))


class Interior(Entity):
    def __init__(self, obj, size, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("data/houses/inn/" + obj), size), pygame.Vector2(x, y))


class NPC(Entity):
    def __init__(self, name, x, y):
        super().__init__(pygame.transform.scale(Loader.get_image("data/npc/" + name), (70, 100)), pygame.Vector2(x, y))


class Tool(Entity):
    def __init__(self, tool):
        super().__init__(pygame.transform.scale(Loader.get_image("data/tool/" + tool), (50, 60)), pygame.Vector2())


class Inventory(Entity):
    def __init__(self):
        super().__init__(Loader.get_image("data/inventory.png"), pygame.Vector2(50, 92))
        self.inventory = {(100, 200): 0, (170, 200): 0, (240, 200): 0, (310, 200): 0,
                          (100, 295): 0, (170, 295): 0, (240, 295): 0, (310, 295): 0,
                          (100, 390): 0, (170, 390): 0, (240, 390): 0, (310, 390): 0}

    def add_object(self, obj):
        for i in self.inventory:
            if self.inventory[i] == 0:
                self.inventory[i] = obj
                return True

    def del_object(self, obj):
        for i in self.inventory:
            if self.inventory[i] == obj:
                self.inventory[i] = 0

    def return_inventory(self):
        return self.inventory


class Dialog(Entity):
    def __init__(self):
        super().__init__(pygame.transform.scale(Loader.get_image("data/DialogWindow/dialogwindow.png"), (800, 250)),
                         pygame.Vector2(140, 450))

class Button(Entity):
    def __init__(self, btn):
        super().__init__(Loader.get_image("data/DialogWindow/" + btn + "_btn.png"), pygame.Vector2(420, 69))
        self.rect = self.image.get_rect()



# [Game] -> Push Pause
# [Game, Pause] -> Pop
# []
class MainMenu(State):
    def handle_event(self, event) -> Transition:
        pos = (270, 810), (200, 300)
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
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("grass.png"), (2000, 2000)), [0, 0])
        if not self.onbut:
            pygame.display.get_surface().blit(Loader.get_image("Play_btn.png"), [270, 200])
        else:
            pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("Play_btn.png"), (600, 120)), [240, 190])
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("data/main_hero/chill.png"), (100, 100)), [490, 400])
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("tree1.png"), (100, 400)), [150, 100])
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("tree1.png"), (100, 400)), [80, 150])
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("tree1.png"), (100, 400)), [950, 120])
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("tree1.png"), (100, 400)), [830, 110])
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("tree1.png"), (100, 400)), [880, 180])
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

        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("grass.png"), (2000, 2000)), [0, 0])
        Renderer.clear_screen((235, 215, 160))
        pygame.display.get_surface().blit(pygame.transform.scale(Loader.get_image("data/main_hero/chill.png"), (90, 90)), [495, 315])

        f = pygame.font.SysFont('Impact', 70)
        text = f.render("Pause", 1, (165, 115, 100))
        pygame.display.get_surface().blit(text, [450, 100])
        return Trans.Pass


class GameState(State):
    def do_some_cut(self, c, r, picture):
        rects = []
        sheetImage = pygame.image.load(picture).convert_alpha()
        spriteWidth = sheetImage.get_width() // c
        spriteHeight = sheetImage.get_height() // r

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
        return returnedSurfaces

    def on_start(self):
        with open("map.csv", newline='') as csvfile:
            m = Map()
            self.coords = m.drawing(csvfile, 100)
        self.in_home = False
        self.on_facade = False
        self.tree_fall = False
        self.inventory_is_open = False
        self.dialog_is_open = False
        self.anim = 0
        self.count = 0
        self.wood = 0
        self.broken = 0
        self.quest = 1
        self.dir = 3
        self.types_of_houses = {2: "inn", 3: "house"}
        self.types_of_rooms = {}
        self.types_of_furniture = {1: "chest", 2: "bed", 3: "chair", 4: "table"}
        self.trees = {}
        self.buttons = {}
        self.entities = []
        self.building = []
        self.furniture = []
        self.talking_areas = []
        self.player = Player()
        self.inventory = Inventory()
        self.dialog = Dialog()
        self.npc_icon = NPC("woodcutter.png", 165, 473)
        self.ax_icon = Tool("ax.png")
        self.wood_icon = Player()
        self.cancel_btn = Button("cancel")
        self.accept_btn = Button("accept")
        self.wood_icon.image = pygame.transform.scale(Loader.get_image("data/trees/wood.png"), (60, 50))
        self.ax_icon.image = pygame.transform.scale(self.do_some_cut(2, 2, "data/tool/ax.png")[0][0], (60, 70))



        self.tool = Tool("ax.png")
        self.ground = Ground(0, 0)
        self.pos = pygame.Vector2()
        self.tool.pos = (1000, 500)
        self.player.pos = (1000, 500)
        for i in self.coords:
            for j in self.coords[i]:
                x, y = j[0], j[1]
                if i == 1:
                    n = str(random.randint(1, 3))
                    tree = Tree("tree" + n + ".png", x, y)
                    tree.image = pygame.transform.scale(self.do_some_cut(4, 1, "data/trees/tree" + n + ".png")[0][0], (100, 400))
                    self.entities.append(tree)
                    self.trees[(x + 30, y - 30)] = tree, 100, n
                elif i == 4:
                    self.entities.append(NPC("woodcutter.png", x, y))
                else:
                    self.building.append(Houses(self.types_of_houses[i], x, y))

    def handle_event(self, event) -> Transition:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.dialog_is_open:
                pos = Input.mouse_position - Renderer.cameraTranslation
                if self.cancel_btn.rect.collidepoint(pos):
                    self.dialog_is_open = False
                if self.accept_btn.rect.collidepoint(pos):
                    if self.quest == 1:
                        self.inventory.add_object(self.ax_icon)
                    self.quest += 1
                    self.dialog_is_open = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                if self.player.check(self.doors, self.player.pos + Renderer.cameraTranslation):
                    self.coord_of_house = self.player.check(self.doors, (
                    self.player.x, self.player.y) + Renderer.cameraTranslation).rect.topleft
                    if not self.in_home:
                        self.camera_pos = Renderer.cameraTranslation
                        self.in_home = True
                        self.premises = self.types_of_rooms[self.player.check(self.doors, (self.player.x, self.player.y) + Renderer.cameraTranslation)]
                    else:
                        self.in_home = False
                if self.player.check(self.talking_areas, self.player.pos + Renderer.cameraTranslation):
                    print(self.talking_areas)
                    self.dialog_is_open = True

            if event.key == pygame.K_TAB:
                if not self.inventory_is_open:
                    self.inventory_is_open = True
                else:
                    self.inventory_is_open = False

            if event.key == pygame.K_ESCAPE:
                return Trans.Push(PauseState())
        # pos = Input.mouse_position
        # if self.player.check(self.inventory.cells, pos):
        #     if self.inventory_is_open:
        #         print('asd')
        #         if self.inventory.inventory[self.player.check(self.inventory.cells, pos).rect.topleft] != 0:
        #             self.inventory.inventory[self.player.check(self.inventory.cells, pos).rect.topleft].image = \
        #                 pygame.transform.scale(self.do_some_cut(2, 2, "data/tool/ax.png")[0][0], (60, 100))
        #             print('asdasdasdasd')

        if event.type == pygame.QUIT:
            return Trans.Quit
        return Trans.Pass

    def slerp(self, p0, p1, t):
        return p0 + (p1 - p0) * t

    def room(self, coords):
        self.platforms = []
        self.furniture = []
        Renderer.cameraTranslation = self.camera_pos + (0, 100)
        x, y = coords[0] - self.camera_pos[0] - 175, coords[1] - self.camera_pos[1] - 300
        Renderer.clear_screen((0, 0, 0))
        Renderer.submit(Interior("floor.png", (500, 411), x, y))
        for i in sorted(self.interior, reverse=True):
            for j in self.interior[i]:
                a, b = x + j[0], y + j[1]
                if i == 1:
                    self.furniture.append(Interior("chest.png", (50, 50), a, b))
                elif i == 2:
                    self.furniture.append(Interior("bed.png", (100, 160), a, b))
                elif i == 3:
                    self.furniture.append(Interior("chair.png", (50, 50), a, b))
                elif i == 4:
                    self.furniture.append(Interior("table.png", (150, 100), a, b))
        for f in self.furniture:
            Renderer.submit(f)
        Renderer.submit(self.player)

    def move(self):
        if Input.is_key_held(pygame.K_SPACE):
            if self.quest != 1:
                if self.player.check(self.cutting, self.player.pos + Renderer.cameraTranslation):
                    coord = self.player.check(self.cutting, (
                        self.player.pos) + Renderer.cameraTranslation).rect.topleft - Renderer.cameraTranslation
                    coord = (round(coord[0], -1), round(coord[1], -1))
                    if self.player.x + Renderer.cameraTranslation[0] >= self.player.check(self.cutting, (self.player.x, self.player.y) + Renderer.cameraTranslation).rect.center[0] - 50:
                        self.tool.image = pygame.transform.scale(self.do_some_cut(2, 2, "data/tool/ax.png")[1][self.count // 20], (60, 70))
                        self.player.image = pygame.transform.scale(self.do_some_cut(4, 4, "data/main_hero/hero.png")[0][1], (100, 100))
                        self.tool.pos = self.player.pos[0], self.player.pos[1] + 65 - (self.count // 20) * 50
                    else:
                        self.tool.image = pygame.transform.scale(self.do_some_cut(2, 2, "data/tool/ax.png")[0][self.count // 20], (60, 70))
                        self.player.image = pygame.transform.scale(self.do_some_cut(4, 4, "data/main_hero/hero.png")[1][1], (100, 100))
                        self.tool.pos = self.player.pos[0] + 35, self.player.pos[1] + 15 + (self.count // 20) * 50
                    if self.count == 39 and self.trees[coord][1] != 20:
                        n = self.trees[coord][2]
                        self.trees[coord] = (self.trees[coord][0], self.trees[coord][1] - 20, self.trees[coord][2])
                        self.trees[coord][0].image = pygame.transform.scale(self.do_some_cut(4, 1, "data/trees/tree" + n + ".png")[0][::-1][self.trees[coord][1] // 25 - 1], (100, 400))
                        if self.trees[coord][1] == 20:
                            self.tree_fall = self.trees[coord][0], int(self.trees[coord][2]) - 1
        else:
            if Input.is_key_held(pygame.K_a):
                self.player.x -= 5
                if self.player.check(self.platforms, self.player.pos + Renderer.cameraTranslation) or \
                        self.player.x < 0:
                    self.player.x += 5
                self.player.image = pygame.transform.scale(self.do_some_cut(4, 4, "data/main_hero/hero.png")[0][self.count // 10], (100, 100))
                self.dir = 0
            if Input.is_key_held(pygame.K_d):
                self.player.x += 5
                if self.player.check(self.platforms, self.player.pos + Renderer.cameraTranslation) or \
                        self.player.x > 1900:
                    self.player.x -= 5
                self.player.image = pygame.transform.scale(self.do_some_cut(4, 4, "data/main_hero/hero.png")[1][self.count // 10], (100, 100))
                self.dir = 1
            if Input.is_key_held(pygame.K_w):
                self.player.y -= 5
                if self.player.check(self.platforms, self.player.pos + Renderer.cameraTranslation) or \
                        self.player.y < 0:
                    self.player.y += 5
                self.player.image = pygame.transform.scale(self.do_some_cut(4, 4, "data/main_hero/hero.png")[2][self.count // 10], (100, 100))
                self.dir = 2
            if Input.is_key_held(pygame.K_s):
                self.player.y += 5
                if self.player.check(self.platforms, self.player.pos + Renderer.cameraTranslation) or \
                        self.player.y > 1900:
                    self.player.y -= 5
                self.player.image = pygame.transform.scale(self.do_some_cut(4, 4, "data/main_hero/hero.png")[3][self.count // 10], (100, 100))
                self.dir = 3

        self.count += 1
        if self.count == 40:
            self.count = 0

    def create_map(self):
        for i in self.coords:
            for j in self.coords[i]:
                x, y = j[0] + Renderer.cameraTranslation[0], j[1] + Renderer.cameraTranslation[1]
                if i in self.types_of_houses:
                    pf = Platform(x, y, "house")
                    self.platforms.append(pf)
                    f = Facade(x, y)
                    self.facade.append(f)
                    self.posit.append(((x, y), i))

                    d = Door(x + 175, y + 480)
                    self.doors.append(d)
                    self.types_of_rooms[d] = i
                    self.posit.append(((x + 175, y + 480), 'door'))
                else:
                    if i == 1:
                        cut = Cutting(x, y)
                        self.cutting.append(cut)
                        self.posit.append(((x, y), 'cut'))
                    elif i == 4:
                        t = Talking_area(x - 50, y - 50)
                        self.talking_areas.append(t)
                        self.posit.append(((x - 50, y - 50), 'dialog'))
                    pf = Platform(x, y, i)
                    self.platforms.append(pf)
                    self.posit.append(((x, y), i))

    def create_room(self, coord, premises):
        x, y = coord[0] - 175, coord[1] - 210
        with open(self.types_of_houses[premises] + ".csv", newline='') as csvfile:
            m = Map()
            self.interior = m.drawing(csvfile, 50)
            for i in sorted(self.interior, reverse=True):
                for j in self.interior[i]:
                    a, b = x + j[0], y + j[1]
                    pf = Platform(a, b, self.types_of_furniture[i])
                    self.platforms.append(pf)
                    self.posit.append(((a, b), self.types_of_furniture[i]))
        self.platforms.append(pygame.Rect(x, y, 500, 10))
        self.platforms.append(pygame.Rect(x, y + 420, 500, 10))
        self.platforms.append(pygame.Rect(x - 10, y + 10, 10, 500))
        self.platforms.append(pygame.Rect(x + 500, y + 10, 10, 500))
        self.posit.append(((x, y), 'wool_hor'))
        self.posit.append(((x, y + 420), 'wool_hor'))
        self.posit.append(((x - 10, y + 10), 'wool_ver'))
        self.posit.append(((x + 500, y + 10), 'wool_ver'))
        d = Door(x + 175, y + 360)
        self.doors.append(d)
        self.posit.append(((x + 175, y + 360), 'door'))

    def update(self) -> Transition:
        f = pygame.font.SysFont('Impact', 40)
        self.talking_areas = []
        self.platforms = []
        self.cutting = []
        self.doors = []
        self.facade = []
        self.posit = []
        self.player.image = pygame.transform.scale(self.do_some_cut(4, 4, "data/main_hero/hero.png")[self.dir][1], (100, 100))
        self.tool.pos = (-420, 420)
        if self.tree_fall:
            self.anim += 1
            self.tree_fall[0].image = pygame.transform.scale(
                            self.do_some_cut(5, 3, "data/trees/falling_tree.png")[self.tree_fall[1]][self.anim // 10], (480, 400))
            if self.anim == 49:
                self.tree_fall[0].image = pygame.transform.scale(Loader.get_image("data/trees/stump.png"), (100, 400))
                self.anim = 0
                self.tree_fall = False
                self.inventory.add_object(self.wood_icon)
                if self.quest == 2:
                    self.wood += 1


        if not self.in_home:
            self.create_map()
        else:
            self.create_room(self.coord_of_house, self.premises)
        if not self.dialog_is_open:
            self.move()

        if self.player.check(self.facade, self.player.pos + Renderer.cameraTranslation):
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
            self.room(self.coord_of_house)
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
        Renderer.submit(self.tool)
        if self.inventory_is_open:
            # self.inventory.pos = self.player.pos - (440, 215)
            if self.pos.x < 490:
                self.inventory.pos = 650, self.inventory.y
            else:
                self.inventory.pos = 50, self.inventory.y
            Renderer.submit(self.inventory, False)
            for i in self.inventory.inventory:
                if self.inventory.inventory[i] != 0:
                    pos = i
                    if self.pos.x < 490:
                        pos = pos[0] + 600, pos[1]
                    self.inventory.inventory[i].pos = pos
                    # self.inventory.inventory[i] = self.player.pos - self.inventory.inventory[i] + (-80, 280)
                    Renderer.submit(self.inventory.inventory[i], False)
        if self.dialog_is_open:
            self.cancel_btn.pos = (800, 640)
            self.cancel_btn.rect[0] = 800 - Renderer.cameraTranslation[0]
            self.cancel_btn.rect[1] = 640 - Renderer.cameraTranslation[1]
            self.accept_btn.pos = (650, 640)
            self.accept_btn.rect[0] = 650 - Renderer.cameraTranslation[0]
            self.accept_btn.rect[1] = 640 - Renderer.cameraTranslation[1]

            self.npc_icon.image = Loader.get_image("data/DialogWindow/woodcutter_icon.png")
            Renderer.submit(self.dialog, False)
            Renderer.submit(self.npc_icon, False)
            Renderer.submit(self.cancel_btn, False)

            if self.quest == 1:
                string = ["Oh, finally somebody who could ", "help an old man out! Chop some ", "wood for me, will ya?"]
                for i in range(3):
                    text = f.render(string[i], 1, (160, 135, 132))
                    Renderer.submit((text, [320, 480 + (i * 40)] - Renderer.cameraTranslation))
                Renderer.submit(self.accept_btn, False)
            if self.quest == 2:
                if self.wood < 3:
                    text = f.render("Нou haven’t done anything yet.", 1, (160, 135, 132))
                    Renderer.submit((text, [320, 480] - Renderer.cameraTranslation))
                else:
                    self.inventory.del_object(self.wood_icon)
                    string = ["Thank you so much, young man.", "Take this axe as a reward."]
                    for i in range(2):
                        text = f.render(string[i], 1, (160, 135, 132))
                        Renderer.submit((text, [320, 480 + (i * 40)] - Renderer.cameraTranslation))
                    Renderer.submit(self.accept_btn, False)
            if self.quest == 3:
                string = ["I used to be an adventurer like you,", "but then..."]
                for i in range(2):
                    text = f.render(string[i], 1, (160, 135, 132))
                    Renderer.submit((text, [320, 480 + (i * 40)] - Renderer.cameraTranslation))
        if self.quest == 2:
            text = f.render("Wood: " + str(self.wood) + "/3", 1, (170, 120, 104))
            Renderer.submit((text, [100, 100] - Renderer.cameraTranslation))

        Renderer.present()

        # Renderer.check(self.posit)

        return Trans.Pass




if __name__ == "__main__":
    app = Application(MainMenu(), "Game", 1080, 720)
    app.run()
