import sys
import os
import pygame

# Permite importar zebra.py que está na pasta acima
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zebra import zebra


# ============================================================
# CONFIGURAÇÕES
# ============================================================

pygame.init()

LARGURA, ALTURA = 1280, 720

janela = pygame.display.set_mode(
    (LARGURA, ALTURA),
    pygame.FULLSCREEN
)

pygame.display.set_caption("Einstein - O Enigma")

clock = pygame.time.Clock()


# ============================================================
# CORES
# ============================================================

FUNDO = (14, 16, 20)
FUNDO_2 = (20, 23, 29)

PAINEL = (25, 28, 35)
PAINEL_2 = (31, 35, 43)

BORDA = (55, 61, 72)

BRANCO = (235, 238, 243)
CINZA = (145, 151, 162)
CINZA_ESCURO = (85, 91, 103)

AMARELO = (225, 174, 70)
AMARELO_CLARO = (255, 205, 100)

VERDE = (75, 190, 125)
VERMELHO = (210, 75, 75)

PRETO = (8, 9, 12)


# ============================================================
# FONTES
# ============================================================

def carregar_fonte(tamanho, negrito=False):
    caminho = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "fonte",
        "Roboto-Regular.ttf"
    )

    if os.path.exists(caminho):
        fonte = pygame.font.Font(caminho, tamanho)
        fonte.set_bold(negrito)
        return fonte

    return pygame.font.SysFont("Arial", tamanho, bold=negrito)


FONTE_TITULO = carregar_fonte(34, True)
FONTE_SUBTITULO = carregar_fonte(18)
FONTE_CATEGORIA = carregar_fonte(15, True)
FONTE_NORMAL = carregar_fonte(15)
FONTE_PEQUENA = carregar_fonte(13)
FONTE_CASA = carregar_fonte(20, True)
FONTE_GRANDE = carregar_fonte(26, True)


# ============================================================
# FUNÇÕES VISUAIS
# ============================================================

def texto(surface, mensagem, fonte, cor, x, y, centralizado=False):
    render = fonte.render(str(mensagem), True, cor)

    if centralizado:
        rect = render.get_rect(center=(x, y))
    else:
        rect = render.get_rect(topleft=(x, y))

    surface.blit(render, rect)

    return rect


def painel(surface, rect, cor=PAINEL, borda=BORDA, raio=10):
    pygame.draw.rect(surface, cor, rect, border_radius=raio)
    pygame.draw.rect(surface, borda, rect, 1, border_radius=raio)


def botao(surface, rect, mensagem, mouse_pos, ativo=False):
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

    pygame.draw.rect(surface, cor, rect, border_radius=7)
    pygame.draw.rect(surface, borda, rect, 1, border_radius=7)

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


# ============================================================
# GERADOR DO ENIGMA
# ============================================================

gerador = zebra()
chave = gerador.geraChave()

puzzle = zebra(chave)

categorias = puzzle.buscaCategorias(
    mostraValores=True,
    mostraTodas=False
)

dicas = puzzle.geraDicas()

resposta = puzzle.pegaResposta()


# ============================================================
# PREPARAÇÃO DAS CATEGORIAS
# ============================================================

# buscaCategorias() retorna os nomes das categorias selecionadas
#
# Para cada categoria, buscamos os seus valores.

dados_categorias = {}

for categoria in categorias:

    # Descobre o código da categoria através da chave
    codigo = None

    for i in range(1, 10):
        nome = puzzle.buscaCategoria(str(i))

        if nome.upper() == categoria.upper():
            codigo = str(i)
            break

    if codigo is not None:
        dados_categorias[categoria] = puzzle.buscaValores(
            codigo,
            mostraValores=True
        )


# ============================================================
# ESTADO DA INTERFACE
# ============================================================

rodando = True

casa_selecionada = 0

categoria_selecionada = 0

dica_selecionada = 0

pagina_dicas = 0


# ============================================================
# DIMENSÕES
# ============================================================

TOPO = 78
RODAPE = 58

PAINEL_ESQUERDO = pygame.Rect(
    20,
    TOPO + 15,
    300,
    ALTURA - TOPO - RODAPE - 30
)

