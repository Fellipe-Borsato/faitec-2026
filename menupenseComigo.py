import pygame
import sys
import os
import subprocess
import random
import importlib.util


# ============================================================
# CARREGAR CORES DO ARQUIVO EXISTENTE
# ============================================================

CAMINHO_CORES = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "interface",
    "config",
    "cores.py"
)

spec = importlib.util.spec_from_file_location("cores", CAMINHO_CORES)
cores = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cores)


# ============================================================
# CORES
# ============================================================

FUNDO = cores.FUNDO
FUNDO_2 = cores.FUNDO_2

PAINEL = cores.PAINEL
PAINEL_2 = cores.PAINEL_2
PAINEL_3 = cores.PAINEL_3

BORDA = cores.BORDA
BORDA_CLARA = cores.BORDA_CLARA

BRANCO = cores.BRANCO
CINZA = cores.CINZA
CINZA_ESCURO = cores.CINZA_ESCURO

AMARELO = cores.AMARELO
AMARELO_CLARO = cores.AMARELO_CLARO

VERDE = cores.VERDE
VERMELHO = cores.VERMELHO

PRETO = cores.PRETO


# ============================================================
# CONFIGURAÇÕES
# ============================================================

pygame.init()

LARGURA = 1000
ALTURA = 700

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PENSE COMIGO")

clock = pygame.time.Clock()


# ============================================================
# FONTES
# ============================================================

fonte_titulo = pygame.font.SysFont("arial", 58, bold=True)
fonte_subtitulo = pygame.font.SysFont("arial", 20)
fonte_botao = pygame.font.SysFont("arial", 27, bold=True)
fonte_pequena = pygame.font.SysFont("arial", 18)
fonte_seed = pygame.font.SysFont("arial", 25)
fonte_interrogacao = pygame.font.SysFont("arial", 24, bold=True)


# ============================================================
# FUNÇÕES
# ============================================================

def desenhar_texto(texto, fonte, cor, x, y, centralizado=True):
    superficie = fonte.render(texto, True, cor)

    if centralizado:
        rect = superficie.get_rect(center=(x, y))
    else:
        rect = superficie.get_rect(topleft=(x, y))

    tela.blit(superficie, rect)


def desenhar_botao(rect, texto, mouse_pos, destaque=False):
    passou_mouse = rect.collidepoint(mouse_pos)

    if destaque:
        cor_fundo = AMARELO_CLARO if passou_mouse else AMARELO
        cor_texto = PRETO
    else:
        cor_fundo = PAINEL_2 if not passou_mouse else PAINEL_3
        cor_texto = BRANCO

    pygame.draw.rect(
        tela,
        cor_fundo,
        rect,
        border_radius=10
    )

    pygame.draw.rect(
        tela,
        BORDA_CLARA if passou_mouse else BORDA,
        rect,
        width=2,
        border_radius=10
    )

    desenhar_texto(
        texto,
        fonte_botao,
        cor_texto,
        rect.centerx,
        rect.centery
    )


def abrir_jogo(seed=None):
    """
    Abre o 'penseComigo.py'.

    Se houver seed, envia a seed para o jogo.
    """

    pasta = os.path.dirname(os.path.abspath(__file__))
    arquivo_jogo = os.path.join(pasta, "penseComigo.py")

    if seed is None:
        subprocess.Popen(
            ["py", "-3.14", arquivo_jogo],
            cwd=pasta
        )
    else:
        subprocess.Popen(
            ["py", "-3.14", arquivo_jogo, str(seed)],
            cwd=pasta
        )

    pygame.quit()
    sys.exit()


# ============================================================
# TELA DE AJUDA
# ============================================================

def desenhar_ajuda():
    largura = 500
    altura = 270

    x = (LARGURA - largura) // 2
    y = (ALTURA - altura) // 2

    sombra = pygame.Rect(x + 8, y + 8, largura, altura)

    pygame.draw.rect(
        tela,
        PRETO,
        sombra,
        border_radius=14
    )

    painel = pygame.Rect(x, y, largura, altura)

    pygame.draw.rect(
        tela,
        PAINEL,
        painel,
        border_radius=14
    )

    pygame.draw.rect(
        tela,
        BORDA_CLARA,
        painel,
        width=2,
        border_radius=14
    )

    desenhar_texto(
        "COMO JOGAR",
        fonte_botao,
        BRANCO,
        LARGURA // 2,
        y + 40
    )

    desenhar_texto(
        "Resolva o quebra-cabeça usando a lógica.",
        fonte_pequena,
        CINZA,
        LARGURA // 2,
        y + 95
    )

    desenhar_texto(
        "Use as pistas para descobrir a posição correta.",
        fonte_pequena,
        CINZA,
        LARGURA // 2,
        y + 125
    )

    desenhar_texto(
        "Acerte todas as posições para vencer.",
        fonte_pequena,
        CINZA,
        LARGURA // 2,
        y + 155
    )

    desenhar_texto(
        "Passe o mouse no '?' para fechar.",
        fonte_pequena,
        AMARELO_CLARO,
        LARGURA // 2,
        y + 210
    )


# ============================================================
# TELA PRINCIPAL
# ============================================================

