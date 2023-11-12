import pygame
import sys
import json

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
        self.pausado = False  # Variável de estado de pausa
        self.current_scene = 0  # Índice do cenário atual
        self.newText = 0
        self.aswnserText = None
        self.characters_quantity_cenario = 0
        self.characters_name_cenario = []
        self.scenes = [
            pygame.transform.scale(pygame.image.load("./assets/background/corredor.png"), (self.width, self.height)),
            pygame.transform.scale(pygame.image.load("./assets/background/sala_de_aula.png"), (self.width, self.height)),
            pygame.transform.scale(pygame.image.load("./assets/background/Frente_da_escola.png"), (self.width, self.height)),
        ]
        self.character = [
            "./assets/dialog_box/TextNarrador.png", # 0
            "./assets/dialog_box/TextTeo.png", # 1
            "./assets/dialog_box/TextFelix.png", # 2
            "./assets/dialog_box/TextRafa.png", # 3
            "./assets/dialog_box/TextEnzo.png", # 4
            "./assets/dialog_box/TextStella.png" # 5
        ]
        with open ('./roteiro.json', 'r', encoding='utf-8') as arquivo_json:
            self.roteiro = json.load(arquivo_json)

    def show_text(self, text):
        speaker_character = text[0]
        text = text.replace(f"{speaker_character}-", "")
        background_text = pygame.image.load(self.character[int(speaker_character)])
        background_text = pygame.transform.scale(background_text, (self.width, 300))
        self.screen.blit(self.scenes[self.current_scene], (0, 0))
        render_text = self.font.render(text, True, self.color["white"])
        if self.characters_quantity_cenario == 1:
            self.player_character(self.characters_name_cenario[0], "left")
        if self.characters_quantity_cenario == 2:
            self.player_character(self.characters_name_cenario[0], "left")
            self.player_character(self.characters_name_cenario[1], "right")
        self.screen.blit(background_text, (0, (self.height - 300)))
        self.screen.blit(render_text, (400,  (self.height - 175)))

    def show_options(self, options, text):
        self.show_text(text)
        for i, option in enumerate(options):
            background_text = pygame.image.load("./assets/dialog_box/options.png")
            background_text = pygame.transform.scale(background_text, (650, 200))
            self.screen.blit(background_text, (600, 150 + i * 250))
            render_option = self.font.render(option, True, self.color["white"])
            self.screen.blit(render_option, (850, 240 + i * 250))
        
    def player_character(self, character_name, position):
        background_character = pygame.image.load(f"./assets/characters/{character_name}.png")
        background_character = pygame.transform.scale(background_character, (800, 1000))
        if position == 'right':
            self.screen.blit(background_character, (1300, 100))
        else:
            self.screen.blit(background_character, (50, 100))

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
                        self.screen.blit(self.scenes[self.current_scene], (0, 0))
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
                                        print(skip_number[1])
                                        self.index = int(skip_number[1])
                                    # self.index += (i + 1)
                                    # if "characters:" in self.roteiro.get(str(self.index - 1)):
                                    #     character = self.roteiro.get(str(self.index - 1))
                                    #     self.characters_quantity_cenario = int(character[11])
                                    #     self.characters_name_cenario = character[13:].split("-")
                                    #     self.index += 1

                                    # if "characters:" in self.roteiro.get(str(self.index)):
                                    #     character = self.roteiro.get(str(self.index))
                                    #     self.characters_quantity_cenario = int(character[11])
                                    #     self.characters_name_cenario = character[13:].split("-")
                                    #     self.index += (i + 1)
                                    # self.aswnserText = self.index

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
