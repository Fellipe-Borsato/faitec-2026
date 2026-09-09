from zebra import zebra
from thermal import thermal

def main():
    impressora = thermal()
    chave = 2314543152415235312453412243513# zebra().geraChave()
    #chave = zebra().geraChave()
    puzzle = zebra(chave)
    dicas = puzzle.geraDicas()
    if impressora:
      impressora.fonte(True)
      for dica in dicas:
        impressora.print_text(dica)
      impressora.print_text()
      impressora.print_text(puzzle.chave)
      impressora.cut()
    else:
      for dica in dicas:
        print(dica)
      print()
      print(puzzle.chave)
       

if __name__ == "__main__":
    main()