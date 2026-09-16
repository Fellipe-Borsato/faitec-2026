import pygame

from interface.ui.componentes import (
    texto,
    painel
)

from interface.config.cores import (
    PAINEL,
    PAINEL_2,
    FUNDO_2,
    BORDA,
    CINZA,
    CINZA_ESCURO,
    BRANCO,
    AMARELO,
    AMARELO_CLARO
)

from interface.config.fontes import (
    FONTE_CATEGORIA,
    FONTE_GRANDE,
    FONTE_PEQUENA,
    FONTE_MUITO_PEQUENA
)


def desenhar_investigacao(
    janela,
    mouse_pos,
    painel_direito,
    categorias,
    dados_categorias,
    tabela_jogador,
    casa_selecionada,
    categoria_selecionada
):

    painel(
        janela,
        painel_direito
    )

    texto(
        janela,
        "PREENCHER CASA",
        FONTE_CATEGORIA,
        AMARELO,
        painel_direito.x + 18,
        painel_direito.y + 18
    )

    texto(
        janela,
        f"CASA {casa_selecionada + 1}",
        FONTE_GRANDE,
        BRANCO,
        painel_direito.x + 18,
        painel_direito.y + 47
    )

    texto(
        janela,
        "Categorias",
        FONTE_PEQUENA,
        CINZA,
        painel_direito.x + 18,
        painel_direito.y + 84
    )

    inicio_y = (
        painel_direito.y + 110
    )

    altura_categoria = 39
    espacamento_categoria = 6

    for i, categoria in enumerate(
        categorias
    ):

        y = (
            inicio_y
            + i * (
                altura_categoria
                + espacamento_categoria
            )
        )

        rect = pygame.Rect(
            painel_direito.x + 15,
            y,
            painel_direito.width - 30,
            altura_categoria
        )

        selecionada = (
            i == categoria_selecionada
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
            6
        )

        render_categoria = FONTE_MUITO_PEQUENA.render(
            categoria.upper(),
            True,
            AMARELO if selecionada else BRANCO
        )
        rect_categoria = render_categoria.get_rect(
            midleft=(rect.x + 12, rect.centery)
        )
        janela.blit(render_categoria, rect_categoria)

        valor_atual = tabela_jogador[
            casa_selecionada
        ][i]

        valor_texto = "?" if valor_atual is None else valor_atual
        cor_valor = CINZA_ESCURO if valor_atual is None else BRANCO
        render_valor = FONTE_MUITO_PEQUENA.render(
            str(valor_texto),
            True,
            cor_valor
        )
        rect_valor = render_valor.get_rect(
            center=(rect.right - 70, rect.centery)
        )
        janela.blit(render_valor, rect_valor)

    categoria_nome = categorias[
        categoria_selecionada
    ]

    valores = dados_categorias.get(
        categoria_nome,
        []
    )

    valores_y = (
        inicio_y
        + len(categorias)
        * (
            altura_categoria
            + espacamento_categoria
        )
        + 18
    )

    texto(
        janela,
        categoria_nome.upper(),
        FONTE_CATEGORIA,
        AMARELO,
        painel_direito.x + 18,
        valores_y
    )

    texto(
        janela,
        "Escolha um valor",
        FONTE_MUITO_PEQUENA,
        CINZA,
        painel_direito.x + 18,
        valores_y + 23
    )

    valor_inicio_y = (
        valores_y + 45
    )

    altura_valor = 34
    espacamento_valor = 6

    for i, valor in enumerate(
        valores
    ):

        y = (
            valor_inicio_y
            + i * (
                altura_valor
                + espacamento_valor
            )
        )

        rect = pygame.Rect(
            painel_direito.x + 15,
            y,
            painel_direito.width - 30,
            altura_valor
        )

        casa_com_valor = None

        for casa in range(5):

            if casa == casa_selecionada:
                continue

            if tabela_jogador[
                casa
            ][categoria_selecionada] == valor:

                casa_com_valor = (
                    casa + 1
                )

                break

        valor_atual = tabela_jogador[
            casa_selecionada
        ][categoria_selecionada]

        selecionado = (
            valor_atual == valor
        )

        ocupado = (
            casa_com_valor is not None
        )

        if selecionado:

            cor = (65, 59, 43)
            borda = AMARELO
            cor_texto = AMARELO_CLARO

        elif ocupado:

            cor = FUNDO_2
            borda = BORDA
            cor_texto = CINZA_ESCURO

        elif rect.collidepoint(mouse_pos):

            cor = PAINEL_2
            borda = CINZA
            cor_texto = BRANCO

        else:

            cor = PAINEL
            borda = BORDA
            cor_texto = BRANCO

        pygame.draw.rect(
            janela,
            cor,
            rect,
            border_radius=6
        )

        pygame.draw.rect(
            janela,
            borda,
            rect,
            1,
            border_radius=6
        )

        render_valor = FONTE_MUITO_PEQUENA.render(
            str(valor),
            True,
            cor_texto
        )
        rect_valor = render_valor.get_rect(
            midleft=(rect.x + 12, rect.centery)
        )
        janela.blit(render_valor, rect_valor)

        if selecionado:

            render_status = FONTE_MUITO_PEQUENA.render(
                "ATIVO",
                True,
                AMARELO
            )
            rect_status = render_status.get_rect(
                center=(rect.right - 32, rect.centery)
            )
            janela.blit(render_status, rect_status)

        elif ocupado:

            texto_status = f"CASA {casa_com_valor}"
            render_status = FONTE_MUITO_PEQUENA.render(
                texto_status,
                True,
                CINZA_ESCURO
            )
            rect_status = render_status.get_rect(
                center=(rect.right - 35, rect.centery)
            )
            janela.blit(render_status, rect_status)


def obter_rect_categorias(
    painel_direito,
    categorias
):

    inicio_y = (
        painel_direito.y + 110
    )

    altura = 39
    espacamento = 6

    rects = []

    for i in range(
        len(categorias)
    ):

        y = (
            inicio_y
            + i * (
                altura
                + espacamento
            )
        )

        rects.append(
            pygame.Rect(
                painel_direito.x + 15,
                y,
                painel_direito.width - 30,
                altura
            )
        )

    return rects


def obter_rect_valores(
    painel_direito,
    categorias,
    dados_categorias,
    categoria_selecionada
):

    categoria_nome = categorias[
        categoria_selecionada
    ]

    valores = dados_categorias.get(
        categoria_nome,
        []
    )

    inicio_y = (
        painel_direito.y + 110
    )

    altura_categoria = 39
    espacamento_categoria = 6

    valores_y = (
        inicio_y
        + len(categorias)
        * (
            altura_categoria
            + espacamento_categoria
        )
        + 18
    )

    valor_inicio_y = (
        valores_y + 45
    )

    altura_valor = 34
    espacamento_valor = 6

    rects = []

    for i, valor in enumerate(
        valores
    ):

        y = (
            valor_inicio_y
            + i * (
                altura_valor
                + espacamento_valor
            )
        )

        rects.append(
            (
                valor,
                pygame.Rect(
                    painel_direito.x + 15,
                    y,
                    painel_direito.width - 30,
                    altura_valor
                )
            )
        )

    return rects