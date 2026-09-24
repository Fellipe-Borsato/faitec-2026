import pygame
import hashlib
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
    VERMELHO,
    VERDE
)

from interface.ui.dimensoes import (
    TOPO,
    RODAPE,
    criar_dimensoes
)

from interface.config.fontes import (
    FONTE_TITULO,
    FONTE_PEQUENA,
    FONTE_NORMAL,
    FONTE_CATEGORIA
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
        self.runonce = False
        self.nome_vencedor = ""
        self.fonte_titulo = FONTE_TITULO
        self.fonte_pequena = FONTE_PEQUENA
        self.fonte_seed = FONTE_NORMAL
        self.fonte_botao = FONTE_CATEGORIA
        self.contador_backspace = 0
        self.jagravado = False
        self.cheat = False
        self.trapaca = ''
        self.segredo = '4c4d384f1a9d0a3a89406aa2317a71922076f065279e494fa8446e7e890d2410'

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
        self.info = info

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

            janela.blit(superficie, rect)


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
            if not self.runonce:
                info = self.info
                self.LARGURA = info.current_w
                self.ALTURA = info.current_h
                largura_painel = int(self.LARGURA * 0.60)
                altura_painel = int(self.ALTURA * 0.55)
                self.painel_menu = pygame.Rect(
                    (self.LARGURA - largura_painel) // 2,
                    (self.ALTURA - altura_painel) // 2,
                    largura_painel,
                    altura_painel
                )
                self.botao_confirmar = pygame.Rect(
                    int(self.LARGURA * 0.31),
                    int(self.ALTURA * 0.58),
                    int(self.LARGURA * 0.17),
                    int(self.ALTURA * 0.08)
                )
                self.botao_voltar = pygame.Rect(
                    int(self.LARGURA * 0.52),
                    int(self.ALTURA * 0.58),
                    int(self.LARGURA * 0.17),
                    int(self.ALTURA * 0.08)
                )
                self.campo_nome = pygame.Rect(
                    (self.LARGURA - int(self.LARGURA * 0.40)) // 2,
                    int(self.ALTURA * 0.44),
                    int(self.LARGURA * 0.40),
                    int(self.ALTURA * 0.08)
                )
                self.runonce = True
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(
                janela,
                PAINEL,
                self.painel_menu,
                border_radius=16
            )

            pygame.draw.rect(
                janela,
                BORDA,
                self.painel_menu,
                width=2,
                border_radius=16
            )

            desenhar_texto(
                "PARABÉNS!!",
                self.fonte_titulo,
                BRANCO,
                self.LARGURA // 2,
                int(self.ALTURA * 0.28)
            )

            desenhar_texto(
                "Favor informar seu nome para registro:",
                self.fonte_pequena,
                CINZA,
                self.LARGURA // 2,
                int(self.ALTURA * 0.34)
            )

            pygame.draw.rect(
                janela,
                PAINEL_2,
                self.campo_nome,
                border_radius=10
            )

            pygame.draw.rect(
                janela,
                AMARELO if self.nome_vencedor else BORDA,
                self.campo_nome,
                width=2,
                border_radius=10
            )

            texto_mostrado = self.nome_vencedor if self.nome_vencedor else "Digite seu nome"
            cor_texto = BRANCO if self.nome_vencedor else CINZA_ESCURO

            desenhar_texto(
                texto_mostrado,
                self.fonte_seed,
                cor_texto,
                self.campo_nome.centerx,
                self.campo_nome.centery
            )

            desenhar_botao(
                self.botao_confirmar,
                "CONFIRMAR",
                mouse_pos,
                destaque=True
            )

            desenhar_botao(
                self.botao_voltar,
                "VOLTAR",
                mouse_pos
            )
        impressora = thermal()
        while self.rodando:
            window = Window.from_display_module()
            window.position = (0, 0)
            mouse_pos = pygame.mouse.get_pos()
            self.contador_backspace += 1
            if hashlib.sha256(self.trapaca.encode()).hexdigest() == self.segredo:
                self.tabela_jogador = [lista[:] for lista in self.respostas]
                print(self.respostas)
                print(self.tabela_jogador)
                self.cheat = False
                self.trapaca = ''

            if pygame.key.get_pressed()[pygame.K_BACKSPACE] and self.completo:
                if self.contador_backspace >= 10:
                    self.nome_vencedor = self.nome_vencedor[:-1]
                    self.contador_backspace = 0
            else:
                self.contador_backspace = 0
            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:
                    pygame.key.stop_text_input()
                    self.rodando = False
                    
                elif evento.type == pygame.TEXTINPUT:
                    if self.completo:
                        for caractere in evento.text:
                            self.nome_vencedor += caractere.upper()
                    if self.cheat:
                        for caractere in evento.text:
                            self.trapaca += caractere.upper()



                elif evento.type == pygame.KEYDOWN:
                    if self.completo:
                        if evento.key == pygame.K_BACKSPACE:
                            self.nome_vencedor = self.nome_vencedor[:-1]

                        if evento.key == pygame.K_DELETE:
                            self.nome_vencedor = ''

                        if evento.key == pygame.K_RETURN:
                            if self.nome_vencedor and len(self.nome_vencedor) >= 3:
                                pygame.key.stop_text_input()
                                self.puzzle.gravaRank(self.nome_vencedor)
                                self.jagravado = True
                        if evento.key == pygame.K_ESCAPE:
                            pygame.key.stop_text_input()
                            self.nome_vencedor=''
                            self.completo = False

                    else:
                        if evento.key == pygame.K_ESCAPE:
                            self.rodando = False
                        if evento.key == pygame.K_F5:
                            self.cheat = not self.cheat
                            if not self.cheat:
                                pygame.key.stop_text_input()
                            else:
                                pygame.key.start_text_input()


                elif evento.type == pygame.MOUSEWHEEL and not self.completo:

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
                            pass

                    elif evento.button == 1 and not self.completo:
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

                    elif evento.button == 1 and self.completo:
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
                        if botao_confirmar.collidepoint(evento.pos):
                            if len(self.nome_vencedor) >= 3 and not self.jagravado:
                                self.puzzle.gravaRank(self.nome_vencedor)
                                self.mostrar_mensagem(
                                        "VENCEDOR GRAVADO COM SUCESSO",
                                        VERDE
                                    )
                                self.jagravado = True
                            elif self.jagravado:
                                self.mostrar_mensagem(
                                        "VENCEDOR JA GRAVADO".upper(),
                                        VERMELHO
                                    )
                            else:
                                self.mostrar_mensagem(
                                        "Nome precisa ter pelo menos 3 caracteres".upper(),
                                        VERMELHO
                                    )

                        if botao_voltar.collidepoint(evento.pos):
                            self.completo=False
                            self.nome_vencedor=''

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
                pygame.key.start_text_input()
                ranking()
            pygame.display.flip()

            clock.tick(60)
        impressora.close()
        menuInicial().menu_principal()
        pygame.quit()
