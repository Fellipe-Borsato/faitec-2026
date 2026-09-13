import pygame

from interface.config.cores import (
    PAINEL,
    PAINEL_2,
    BORDA,
    CINZA,
    BRANCO,
    AMARELO,
    AMARELO_CLARO
)

from interface.config.fontes import FONTE_NORMAL


def texto(
    surface,
    mensagem,
    fonte,
    cor,
    x,
    y,
    centralizado=False
):

    render = fonte.render(
        str(mensagem),
        True,
        cor
    )

    if centralizado:

        rect = render.get_rect(
            center=(x, y)
        )

    else:

        rect = render.get_rect(
            topleft=(x, y)
        )

    surface.blit(
        render,
        rect
    )

    return rect

def painel(
    surface,
    rect,
    cor=PAINEL,
    borda=BORDA,
    raio=10
):

    pygame.draw.rect(
        surface,
        cor,
        rect,
        border_radius=raio
    )

    pygame.draw.rect(
        surface,
        borda,
        rect,
        1,
        border_radius=raio
    )

def botao(
    surface,
    rect,
    mensagem,
    mouse_pos,
    ativo=False
):

    hover = rect.collidepoint(mouse_pos)

    if ativo:

        cor = (65, 59, 43)
        borda = AMARELO
        cor_texto = AMARELO_CLARO

    elif hover:

        cor = PAINEL_2
        borda = CINZA
        cor_texto = BRANCO

    else:

        cor = PAINEL
        borda = BORDA
        cor_texto = CINZA

    pygame.draw.rect(
        surface,
        cor,
        rect,
        border_radius=7
    )

    pygame.draw.rect(
        surface,
        borda,
        rect,
        1,
        border_radius=7
    )

    texto(
        surface,
        mensagem,
        FONTE_NORMAL,
        cor_texto,
        rect.centerx,
        rect.centery,
        True
    )

    return hover

def quebrar_texto(
    mensagem,
    fonte,
    largura_max
):

    palavras = mensagem.split()

    linhas = []

    linha_atual = ""

    for palavra in palavras:

        teste = (
            palavra
            if not linha_atual
            else linha_atual + " " + palavra
        )

        largura = fonte.size(teste)[0]

        if largura <= largura_max:

            linha_atual = teste

        else:

            if linha_atual:
                linhas.append(
                    linha_atual
                )

            linha_atual = palavra

    if linha_atual:
        linhas.append(
            linha_atual
        )

    return linhas
