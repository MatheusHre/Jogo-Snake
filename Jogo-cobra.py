import pygame
import random

# Configurações
largura_tela = 800
altura_tela = 600
tamanho_bloco = 20
fps = 10 # Velocidade da cobra 

rodando = True
game_over = False

# Inicialização da cobra
cobra = [(100, 100)]
direcao = (tamanho_bloco, 0)

# Comida
comida = (
    random.randrange(0, largura_tela, tamanho_bloco),
    random.randrange(0, altura_tela, tamanho_bloco)
)

def reiniciar_jogo():
    global cobra, direcao, comida, game_over

    cobra = [(100, 100)]
    direcao = (tamanho_bloco, 0)
    comida = (
        random.randrange(0, largura_tela, tamanho_bloco),
        random.randrange(0, altura_tela, tamanho_bloco)
    )
    game_over = False

def mostrar_game_over(tela):
    fonte = pygame.font.SysFont(None, 50)

    texto1 = fonte.render("GAME OVER", True, (255, 0, 0))
    texto2 = fonte.render("Pressione qualquer tecla para reiniciar", True, (255, 255, 255))

    rect1 = texto1.get_rect(center=(largura_tela // 2, altura_tela // 2 - 30))
    rect2 = texto2.get_rect(center=(largura_tela // 2, altura_tela // 2 + 30))

    tela.blit(texto1, rect1)
    tela.blit(texto2, rect2)

def proc_eventos():
    global rodando, direcao, game_over

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if game_over:
                reiniciar_jogo()
                return

            if evento.key == pygame.K_UP and direcao != (0, tamanho_bloco):
                direcao = (0, -tamanho_bloco)

            elif evento.key == pygame.K_DOWN and direcao != (0, -tamanho_bloco):
                direcao = (0, tamanho_bloco)

            elif evento.key == pygame.K_LEFT and direcao != (tamanho_bloco, 0):
                direcao = (-tamanho_bloco, 0)

            elif evento.key == pygame.K_RIGHT and direcao != (-tamanho_bloco, 0):
                direcao = (tamanho_bloco, 0)

def mover_cobra():
    global comida, game_over

    if game_over:
        return

    cabeca = cobra[0]
    nova_cabeca = (cabeca[0] + direcao[0], cabeca[1] + direcao[1])

    # Colisão com parede
    if (nova_cabeca[0] < 0 or nova_cabeca[0] >= largura_tela or
        nova_cabeca[1] < 0 or nova_cabeca[1] >= altura_tela):
        game_over = True
        return

    # Colisão com o próprio corpo
    if nova_cabeca in cobra:
        game_over = True
        return

    cobra.insert(0, nova_cabeca)

    # Comer comida
    if nova_cabeca == comida:
        comida = (
            random.randrange(0, largura_tela, tamanho_bloco),
            random.randrange(0, altura_tela, tamanho_bloco)
        )
    else:
        cobra.pop()

def desenhar(tela):
    tela.fill("#5593AE")

    # Cobra
    for parte in cobra:
        pygame.draw.rect(tela, "#00FF00", (parte[0], parte[1], tamanho_bloco, tamanho_bloco))

    # Comida
    pygame.draw.rect(tela, "#FF0000", (comida[0], comida[1], tamanho_bloco, tamanho_bloco))

    if game_over:
        mostrar_game_over(tela)

    pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Jogo da Cobrinha 🐍")

    relogio = pygame.time.Clock()

    while rodando:
        proc_eventos()
        mover_cobra()
        desenhar(tela)
        relogio.tick(fps)

    pygame.quit()