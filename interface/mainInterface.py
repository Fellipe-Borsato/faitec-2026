import pygame
from thermal import thermal
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
    CINZA,
    AMARELO,
    VERDE,
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
        
    def mostrar_mensagem(self,
        mensagem,
        cor=CINZA
    ):
        self.mensagem_jogo = mensagem
        self.cor_mensagem = cor

    def obter_mensagem(self):
        return self.mensagem_jogo, self.cor_mensagem




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

        rodando = True
        impressora = thermal()
        while rodando:

            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():


                if evento.type == pygame.QUIT:

                    rodando = False



                elif evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:

                        rodando = False


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

                        rodando = False

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

                        if rect.collidepoint(
                            evento.pos
                        ):

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
                        else:
                            self.mostrar_mensagem(
                                "SOLUÇÃO INCORRETA",
                                VERMELHO
                            )
                        
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
                cor_mensagem
            )

            clock.tick(60)
        impressora.close()
        menuInicial().menu_principal()
        pygame.quit()
