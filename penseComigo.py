from zebra import zebra
from thermal import thermal

from interface.mainInterface import (
    executar_interface
)

from interface.config.cores import (
    CINZA,
    VERDE,
    VERMELHO
)


def main():

    gerador = zebra()
    chave = gerador.geraChave()
    puzzle = zebra("23798:39457:83295:59168:15826:16784:13973")
    dicas = puzzle.geraDicas()
    respostas = puzzle.pegaResposta()
    for resposta in range(len(respostas)):
        listasol = []
        dicionario_ordenado = dict(sorted(respostas[resposta].items()))
        respostas[resposta] = dicionario_ordenado
        for key,value in respostas[resposta].items():
            listasol.append(value)
        respostas[resposta] = listasol
    print(respostas)

    categorias = puzzle.buscaCategorias(mostraValores=True,mostraTodas=False)
    #impressora = thermal()
    impressora = False
    if impressora:
        impressora.fonte(True)
        for dica in dicas:
            impressora.print_text(dica)
        impressora.print_text()
        impressora.center(True)
        impressora.print_text(puzzle.chaveFormatada())
        impressora.cut()
    else:
        for dica in dicas:
            print(dica)
        print()
        print(puzzle.chaveFormatada())
        print()

    dados_categorias = {}
    for categoria in categorias:
        codigo = None
        for i in range(1, 10):
            nome = puzzle.buscaCategoria(str(i))
            if nome.upper() == categoria.upper():
                codigo = str(i)
                break
        if codigo is not None:
            dados_categorias[categoria] = (
                puzzle.buscaValores(codigo,mostraValores=True))


    tabela_jogador = [
        [None for _ in categorias]
        for _ in range(5)
    ]

    mensagem_jogo = ""
    cor_mensagem = CINZA


    def mostrar_mensagem(
        mensagem,
        cor=CINZA
    ):

        nonlocal mensagem_jogo
        nonlocal cor_mensagem

        mensagem_jogo = mensagem
        cor_mensagem = cor

    def obter_mensagem():

        return mensagem_jogo, cor_mensagem




    def selecionar_valor(
        valor,
        casa_selecionada,
        categoria_selecionada
    ):

        casa = casa_selecionada

        categoria = categoria_selecionada

        valor_atual = tabela_jogador[
            casa
        ][categoria]



        if valor_atual == valor:

            tabela_jogador[
                casa
            ][categoria] = None

            mostrar_mensagem(
                "Valor removido.",
                CINZA
            )

            return



        for outra_casa in range(5):

            if outra_casa == casa:
                continue

            if tabela_jogador[
                outra_casa
            ][categoria] == valor:

                mostrar_mensagem(
                    f"Valor já está na CASA {outra_casa + 1}.",
                    VERMELHO
                )

                return


        tabela_jogador[
            casa
        ][categoria] = valor

        mostrar_mensagem(
            f"{valor} → CASA {casa + 1}",
            VERDE
        )

    executar_interface(
        categorias,
        dicas,
        respostas,
        dados_categorias,
        tabela_jogador,
        selecionar_valor,
        mostrar_mensagem,
        obter_mensagem
    )


if __name__ == "__main__":

    main()