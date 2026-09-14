import pygame

from interface.ui.componentes import (
    texto,
    botao
)

from interface.config.cores import (
    BORDA,
    CINZA
)

from interface.config.fontes import (
    FONTE_PEQUENA,
    FONTE_MUITO_PEQUENA
)


def desenhar_rodape(
    janela,
    mouse_pos,
    largura,
    altura,
    rodape,
    painel_esquerdo,
    mensagem_jogo,
    cor_mensagem
):

    y = altura - rodape

    pygame.draw.line(
        janela,
        BORDA,
        (20, y),
        (largura - 20, y),
        1
    )

    if mensagem_jogo:

        texto(
            janela,
            mensagem_jogo,
            FONTE_MUITO_PEQUENA,
            cor_mensagem,
            largura // 2,
            y + 30,
            True
        )

        texto(
                    janela,
                    "ESC  •  SAIR",
                    FONTE_PEQUENA,
                    CINZA,
                    painel_esquerdo.x + 18,
                    y + 22
                )

    else:

        texto(
            janela,
            "ESC  •  SAIR",
            FONTE_PEQUENA,
            CINZA,
            painel_esquerdo.x + 18,
            y + 22
        )

    botao(
        janela,
        pygame.Rect(
            largura - 270,
            y + 9,
            245,
            42
        ),
        "VERIFICAR SOLUÇÃO",
        mouse_pos,
        True
    )


def obter_rect_verificar(
    largura,
    altura,
    rodape
):

    return pygame.Rect(
        largura - 270,
        altura - rodape + 9,
        245,
        42
    )