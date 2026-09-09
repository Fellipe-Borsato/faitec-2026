import random
import os

class zebra:
    def __init__(self,chave='12345'*6+'1'):
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
        chave += str(random.randint(1,3))
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
            if dados1[1] != dados2[1]:
                raise Exception(f'Dica inválida: {dados1} não fica na mesma posição de {dados2}')
            dica = f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'ESQ':
            if dados2[1] - dados1[1] != 1:
                raise Exception(f'Dica inválida: {dados1} não fica exatamente a esquerda de {dados2}')
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA A ESQUERDA DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'ESQ+':
            if dados2[1] - dados1[1] < 1:
                raise Exception(f'Dica inválida: {dados1} não a esquerda de {dados2}')
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA A ALGUM LUGAR PARA A ESQUERDA DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'DIR':
            if dados1[1] - dados2[1] != 1:
                raise Exception(f'Dica inválida: {dados1} não fica exatamente a direita de {dados2}')
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA A DIREITA DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'DIR+':
            if dados1[1] - dados2[1] < 1:
                raise Exception(f'Dica inválida: {dados1} não fica exatamente a direita de {dados2}')
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA A ALGUM LUGAR PARA A DIREITA DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'LADO':
            if abs(dados1[1] - dados2[1]) != 1:
                raise Exception(f'Dica inválida: {dados1} não fica ao lado de {dados2}')
            dica = 'QUEM '
            dica += f'{self.buscaValor((int(extraichave[0]),0))} {self.buscaValor((int(extraichave[0]),int(extraichave[1])))}'
            dica += ' FICA AO LADO DE QUEM '
            dica += f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
        elif tipo == 'PONTA':
            if dados2[1] != 5 and dados2[1] != 1:
                raise Exception(f'Dica inválida: {dados2} não fica na ponta')
            dica = f'{self.buscaValor((int(extraichave[2]),0))} {self.buscaValor((int(extraichave[2]),int(extraichave[3])))}'
            dica += ' ESTÁ EM UMA DAS PONTAS'
        return corrigeGramatica(dica)
    def geraDicas(self):
        regras = []
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
        regras.append(regradicas)
        regradicas = [
            ('POS',(0,0),(2,5)),
            ('DIR',(2,5),(2,4)),
            ('PONTA',(0,0),(2,1)),
            ('POS',(0,0),(3,4)),
            ('MESMAPOS',(2,4),(5,4)),
            ('MESMAPOS',(2,4),(1,4)),
            ('ESQ+',(1,4),(5,5)),
            ('LADO',(1,4),(2,3)),
            ('DIR',(4,2),(1,1)),
            ('LADO',(4,4),(5,5)),
            ('MESMAPOS',(4,2),(5,2)),
            ('MESMAPOS',(1,3),(5,3)),
            ('ESQ+',(1,2),(5,3)),
            ('DIR+',(4,5),(1,3)),
            ('LADO',(1,3),(3,4)),
            ('LADO',(3,3),(4,4)),
            ('ESQ',(3,4),(3,5)),
            ('ESQ+',(3,2),(3,5)),
            ('DIR',(3,2),(3,1))
        ]
        regras.append(regradicas)
        regradicas = [
            ('MESMAPOS',(2,2),(4,2)),
            ('MESMAPOS',(4,2),(3,2)),
            ('POS',(0,0),(1,3)),
            ('MESMAPOS',(2,4),(4,4)),
            ('MESMAPOS',(2,1),(1,1)),
            ('ESQ',(2,1),(3,2)),
            ('DIR',(5,4),(3,3)),
            ('MESMAPOS',(2,3),(5,3)),
            ('LADO',(3,4),(1,5)),
            ('MESMAPOS',(5,1),(4,1)),
            ('MESMAPOS',(2,5),(4,5)),
            ('DIR',(2,5),(5,4)),
            ('MESMAPOS',(1,2),(5,2)),
            ('LADO',(4,5),(1,4)),
            ('PONTA',(0,0),(3,5)),
            ('MESMAPOS',(1,3),(4,3)),
            ('LADO',(3,5),(3,4)),
            ('MESMAPOS',(5,2),(4,2))
        ]
        regras.append(regradicas)
        regradicas = regras[int(self.chave[-1])-1]
        random.shuffle(regradicas)
        dicas = []
        for regra in regradicas:
            dicas.append(self.geraDica(regra[0],regra[1],regra[2]))
        return dicas