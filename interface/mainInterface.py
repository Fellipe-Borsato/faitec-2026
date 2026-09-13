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

print("PYGAME INICIOU")

info = pygame.display.Info()

LARGURA = info.current_w
ALTURA = info.current_h

janela = pygame.display.set_mode(
    (LARGURA, ALTURA),
    pygame.NOFRAME
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
PAINEL_3 = (37, 41, 49)

BORDA = (55, 61, 72)
BORDA_CLARA = (72, 79, 92)

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


# ============================================================
# FUNÇÕES VISUAIS
# ============================================================

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


def quebrar_texto(mensagem, fonte, largura_max):

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
                linhas.append(linha_atual)

            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    return linhas


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

dados_categorias = {}

for categoria in categorias:

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

TOPO = 82
RODAPE = 62

MARGEM = 20
ESPACO = 14

ALTURA_PAINEL = ALTURA - TOPO - RODAPE - 30


# ------------------------------------------------------------
# LARGURA DOS PAINÉIS
# ------------------------------------------------------------

# Aproximadamente:
# 23% esquerda
# 52% centro
# restante direita

LARGURA_ESQUERDO = int(LARGURA * 0.23)
LARGURA_DIREITO = int(LARGURA * 0.21)

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


# ============================================================
# BOTÕES DA JANELA
# ============================================================

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


# ============================================================
# DESENHO DO CABEÇALHO
# ============================================================

def desenhar_cabecalho(mouse_pos):

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

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    x_status = LARGURA - 190

    texto(
        janela,
        "CASO #001",
        FONTE_CATEGORIA,
        CINZA,
        x_status,
        15
    )

    texto(
        janela,
        "INVESTIGAÇÃO",
        FONTE_NORMAL,
        BRANCO,
        x_status,
        39
    )

    pygame.draw.circle(
        janela,
        VERDE,
        (LARGURA - 115, 39),
        6
    )

    # --------------------------------------------------------
    # BOTÃO MINIMIZAR
    # --------------------------------------------------------

    hover_minimizar = BOTAO_MINIMIZAR.collidepoint(
        mouse_pos
    )

    pygame.draw.rect(
        janela,
        PAINEL_2 if hover_minimizar else PAINEL,
        BOTAO_MINIMIZAR,
        border_radius=5
    )

    pygame.draw.rect(
        janela,
        CINZA if hover_minimizar else BORDA,
        BOTAO_MINIMIZAR,
        1,
        border_radius=5
    )

    pygame.draw.line(
        janela,
        BRANCO,
        (
            BOTAO_MINIMIZAR.x + 8,
            BOTAO_MINIMIZAR.centery
        ),
        (
            BOTAO_MINIMIZAR.right - 8,
            BOTAO_MINIMIZAR.centery
        ),
        2
    )

    # --------------------------------------------------------
    # BOTÃO FECHAR
    # --------------------------------------------------------

    hover_fechar = BOTAO_FECHAR.collidepoint(
        mouse_pos
    )

    pygame.draw.rect(
        janela,
        (70, 35, 38) if hover_fechar else PAINEL,
        BOTAO_FECHAR,
        border_radius=5
    )

    pygame.draw.rect(
        janela,
        VERMELHO if hover_fechar else BORDA,
        BOTAO_FECHAR,
        1,
        border_radius=5
    )

    pygame.draw.line(
        janela,
        VERMELHO if hover_fechar else CINZA,
        (
            BOTAO_FECHAR.x + 8,
            BOTAO_FECHAR.y + 8
        ),
        (
            BOTAO_FECHAR.right - 8,
            BOTAO_FECHAR.bottom - 8
        ),
        2
    )

    pygame.draw.line(
        janela,
        VERMELHO if hover_fechar else CINZA,
        (
            BOTAO_FECHAR.right - 8,
            BOTAO_FECHAR.y + 8
        ),
        (
            BOTAO_FECHAR.x + 8,
            BOTAO_FECHAR.bottom - 8
        ),
        2
    )


# ============================================================
# DESENHO DAS DICAS
# ============================================================

def desenhar_dicas():

    painel(
        janela,
        PAINEL_ESQUERDO
    )

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

    limite = max(
        1,
        int(
            (
                PAINEL_ESQUERDO.height - 125
            )
            /
            (altura_card + espacamento)
        )
    )

    inicio = pagina_dicas * limite

    fim = min(
        inicio + limite,
        len(dicas)
    )

    for indice in range(inicio, fim):

        y = inicio_y + (
            indice - inicio
        ) * (
            altura_card + espacamento
        )

        rect = pygame.Rect(
            PAINEL_ESQUERDO.x + 15,
            y,
            PAINEL_ESQUERDO.width - 30,
            altura_card
        )

        selecionada = (
            indice == dica_selecionada
        )

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
                rect.y + 7 + linha_numero * 18
            )

    # --------------------------------------------------------
    # PAGINAÇÃO
    # --------------------------------------------------------

    total_paginas = max(
        1,
        (
            len(dicas) + limite - 1
        ) // limite
    )

    texto(
        janela,
        f"{pagina_dicas + 1} / {total_paginas}",
        FONTE_PEQUENA,
        CINZA,
        PAINEL_ESQUERDO.centerx,
        PAINEL_ESQUERDO.bottom - 22,
        True
    )