PAINEL_CENTRAL = pygame.Rect(
    335,
    TOPO + 15,
    615,
    ALTURA - TOPO - RODAPE - 30
)

PAINEL_DIREITO = pygame.Rect(
    965,
    TOPO + 15,
    295,
    ALTURA - TOPO - RODAPE - 30
)


# ============================================================
# DESENHO DO CABEÇALHO
# ============================================================

def desenhar_cabecalho():

    pygame.draw.rect(
        janela,
        FUNDO_2,
        (0, 0, LARGURA, TOPO)
    )

    pygame.draw.line(
        janela,
        BORDA,
        (20, TOPO),
        (LARGURA - 20, TOPO),
        1
    )

    texto(
        janela,
        "EINSTEIN",
        FONTE_TITULO,
        BRANCO,
        25,
        18
    )

    texto(
        janela,
        "O ENIGMA",
        FONTE_SUBTITULO,
        AMARELO,
        27,
        52
    )

    # Caso
    texto(
        janela,
        "CASO #001",
        FONTE_CATEGORIA,
        CINZA,
        LARGURA - 220,
        18
    )

    texto(
        janela,
        "INVESTIGAÇÃO",
        FONTE_NORMAL,
        BRANCO,
        LARGURA - 220,
        40
    )

    # Indicador
    pygame.draw.circle(
        janela,
        VERDE,
        (LARGURA - 35, 30),
        6
    )


# ============================================================
# DESENHO DAS DICAS
# ============================================================

