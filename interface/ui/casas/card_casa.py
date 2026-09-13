import pygame

from interface.ui.componentes import texto

from interface.config.cores import (
    FUNDO_2,
    PAINEL,
    PAINEL_3,
    BORDA,
    BORDA_CLARA,
    BRANCO,
    CINZA,
    CINZA_ESCURO,
    AMARELO
)

from interface.config.fontes import (
    FONTE_CATEGORIA,
    FONTE_MUITO_PEQUENA,
    FONTE_CASA
)

def desenhar_card_casa(
    janela,
    rect,
    numero,
    selecionado,
    categorias,
    tabela_jogador
):

    if selecionado:

        cor = (52, 48, 38)
        borda = AMARELO

    else:

        cor = PAINEL
        borda = BORDA

    pygame.draw.rect(
        janela,
        cor,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        janela,
        borda,
        rect,
        2 if selecionado else 1,
        border_radius=10
    )

    texto(
        janela,
        f"{numero:02d}",
        FONTE_CASA,
        AMARELO
        if selecionado
        else BRANCO,
        rect.x + 18,
        rect.y + 15
    )

    texto(
        janela,
        f"CASA {numero}",
        FONTE_CATEGORIA,
        BRANCO,
        rect.x + 65,
        rect.y + 18
    )

    pygame.draw.circle(
        janela,
        AMARELO
        if selecionado
        else CINZA_ESCURO,
        (
            rect.right - 20,
            rect.y + 25
        ),
        5
    )

    pygame.draw.line(
        janela,
        borda,
        (
            rect.x + 15,
            rect.y + 70
        ),
        (
            rect.right - 15,
            rect.y + 70
        ),
        1
    )

    altura_linha = 29

    for i, categoria in enumerate(
        categorias
    ):

        if i >= 5:
            break

        y = rect.y + 82 + (
            i * altura_linha
        )

        valor = tabela_jogador[
            numero - 1
        ][i]

        texto(
            janela,
            categoria.upper(),
            FONTE_MUITO_PEQUENA,
            CINZA,
            rect.x + 16,
            y
        )

        valor_rect = pygame.Rect(
            rect.right - 95,
            y - 4,
            78,
            21
        )

        pygame.draw.rect(
            janela,
            FUNDO_2
            if valor is None
            else PAINEL_3,
            valor_rect,
            border_radius=4
        )

        pygame.draw.rect(
            janela,
            BORDA
            if valor is None
            else (
                AMARELO
                if selecionado
                else BORDA_CLARA
            ),
            valor_rect,
            1,
            border_radius=4
        )

        texto(
            janela,
            "?"
            if valor is None
            else valor,
            FONTE_MUITO_PEQUENA,
            CINZA_ESCURO
            if valor is None
            else BRANCO,
            valor_rect.centerx,
            valor_rect.centery,
            True
        )