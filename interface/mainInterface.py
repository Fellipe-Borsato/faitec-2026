import pygame

from interface.ui.interface import (
    desenhar_interface
)

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
    obter_rect_verificar
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


def executar_interface(
    categorias,
    dicas,
    resposta,
    chave_formatada,
    dados_categorias,
    tabela_jogador,
    selecionar_valor,
    mostrar_mensagem,
    obter_mensagem
):

    pygame.init()

    info = pygame.display.Info()

    largura = info.current_w
    altura = info.current_h

    janela = pygame.display.set_mode(
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

    while rodando:

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            # ==================================================
            # SAIR
            # ==================================================

            if evento.type == pygame.QUIT:

                rodando = False

            # ==================================================
            # TECLADO
            # ==================================================

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    rodando = False

            # ==================================================
            # SCROLL DAS DICAS
            # ==================================================

            elif evento.type == pygame.MOUSEWHEEL:

                if painel_esquerdo.collidepoint(
                    mouse_pos
                ):

                    total_paginas = (
                        obter_total_paginas_dicas(
                            dicas,
                            painel_esquerdo
                        )
                    )

                    if evento.y < 0:

                        if pagina_dicas < total_paginas - 1:

                            pagina_dicas += 1

                    elif evento.y > 0:

                        if pagina_dicas > 0:

                            pagina_dicas -= 1

            # ==================================================
            # CLIQUE
            # ==================================================

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button != 1:
                    continue

                # ----------------------------------------------
                # PAGINAÇÃO
                # ----------------------------------------------

                botao_anterior, botao_proximo = (
                    obter_botoes_paginacao(
                        painel_esquerdo
                    )
                )

                total_paginas = (
                    obter_total_paginas_dicas(
                        dicas,
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

                # ----------------------------------------------
                # MINIMIZAR
                # ----------------------------------------------

                if botao_minimizar.collidepoint(
                    evento.pos
                ):

                    pygame.display.iconify()

                    continue

                # ----------------------------------------------
                # FECHAR
                # ----------------------------------------------

                if botao_fechar.collidepoint(
                    evento.pos
                ):

                    rodando = False

                    continue

                # ----------------------------------------------
                # CASAS
                # ----------------------------------------------

                for i, rect in enumerate(
                    obter_rect_casas(
                        painel_central
                    )
                ):

                    if rect.collidepoint(
                        evento.pos
                    ):

                        casa_selecionada = i

                        mostrar_mensagem(
                            f"CASA {i + 1} selecionada.",
                            AMARELO
                        )

                        break

                # ----------------------------------------------
                # DICAS
                # ----------------------------------------------

                for indice, rect in obter_rect_dicas(
                    painel_esquerdo,
                    dicas,
                    pagina_dicas
                ):

                    if rect.collidepoint(
                        evento.pos
                    ):

                        dica_selecionada = indice

                        mostrar_mensagem(
                            f"Dica {indice + 1} selecionada.",
                            AMARELO
                        )

                        break

                # ----------------------------------------------
                # CATEGORIAS
                # ----------------------------------------------

                for i, rect in enumerate(
                    obter_rect_categorias(
                        painel_direito,
                        categorias
                    )
                ):

                    if rect.collidepoint(
                        evento.pos
                    ):

                        categoria_selecionada = i

                        mostrar_mensagem(
                            f"{categorias[i]} selecionada.",
                            AMARELO
                        )

                        break

                # ----------------------------------------------
                # VALORES
                # ----------------------------------------------

                for valor, rect in obter_rect_valores(
                    painel_direito,
                    categorias,
                    dados_categorias,
                    categoria_selecionada
                ):

                    if rect.collidepoint(
                        evento.pos
                    ):

                        selecionar_valor(
                            valor,
                            casa_selecionada,
                            categoria_selecionada
                        )

                        break

                # ----------------------------------------------
                # VERIFICAR
                # ----------------------------------------------

                rect_verificar = obter_rect_verificar(
                    largura,
                    altura,
                    RODAPE
                )

                if rect_verificar.collidepoint(
                    evento.pos
                ):

                    print()
                    print("============================")
                    print("SOLUÇÃO DO ENIGMA")
                    print("============================")
                    print(resposta)

                    mostrar_mensagem(
                        "Verificação enviada ao console.",
                        VERDE
                    )

        # ======================================================
        # DESENHO
        # ======================================================

        mensagem_jogo, cor_mensagem = obter_mensagem()

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
            dicas,
            dica_selecionada,
            pagina_dicas,
            chave_formatada,
            categorias,
            tabela_jogador,
            casa_selecionada,
            dados_categorias,
            categoria_selecionada,
            mensagem_jogo,
            cor_mensagem
        )

        clock.tick(60)

    pygame.quit()
