import os
from typing import Callable

import pygame

from framework.renderer import Renderer

_MODE = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE

if pygame.vernum[0] >= 2:
    _MODE |= pygame.SCALED


class Window:
    Instance = None

    def __init__(self, title: str, width: int, height: int):
        Window.Instance = self
        self.title = title
        self.width = width
        self.height = height

        self.fullscreen = False

        self.eventCallback: Callable[[pygame.event.EventType], bool] = lambda event: False

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        if not pygame.get_init():
            pygame.init()
        pygame.display.set_mode((width, height), _MODE)
        pygame.display.set_caption(title)

        Renderer.windowSurface = pygame.display.get_surface()

    def request_redraw(self):
        pygame.display.flip()
        Renderer.windowSurface = pygame.display.get_surface()

    def poll_events(self):
        for event in pygame.event.get():
            yield event