# ============================================================
# CARD DE INVESTIGAÇÃO
# ============================================================

def desenhar_card_investigacao(
    rect,
    numero,
    selecionado
):

    if selecionado:

        cor = (52, 48, 38)
        borda = AMARELO

    else:

        cor = PAINEL
        borda = BORDA

    # --------------------------------------------------------
    # CARD
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # NÚMERO
    # --------------------------------------------------------

    texto(
        janela,
        f"{numero:02d}",
        FONTE_CASA,
        AMARELO if selecionado else BRANCO,
        rect.x + 18,
        rect.y + 15
    )

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    texto(
        janela,
        f"CASA {numero}",
        FONTE_CATEGORIA,
        BRANCO,
        rect.x + 65,
        rect.y + 18
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if selecionado:

        pygame.draw.circle(
            janela,
            AMARELO,
            (
                rect.right - 20,
                rect.y + 24
            ),
            5
        )

        texto(
            janela,
            "SELECIONADA",
            FONTE_MUITO_PEQUENA,
            AMARELO,
            rect.x + 65,
            rect.y + 39
        )

    else:

        pygame.draw.circle(
            janela,
            CINZA_ESCURO,
            (
                rect.right - 20,
                rect.y + 24
            ),
            5
        )

        texto(
            janela,
            "AGUARDANDO INVESTIGAÇÃO",
            FONTE_MUITO_PEQUENA,
            CINZA,
            rect.x + 65,
            rect.y + 39
        )

    # --------------------------------------------------------
    # LINHA
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CATEGORIAS
    # --------------------------------------------------------

    altura_linha = 29

    for i, categoria in enumerate(
        categorias
    ):

        if i >= 5:
            break

        y = rect.y + 82 + (
            i * altura_linha
        )

        # Nome da categoria
        texto(
            janela,
            categoria.upper(),
            FONTE_MUITO_PEQUENA,
            CINZA,
            rect.x + 16,
            y
        )

        # Valor ainda desconhecido
        valor_rect = pygame.Rect(
            rect.right - 72,
            y - 3,
            55,
            20
        )

        pygame.draw.rect(
            janela,
            FUNDO_2,
            valor_rect,
            border_radius=4
        )

        pygame.draw.rect(
            janela,
            BORDA,
            valor_rect,
            1,
            border_radius=4
        )

        texto(
            janela,
            "?",
            FONTE_MUITO_PEQUENA,
            CINZA_ESCURO,
            valor_rect.centerx,
            valor_rect.centery,
            True
        )


# ============================================================
# DESENHO DAS CASAS / INVESTIGAÇÃO
# ============================================================

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
        "Selecione uma posição para investigar",
        FONTE_PEQUENA,
        CINZA,
        PAINEL_CENTRAL.x + 20,
        PAINEL_CENTRAL.y + 42
    )

    # --------------------------------------------------------
    # PROGRESSO
    # --------------------------------------------------------

    progresso_x = PAINEL_CENTRAL.right - 190
    progresso_y = PAINEL_CENTRAL.y + 25

    texto(
        janela,
        "PROGRESSO",
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
            30,
            5
        ),
        border_radius=3
    )

    # --------------------------------------------------------
    # CARDS
    # --------------------------------------------------------

    area_x = PAINEL_CENTRAL.x + 20
    area_y = PAINEL_CENTRAL.y + 88

    area_largura = (
        PAINEL_CENTRAL.width - 40
    )

    area_altura = (
        PAINEL_CENTRAL.height - 105
    )

    # 3 cards em cima
    # 2 cards embaixo

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

        x = area_x + coluna * (
            largura_card + espacamento_x
        )

        y = area_y + linha * (
            altura_card + espacamento_y
        )

        rect = pygame.Rect(
            x,
            y,
            largura_card,
            altura_card
        )

        desenhar_card_investigacao(
            rect,
            i + 1,
            i == casa_selecionada
        )