def menu_principal():

    botao_jogar = pygame.Rect(
        350, 290, 300, 65
    )

    botao_sair = pygame.Rect(
        350, 380, 300, 65
    )

    botao_ajuda = pygame.Rect(
        930, 630, 45, 45
    )

    while True:

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    if botao_jogar.collidepoint(mouse_pos):
                        menu_jogar()

                    if botao_sair.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        # ----------------------------------------------------
        # FUNDO
        # ----------------------------------------------------

        tela.fill(FUNDO)

        # detalhe superior
        pygame.draw.rect(
            tela,
            FUNDO_2,
            (0, 0, LARGURA, 8)
        )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        desenhar_texto(
            "PENSE COMIGO",
            fonte_titulo,
            BRANCO,
            LARGURA // 2,
            150
        )

        desenhar_texto(
            "DESAFIE SUA LÓGICA",
            fonte_subtitulo,
            CINZA,
            LARGURA // 2,
            205
        )

        # ----------------------------------------------------
        # BOTÕES
        # ----------------------------------------------------

        desenhar_botao(
            botao_jogar,
            "JOGAR",
            mouse_pos,
            destaque=True
        )

        desenhar_botao(
            botao_sair,
            "SAIR",
            mouse_pos
        )

        # ----------------------------------------------------
        # BOTÃO ?
        # ----------------------------------------------------

        mouse_na_ajuda = botao_ajuda.collidepoint(mouse_pos)

        pygame.draw.rect(
            tela,
            PAINEL_2 if not mouse_na_ajuda else PAINEL_3,
            botao_ajuda,
            border_radius=10
        )

        pygame.draw.rect(
            tela,
            BORDA_CLARA if mouse_na_ajuda else BORDA,
            botao_ajuda,
            width=2,
            border_radius=10
        )

        desenhar_texto(
            "?",
            fonte_interrogacao,
            BRANCO,
            botao_ajuda.centerx,
            botao_ajuda.centery
        )

        # ----------------------------------------------------
        # AJUDA AO PASSAR O MOUSE
        # ----------------------------------------------------

        if mouse_na_ajuda:
            desenhar_ajuda()

        pygame.display.flip()
        clock.tick(60)


# ============================================================
# MENU JOGAR
# ============================================================

def menu_jogar():

    botao_classico = pygame.Rect(
        300, 200, 400, 60
    )

    botao_aleatorio = pygame.Rect(
        300, 285, 400, 60
    )

    botao_seed = pygame.Rect(
        300, 370, 400, 60
    )

    botao_voltar = pygame.Rect(
        300, 500, 400, 60
    )

    while True:

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    if botao_aleatorio.collidepoint(mouse_pos):

                        seed = random.randint(100000, 999999)

                        abrir_jogo(seed)

                    if botao_seed.collidepoint(mouse_pos):

                        menu_seed()

                    if botao_voltar.collidepoint(mouse_pos):

                        return

        tela.fill(FUNDO)

        desenhar_texto(
            "JOGAR",
            fonte_titulo,
            BRANCO,
            LARGURA // 2,
            100
        )

        desenhar_botao(
            botao_classico,
            "CLÁSSICO",
            mouse_pos
        )

        desenhar_botao(
            botao_aleatorio,
            "ALEATÓRIO",
            mouse_pos,
            destaque=True
        )

        desenhar_botao(
            botao_seed,
            "INFORMAR SEED",
            mouse_pos
        )

        desenhar_botao(
            botao_voltar,
            "VOLTAR",
            mouse_pos
        )

        pygame.display.flip()
        clock.tick(60)


# ============================================================
# INFORMAR SEED
# ============================================================

def menu_seed():

    seed_texto = ""

    botao_confirmar = pygame.Rect(
        300, 400, 190, 60
    )

    botao_voltar = pygame.Rect(
        510, 400, 190, 60
    )

    campo_seed = pygame.Rect(
        300, 300, 400, 60
    )

    pygame.key.start_text_input()

    while True:

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.key.stop_text_input()

                pygame.quit()
                sys.exit()

            if evento.type == pygame.TEXTINPUT:

                # aceita somente números
                somente_numeros = ""

                for caractere in evento.text:

                    if caractere.isdigit():
                        somente_numeros += caractere

                if len(seed_texto) + len(somente_numeros) <= 9:
                    seed_texto += somente_numeros

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_BACKSPACE:

                    seed_texto = seed_texto[:-1]

                elif evento.key == pygame.K_RETURN:

                    if seed_texto:

                        pygame.key.stop_text_input()

                        seed = int(seed_texto)

                        abrir_jogo(seed)

                elif evento.key == pygame.K_ESCAPE:

                    pygame.key.stop_text_input()

                    return

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1:

                    if botao_confirmar.collidepoint(mouse_pos):

                        if seed_texto:

                            pygame.key.stop_text_input()

                            seed = int(seed_texto)

                            abrir_jogo(seed)

                    if botao_voltar.collidepoint(mouse_pos):

                        pygame.key.stop_text_input()

                        return

        tela.fill(FUNDO)

        desenhar_texto(
            "INFORMAR SEED",
            fonte_titulo,
            BRANCO,
            LARGURA // 2,
            120
        )

        desenhar_texto(
            "Digite uma seed numérica:",
            fonte_pequena,
            CINZA,
            LARGURA // 2,
            240
        )

        # campo
        pygame.draw.rect(
            tela,
            PAINEL,
            campo_seed,
            border_radius=10
        )

        pygame.draw.rect(
            tela,
            AMARELO if seed_texto else BORDA,
            campo_seed,
            width=2,
            border_radius=10
        )

        texto_mostrado = seed_texto

        if not texto_mostrado:
            texto_mostrado = "Digite a seed..."

        cor_texto = BRANCO if seed_texto else CINZA_ESCURO

        desenhar_texto(
            texto_mostrado,
            fonte_seed,
            cor_texto,
            campo_seed.centerx,
            campo_seed.centery
        )

        desenhar_botao(
            botao_confirmar,
            "CONFIRMAR",
            mouse_pos,
            destaque=True
        )

        desenhar_botao(
            botao_voltar,
            "VOLTAR",
            mouse_pos
        )

        pygame.display.flip()
        clock.tick(60)


# ============================================================
# INICIAR
# ============================================================

menu_principal()