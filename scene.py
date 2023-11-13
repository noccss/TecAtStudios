import pygame

class Scene:
    def __init__(self, image_path, width, height):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
