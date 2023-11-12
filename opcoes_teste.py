import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Seleção de Opções")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

def selecionar_opcao(opcoes):
    selecionado = None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()
                for i, opcao in enumerate(opcoes):
                    opcao_renderizada = fonte.render(opcao, True, preto)
                    opcao_rect = opcao_renderizada.get_rect(topleft=(100, 100 + i * 50))
                    if opcao_rect.collidepoint(posicao_mouse):
                        selecionado = opcao

        tela.fill(branco)

        for i, opcao in enumerate(opcoes):
            opcao_renderizada = fonte.render(opcao, True, preto)
            tela.blit(opcao_renderizada, (100, 100 + i * 50))

        pygame.display.flip()

        if selecionado:
            return selecionado

if __name__ == "__main__":
    opcoes = ["Opção 1", "Opção 2", "Opção 3", "Opção 4"]

    opcao_selecionada = selecionar_opcao(opcoes)

    print("Opção selecionada:", opcao_selecionada)

    pygame.quit()
    sys.exit()