from zebra import zebra
from thermal import thermal
from menupensaComigo import menuInicial

def start():
    """
    puzzle = zebra('64189479859314279538168975386147791')
    #puzzle.geraChave()
    print(puzzle.chaveFormatada())
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
    impressora = thermal()
    impressora = False
    if impressora:
        impressora.fonte(True)
        for dica in dicas:
            impressora.print_text(dica)
        impressora.print_text()
        impressora.center(True)
        impressora.print_text(puzzle.chaveFormatada())
        for n in range(0, 35, 5):
            impressora.print_barcode(puzzle.chave[n:n+5])
        #impressora.print_barcode(puzzle.chave)
        impressora.cut()
        pass
    else:
        for dica in dicas:
            print(dica)
        print()
        print(puzzle.chaveFormatada())
        print()
"""
    menuInicial().menu_principal()



if __name__ == "__main__":

    start()