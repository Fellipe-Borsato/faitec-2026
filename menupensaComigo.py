import pygame
import sys
import os
import subprocess
import random

from interface.config.cores import (
    FUNDO,
    FUNDO_2,
    PAINEL,
    PAINEL_2,
    PAINEL_3,
    BORDA,
    BORDA_CLARA,
    BRANCO,
    CINZA,
    CINZA_ESCURO,
    AMARELO,
    AMARELO_CLARO,
    PRETO,
)

from interface.config.fontes import (
    FONTE_TITULO,
    FONTE_SUBTITULO,
    FONTE_CATEGORIA,
    FONTE_NORMAL,
    FONTE_PEQUENA,
)



pygame.init()

info_tela = pygame.display.Info()
LARGURA = info_tela.current_w
ALTURA = info_tela.current_h

tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("PENSE COMIGO")

clock = pygame.time.Clock()


fonte_titulo = FONTE_TITULO
fonte_subtitulo = FONTE_SUBTITULO
fonte_botao = FONTE_CATEGORIA
fonte_pequena = FONTE_PEQUENA
fonte_seed = FONTE_NORMAL
fonte_interrogacao = FONTE_CATEGORIA


def desenhar_texto(texto, fonte, cor, x, y, centralizado=True):
    superficie = fonte.render(texto, True, cor)

    if centralizado:
        rect = superficie.get_rect(center=(x, y))
    else:
        rect = superficie.get_rect(topleft=(x, y))

    tela.blit(superficie, rect)


def desenhar_botao(rect, texto, mouse_pos, destaque=False):
    passou_mouse = rect.collidepoint(mouse_pos)

    if destaque:
        cor_fundo = AMARELO_CLARO if passou_mouse else AMARELO
        cor_texto = PRETO
        cor_borda = AMARELO_CLARO if passou_mouse else AMARELO
    else:
        cor_fundo = PAINEL_2 if not passou_mouse else PAINEL_3
        cor_texto = BRANCO if not passou_mouse else BRANCO
        cor_borda = BORDA_CLARA if passou_mouse else BORDA

    pygame.draw.rect(
        tela,
        cor_fundo,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        tela,
        cor_borda,
        rect,
        width=2,
        border_radius=12
    )

    desenhar_texto(
        texto,
        fonte_botao,
        cor_texto,
        rect.centerx,
        rect.centery
    )


def abrir_jogo(seed=None):
    """
    Abre o 'penseComigo.py'.

    Se houver seed, envia a seed para o jogo.
    """

    pasta = os.path.dirname(os.path.abspath(__file__))
    arquivo_jogo = os.path.join(pasta, "penseComigo.py")
    interpretador = sys.executable

    if seed is None:
        subprocess.Popen(
            [interpretador, arquivo_jogo],
            cwd=pasta
        )
    else:
        subprocess.Popen(
            [interpretador, arquivo_jogo, str(seed)],
            cwd=pasta
        )

    pygame.quit()
    sys.exit()


def desenhar_ajuda():
    largura = 540
    altura = 260

    x = (LARGURA - largura) // 2
    y = (ALTURA - altura) // 2

    sombra = pygame.Rect(x + 10, y + 10, largura, altura)
    painel = pygame.Rect(x, y, largura, altura)

    pygame.draw.rect(
        tela,
        PRETO,
        sombra,
        border_radius=16
    )

    pygame.draw.rect(
        tela,
        PAINEL,
        painel,
        border_radius=16
    )

    pygame.draw.rect(
        tela,
        BORDA_CLARA,
        painel,
        width=2,
        border_radius=16
    )

    desenhar_texto(
        "COMO JOGAR",
        fonte_botao,
        BRANCO,
        LARGURA // 2,
        y + 42
    )

    for indice, linha in enumerate([
        "Resolva o quebra-cabeça usando a lógica.",
        "Use as pistas para descobrir a posição correta.",
        "Acerte todas as posições para vencer."
    ]):
        desenhar_texto(
            linha,
            fonte_pequena,
            CINZA,
            LARGURA // 2,
            y + 95 + indice * 30
        )

    desenhar_texto(
        "Passe o mouse no '?' para fechar.",
        fonte_pequena,
        AMARELO_CLARO,
        LARGURA // 2,
        y + 210
    )


