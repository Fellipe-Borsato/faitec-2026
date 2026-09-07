import random
import os

class zebra:
    def __init__(self,chave='12345'*6):
        self.path = r'./Categorias/'
        self.chave=str(chave)

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

    def buscaValores(self,categoria,mostraValores=True,mostraVerbo=False):
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
                        valores.append(str(conteudo.index(linha)))
        if not mostraVerbo:
            valores.pop(0)
        return valores
    
    def buscaValor(self,dados):
        posicao = int(dados[1])
        for file in os.listdir(self.path):
            if int(file[0]) == int(dados[0]):
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
        categorias = self.buscaCategorias(False)
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

    def geraDica(self,tipo,dados1,dados2):

        if tipo.upper() == 'POSICIONAL':
            extraichave = (self.chave[dados2[0]],self.chave[5*dados2[0]+dados2[1]])
            print('---')
            print(extraichave)
            print('---')
            dica = f'Na posição {dados2[1]} fica quem {self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])+1))}'.upper().replace('QUEM A', 'A').replace('É,O','O').replace('QUEM O', 'O')
        else:
            dica = f'{self.buscaValor((extraichave[0],0)).replace('É,','')} {self.buscaValor((extraichave[0],extraichave[1]))}'
        extraichave = (self.chave[dados2[0]-1],self.chave[5*dados2[0]+dados2[1]])
        
        return dica
        

        

#print(zebra().pegaResposta())
#chavealeatoria = zebra().geraChave()
#print(chavealeatoria)
#print(zebra(chavealeatoria).pegaResposta())
#print(zebra(chavealeatoria).geraDica('posicional',(0,3),(3,3)))