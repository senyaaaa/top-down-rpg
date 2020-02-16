from typing import Tuple

import pygame

from framework.renderer import Renderer
from .states import State, StateMachine
from .window import Window


class Input:
    mouse_position = (0, 0)
    _pressed_buttons = (0, 0, 0)
    _pressed_keys = None

    @staticmethod
    def update():
        Input.mouse_position = pygame.mouse.get_pos()
        Input._pressed_buttons = pygame.mouse.get_pressed()
        Input._pressed_keys = pygame.key.get_pressed()

    @staticmethod
    def is_key_held(key: int) -> bool:
        return Input._pressed_keys[key]

    @staticmethod
    def is_button_pressed(btn: int) -> bool:
        return Input._pressed_buttons[btn]

    @staticmethod
    def get_mouse_pos() -> Tuple[int, int]:
        return Input.mouse_position


class Application:
    def __init__(self, initial_state: State, *args):
        self.stateMachine: StateMachine = StateMachine(initial_state)
        self.window = Window(*args)

    def run(self):
        self.stateMachine.start()
        clock = pygame.time.Clock()
        while self.stateMachine.running:
            clock.tick(60)
            print(int(clock.get_fps()))
            Renderer.start_frame()
            for event in pygame.event.get():
                self.stateMachine.handle_event(event)

            Input.update()

            self.stateMachine.update()
            self.window.request_redraw()