def menu_principal():

    largura_painel = int(LARGURA * 0.50)
    altura_painel = int(ALTURA * 0.48)
    painel_menu = pygame.Rect(
        (LARGURA - largura_painel) // 2,
        (ALTURA - altura_painel) // 2,
        largura_painel,
        altura_painel
    )
    botao_jogar = pygame.Rect(
        (LARGURA - int(LARGURA * 0.38)) // 2,
        int(ALTURA * 0.45),
        int(LARGURA * 0.38),
        int(ALTURA * 0.08)
    )
    botao_sair = pygame.Rect(
        (LARGURA - int(LARGURA * 0.38)) // 2,
        int(ALTURA * 0.56),
        int(LARGURA * 0.38),
        int(ALTURA * 0.08)
    )
    botao_ajuda = pygame.Rect(
        LARGURA - 90,
        ALTURA - 90,
        50,
        50
    )

    while True:

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    if botao_jogar.collidepoint(mouse_pos):
                        menu_jogar()

                    if botao_sair.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        tela.fill(FUNDO)

        pygame.draw.rect(
            tela,
            FUNDO_2,
            (0, 0, LARGURA, 10)
        )

        pygame.draw.rect(
            tela,
            PAINEL,
            painel_menu,
            border_radius=16
        )

        pygame.draw.rect(
            tela,
            BORDA,
            painel_menu,
            width=2,
            border_radius=16
        )

        desenhar_texto(
            "PENSE COMIGO",
            fonte_titulo,
            BRANCO,
            LARGURA // 2,
            int(ALTURA * 0.31)
        )

        desenhar_texto(
            "DESAFIE SUA LÓGICA",
            fonte_subtitulo,
            CINZA,
            LARGURA // 2,
            int(ALTURA * 0.38)
        )

        desenhar_botao(
            botao_jogar,
            "JOGAR",
            mouse_pos,
            destaque=True
        )

        desenhar_botao(
            botao_sair,
            "SAIR",
            mouse_pos
        )

        mouse_na_ajuda = botao_ajuda.collidepoint(mouse_pos)

        pygame.draw.rect(
            tela,
            PAINEL_2 if not mouse_na_ajuda else PAINEL_3,
            botao_ajuda,
            border_radius=12
        )

        pygame.draw.rect(
            tela,
            BORDA_CLARA if mouse_na_ajuda else BORDA,
            botao_ajuda,
            width=2,
            border_radius=12
        )

        desenhar_texto(
            "?",
            fonte_interrogacao,
            BRANCO,
            botao_ajuda.centerx,
            botao_ajuda.centery
        )

        if mouse_na_ajuda:
            desenhar_ajuda()

        pygame.display.flip()
        clock.tick(60)


def menu_jogar():

    largura_painel = int(LARGURA * 0.56)
    altura_painel = int(ALTURA * 0.66)
    painel_menu = pygame.Rect(
        (LARGURA - largura_painel) // 2,
        (ALTURA - altura_painel) // 2,
        largura_painel,
        altura_painel
    )
    botao_classico = pygame.Rect(
        (LARGURA - int(LARGURA * 0.40)) // 2,
        int(ALTURA * 0.28),
        int(LARGURA * 0.40),
        int(ALTURA * 0.08)
    )
    botao_aleatorio = pygame.Rect(
        (LARGURA - int(LARGURA * 0.40)) // 2,
        int(ALTURA * 0.39),
        int(LARGURA * 0.40),
        int(ALTURA * 0.08)
    )
    botao_seed = pygame.Rect(
        (LARGURA - int(LARGURA * 0.40)) // 2,
        int(ALTURA * 0.50),
        int(LARGURA * 0.40),
        int(ALTURA * 0.08)
    )
    botao_voltar = pygame.Rect(
        (LARGURA - int(LARGURA * 0.40)) // 2,
        int(ALTURA * 0.61),
        int(LARGURA * 0.40),
        int(ALTURA * 0.08)
    )

    while True:

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    if botao_aleatorio.collidepoint(mouse_pos):
                        seed = random.randint(100000, 999999)
                        abrir_jogo(seed)

                    if botao_seed.collidepoint(mouse_pos):
                        menu_seed()

                    if botao_voltar.collidepoint(mouse_pos):
                        return

        tela.fill(FUNDO)

        pygame.draw.rect(
            tela,
            FUNDO_2,
            (0, 0, LARGURA, 10)
        )

        pygame.draw.rect(
            tela,
            PAINEL,
            painel_menu,
            border_radius=16
        )

        pygame.draw.rect(
            tela,
            BORDA,
            painel_menu,
            width=2,
            border_radius=16
        )

        desenhar_texto(
            "JOGAR",
            fonte_titulo,
            BRANCO,
            LARGURA // 2,
            int(ALTURA * 0.22)
        )

        desenhar_botao(
            botao_classico,
            "CLÁSSICO",
            mouse_pos
        )

        desenhar_botao(
            botao_aleatorio,
            "ALEATÓRIO",
            mouse_pos,
            destaque=True
        )

        desenhar_botao(
            botao_seed,
            "INFORMAR SEED",
            mouse_pos
        )

        desenhar_botao(
            botao_voltar,
            "VOLTAR",
            mouse_pos
        )

        pygame.display.flip()
        clock.tick(60)


