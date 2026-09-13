import os
import pygame

pygame.init()


def carregar_fonte(tamanho, negrito=False):

    caminho = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        ),
        "fonte",
        "Roboto-Regular.ttf"
    )

    if os.path.exists(caminho):

        fonte = pygame.font.Font(
            caminho,
            tamanho
        )

        fonte.set_bold(negrito)

        return fonte

    return pygame.font.SysFont(
        "Arial",
        tamanho,
        bold=negrito
    )


FONTE_TITULO = carregar_fonte(34, True)
FONTE_SUBTITULO = carregar_fonte(18)
FONTE_CATEGORIA = carregar_fonte(15, True)
FONTE_NORMAL = carregar_fonte(15)
FONTE_PEQUENA = carregar_fonte(13)
FONTE_MUITO_PEQUENA = carregar_fonte(11)
FONTE_CASA = carregar_fonte(22, True)
FONTE_GRANDE = carregar_fonte(27, True)