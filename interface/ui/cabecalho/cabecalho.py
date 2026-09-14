import pygame

from interface.ui.componentes import texto

from interface.config.cores import (
    FUNDO_2,
    BORDA,
    PAINEL,
    PAINEL_2,
    BRANCO,
    CINZA,
    AMARELO,
    VERMELHO
)

from interface.config.fontes import (
    FONTE_TITULO,
    FONTE_SUBTITULO,
    FONTE_MUITO_PEQUENA
)

def desenhar_cabecalho(
    janela,
    mouse_pos,
    largura,
    topo,
    botao_minimizar,
    botao_fechar,
    chave_formatada
):

    pygame.draw.rect(
        janela,
        FUNDO_2,
        (0, 0, largura, topo)
    )

    pygame.draw.line(
        janela,
        BORDA,
        (20, topo),
        (largura - 20, topo),
        1
    )

    # LOGO

    texto(
        janela,
        "PENSA",
        FONTE_TITULO,
        BRANCO,
        25,
        18
    )

    texto(
        janela,
        "COMIGO",
        FONTE_SUBTITULO,
        AMARELO,
        27,
        52
    )

    texto(
        janela,
        f"CHAVE: {chave_formatada}",
        FONTE_MUITO_PEQUENA,
        CINZA,
         largura // 2,
        37,
        True
    )

    # MINIMIZAR

    hover_minimizar = (
        botao_minimizar.collidepoint(
            mouse_pos
        )
    )

    pygame.draw.rect(
        janela,
        PAINEL_2 if hover_minimizar else PAINEL,
        botao_minimizar,
        border_radius=5
    )

    pygame.draw.rect(
        janela,
        CINZA if hover_minimizar else BORDA,
        botao_minimizar,
        1,
        border_radius=5
    )

    pygame.draw.line(
        janela,
        BRANCO,
        (
            botao_minimizar.x + 8,
            botao_minimizar.centery
        ),
        (
            botao_minimizar.right - 8,
            botao_minimizar.centery
        ),
        2
    )

    # FECHAR

    hover_fechar = (
        botao_fechar.collidepoint(
            mouse_pos
        )
    )

    pygame.draw.rect(
        janela,
        (70, 35, 38)
        if hover_fechar
        else PAINEL,
        botao_fechar,
        border_radius=5
    )

    pygame.draw.rect(
        janela,
        VERMELHO
        if hover_fechar
        else BORDA,
        botao_fechar,
        1,
        border_radius=5
    )

    pygame.draw.line(
        janela,
        VERMELHO
        if hover_fechar
        else CINZA,
        (
            botao_fechar.x + 8,
            botao_fechar.y + 8
        ),
        (
            botao_fechar.right - 8,
            botao_fechar.bottom - 8
        ),
        2
    )

    pygame.draw.line(
        janela,
        VERMELHO
        if hover_fechar
        else CINZA,
        (
            botao_fechar.right - 8,
            botao_fechar.y + 8
        ),
        (
            botao_fechar.x + 8,
            botao_fechar.bottom - 8
        ),
        2
    )
