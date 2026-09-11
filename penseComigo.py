from zebra import zebra
from thermal import thermal

def main():
    impressora = thermal()
    chave = '34798:36754:39621:31742:52749:92657:59941'# zebra().geraChave()
    #chave = zebra().geraChave()
    puzzle = zebra()
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
      for resposta in puzzle.pegaResposta():
        print(resposta)
      
       

if __name__ == "__main__":
    main()