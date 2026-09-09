from zebra import zebra
from thermal import thermal

def main():
    impressora = thermal()
    #chave = 12345123451234512345123451234599991# zebra().geraChave()
    chave = zebra().geraChave()
    puzzle = zebra(chave)
    dicas = puzzle.geraDicas()
    if impressora:
      impressora.fonte(True)
      for dica in dicas:
        impressora.print_text(dica)
      impressora.print_text()
      impressora.center(True)
      impressora.print_text(puzzle.chave)
      impressora.cut()
    else:
      for dica in dicas:
        print(dica)
      print()
      print(puzzle.chave)
      print(puzzle.pegaResposta())
       

if __name__ == "__main__":
    main()