# ============================================================
# PAINEL DIREITO
# ============================================================

def desenhar_investigacao():

    painel(
        janela,
        PAINEL_DIREITO
    )

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
        PAINEL_DIREITO.y + 47
    )

    texto(
        janela,
        "Selecione uma categoria",
        FONTE_PEQUENA,
        CINZA,
        PAINEL_DIREITO.x + 18,
        PAINEL_DIREITO.y + 84
    )

    # --------------------------------------------------------
    # CATEGORIAS
    # --------------------------------------------------------

    inicio_y = PAINEL_DIREITO.y + 112

    altura = 43
    espacamento = 7

    for i, categoria in enumerate(
        categorias
    ):

        y = inicio_y + i * (
            altura + espacamento
        )

        rect = pygame.Rect(
            PAINEL_DIREITO.x + 15,
            y,
            PAINEL_DIREITO.width - 30,
            altura
        )

        selecionada = (
            i == categoria_selecionada
        )

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
            rect.y + 8
        )

        # Valor selecionado
        texto(
            janela,
            "?",
            FONTE_PEQUENA,
            CINZA_ESCURO,
            rect.right - 28,
            rect.centery,
            True
        )

    # --------------------------------------------------------
    # INSTRUÇÃO
    # --------------------------------------------------------

    caixa_info = pygame.Rect(
        PAINEL_DIREITO.x + 15,
        PAINEL_DIREITO.bottom - 100,
        PAINEL_DIREITO.width - 30,
        75
    )

    painel(
        janela,
        caixa_info,
        FUNDO_2,
        BORDA,
        7
    )

    texto(
        janela,
        "COMO JOGAR",
        FONTE_MUITO_PEQUENA,
        AMARELO,
        caixa_info.x + 12,
        caixa_info.y + 10
    )

    texto(
        janela,
        "Selecione uma evidência",
        FONTE_MUITO_PEQUENA,
        CINZA,
        caixa_info.x + 12,
        caixa_info.y + 29
    )

    texto(
        janela,
        "e investigue as posições.",
        FONTE_MUITO_PEQUENA,
        CINZA,
        caixa_info.x + 12,
        caixa_info.y + 46
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

    # --------------------------------------------------------
    # BOTÃO EVIDÊNCIAS
    # --------------------------------------------------------

    botao(
        janela,
        pygame.Rect(
            25,
            y + 13,
            150,
            34
        ),
        "EVIDÊNCIAS",
        mouse_pos
    )

    # --------------------------------------------------------
    # TEXTO ESC
    # --------------------------------------------------------

    texto(
        janela,
        "ESC  •  SAIR",
        FONTE_PEQUENA,
        CINZA,
        195,
        y + 22
    )

    # --------------------------------------------------------
    # BOTÃO VERIFICAR
    # --------------------------------------------------------

    botao(
        janela,
        pygame.Rect(
            LARGURA - 270,
            y + 9,
            245,
            42
        ),
        "VERIFICAR SOLUÇÃO",
        mouse_pos,
        True
    )


# ============================================================
# RETÂNGULOS DAS CASAS
# ============================================================

def obter_rect_casas():

    area_x = PAINEL_CENTRAL.x + 20
    area_y = PAINEL_CENTRAL.y + 88

    area_largura = (
        PAINEL_CENTRAL.width - 40
    )

    area_altura = (
        PAINEL_CENTRAL.height - 105
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

    rects = []

    for i in range(5):

        linha = i // colunas
        coluna = i % colunas

        x = area_x + coluna * (
            largura_card + espacamento_x
        )

        y = area_y + linha * (
            altura_card + espacamento_y
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


# ============================================================
# RETÂNGULOS DAS DICAS
# ============================================================

def obter_rect_dicas():

    inicio_y = PAINEL_ESQUERDO.y + 72

    altura_card = 54
    espacamento = 8

    limite = max(
        1,
        int(
            (
                PAINEL_ESQUERDO.height - 125
            )
            /
            (altura_card + espacamento)
        )
    )

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
# BOTÃO VERIFICAR
# ============================================================

def obter_rect_verificar():

    return pygame.Rect(
        LARGURA - 270,
        ALTURA - RODAPE + 9,
        245,
        42
    )


# ============================================================
# LOOP PRINCIPAL
# ============================================================

print("CHEGOU ANTES DO LOOP")

while rodando:

    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():

        # ====================================================
        # SAIR
        # ====================================================

        if evento.type == pygame.QUIT:

            rodando = False

        # ====================================================
        # TECLAS
        # ====================================================

        elif evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_ESCAPE:

                rodando = False

            # F11 agora não precisa mais fazer nada,
            # pois a janela já ocupa toda a tela.
            elif evento.key == pygame.K_F11:

                pass

        # ====================================================
        # CLIQUE
        # ====================================================

        elif evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1:

                # --------------------------------------------
                # MINIMIZAR
                # --------------------------------------------

                if BOTAO_MINIMIZAR.collidepoint(
                    evento.pos
                ):

                    pygame.display.iconify()

                # --------------------------------------------
                # FECHAR
                # --------------------------------------------

                elif BOTAO_FECHAR.collidepoint(
                    evento.pos
                ):

                    rodando = False

                # --------------------------------------------
                # CASA
                # --------------------------------------------

                else:

                    for i, rect in enumerate(
                        obter_rect_casas()
                    ):

                        if rect.collidepoint(
                            evento.pos
                        ):

                            casa_selecionada = i

                    # ----------------------------------------
                    # DICA
                    # ----------------------------------------

                    for indice, rect in obter_rect_dicas():

                        if rect.collidepoint(
                            evento.pos
                        ):

                            dica_selecionada = indice

                    # ----------------------------------------
                    # CATEGORIA
                    # ----------------------------------------

                    inicio_y = (
                        PAINEL_DIREITO.y + 112
                    )

                    for i in range(
                        len(categorias)
                    ):

                        rect = pygame.Rect(
                            PAINEL_DIREITO.x + 15,
                            inicio_y + i * 50,
                            PAINEL_DIREITO.width - 30,
                            43
                        )

                        if rect.collidepoint(
                            evento.pos
                        ):

                            categoria_selecionada = i

                    # ----------------------------------------
                    # VERIFICAR
                    # ----------------------------------------

                    if obter_rect_verificar().collidepoint(
                        evento.pos
                    ):

                        print()
                        print("============================")
                        print("SOLUÇÃO DO ENIGMA")
                        print("============================")
                        print(resposta)


    # ========================================================
    # DESENHO
    # ========================================================

    janela.fill(FUNDO)

    desenhar_cabecalho(
        mouse_pos
    )

    desenhar_dicas()

    painel(
        janela,
        PAINEL_CENTRAL
    )

    desenhar_casas()

    desenhar_investigacao()

    desenhar_rodape(
        mouse_pos
    )

    pygame.display.flip()

    clock.tick(60)


pygame.quit()