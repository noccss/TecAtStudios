import pygame
import json

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Roteiro de Diálogos")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

# Carregar o arquivo JSON
with open('roteiro.json', 'r') as arquivo_json:
    roteiro = json.load(arquivo_json)

# Função para exibir o texto na tela
def exibir_texto(texto):
    tela.fill(branco)
    texto_renderizado = fonte.render(texto, True, preto)
    tela.blit(texto_renderizado, (100, 100))
    pygame.display.flip()

# Função para exibir as falas e ações
def exibir_roteiro(roteiro):
    indice = 1
    continuar = True
    while continuar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                continuar = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                print("Aqui")
                linha = roteiro.get(str(indice))
                if linha is not None:
                    if isinstance(linha, list):
                        # Executar ações especiais
                        for acao in linha:
                            print(f"Ação especial: {acao}")
                    else:
                        # Exibir fala na tela
                        exibir_texto(f"Fala do personagem: {linha}")
                    indice += 1

# Executar a função para exibir o roteiro
exibir_roteiro(roteiro)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

pygame.quit()
