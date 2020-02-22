from typing import Dict
import pygame


class Loader:
    loadedImages: Dict[str, pygame.Surface] = {}

    @staticmethod
    def __load_image(name: str) -> pygame.Surface:
        key = name.lower()
        item = pygame.image.load(key)
        Loader.loadedImages[key] = item
        return item

    @staticmethod
    def get_image(key: str) -> pygame.Surface:
        return Loader.loadedImages.get(key, Loader.__load_image(key))

