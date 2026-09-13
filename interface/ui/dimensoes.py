import pygame


TOPO = 82
RODAPE = 62

MARGEM = 20
ESPACO = 14


def criar_dimensoes(LARGURA, ALTURA):

    ALTURA_PAINEL = (
        ALTURA
        - TOPO
        - RODAPE
        - 30
    )

    LARGURA_ESQUERDO = int(
        LARGURA * 0.23
    )

    LARGURA_DIREITO = int(
        LARGURA * 0.21
    )

    LARGURA_CENTRAL = (
        LARGURA
        - (MARGEM * 2)
        - (ESPACO * 2)
        - LARGURA_ESQUERDO
        - LARGURA_DIREITO
    )

    PAINEL_ESQUERDO = pygame.Rect(
        MARGEM,
        TOPO + 15,
        LARGURA_ESQUERDO,
        ALTURA_PAINEL
    )

    PAINEL_CENTRAL = pygame.Rect(
        PAINEL_ESQUERDO.right + ESPACO,
        TOPO + 15,
        LARGURA_CENTRAL,
        ALTURA_PAINEL
    )

    PAINEL_DIREITO = pygame.Rect(
        PAINEL_CENTRAL.right + ESPACO,
        TOPO + 15,
        LARGURA_DIREITO,
        ALTURA_PAINEL
    )

    BOTAO_MINIMIZAR = pygame.Rect(
        LARGURA - 95,
        22,
        30,
        30
    )

    BOTAO_FECHAR = pygame.Rect(
        LARGURA - 55,
        22,
        30,
        30
    )

    return {
        "painel_esquerdo": PAINEL_ESQUERDO,
        "painel_central": PAINEL_CENTRAL,
        "painel_direito": PAINEL_DIREITO,
        "botao_minimizar": BOTAO_MINIMIZAR,
        "botao_fechar": BOTAO_FECHAR,
    }