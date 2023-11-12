import pygame
import sys
import time

class VisualNovelGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 1920
        self.screen_height = 1080
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Visual Novel Game")
        self.clock = pygame.time.Clock()
        self.colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "purple": (128, 0, 128),
            "dark_green": (0, 128, 0),
            "dark_blue": (0, 0, 128)
        }
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.current_state = "intro"
        self.choice = None
        self.text_index = 0
        self.dialog_timer = None
        self.option_text_displayed = True
        self.scene_change_timer = None
        self.current_scene = 0  # Índice do cenário atual
        self.scenes = [
            pygame.transform.scale(pygame.image.load("corredor.png"), (self.screen_width, self.screen_height)),
            pygame.transform.scale(pygame.image.load("sala_de_aula.png"), (self.screen_width, self.screen_height)),
        ]

        self.intro_text = "Téo andava pelo corredor"
        self.npc_text = [
            "Olha é ele de novo, aquele gato com a cara esquisita.",
            "Cara?! Aquilo parece mais um prato do que uma cara (Risadas)",
            "É sério que ele não se toca que aqueles óculos o deixam mais esquisito do que já é?",
            "Para cara, ele tá olhando para cá! (Risadas)"
        ]
        self.player_dialog = {
            "REAGIR": "Téo – Acho melhor não, da última vez ganhei uma fatura nova no cartão e um óculos novo.",
            "NÃO REAGIR": "Téo – Ué, dessa vez ficaram somente na ofensa? Devo estar com uma sorte tremenda hoje mesmo."
        }

        self.narrator_text = ""

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.current_state == "choice" and self.option_text_displayed:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.choice = "REAGIR"
                        self.option_text_displayed = False
                    elif event.key == pygame.K_2:
                        self.choice = "NÃO REAGIR"
                        self.option_text_displayed = False
                # Verifique os eventos do mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Obtém a posição do mouse
                        mouse_pos = pygame.mouse.get_pos()
                        option1_rect = self.font.render("1: REAGIR", True, self.colors["dark_green"]).get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
                        option2_rect = self.font.render("2: NÃO REAGIR", True, self.colors["dark_green"]).get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 30))
                        if option1_rect.collidepoint(mouse_pos):
                            self.choice = "REAGIR"
                            self.option_text_displayed = False
                        elif option2_rect.collidepoint(mouse_pos):
                            self.choice = "NÃO REAGIR"
                            self.option_text_displayed = False

    def update(self):
        if self.current_state == "intro":
            if not self.dialog_timer:
                self.dialog_timer = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.dialog_timer >= 2000:
                self.dialog_timer = None
                self.current_state = "dialog"

        if self.current_state == "dialog":
            if self.text_index < len(self.npc_text):
                if not self.dialog_timer:
                    self.dialog_timer = pygame.time.get_ticks()
                if pygame.time.get_ticks() - self.dialog_timer >= 2000:
                    self.text_index += 1
                    self.dialog_timer = None
            else:
                self.current_state = "choice"

        if self.current_state == "choice" and not self.option_text_displayed:
            if self.choice:
                if self.choice == "REAGIR":
                    self.scene_change_timer = time.time()  # Registra o tempo atual
                    self.option_text_displayed = True
                elif self.choice == "NÃO REAGIR":
                    self.scene_change_timer = time.time()  # Registra o tempo atual
                    self.option_text_displayed = True

                self.text_index = 0  # Limpa o texto

        if self.scene_change_timer and not self.option_text_displayed:
            if time.time() - self.scene_change_timer >= 2:  # Espere por 2 segundos
                self.current_scene = 1  # Altere para o índice do cenário "sala_de_aula"
                self.scene_change_timer = None
                self.option_text_displayed = True
                self.narrator_text = "Já dentro da sala de aula. Téo se direcionou imediatamente a sua mesa, mas no meio de seu caminho ele acaba de trombar com um armar... colega seu."

    def draw(self):
        # Desenhe o cenário
        self.screen.blit(self.scenes[self.current_scene], (0, 0))

        if self.current_state == "intro":
            intro_text_surface = self.font.render(self.intro_text, True, self.colors["white"])
            intro_text_rect = intro_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 70))
            self.screen.blit(intro_text_surface, intro_text_rect)

        elif self.current_state == "dialog":
            if self.text_index < len(self.npc_text):
                npc_text_surface = self.font.render(self.npc_text[self.text_index], True, self.colors["purple"])
                npc_text_rect = npc_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 140))
                self.screen.blit(npc_text_surface, npc_text_rect)

        elif self.current_state == "choice":
            if self.option_text_displayed:
                option1_text_surface = self.font.render("1: REAGIR", True, self.colors["dark_green"])
                option1_text_rect = option1_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
                self.screen.blit(option1_text_surface, option1_text_rect)

                option2_text_surface = self.font.render("2: NÃO REAGIR", True, self.colors["dark_green"])
                option2_text_rect = option2_text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 30))
                self.screen.blit(option2_text_surface, option2_text_rect)

            if self.narrator_text:
                narrator_surface = self.font.render(self.narrator_text, True, self.colors["black"])
                narrator_rect = narrator_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 220))
                self.screen.blit(narrator_surface, narrator_rect)

            if self.choice:
                player_dialog_surface = self.font.render(self.player_dialog[self.choice], True, self.colors["dark_blue"])
                player_dialog_rect = player_dialog_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 220))
                self.screen.blit(player_dialog_surface, player_dialog_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = VisualNovelGame()
    game.run()