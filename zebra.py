import random
import os

class zebra:
    def __init__(self,chave='12345'*6):
        self.path = r'./Categorias/'
        self.chave=str(chave)
    def chave(self):
        return self.chave
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
        tipo = tipo.upper()
        extraichave = (self.chave[dados1[0]-1],self.chave[5*dados1[0]-1+dados1[1]],self.chave[dados2[0]-1],self.chave[5*dados2[0]-1+dados2[1]])
        def corrigeGramatica(texto):
            texto = texto.upper()
            texto = texto.replace('QUEM A', 'A')
            texto = texto.replace('É,O','O')
            texto = texto.replace('QUEM O', 'O')
            texto = texto.replace('DE O ','DO ')
            return texto
        dica = 'Algo errado aconteceu'
        if tipo == 'POS':
            dica = f'Na posição {dados2[1]} fica quem {self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'MESMAPOS':
            dica = f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'ESQ':
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA A ESQUERDA DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'DIR':
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA A DIREITA DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'LADO':
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA AO LADO DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        return corrigeGramatica(dica)
    def geraDicas(self):
        regradicas = [
            ('MESMAPOS',(2,3),(1,3)),
            ('MESMAPOS',(2,5),(5,5)),
            ('MESMAPOS',(2,2),(3,2)),
            ('ESQ', (1,4),(1,5)),
            ('MESMAPOS', (1,4), (3,4)),
            ('MESMAPOS', (4,3), (5,3)),
            ('MESMAPOS', (1,1), (4,1)),
            ('POS',(0,0),(3,3)),
            ('POS',(0,0),(2,1)),
            ('LADO',(4,2),(5,1)),
            ('LADO',(5,2),(4,1)),
            ('MESMAPOS',(4,5),(3,5)),
            ('MESMAPOS',(2,4),(4,4)),
            ('LADO',(2,1),(1,2)),
            ('LADO',(4,2),(3,1)),
        ]
        dicas = []
        for regra in regradicas:
            dicas.append(self.geraDica(regra[0],regra[1],regra[2]))
        return dicas