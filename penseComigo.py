from zebra import zebra
from thermal import thermal
from interface import interface
def main():
    impressora = thermal()
    chave = '34798:36754:39621:31742:52749:92657:59941'# zebra().geraChave()
    chave = zebra().geraChave()
    puzzle = zebra(chave)
    dicas = puzzle.geraDicas()
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
      valores = {}
      for resposta in puzzle.pegaResposta():
        for chave, valor in resposta.items():
           if chave not in valores.keys():
              valores[chave] = []
           valores[chave].append(valor)
        print(resposta)
      print(valores)
      print(puzzle.buscaValores(puzzle.chave[0],mostraTodos=False))
      categorias = puzzle.buscaCategorias()
      categorias.sort()
    ui = interface()
    ui.popular_categorias(categorias)
    ui.popular_valores(valores)
    ui.popular_dicas(puzzle.geraDicas())
    ui.executar()
       

if __name__ == "__main__":
    main()