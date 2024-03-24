import pygame
import random
from pygame.locals import *

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (220, 20, 60)
verde = (0, 255, 0)
amarelo = (255, 255, 0)
azul = (30, 144, 255)

# Tamanho da tela e da grade
largura_tela = 600
altura_tela = 600
tamanho_grade = 20

# Moviento
cima = 0
direita = 1
baixo = 2
esquerda = 3


def em_posicao_aleatoria():
    x = random.randint(0, largura_tela // tamanho_grade - 1) * tamanho_grade
    y = random.randint(0, altura_tela // tamanho_grade - 1) * tamanho_grade
    return (x, y)


def colisao(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


def desenhar_grade(tela):
    for x in range(0, largura_tela, tamanho_grade):
        pygame.draw.line(tela, preto, (x, 0), (x, altura_tela))
    for y in range(0, altura_tela, tamanho_grade):
        pygame.draw.line(tela, preto, (0, y), (largura_tela, y))


def jogo():
    pygame.init()
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption('Joguinho da Cobrinha')

    cobra = [(200, 200), (210, 200), (220, 200)]
    cobra_corpo = pygame.Surface((tamanho_grade, tamanho_grade))
    cobra_corpo.fill(verde)

    maca_pos = em_posicao_aleatoria()
    maca = pygame.Surface((tamanho_grade, tamanho_grade))
    pygame.draw.circle(maca, vermelho, (tamanho_grade // 2, tamanho_grade // 2), tamanho_grade // 2)

    direcao_atual = esquerda

    velocidade_cobra = pygame.time.Clock()

    fonte = pygame.font.Font('freesansbold.ttf', 18)
    pontuacao = 0

    fim_jogo = False
    while not fim_jogo:
        velocidade_cobra.tick(10)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()

            if evento.type == KEYDOWN:
                if evento.key == K_w or evento.key == K_UP and direcao_atual != baixo:
                    direcao_atual = cima
                if evento.key == K_s or evento.key == K_DOWN and direcao_atual != cima:
                    direcao_atual = baixo
                if evento.key == K_a or evento.key == K_LEFT and direcao_atual != direita:
                    direcao_atual = esquerda
                if evento.key == K_d or evento.key == K_RIGHT and direcao_atual != esquerda:
                    direcao_atual = direita

        if colisao(cobra[0], maca_pos):
            maca_pos = em_posicao_aleatoria()
            cobra.append((0, 0))
            pontuacao += 1

        # Colisão
        if (cobra[0][0] >= largura_tela or cobra[0][1] >= altura_tela or
                cobra[0][0] < 0 or cobra[0][1] < 0):
            fim_jogo = True
            break

        # Colisão dela mesma
        for i in range(1, len(cobra) - 1):
            if cobra[0][0] == cobra[i][0] and cobra[0][1] == cobra[i][1]:
                fim_jogo = True
                break

        if fim_jogo:
            break

        for i in range(len(cobra) - 1, 0, -1):
            cobra[i] = (cobra[i - 1][0], cobra[i - 1][1])

        # Movimentação
        if direcao_atual == cima:
            cobra[0] = (cobra[0][0], cobra[0][1] - tamanho_grade)
        if direcao_atual == baixo:
            cobra[0] = (cobra[0][0], cobra[0][1] + tamanho_grade)
        if direcao_atual == direita:
            cobra[0] = (cobra[0][0] + tamanho_grade, cobra[0][1])
        if direcao_atual == esquerda:
            cobra[0] = (cobra[0][0] - tamanho_grade, cobra[0][1])

        tela.fill(azul)  # Fundo
        desenhar_grade(tela)
        tela.blit(maca, maca_pos)

        pontuacao_fonte = fonte.render('Pontuação: %s' % (pontuacao), True, amarelo)
        pontuacao_retangulo = pontuacao_fonte.get_rect()
        pontuacao_retangulo.topleft = (largura_tela - 120, 10)
        tela.blit(pontuacao_fonte, pontuacao_retangulo)

        for pos in cobra:
            tela.blit(cobra_corpo, pos)

        pygame.display.update()

    while True:
        fim_jogo_fonte = pygame.font.Font('freesansbold.ttf', 75)
        fim_jogo_tela = fim_jogo_fonte.render('Fim de Jogo', True, branco)
        fim_jogo_retangulo = fim_jogo_tela.get_rect()
        fim_jogo_retangulo.midtop = (largura_tela // 2, 10)
        tela.blit(fim_jogo_tela, fim_jogo_retangulo)

        pygame.display.update()
        pygame.time.wait(500)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()


if __name__ == '__main__':
    jogo()
