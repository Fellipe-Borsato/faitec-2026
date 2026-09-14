import pygame

from interface.ui.componentes import texto
from interface.ui.casas.card_casa import desenhar_card_casa

from interface.config.cores import (
    FUNDO_2,
    CINZA,
    AMARELO
)

from interface.config.fontes import (
    FONTE_CATEGORIA,
    FONTE_PEQUENA,
    FONTE_MUITO_PEQUENA
)

def desenhar_casas(
    janela,
    painel_central,
    categorias,
    tabela_jogador,
    casa_selecionada
):

    texto(
        janela,
        "CASAS",
        FONTE_CATEGORIA,
        AMARELO,
        painel_central.x + 20,
        painel_central.y + 18
    )

    texto(
        janela,
        "Preencha a tabela usando as dicas",
        FONTE_PEQUENA,
        CINZA,
        painel_central.x + 20,
        painel_central.y + 42
    )

    total_campos = (
        5 * len(categorias)
    )

    preenchidos = 0

    for casa in tabela_jogador:

        for valor in casa:

            if valor is not None:

                preenchidos += 1

    if total_campos > 0:

        percentual = (
            preenchidos
            / total_campos
        )

    else:

        percentual = 0

    progresso_x = (
        painel_central.right - 190
    )

    progresso_y = (
        painel_central.y + 25
    )

    texto(
        janela,
        f"PROGRESSO  {int(percentual * 100)}%",
        FONTE_MUITO_PEQUENA,
        CINZA,
        progresso_x,
        progresso_y
    )

    pygame.draw.rect(
        janela,
        FUNDO_2,
        (
            progresso_x,
            progresso_y + 19,
            150,
            5
        ),
        border_radius=3
    )

    pygame.draw.rect(
        janela,
        AMARELO,
        (
            progresso_x,
            progresso_y + 19,
            int(150 * percentual),
            5
        ),
        border_radius=3
    )

    area_x = painel_central.x + 20
    area_y = painel_central.y + 88

    area_largura = (
        painel_central.width - 40
    )

    area_altura = (
        painel_central.height - 105
    )

    colunas = 3
    linhas = 2

    espacamento_x = 12
    espacamento_y = 12

    largura_card = (
        area_largura
        - espacamento_x * (colunas - 1)
    ) // colunas

    altura_card = (
        area_altura
        - espacamento_y * (linhas - 1)
    ) // linhas

    for i in range(5):

        linha = i // colunas
        coluna = i % colunas

        x = (
            area_x
            + coluna * (
                largura_card
                + espacamento_x
            )
        )

        y = (
            area_y
            + linha * (
                altura_card
                + espacamento_y
            )
        )

        rect = pygame.Rect(
            x,
            y,
            largura_card,
            altura_card
        )

        desenhar_card_casa(
            janela,
            rect,
            i + 1,
            i == casa_selecionada,
            categorias,
            tabela_jogador
        )

def obter_rect_casas(
    painel_central
):

    area_x = (
        painel_central.x + 20
    )

    area_y = (
        painel_central.y + 88
    )

    area_largura = (
        painel_central.width - 40
    )

    area_altura = (
        painel_central.height - 105
    )

    colunas = 3
    linhas = 2

    espacamento_x = 12
    espacamento_y = 12

    largura_card = (
        area_largura
        - espacamento_x * (
            colunas - 1
        )
    ) // colunas

    altura_card = (
        area_altura
        - espacamento_y * (
            linhas - 1
        )
    ) // linhas

    rects = []

    for i in range(5):

        linha = i // colunas
        coluna = i % colunas

        x = (
            area_x
            + coluna * (
                largura_card
                + espacamento_x
            )
        )

        y = (
            area_y
            + linha * (
                altura_card
                + espacamento_y
            )
        )

        rects.append(
            pygame.Rect(
                x,
                y,
                largura_card,
                altura_card
            )
        )

    return rects