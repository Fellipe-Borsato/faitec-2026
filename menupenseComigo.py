import pygame
import sys
from zebra import zebra


from interface.config.cores import (
    FUNDO,
    FUNDO_2,
    PAINEL,
    PAINEL_2,
    PAINEL_3,
    BORDA,
    BORDA_CLARA,
    BRANCO,
    CINZA,
    CINZA_ESCURO,
    AMARELO,
    AMARELO_CLARO,
    PRETO,
    VERMELHO
)

from interface.config.fontes import (
    FONTE_TITULO,
    FONTE_SUBTITULO,
    FONTE_CATEGORIA,
    FONTE_NORMAL,
    FONTE_PEQUENA,
)

class menuInicial():
    def __init__(self):
        from interface.mainInterface import ui
        self.telajogo = ui()
        self.rodando=False
        pygame.init()
        pdisplay = pygame.display
        pdisplay.set_mode(display=0)
        info = pdisplay.Info()

        self.LARGURA = info.current_w
        self.ALTURA = info.current_h
        self.tela = pdisplay.set_mode(
                (self.LARGURA, self.ALTURA),
                pygame.NOFRAME
            )
        pygame.display.set_caption("PENSA COMIGO")
        self.clock = pygame.time.Clock()

        self.fonte_titulo = FONTE_TITULO
        self.fonte_subtitulo = FONTE_SUBTITULO
        self.fonte_botao = FONTE_CATEGORIA
        self.fonte_pequena = FONTE_PEQUENA
        self.fonte_seed = FONTE_NORMAL
        self.fonte_interrogacao = FONTE_CATEGORIA


    def desenhar_texto(self,texto, fonte, cor, x, y, centralizado=True):
        superficie = fonte.render(texto, True, cor)

        if centralizado:
            rect = superficie.get_rect(center=(x, y))
        else:
            rect = superficie.get_rect(topleft=(x, y))

        self.tela.blit(superficie, rect)


    def desenhar_botao(self,rect, texto, mouse_pos, destaque=False):
        passou_mouse = rect.collidepoint(mouse_pos)

        if destaque:
            cor_fundo = AMARELO_CLARO if passou_mouse else AMARELO
            cor_texto = PRETO
            cor_borda = AMARELO_CLARO if passou_mouse else AMARELO
        else:
            cor_fundo = PAINEL_2 if not passou_mouse else PAINEL_3
            cor_texto = BRANCO if not passou_mouse else BRANCO
            cor_borda = BORDA_CLARA if passou_mouse else BORDA

        pygame.draw.rect(
            self.tela,
            cor_fundo,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.tela,
            cor_borda,
            rect,
            width=2,
            border_radius=12
        )

        self.desenhar_texto(
            texto,
            self.fonte_botao,
            cor_texto,
            rect.centerx,
            rect.centery
        )


    def abrir_jogo(self,seed=''):
        puzzle = zebra()
        seed = str(seed)
        if seed == 'random':
            puzzle.geraChave()
        elif len(seed) in (35,41):
            puzzle.chave = str(seed)
        self.telajogo.puzzle = puzzle
        self.telajogo.executar_interface()
        self.rodando=False
        pygame.quit()
        


    def desenhar_ajuda(self):
        largura = 540
        altura = 260

        x = (self.LARGURA - largura) // 2
        y = (self.ALTURA - altura) // 2

        sombra = pygame.Rect(x + 10, y + 10, largura, altura)
        painel = pygame.Rect(x, y, largura, altura)

        pygame.draw.rect(
            self.tela,
            PRETO,
            sombra,
            border_radius=16
        )

        pygame.draw.rect(
            self.tela,
            PAINEL,
            painel,
            border_radius=16
        )

        pygame.draw.rect(
            self.tela,
            BORDA_CLARA,
            painel,
            width=2,
            border_radius=16
        )

        self.desenhar_texto(
            "COMO JOGAR",
            self.fonte_botao,
            BRANCO,
            self.LARGURA // 2,
            y + 42
        )

        for indice, linha in enumerate([
            "Resolva o quebra-cabeça usando a lógica.",
            "Use as pistas para descobrir a posição correta.",
            "Acerte todas as posições para vencer."
        ]):
            self.desenhar_texto(
                linha,
                self.fonte_pequena,
                CINZA,
                self.LARGURA // 2,
                y + 95 + indice * 30
            )

        self.desenhar_texto(
            "Passe o mouse no '?' para fechar.",
            self.fonte_pequena,
            AMARELO_CLARO,
            self.LARGURA // 2,
            y + 210
        )


    def menu_principal(self):

        largura_painel = int(self.LARGURA * 0.50)
        altura_painel = int(self.ALTURA * 0.48)
        painel_menu = pygame.Rect(
            (self.LARGURA - largura_painel) // 2,
            (self.ALTURA - altura_painel) // 2,
            largura_painel,
            altura_painel
        )
        botao_jogar = pygame.Rect(
            (self.LARGURA - int(self.LARGURA * 0.38)) // 2,
            int(self.ALTURA * 0.45),
            int(self.LARGURA * 0.38),
            int(self.ALTURA * 0.08)
        )
        botao_sair = pygame.Rect(
            (self.LARGURA - int(self.LARGURA * 0.38)) // 2,
            int(self.ALTURA * 0.56),
            int(self.LARGURA * 0.38),
            int(self.ALTURA * 0.08)
        )
        botao_ajuda = pygame.Rect(
            self.LARGURA - 90,
            self.ALTURA - 90,
            50,
            50
        )
        self.rodando=True
        while self.rodando:

            mouse_pos = pygame.mouse.get_pos()

            self.tela.fill(FUNDO)

            pygame.draw.rect(
                self.tela,
                FUNDO_2,
                (0, 0, self.LARGURA, 10)
            )

            pygame.draw.rect(
                self.tela,
                PAINEL,
                painel_menu,
                border_radius=16
            )

            pygame.draw.rect(
                self.tela,
                BORDA,
                painel_menu,
                width=2,
                border_radius=16
            )

            self.desenhar_texto(
                "PENSA COMIGO",
                self.fonte_titulo,
                BRANCO,
                self.LARGURA // 2,
                int(self.ALTURA * 0.31)
            )

            self.desenhar_texto(
                "DESAFIE SUA LÓGICA",
                self.fonte_subtitulo,
                CINZA,
                self.LARGURA // 2,
                int(self.ALTURA * 0.38)
            )

            self.desenhar_botao(
                botao_jogar,
                "JOGAR",
                mouse_pos,
                destaque=True
            )

            self.desenhar_botao(
                botao_sair,
                "SAIR",
                mouse_pos
            )

            mouse_na_ajuda = botao_ajuda.collidepoint(mouse_pos)

            pygame.draw.rect(
                self.tela,
                PAINEL_2 if not mouse_na_ajuda else PAINEL_3,
                botao_ajuda,
                border_radius=12
            )

            pygame.draw.rect(
                self.tela,
                BORDA_CLARA if mouse_na_ajuda else BORDA,
                botao_ajuda,
                width=2,
                border_radius=12
            )

            self.desenhar_texto(
                "?",
                self.fonte_interrogacao,
                BRANCO,
                botao_ajuda.centerx,
                botao_ajuda.centery
            )

            if mouse_na_ajuda:
                self.desenhar_ajuda()

            pygame.display.flip()
            self.clock.tick(60)
            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.MOUSEBUTTONDOWN:

                    if evento.button == 1:

                        if botao_jogar.collidepoint(mouse_pos):
                            self.menu_jogar()

                        if botao_sair.collidepoint(mouse_pos):
                            self.rodando = False
                            pygame.quit()



    def menu_jogar(self):

        largura_painel = int(self.LARGURA * 0.56)
        altura_painel = int(self.ALTURA * 0.66)
        painel_menu = pygame.Rect(
            (self.LARGURA - largura_painel) // 2,
            (self.ALTURA - altura_painel) // 2,
            largura_painel,
            altura_painel
        )
        botao_classico = pygame.Rect(
            (self.LARGURA - int(self.LARGURA * 0.40)) // 2,
            int(self.ALTURA * 0.28),
            int(self.LARGURA * 0.40),
            int(self.ALTURA * 0.08)
        )
        botao_aleatorio = pygame.Rect(
            (self.LARGURA - int(self.LARGURA * 0.40)) // 2,
            int(self.ALTURA * 0.39),
            int(self.LARGURA * 0.40),
            int(self.ALTURA * 0.08)
        )
        botao_seed = pygame.Rect(
            (self.LARGURA - int(self.LARGURA * 0.40)) // 2,
            int(self.ALTURA * 0.50),
            int(self.LARGURA * 0.40),
            int(self.ALTURA * 0.08)
        )
        botao_voltar = pygame.Rect(
            (self.LARGURA - int(self.LARGURA * 0.40)) // 2,
            int(self.ALTURA * 0.61),
            int(self.LARGURA * 0.40),
            int(self.ALTURA * 0.08)
        )
        self.rodando = True
        while self.rodando:
            self.tela.fill(FUNDO)
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(
                self.tela,
                FUNDO_2,
                (0, 0, self.LARGURA, 10)
            )

            pygame.draw.rect(
                self.tela,
                PAINEL,
                painel_menu,
                border_radius=16
            )

            pygame.draw.rect(
                self.tela,
                BORDA,
                painel_menu,
                width=2,
                border_radius=16
            )

            self.desenhar_texto(
                "JOGAR",
                self.fonte_titulo,
                BRANCO,
                self.LARGURA // 2,
                int(self.ALTURA * 0.22)
            )

            self.desenhar_botao(
                botao_classico,
                "CLÁSSICO",
                mouse_pos
            )

            self.desenhar_botao(
                botao_aleatorio,
                "ALEATÓRIO",
                mouse_pos,
                destaque=True
            )

            self.desenhar_botao(
                botao_seed,
                "INFORMAR SEED",
                mouse_pos
            )

            self.desenhar_botao(
                botao_voltar,
                "VOLTAR",
                mouse_pos
            )

            pygame.display.flip()
            self.clock.tick(60)


            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    self.rodando = False

                elif evento.type == pygame.MOUSEBUTTONDOWN:

                    if evento.button == 1:

                        if botao_aleatorio.collidepoint(mouse_pos):
                            seed = 'random'
                            self.abrir_jogo(seed)
                        elif botao_classico.collidepoint(mouse_pos)                        :
                            self.abrir_jogo()
                        elif botao_seed.collidepoint(mouse_pos):
                            self.menu_seed()


                        elif botao_voltar.collidepoint(mouse_pos):
                            return
                        continue

                elif evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:

                        return




    def menu_seed(self):

        seed_texto = ""
        largura_painel = int(self.LARGURA * 0.60)
        altura_painel = int(self.ALTURA * 0.55)
        painel_menu = pygame.Rect(
            (self.LARGURA - largura_painel) // 2,
            (self.ALTURA - altura_painel) // 2,
            largura_painel,
            altura_painel
        )
        botao_confirmar = pygame.Rect(
            int(self.LARGURA * 0.31),
            int(self.ALTURA * 0.58),
            int(self.LARGURA * 0.17),
            int(self.ALTURA * 0.08)
        )
        botao_voltar = pygame.Rect(
            int(self.LARGURA * 0.52),
            int(self.ALTURA * 0.58),
            int(self.LARGURA * 0.17),
            int(self.ALTURA * 0.08)
        )
        campo_seed = pygame.Rect(
            (self.LARGURA - int(self.LARGURA * 0.40)) // 2,
            int(self.ALTURA * 0.44),
            int(self.LARGURA * 0.40),
            int(self.ALTURA * 0.08)
        )

        pygame.key.start_text_input()
        self.rodando = True
        self.invalida = False
        while self.rodando:
            mouse_pos = pygame.mouse.get_pos()
            self.tela.fill(FUNDO)
            pygame.draw.rect(
                self.tela,
                FUNDO_2,
                (0, 0, self.LARGURA, 10)
            )

            pygame.draw.rect(
                self.tela,
                PAINEL,
                painel_menu,
                border_radius=16
            )

            pygame.draw.rect(
                self.tela,
                BORDA,
                painel_menu,
                width=2,
                border_radius=16
            )

            self.desenhar_texto(
                "INFORMAR SEED",
                self.fonte_titulo,
                BRANCO,
                self.LARGURA // 2,
                int(self.ALTURA * 0.22)
            )

            self.desenhar_texto(
                "Digite uma seed numérica:",
                self.fonte_pequena,
                CINZA,
                self.LARGURA // 2,
                int(self.ALTURA * 0.34)
            )

            pygame.draw.rect(
                self.tela,
                PAINEL_2,
                campo_seed,
                border_radius=10
            )

            pygame.draw.rect(
                self.tela,
                AMARELO if seed_texto else BORDA,
                campo_seed,
                width=2,
                border_radius=10
            )

            texto_mostrado = seed_texto if seed_texto else "Digite a seed..."
            cor_texto = BRANCO if seed_texto else CINZA_ESCURO

            self.desenhar_texto(
                texto_mostrado,
                self.fonte_seed,
                cor_texto,
                campo_seed.centerx,
                campo_seed.centery
            )

            self.desenhar_botao(
                botao_confirmar,
                "CONFIRMAR",
                mouse_pos,
                destaque=True
            )

            self.desenhar_botao(
                botao_voltar,
                "VOLTAR",
                mouse_pos
            )
            if self.invalida:
                    self.desenhar_texto(
                    "CHAVE INVALIDA OU INCOMPLETA",
                    FONTE_PEQUENA,
                    VERMELHO,
                    self.LARGURA // 2,
                    self.ALTURA - 90,
                    True
                )
            pygame.display.flip()
            self.clock.tick(60)


            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    pygame.key.stop_text_input()
                    pygame.quit()

                if evento.type == pygame.TEXTINPUT:
                    somente_numeros = ""

                    for caractere in evento.text:
                        if caractere.isdigit() or caractere == ":":
                            somente_numeros += caractere

                    if (len(seed_texto) + len(somente_numeros) <= 35 and ":" not in seed_texto) or (len(seed_texto) + len(somente_numeros) <= 42 and ":" in seed_texto):
                        seed_texto += somente_numeros

                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_BACKSPACE:
                        seed_texto = seed_texto[:-1]

                    elif evento.key == pygame.K_DELETE:
                        seed_texto = ''

                    elif evento.key == pygame.K_RETURN:
                        if seed_texto and len(seed_texto) in (35,41):
                            pygame.key.stop_text_input()
                            seed = int(seed_texto)
                            self.abrir_jogo(seed)
                        else:
                            self.invalida = True

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.key.stop_text_input()
                        self.invalida = False
                        return

                if evento.type == pygame.MOUSEBUTTONDOWN:

                    if evento.button == 1:

                        if botao_confirmar.collidepoint(mouse_pos):
                            if seed_texto and len(seed_texto) in (35,41):
                                pygame.key.stop_text_input()
                                seed = int(seed_texto)
                                self.abrir_jogo(seed)
                            else:
                                self.invalida = True

                        if botao_voltar.collidepoint(mouse_pos):
                            pygame.key.stop_text_input()
                            self.invalida = False
                            return

 



if __name__ == "__main__":

    menuInicial().menu_principal()
