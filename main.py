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
        self.font = pygame.font.Font("./PixeloidSans.ttf", 28)
        self.running = True
        self.pausado = False  # Variável de estado de pausa
        self.current_scene = 0  # Índice do cenário atual
        self.newText = 0
        self.aswnserText = None
        self.scenes = [
            pygame.transform.scale(pygame.image.load("corredor.png"), (self.width, self.height)),
            pygame.transform.scale(pygame.image.load("sala_de_aula.png"), (self.width, self.height)),
        ]
        self.character = [
            "TextNarrador.png", # 0
            "TextTeo.png", # 1
            "TextFelix.png", # 2
            "TextRafa.png", # 3
            "TextEnzo.png", # 4
            "TextStella.png" # 5
        ]
        with open ('roteiro.json', 'r', encoding='utf-8') as arquivo_json:
            self.roteiro = json.load(arquivo_json)

    def show_text(self, text):
        speaker_character = text[0]
        text = text.replace(f"{speaker_character}-", "")
        background_text = pygame.image.load(self.character[int(speaker_character)])
        background_text = pygame.transform.scale(background_text, (self.width, 300))
        self.screen.blit(self.scenes[self.current_scene], (0, 0))
        render_text = self.font.render(text, True, self.color["white"])
        self.screen.blit(background_text, (0, (self.height - 300)))
        self.screen.blit(render_text, (400,  (self.height - 175)))

    def show_options(self, options, text):
        self.show_text(text)
        for i, option in enumerate(options):
            background_text = pygame.image.load("options.png")
            background_text = pygame.transform.scale(background_text, (650, 200))
            self.screen.blit(background_text, (600, 150 + i * 250))
            render_option = self.font.render(option, True, self.color["white"])
            self.screen.blit(render_option, (850, 240 + i * 250))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.aswnserText is not None:
                row = self.roteiro.get(str(self.aswnserText))
                row = row.replace("aswnser:", "")
            else:
                row = self.roteiro.get(str(self.index))
            past_row = self.roteiro.get(str(self.index - 1))
            if row is not None:
                if "change_cenario" in row:
                    splitRow = str(row).split(":")
                    self.current_scene = int(splitRow[1])
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
                                    self.aswnserText = self.index
                                if "aswnser" in self.roteiro.get(str(self.index)):
                                    self.index += 1
                    else:
                        self.show_text(f"{row}")
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
