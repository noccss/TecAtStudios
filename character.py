import pygame

class Character:
    def __init__(self, image_path, width, height, position):
        self.image_path = image_path  # Corrigir o nome do atributo
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.position = position

class Option:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.background = pygame.transform.scale(pygame.image.load("./assets/dialog_box/options.png"), (width, height))
        self.rect = pygame.Rect(x, y, width, height)
