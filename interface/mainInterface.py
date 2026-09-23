import pygame
from thermal import thermal
from pygame._sdl2 import Window
from interface.ui.interface import (
    desenhar_interface
)
import pensaComigo
from interface.ui.dicas.dicas import (
    obter_botoes_paginacao,
    obter_total_paginas_dicas,
    obter_rect_dicas
)

from interface.ui.casas.casas import (
    obter_rect_casas
)

from interface.ui.investigacao.investigacao import (
    obter_rect_categorias,
    obter_rect_valores
)

from interface.ui.rodape.rodape import (
    obter_rect_verificar,
    obter_rect_imprimir
)

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

from interface.ui.dimensoes import (
    TOPO,
    RODAPE,
    criar_dimensoes
)

from menupensaComigo import menuInicial
class ui():
    def __init__(self,puzzle=''):
        self.puzzle=puzzle
        self.mensagem_jogo = ""
        self.cor_mensagem = CINZA
        self.dicas_usadas = set()
        self.completo = False
        self.rodando = True
        
    def mostrar_mensagem(self,
        mensagem,
        cor=CINZA
    ):
        self.mensagem_jogo = mensagem
        self.cor_mensagem = cor

    def obter_mensagem(self):
        return self.mensagem_jogo, self.cor_mensagem

    def alternar_dica_usada(self, indice):
        if indice in self.dicas_usadas:
            self.dicas_usadas.remove(indice)
        else:
            self.dicas_usadas.add(indice)

    def selecionar_valor(self,
        valor,
        casa_selecionada,
        categoria_selecionada
    ):
        casa = casa_selecionada
        categoria = categoria_selecionada

        valor_atual = self.tabela_jogador[
            casa
        ][categoria]



        if valor_atual == valor:

            self.tabela_jogador[
                casa
            ][categoria] = None

            self.mostrar_mensagem(
                "Valor removido.",
                CINZA
            )

            return



        for outra_casa in range(5):

            if outra_casa == casa:
                continue

            if self.tabela_jogador[outra_casa][categoria] == valor:

                self.mostrar_mensagem(
                    f"Valor já está na CASA {outra_casa + 1}.",
                    VERMELHO
                )
                return

        self.tabela_jogador[casa][categoria] = valor
        self.mostrar_mensagem(
            f"{valor} -> CASA {casa + 1}",
            VERDE
        )

    

    def executar_interface(self):
        self.categorias = self.puzzle.buscaCategorias()
        self.tabela_jogador = [
        [None for _ in self.categorias]
        for _ in range(5)
        ]
        self.dicas = self.puzzle.geraDicas()
        self.respostas = self.puzzle.pegaResposta()
        for resposta in range(len(self.respostas)):
            listasol = []
            dicionario_ordenado = dict(sorted(self.respostas[resposta].items()))
            self.respostas[resposta] = dicionario_ordenado
            for key,value in self.respostas[resposta].items():
                listasol.append(value)
            self.respostas[resposta] = listasol
        self.chave_formatada = self.puzzle.chaveFormatada()
        self.dados_categorias = {}
        for categoria in self.categorias:
            codigo = None
            for i in range(1, 10):
                nome = self.puzzle.buscaCategoria(str(i))
                if nome.upper() == categoria.upper():
                    codigo = str(i)
                    break
            if codigo is not None:
                self.dados_categorias[categoria] = (
                    self.puzzle.buscaValores(codigo,mostraValores=True))

        pygame.init()
        pdisplay = pygame.display
        pdisplay.set_mode(display=0)
        info = pdisplay.Info()

        largura = info.current_w
        altura = info.current_h

        janela = pdisplay.set_mode(
            (largura, altura),
            pygame.NOFRAME
            
        )

        pygame.display.set_caption(
            "Pensa comigo"
        )

        clock = pygame.time.Clock()

        dimensoes = criar_dimensoes(
            largura,
            altura
        )

        painel_esquerdo = dimensoes["painel_esquerdo"]
        painel_central = dimensoes["painel_central"]
        painel_direito = dimensoes["painel_direito"]

        botao_minimizar = dimensoes["botao_minimizar"]
        botao_fechar = dimensoes["botao_fechar"]

        casa_selecionada = 0
        categoria_selecionada = 0
        dica_selecionada = 0
        pagina_dicas = 0
        def desenhar_texto(texto, fonte, cor, x, y, centralizado=True):
            superficie = fonte.render(texto, True, cor)

            if centralizado:
                rect = superficie.get_rect(center=(x, y))
            else:
                rect = superficie.get_rect(topleft=(x, y))

            self.tela.blit(superficie, rect)


        def desenhar_botao(rect, texto, mouse_pos, destaque=False):
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
                janela,
                cor_fundo,
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                janela,
                cor_borda,
                rect,
                width=2,
                border_radius=12
            )

            desenhar_texto(
                texto,
                self.fonte_botao,
                cor_texto,
                rect.centerx,
                rect.centery
            )
        def ranking():
            pdisplay = pygame.display
            pdisplay.set_mode(display=0)
            info = pdisplay.Info()
            LARGURA = info.current_w
            ALTURA = info.current_h
            largura_painel = int(LARGURA * 0.60)
            altura_painel = int(ALTURA * 0.55)
            painel_menu = pygame.Rect(
                (LARGURA - largura_painel) // 2,
                (ALTURA - altura_painel) // 2,
                largura_painel,
                altura_painel
            )
            botao_confirmar = pygame.Rect(
                int(LARGURA * 0.31),
                int(ALTURA * 0.58),
                int(LARGURA * 0.17),
                int(ALTURA * 0.08)
            )
            botao_voltar = pygame.Rect(
                int(LARGURA * 0.52),
                int(ALTURA * 0.58),
                int(LARGURA * 0.17),
                int(ALTURA * 0.08)
            )
            campo_seed = pygame.Rect(
                (LARGURA - int(LARGURA * 0.40)) // 2,
                int(ALTURA * 0.44),
                int(LARGURA * 0.40),
                int(ALTURA * 0.08)
            )
            pygame.key.start_text_input()

        impressora = thermal()
        while self.rodando:
            window = Window.from_display_module()
            window.position = (0, 0)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    pygame.key.stop_text_input()
                    self.rodando = False
                    
                elif evento.type == pygame.TEXTINPUT:
                    nome_vencedor = ""
                    for caractere in evento.text:
                        nome_vencedor += caractere

                elif evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:

                        self.rodando = False

                elif evento.type == pygame.MOUSEWHEEL:

                    if painel_esquerdo.collidepoint(
                        mouse_pos
                    ):

                        total_paginas = (
                            obter_total_paginas_dicas(
                                self.dicas,
                                painel_esquerdo
                            )
                        )

                        if evento.y < 0:

                            if pagina_dicas < total_paginas - 1:

                                pagina_dicas += 1

                        elif evento.y > 0:

                            if pagina_dicas > 0:

                                pagina_dicas -= 1

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 2:
                        rect_verificar = obter_rect_verificar(
                            largura,
                            altura,
                            RODAPE
                        )

                        if rect_verificar.collidepoint(
                            evento.pos
                        ):
                            print(self.respostas)
                            print(self.tabela_jogador)

                    elif evento.button != 1:
                        continue


                    botao_anterior, botao_proximo = (
                        obter_botoes_paginacao(
                            painel_esquerdo
                        )
                    )

                    total_paginas = (
                        obter_total_paginas_dicas(
                            self.dicas,
                            painel_esquerdo
                        )
                    )

                    if botao_anterior.collidepoint(
                        evento.pos
                    ):

                        if pagina_dicas > 0:

                            pagina_dicas -= 1

                        continue

                    if botao_proximo.collidepoint(
                        evento.pos
                    ):

                        if pagina_dicas < total_paginas - 1:

                            pagina_dicas += 1

                        continue


                    if botao_minimizar.collidepoint(
                        evento.pos
                    ):

                        pygame.display.iconify()

                        continue


                    if botao_fechar.collidepoint(
                        evento.pos
                    ):

                        self.rodando = False

                        continue


                    for i, rect in enumerate(
                        obter_rect_casas(
                            painel_central
                        )
                    ):

                        if rect.collidepoint(
                            evento.pos
                        ):

                            casa_selecionada = i

                            self.mostrar_mensagem(
                                f"CASA {i + 1} selecionada.",
                                AMARELO
                            )

                            break


                    for indice, rect in obter_rect_dicas(
                        painel_esquerdo,
                        self.dicas,
                        pagina_dicas
                    ):

                        x_rect = pygame.Rect(
                            rect.right - 18,
                            rect.bottom - 18,
                            12,
                            12
                        )

                        if x_rect.collidepoint(evento.pos):
                            self.dicas_usadas.discard(indice)
                            if dica_selecionada == indice:
                                dica_selecionada = -1
                            self.mostrar_mensagem(
                                f"Dica {indice + 1} desmarcada.",
                                AMARELO
                            )
                            break

                        if rect.collidepoint(
                            evento.pos
                        ):

                            self.dicas_usadas.add(indice)
                            dica_selecionada = indice

                            self.mostrar_mensagem(
                                f"Dica {indice + 1} selecionada.",
                                AMARELO
                            )

                            break


                    for i, rect in enumerate(
                        obter_rect_categorias(
                            painel_direito,
                            self.categorias
                        )
                    ):

                        if rect.collidepoint(
                            evento.pos
                        ):

                            categoria_selecionada = i

                            self.mostrar_mensagem(
                                f"{self.categorias[i]} selecionada.",
                                AMARELO
                            )

                            break


                    for valor, rect in obter_rect_valores(
                        painel_direito,
                        self.categorias,
                        self.dados_categorias,
                        categoria_selecionada
                    ):

                        if rect.collidepoint(
                            evento.pos
                        ):

                            self.selecionar_valor(
                                valor,
                                casa_selecionada,
                                categoria_selecionada
                            )

                            break


                    rect_verificar = obter_rect_verificar(
                        largura,
                        altura,
                        RODAPE
                    )

                    if rect_verificar.collidepoint(
                        evento.pos
                    ):

                        if self.respostas == self.tabela_jogador:
                            self.mostrar_mensagem(
                                "SOLUÇÃO CORRETA",
                                VERDE
                            )
                            self.completo = True
                        else:
                            self.mostrar_mensagem(
                                "SOLUÇÃO INCORRETA",
                                VERMELHO
                            )
                            self.completo = False
                        
                    rect_imprimir = obter_rect_imprimir(
                        largura,
                        altura,
                        RODAPE
                    )

                    if rect_imprimir.collidepoint(
                        evento.pos
                    ):
                        tempdicas = self.puzzle.geraDicas(True)
                        if impressora:
                            
                            impressora.fonte(True)
                            impressora.print_text("|".join(self.categorias))
                            for dica in tempdicas:
                                impressora.print_text(dica)
                            impressora.print_text()
                            impressora.center(True)
                            impressora.print_text(self.puzzle.chaveFormatada())
                            for n in range(0, 35, 5):
                                impressora.print_barcode(self.puzzle.chave[n:n+5])
                            #impressora.print_barcode(puzzle.chave)
                            impressora.cut()
                            impressora.center(False)
                            pass
                        else:
                            print("|".join(self.categorias))
                            for dica in tempdicas:
                                print(dica)
                            print()
                            print(self.puzzle.chaveFormatada())
                            print()


            mensagem_jogo, cor_mensagem = self.obter_mensagem()

            desenhar_interface(
                janela,
                mouse_pos,
                largura,
                altura,
                TOPO,
                RODAPE,
                painel_esquerdo,
                painel_central,
                painel_direito,
                botao_minimizar,
                botao_fechar,
                self.dicas,
                dica_selecionada,
                pagina_dicas,
                self.chave_formatada,
                self.categorias,
                self.tabela_jogador,
                casa_selecionada,
                self.dados_categorias,
                categoria_selecionada,
                mensagem_jogo,
                cor_mensagem,
                self.dicas_usadas
            )
            if self.completo:
                mouse_pos = pygame.mouse.get_pos()
                pygame.draw.rect(
                    janela,
                    PAINEL,
                    painel_menu,
                    border_radius=16
                )

                pygame.draw.rect(
                    janela,
                    BORDA,
                    painel_menu,
                    width=2,
                    border_radius=16
                )

                desenhar_texto(
                    "INFORMAR SEED",
                    self.fonte_titulo,
                    BRANCO,
                    self.LARGURA // 2,
                    int(self.ALTURA * 0.28)
                )

                desenhar_texto(
                    "Digite uma seed numérica:",
                    self.fonte_pequena,
                    CINZA,
                    self.LARGURA // 2,
                    int(self.ALTURA * 0.34)
                )

                pygame.draw.rect(
                    janela,
                    PAINEL_2,
                    campo_seed,
                    border_radius=10
                )

                pygame.draw.rect(
                    janela,
                    AMARELO if seed_texto else BORDA,
                    campo_seed,
                    width=2,
                    border_radius=10
                )

                texto_mostrado = seed_texto if seed_texto else "Digite seu nome"
                cor_texto = BRANCO if seed_texto else CINZA_ESCURO

                desenhar_texto(
                    texto_mostrado,
                    self.fonte_seed,
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
            clock.tick(60)
        impressora.close()
        menuInicial().menu_principal()
        pygame.quit()
