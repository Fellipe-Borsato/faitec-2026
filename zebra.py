import random
import os

class zebra:
    def __init__(self,chave='12345'*5):
        self.path = r'./Categorias/'
        self.chave=chave
    def buscaCategorias(self,mostraValores=True):
        categorias = []
        for file in os.listdir(self.path):
            if file[0] in self.chave:
                if mostraValores:
                    categorias.append(file.split('.')[1])
                else:
                    categorias.append(file.split('.')[0])
        return categorias
    def buscaCategoria(self,categoria):
        categoria = str(categoria)
        for file in os.listdir(self.path):
            if file[0] in categoria:
                nome = file[2:].replace('.txt','')
        return nome

    def buscaValores(self,categoria,mostraValores=True):
        categoria = str(categoria)
        valores = []
        for file in os.listdir(self.path):
            if file[0] == categoria:
                fileopen = open(self.path + file, encoding="utf-8")
                conteudo = fileopen.readlines()
                for linha in conteudo:
                    if mostraValores:
                        valores.append(linha.strip())
                    else:
                        valores.append(str(conteudo.index(linha)+1))
        return valores
    
    def buscaValor(self,dados):
        posicao = int(dados[1])-1
        for file in os.listdir(self.path):
            if file[0] == dados[0]:
                fileopen = open(self.path + file, encoding="utf-8")
                conteudo = fileopen.readlines()
                return conteudo[posicao].strip()
        else:
            return False
    
    def pegaResposta(self):
        respostas = []
        for valor in range(5):
            resposta={}
            for categoria in range(5):
                nomeCategoria = self.buscaCategoria(self.chave[categoria])
                valorCategoria = self.buscaValor((self.chave[categoria],self.chave[5*categoria+valor]))
                resposta[nomeCategoria] = valorCategoria
            respostas.append(resposta)
        return respostas
    
    def geraChave(self):
        chave = ''
        categorias = []
        for file in os.listdir(self.path):
            categorias.append(file[0])
        escolhas = []
        for _ in range(5):
            escolha = random.randrange(len(categorias))
            chave += categorias.pop(escolha)
        for _ in range(5):
            valores = self.buscaValores(chave[_],False)
            for k in range(5):
                escolha = random.randrange(len(valores))
                chave+= valores.pop(escolha)
                

        return chave
        


chavealeatoria = zebra().geraChave()
print(chavealeatoria)
print(zebra(chavealeatoria).pegaResposta())
'''123451234512345123451234512345
123451111122222333334444455555'''