def menu_seed():

    seed_texto = ""
    largura_painel = int(LARGURA * 0.60)
    altura_painel = int(ALTURA * 0.55)
    painel_menu = pygame.Rect(
        (LARGURA - largura_painel) // 2,
        (ALTURA - altura_painel) // 2,
        largura_painel,
        altura_painel
    )
    botao_confirmar = pygame.Rect(
        int(LARGURA * 0.31),
        int(ALTURA * 0.58),
        int(LARGURA * 0.17),
        int(ALTURA * 0.08)
    )
    botao_voltar = pygame.Rect(
        int(LARGURA * 0.52),
        int(ALTURA * 0.58),
        int(LARGURA * 0.17),
        int(ALTURA * 0.08)
    )
    campo_seed = pygame.Rect(
        (LARGURA - int(LARGURA * 0.40)) // 2,
        int(ALTURA * 0.44),
        int(LARGURA * 0.40),
        int(ALTURA * 0.08)
    )

    pygame.key.start_text_input()

    while True:

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.key.stop_text_input()
                pygame.quit()
                sys.exit()

            if evento.type == pygame.TEXTINPUT:
                somente_numeros = ""

                for caractere in evento.text:
                    if caractere.isdigit():
                        somente_numeros += caractere

                if len(seed_texto) + len(somente_numeros) <= 9:
                    seed_texto += somente_numeros

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_BACKSPACE:
                    seed_texto = seed_texto[:-1]

                elif evento.key == pygame.K_RETURN:
                    if seed_texto:
                        pygame.key.stop_text_input()
                        seed = int(seed_texto)
                        abrir_jogo(seed)

                elif evento.key == pygame.K_ESCAPE:
                    pygame.key.stop_text_input()
                    return

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    if botao_confirmar.collidepoint(mouse_pos):
                        if seed_texto:
                            pygame.key.stop_text_input()
                            seed = int(seed_texto)
                            abrir_jogo(seed)

                    if botao_voltar.collidepoint(mouse_pos):
                        pygame.key.stop_text_input()
                        return

        tela.fill(FUNDO)

        pygame.draw.rect(
            tela,
            FUNDO_2,
            (0, 0, LARGURA, 10)
        )

        pygame.draw.rect(
            tela,
            PAINEL,
            painel_menu,
            border_radius=16
        )

        pygame.draw.rect(
            tela,
            BORDA,
            painel_menu,
            width=2,
            border_radius=16
        )

        desenhar_texto(
            "INFORMAR SEED",
            fonte_titulo,
            BRANCO,
            LARGURA // 2,
            int(ALTURA * 0.22)
        )

        desenhar_texto(
            "Digite uma seed numérica:",
            fonte_pequena,
            CINZA,
            LARGURA // 2,
            int(ALTURA * 0.34)
        )

        pygame.draw.rect(
            tela,
            PAINEL_2,
            campo_seed,
            border_radius=10
        )

        pygame.draw.rect(
            tela,
            AMARELO if seed_texto else BORDA,
            campo_seed,
            width=2,
            border_radius=10
        )

        texto_mostrado = seed_texto if seed_texto else "Digite a seed..."
        cor_texto = BRANCO if seed_texto else CINZA_ESCURO

        desenhar_texto(
            texto_mostrado,
            fonte_seed,
            cor_texto,
            campo_seed.centerx,
            campo_seed.centery
        )

        desenhar_botao(
            botao_confirmar,
            "CONFIRMAR",
            mouse_pos,
            destaque=True
        )

        desenhar_botao(
            botao_voltar,
            "VOLTAR",
            mouse_pos
        )

        pygame.display.flip()
        clock.tick(60)

menu_principal()
