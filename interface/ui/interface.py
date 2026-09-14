import pygame

from interface.config.cores import FUNDO

from interface.ui.componentes import painel

from interface.ui.cabecalho.cabecalho import (
    desenhar_cabecalho
)

from interface.ui.dicas.dicas import (
    desenhar_dicas
)

from interface.ui.casas.casas import (
    desenhar_casas
)

from interface.ui.investigacao.investigacao import (
    desenhar_investigacao
)

from interface.ui.rodape.rodape import (
    desenhar_rodape
)


def desenhar_interface(
    janela,
    mouse_pos,
    largura,
    altura,

    topo,
    rodape,

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
):

    janela.fill(
        FUNDO
    )


    desenhar_cabecalho(
        janela,
        mouse_pos,
        largura,
        topo,
        botao_minimizar,
        botao_fechar,
        chave_formatada
    )

    desenhar_dicas(
        janela,
        painel_esquerdo,
        dicas,
        dica_selecionada,
        pagina_dicas
    )


    painel(
        janela,
        painel_central
    )

    desenhar_casas(
        janela,
        painel_central,
        categorias,
        tabela_jogador,
        casa_selecionada
    )


    desenhar_investigacao(
        janela,
        mouse_pos,
        painel_direito,
        categorias,
        dados_categorias,
        tabela_jogador,
        casa_selecionada,
        categoria_selecionada
    )



    desenhar_rodape(
        janela,
        mouse_pos,
        largura,
        altura,
        rodape,
        painel_esquerdo,
        mensagem_jogo,
        cor_mensagem
    )

    pygame.display.flip()
