from typing import Dict
import pygame


class Loader:
    loadedFonts:  Dict[str, pygame.font.FontType] = {}
    loadedImages: Dict[str, pygame.Surface] = {}

    @staticmethod
    def __load_font(font_name: str, font_size: int, *args, **kwargs) -> pygame.font.FontType:
        if not pygame.font.get_init():
            pygame.font.init()

        key = font_name.lower() + str(font_size)
        item = pygame.font.Font(font_name, font_size, *args, **kwargs)
        Loader.loadedFonts[key] = item
        return item

    @staticmethod
    def get_font(font_name: str, font_size: int) -> pygame.font.FontType:
        key = font_name.lower() + str(font_size)
        return Loader.loadedFonts.get(key, Loader.__load_font(font_name, font_size))

    @staticmethod
    def __load_image(name: str) -> pygame.Surface:
        key = name.lower()
        item = pygame.image.load(key)
        Loader.loadedImages[key] = item
        return item

    @staticmethod
    def get_image(key: str) -> pygame.Surface:
        return Loader.loadedImages.get(key, Loader.__load_image(key))