def desenhar_dicas():

    painel(janela, PAINEL_ESQUERDO)

    texto(
        janela,
        "EVIDÊNCIAS",
        FONTE_CATEGORIA,
        AMARELO,
        PAINEL_ESQUERDO.x + 18,
        PAINEL_ESQUERDO.y + 16
    )

    texto(
        janela,
        f"{len(dicas)} pistas encontradas",
        FONTE_PEQUENA,
        CINZA,
        PAINEL_ESQUERDO.x + 18,
        PAINEL_ESQUERDO.y + 40
    )

    inicio_y = PAINEL_ESQUERDO.y + 72

    altura_card = 54
    espacamento = 8

    limite = 9

    inicio = pagina_dicas * limite
    fim = min(inicio + limite, len(dicas))

    for indice in range(inicio, fim):

        y = inicio_y + (indice - inicio) * (
            altura_card + espacamento
        )

        rect = pygame.Rect(
            PAINEL_ESQUERDO.x + 15,
            y,
            PAINEL_ESQUERDO.width - 30,
            altura_card
        )

        selecionada = indice == dica_selecionada

        painel(
            janela,
            rect,
            PAINEL_2 if selecionada else PAINEL,
            AMARELO if selecionada else BORDA,
            7
        )

        numero = f"{indice + 1:02d}"

        texto(
            janela,
            numero,
            FONTE_CATEGORIA,
            AMARELO if selecionada else CINZA,
            rect.x + 12,
            rect.y + 9
        )

        # Quebra simples da dica
        dica = dicas[indice]

        if len(dica) > 39:
            linha1 = dica[:39]
            linha2 = dica[39:78]

            texto(
                janela,
                linha1,
                FONTE_PEQUENA,
                BRANCO,
                rect.x + 45,
                rect.y + 7
            )

            texto(
                janela,
                linha2,
                FONTE_PEQUENA,
                BRANCO,
                rect.x + 45,
                rect.y + 25
            )

        else:

            texto(
                janela,
                dica,
                FONTE_PEQUENA,
                BRANCO,
                rect.x + 45,
                rect.y + 18
            )

    # Navegação
    total_paginas = max(1, (len(dicas) + limite - 1) // limite)

    texto(
        janela,
        f"{pagina_dicas + 1} / {total_paginas}",
        FONTE_PEQUENA,
        CINZA,
        PAINEL_ESQUERDO.centerx,
        PAINEL_ESQUERDO.bottom - 25,
        True
    )


# ============================================================
# DESENHO DAS CASAS
# ============================================================

def desenhar_casa(rect, numero, selecionada):

    if selecionada:
        cor = (52, 48, 38)
        borda = AMARELO
    else:
        cor = PAINEL
        borda = BORDA

    # Casa
    pygame.draw.rect(
        janela,
        cor,
        rect,
        border_radius=8
    )

    pygame.draw.rect(
        janela,
        borda,
        rect,
        2 if selecionada else 1,
        border_radius=8
    )

    # Telhado
    topo = [
        (rect.centerx, rect.y - 16),
        (rect.x + 12, rect.y + 12),
        (rect.right - 12, rect.y + 12)
    ]

    pygame.draw.polygon(
        janela,
        borda,
        topo
    )

    pygame.draw.polygon(
        janela,
        FUNDO,
        [
            (rect.centerx, rect.y - 10),
            (rect.x + 18, rect.y + 10),
            (rect.right - 18, rect.y + 10)
        ]
    )

    # Número
    texto(
        janela,
        f"{numero}",
        FONTE_CASA,
        AMARELO if selecionada else BRANCO,
        rect.centerx,
        rect.y + 34,
        True
    )

    # Porta
    porta = pygame.Rect(
        rect.centerx - 12,
        rect.bottom - 45,
        24,
        40
    )

    pygame.draw.rect(
        janela,
        FUNDO_2,
        porta,
        border_radius=3
    )

    # Janelas
    for lado in [-1, 1]:

        cx = rect.centerx + lado * 43
        cy = rect.bottom - 33

        pygame.draw.rect(
            janela,
            FUNDO_2,
            (cx - 9, cy - 9, 18, 18),
            border_radius=2
        )


def desenhar_casas():

    texto(
        janela,
        "CENÁRIO DA INVESTIGAÇÃO",
        FONTE_CATEGORIA,
        AMARELO,
        PAINEL_CENTRAL.x + 20,
        PAINEL_CENTRAL.y + 18
    )

    texto(
        janela,
        "Selecione uma casa para investigar",
        FONTE_PEQUENA,
        CINZA,
        PAINEL_CENTRAL.x + 20,
        PAINEL_CENTRAL.y + 42
    )

    largura = 103
    altura = 155
    espacamento = 12

    total_largura = (
        largura * 5 +
        espacamento * 4
    )

    inicio_x = (
        PAINEL_CENTRAL.centerx -
        total_largura // 2
    )

    y = PAINEL_CENTRAL.y + 115

    for i in range(5):

        x = inicio_x + i * (
            largura + espacamento
        )

        rect = pygame.Rect(
            x,
            y,
            largura,
            altura
        )

        desenhar_casa(
            rect,
            i + 1,
            i == casa_selecionada
        )


# ============================================================
# DESENHO DO PAINEL DIREITO
# ============================================================

def desenhar_investigacao():

    painel(janela, PAINEL_DIREITO)

    texto(
        janela,
        "SUA INVESTIGAÇÃO",
        FONTE_CATEGORIA,
        AMARELO,
        PAINEL_DIREITO.x + 18,
        PAINEL_DIREITO.y + 18
    )

    texto(
        janela,
        f"CASA {casa_selecionada + 1}",
        FONTE_GRANDE,
        BRANCO,
        PAINEL_DIREITO.x + 18,
        PAINEL_DIREITO.y + 46
    )

    texto(
        janela,
        "Categorias disponíveis",
        FONTE_PEQUENA,
        CINZA,
        PAINEL_DIREITO.x + 18,
        PAINEL_DIREITO.y + 82
    )

    inicio_y = PAINEL_DIREITO.y + 110

    altura = 40

    for i, categoria in enumerate(categorias):

        y = inicio_y + i * (altura + 7)

        rect = pygame.Rect(
            PAINEL_DIREITO.x + 15,
            y,
            PAINEL_DIREITO.width - 30,
            altura
        )

        selecionada = i == categoria_selecionada

        painel(
            janela,
            rect,
            PAINEL_2 if selecionada else PAINEL,
            AMARELO if selecionada else BORDA,
            6
        )

        texto(
            janela,
            categoria.upper(),
            FONTE_PEQUENA,
            AMARELO if selecionada else BRANCO,
            rect.x + 12,
            rect.centery,
            False
        )


# ============================================================
# RODAPÉ
# ============================================================

def desenhar_rodape(mouse_pos):

    y = ALTURA - RODAPE

    pygame.draw.line(
        janela,
        BORDA,
        (20, y),
        (LARGURA - 20, y),
        1
    )

    # Botão evidências
    botao(
        janela,
        pygame.Rect(25, y + 12, 150, 34),
        "EVIDÊNCIAS",
        mouse_pos
    )

    # Botão verificar
    botao(
        janela,
        pygame.Rect(
            LARGURA - 245,
            y + 8,
            220,
            42
        ),
        "VERIFICAR SOLUÇÃO",
        mouse_pos,
        True
    )

    texto(
        janela,
        "ESC  •  SAIR",
        FONTE_PEQUENA,
        CINZA,
        195,
        y + 22
    )


# ============================================================
# CLIQUE NAS CASAS
# ============================================================

def obter_rect_casas():

    largura = 103
    altura = 155
    espacamento = 12

    total_largura = (
        largura * 5 +
        espacamento * 4
    )

    inicio_x = (
        PAINEL_CENTRAL.centerx -
        total_largura // 2
    )

    y = PAINEL_CENTRAL.y + 115

    rects = []

    for i in range(5):

        x = inicio_x + i * (
            largura + espacamento
        )

        rects.append(
            pygame.Rect(
                x,
                y,
                largura,
                altura
            )
        )

    return rects


# ============================================================
# CLIQUE NAS DICAS
# ============================================================

def obter_rect_dicas():

    inicio_y = PAINEL_ESQUERDO.y + 72

    altura_card = 54
    espacamento = 8

    limite = 9

    inicio = pagina_dicas * limite
    fim = min(
        inicio + limite,
        len(dicas)
    )

    rects = []

    for indice in range(inicio, fim):

        y = inicio_y + (
            indice - inicio
        ) * (
            altura_card + espacamento
        )

        rects.append(
            (
                indice,
                pygame.Rect(
                    PAINEL_ESQUERDO.x + 15,
                    y,
                    PAINEL_ESQUERDO.width - 30,
                    altura_card
                )
            )
        )

    return rects


# ============================================================
# LOOP PRINCIPAL
# ============================================================

while rodando:

    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():

        # ----------------------------------------------------
        # SAIR
        # ----------------------------------------------------

        if evento.type == pygame.QUIT:
            rodando = False

        # ----------------------------------------------------
        # TECLAS
        # ----------------------------------------------------

        elif evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:
                rodando = False

            # F11 alterna fullscreen
            elif evento.key == pygame.K_F11:

                pygame.display.toggle_fullscreen()

        # ----------------------------------------------------
        # CLIQUE
        # ----------------------------------------------------

        elif evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1:

                # -----------------------------
                # CASA
                # -----------------------------

                for i, rect in enumerate(
                    obter_rect_casas()
                ):

                    if rect.collidepoint(
                        evento.pos
                    ):

                        casa_selecionada = i

                # -----------------------------
                # DICA
                # -----------------------------

                for indice, rect in obter_rect_dicas():

                    if rect.collidepoint(
                        evento.pos
                    ):

                        dica_selecionada = indice

                # -----------------------------
                # CATEGORIA
                # -----------------------------

                inicio_y = PAINEL_DIREITO.y + 110

                for i in range(len(categorias)):

                    rect = pygame.Rect(
                        PAINEL_DIREITO.x + 15,
                        inicio_y + i * 47,
                        PAINEL_DIREITO.width - 30,
                        40
                    )

                    if rect.collidepoint(
                        evento.pos
                    ):

                        categoria_selecionada = i

                # -----------------------------
                # VERIFICAR
                # -----------------------------

                botao_verificar = pygame.Rect(
                    LARGURA - 245,
                    ALTURA - RODAPE + 8,
                    220,
                    42
                )

                if botao_verificar.collidepoint(
                    evento.pos
                ):

                    print("\n============================")
                    print("SOLUÇÃO DO ENIGMA")
                    print("============================")
                    print(resposta)

    # ========================================================
    # DESENHO
    # ========================================================

    janela.fill(FUNDO)

    desenhar_cabecalho()

    desenhar_dicas()

    painel(
        janela,
        PAINEL_CENTRAL
    )

    desenhar_casas()

    desenhar_investigacao()

    desenhar_rodape(mouse_pos)

    pygame.display.flip()

    clock.tick(60)


pygame.quit()