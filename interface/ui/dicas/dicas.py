import pygame

from interface.ui.componentes import (
    texto,
    painel,
    quebrar_texto
)

from interface.config.cores import (
    PAINEL,
    PAINEL_2,
    BORDA,
    BRANCO,
    CINZA,
    CINZA_ESCURO,
    AMARELO
)

from interface.config.fontes import (
    FONTE_CATEGORIA,
    FONTE_PEQUENA,
    FONTE_NORMAL
)


def obter_limite_dicas(
    painel_esquerdo
):

    altura_card = 54
    espacamento = 8

    return max(
        1,
        int(
            (
                painel_esquerdo.height
                - 125
            )
            /
            (
                altura_card
                + espacamento
            )
        )
    )


def obter_total_paginas_dicas(
    dicas,
    painel_esquerdo
):

    limite = obter_limite_dicas(
        painel_esquerdo
    )

    return max(
        1,
        (
            len(dicas)
            + limite
            - 1
        )
        // limite
    )


def obter_botoes_paginacao(
    painel_esquerdo
):

    botao_anterior = pygame.Rect(
        painel_esquerdo.x + 20,
        painel_esquerdo.bottom - 39,
        32,
        28
    )

    botao_proximo = pygame.Rect(
        painel_esquerdo.right - 52,
        painel_esquerdo.bottom - 39,
        32,
        28
    )

    return (
        botao_anterior,
        botao_proximo
    )


def desenhar_dicas(
    janela,
    painel_esquerdo,
    dicas,
    dica_selecionada,
    pagina_dicas
):

    painel(
        janela,
        painel_esquerdo
    )

    texto(
        janela,
        "DICAS",
        FONTE_CATEGORIA,
        AMARELO,
        painel_esquerdo.x + 18,
        painel_esquerdo.y + 16
    )

    texto(
        janela,
        f"{len(dicas)} pistas encontradas",
        FONTE_PEQUENA,
        CINZA,
        painel_esquerdo.x + 18,
        painel_esquerdo.y + 40
    )

    inicio_y = (
        painel_esquerdo.y + 72
    )

    altura_card = 54
    espacamento = 8

    limite = obter_limite_dicas(
        painel_esquerdo
    )

    inicio = pagina_dicas * limite

    fim = min(
        inicio + limite,
        len(dicas)
    )

    # --------------------------------------------------------
    # DESENHA AS PISTAS
    # --------------------------------------------------------

    for indice in range(
        inicio,
        fim
    ):

        y = (
            inicio_y
            + (
                indice - inicio
            )
            * (
                altura_card
                + espacamento
            )
        )

        rect = pygame.Rect(
            painel_esquerdo.x + 15,
            y,
            painel_esquerdo.width - 30,
            altura_card
        )

        selecionada = (
            indice == dica_selecionada
        )

        painel(
            janela,
            rect,
            PAINEL_2
            if selecionada
            else PAINEL,
            AMARELO
            if selecionada
            else BORDA,
            7
        )

        numero = f"{indice + 1:02d}"

        texto(
            janela,
            numero,
            FONTE_CATEGORIA,
            AMARELO
            if selecionada
            else CINZA,
            rect.x + 12,
            rect.y + 9
        )

        dica = dicas[indice]

        linhas = quebrar_texto(
            dica,
            FONTE_PEQUENA,
            rect.width - 60
        )

        for linha_numero, linha in enumerate(
            linhas[:2]
        ):

            texto(
                janela,
                linha,
                FONTE_PEQUENA,
                BRANCO,
                rect.x + 45,
                rect.y + 7 + (
                    linha_numero * 18
                )
            )

    # --------------------------------------------------------
    # PAGINAÇÃO
    # --------------------------------------------------------

    total_paginas = (
        obter_total_paginas_dicas(
            dicas,
            painel_esquerdo
        )
    )

    botao_anterior, botao_proximo = (
        obter_botoes_paginacao(
            painel_esquerdo
        )
    )

    texto(
        janela,
        f"{pagina_dicas + 1} / {total_paginas}",
        FONTE_PEQUENA,
        CINZA,
        painel_esquerdo.centerx,
        painel_esquerdo.bottom - 22,
        True
    )

    # --------------------------------------------------------
    # BOTÃO ANTERIOR
    # --------------------------------------------------------

    hover_anterior = (
        botao_anterior.collidepoint(
            pygame.mouse.get_pos()
        )
    )

    pygame.draw.rect(
        janela,
        PAINEL_2
        if hover_anterior and pagina_dicas > 0
        else PAINEL,
        botao_anterior,
        border_radius=5
    )

    pygame.draw.rect(
        janela,
        BORDA,
        botao_anterior,
        1,
        border_radius=5
    )

    texto(
        janela,
        "‹",
        FONTE_NORMAL,
        BRANCO
        if pagina_dicas > 0
        else CINZA_ESCURO,
        botao_anterior.centerx,
        botao_anterior.centery - 1,
        True
    )

    # --------------------------------------------------------
    # BOTÃO PRÓXIMO
    # --------------------------------------------------------

    hover_proximo = (
        botao_proximo.collidepoint(
            pygame.mouse.get_pos()
        )
    )

    pygame.draw.rect(
        janela,
        PAINEL_2
        if (
            hover_proximo
            and pagina_dicas < total_paginas - 1
        )
        else PAINEL,
        botao_proximo,
        border_radius=5
    )

    pygame.draw.rect(
        janela,
        BORDA,
        botao_proximo,
        1,
        border_radius=5
    )

    texto(
        janela,
        "›",
        FONTE_NORMAL,
        BRANCO
        if pagina_dicas < total_paginas - 1
        else CINZA_ESCURO,
        botao_proximo.centerx,
        botao_proximo.centery - 1,
        True
    )


def obter_rect_dicas(
    painel_esquerdo,
    dicas,
    pagina_dicas
):

    inicio_y = (
        painel_esquerdo.y + 72
    )

    altura_card = 54
    espacamento = 8

    limite = obter_limite_dicas(
        painel_esquerdo
    )

    inicio = pagina_dicas * limite

    fim = min(
        inicio + limite,
        len(dicas)
    )

    rects = []

    for indice in range(
        inicio,
        fim
    ):

        y = (
            inicio_y
            + (
                indice - inicio
            )
            * (
                altura_card
                + espacamento
            )
        )

        rects.append(
            (
                indice,
                pygame.Rect(
                    painel_esquerdo.x + 15,
                    y,
                    painel_esquerdo.width - 30,
                    altura_card
                )
            )
        )

    return rects