import random
import os

class zebra:
    def __init__(self,chave='12345'):
        self.path = r'./Categorias/'
        self.chave=chave
    def buscaCategorias(self):
        if len(self.chave) > 5:
            self.chave = self.chave[0:5]
        categorias = []
        for file in os.listdir(self.path):
            if file[0] in self.chave:
                categorias.append(file)
        return categorias
    def buscaValores(self,chave='0'):
        pass
        
            
categorias = zebra('12345').buscaCategorias()
print(categorias)
        
'''123451234512345123451234512345
123451111122222333334444455555'''