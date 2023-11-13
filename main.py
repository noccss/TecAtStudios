import pygame
import sys
import json
from scene import Scene
from character import Character, Option

class KittyFightClub:
    def __init__(self):
        pygame.init()
        self.width = 1920
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Kitty Fight Club")
        self.clock = pygame.time.Clock()
        self.color = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "purple": (128, 0, 128),
            "dark_green": (0, 128, 0),
            "dark_blue": (0, 0, 128)
        }
        self.font = pygame.font.Font("./assets/fonts/PixeloidSans.ttf", 28)
        self.running = True
        self.pausado = False
        self.current_scene = 0
        self.newText = 0
        self.aswnserText = None
        self.characters_quantity_cenario = 0
        self.characters_name_cenario = []

        self.scenes = [
            Scene("./assets/background/corredor.png", self.width, self.height),
            Scene("./assets/background/sala_de_aula.png", self.width, self.height),
            Scene("./assets/background/Frente_da_escola.png", self.width, self.height),
        ]

        self.characters = [
            Character("./assets/dialog_box/TextNarrador.png", 800, 1000, (50, 100)),
            Character("./assets/dialog_box/TextTeo.png", 800, 1000, (1300, 100)),
            Character("./assets/dialog_box/TextEnzo.png", 800, 1000, (1300, 100)),
            Character("./assets/dialog_box/TextFelix.png", 800, 1000, (1300, 100)),
            Character("./assets/dialog_box/TextStella.png", 800, 1000, (1300, 100)),
            # Add other characters here
        ]

        with open('./roteiro.json', 'r', encoding='utf-8') as arquivo_json:
            self.roteiro = json.load(arquivo_json)

    def show_text(self, text):
        speaker_character = text[0]
        text = text.replace(f"{speaker_character}-", "")

        try:
            speaker_character_index = int(speaker_character)
            background_text = pygame.image.load(self.characters[speaker_character_index].image_path)
            background_text = pygame.transform.scale(background_text, (self.width, 300))

            self.screen.blit(self.scenes[self.current_scene].image, (0, 0))
            render_text = self.font.render(text, True, self.color["white"])

            if self.characters_quantity_cenario == 1:
                self.player_character(self.characters_name_cenario[0], "left")

            if self.characters_quantity_cenario == 2:
                self.player_character(self.characters_name_cenario[0], "left")
                self.player_character(self.characters_name_cenario[1], "right")

            self.screen.blit(background_text, (0, (self.height - 300)))
            self.screen.blit(render_text, (400, (self.height - 175)))

        except ValueError:
            print(f"Invalid speaker character: {speaker_character}")

    def show_options(self, options, text):
        self.show_text(text)
        option_height = 250

        for i, option_text in enumerate(options):
            x, y = 600, 150 + i * option_height
            option = Option(option_text, x, y, 650, 200)

            self.screen.blit(option.background, (x, y))
            render_option = self.font.render(option.text, True, self.color["white"])
            self.screen.blit(render_option, (850, y + 90))

    def player_character(self, character_name, position):
        character = next((char for char in self.characters if char.image_path == f"./assets/characters/{character_name}.png"), None)

        if character:
            x, y = character.position if position == 'right' else (character.position[0] + 250, character.position[1])
            self.screen.blit(character.image, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            row = self.roteiro.get(str(self.index))
            past_row = self.roteiro.get(str(self.index - 1))
            if row is not None:
                if "remove:" in row:
                    self.characters_quantity_cenario = 0
                    self.index += 1
                    continue
                if "ignore:" in row:
                    row_ignored_until = self.roteiro.get(str(self.index))
                    ignore_until = row_ignored_until.split(":")
                    self.index = int(ignore_until[1])
                    continue
                if "characters:" in row:
                    self.characters_quantity_cenario = int(row[11])
                    if self.characters_quantity_cenario > 0:
                        self.characters_name_cenario = row[13:].split("-")
                    self.index += 1
                    continue
                if "change_cenario" in row:
                    split_row = str(row).split(":")
                    if int(split_row[1]) != 100:
                        self.current_scene = int(split_row[1])
                    self.index += 1
                    continue
                else:
                    if isinstance(row, list):
                        self.screen.blit(self.scenes[self.current_scene].image, (0, 0))
                        self.show_options(row, past_row)
                        pygame.display.flip()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_position = pygame.mouse.get_pos()
                            for i, action in enumerate(row):
                                render_option = self.font.render(action, True, self.color["white"])
                                rect_option = render_option.get_rect(topleft=(850, 240 + i * 250))
                                if rect_option.collidepoint(mouse_position):
                                    self.index += (i + 1)
                                    if "skip:" in self.roteiro.get(str(self.index)):
                                        row_skiped = self.roteiro.get(str(self.index))
                                        skip_number = row_skiped.split(":")
                                        self.index = int(skip_number[1])

                    else:
                        self.show_text(row)
                        pygame.display.flip()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.pausado:
                    self.pausado = False

                if self.aswnserText is not None:
                    self.aswnserText = None
                    continue
                self.index += 1

    def run(self):
        self.index = 1
        while self.running:
            self.handle_events()
            self.clock.tick(60)
        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = KittyFightClub()
    game.run()
