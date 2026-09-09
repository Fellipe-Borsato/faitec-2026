import pygame

pygame.init() #inicia o pygame

janela = pygame.display.set_mode((800, 600)) #define o tamanho da janela
pygame.display.set_caption("Main")#define o nome da janela

rodando = True

while rodando:
    for evento in pygame.event.get():#verifica se o usuário clicou no botão de fechar a janela
        if evento.type == pygame.QUIT:#verifica se o usuário clicou no botão de fechar a janela
            rodando = False

    janela.fill((30, 30, 30))#define a cor de fundo da janela

    pygame.display.flip()#atualiza a tela

pygame.quit()#fecha o pygame