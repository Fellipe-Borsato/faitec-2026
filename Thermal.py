import usb.core
import usb.util
import libusb_package
class thermal:
    def __init__(self):
        self.maxchars = 32
        self.backend = libusb_package.get_libusb1_backend() #Faz a ponte entre o python e o Usb do Windows
        self.device = usb.core.find(
            idVendor=0x0416, #Vendor da impressora termica, conforme consta na documentação
            idProduct=0x5011, #Id da impressora termica, conforme consta na documentação
            backend=self.backend
        )
        if self.device is None:
            return
            raise Exception("Printer not found!") #Dá erro se não encontrar impressora
        self.device.set_configuration() #Inicializa a funcionalidade USB
        self.device.write(0x01, b"\x1b\x40") #Inicializa / reseta a impressora (P.19 do manual)
        self.device.write(0x01, b"\x1b\x74\x03") #Seleciona a língua de impressao (Pra aparecer ã, é, etc) (P.27 do manual, consta na documentação)
    def __bool__(self):
        return self.device is not None
    
    def print_text(self, text=''):
        text = str(text)+'\n'
        paragraphs = text.split('\n') #Se o texto enviado já tiver quebra de linha, respeita, então separa em uma lista
        output_lines = []
        for paragraph in paragraphs:
            if not paragraph.strip(): #Caso tenha uma linha vazia
                output_lines.append('') #Coloca pra imprimir
                continue
            words = paragraph.split() #Separa por palavras
            current_line = ''
            for word in words:
                if len(current_line) + len(word) + 1 <= self.maxchars: #O tamanho da linha atual mais a palavra + 1 é menor do que o número máximo?
                    if current_line:
                        current_line += ' ' + word #Adiciona a palavra inteira na linha a ser impressa
                    else:
                        current_line = word #Imprime só a palavra
                else:
                    if current_line: #Se tem coisa a ser impressa
                        output_lines.append(current_line)  #Coloca pra imprimir
                    while len(word) > self.maxchars: #Se a palavra for muito grande, mais que 32 caracteres
                        output_lines.append(word[:self.maxchars]) #Coloca o que cabe
                        word = word[self.maxchars:] #Tira a parte que coube e repete
                    current_line = word
            if current_line:
                output_lines.append(current_line) #Poe pra imprimir
        output = '\n'.join(output_lines) #Junta a lista com quebra de linha
        self.device.write(0x01,output.encode('cp860')) #Manda pra impressora

    def print_qr(self, data):
        data = data.encode("utf-8")
        #Configuração dum tanto de coisa pra imprimir QR code
        self.device.write(0x01, b"\x1d\x28\x6b\x04\x00\x31\x41\x32\x00")

        # Tamanho
        self.device.write(0x01, b"\x1d\x28\x6b\x03\x00\x31\x43\x05")

        # Correção de erro (Coisa de qr code) = L
        self.device.write(0x01, b"\x1d\x28\x6b\x03\x00\x31\x45\x30")

        # Guarda os dados
        length = len(data) + 3
        pL = length & 0xFF
        pH = (length >> 8) & 0xFF

        command = (b"\x1d\x28\x6b" + bytes([pL, pH]) + b"\x31\x50\x30" + data) #Prepara tudo pra imprimir

        self.device.write(0x01, command) #Manda pra impressora
        self.device.write(0x01, b"\x1d\x28\x6b\x03\x00\x31\x51\x30") #Imprime

    def underline(self, toggle=False):
        if toggle:
            self.device.write(0x01, b"\x1b\x2d\x32") #Sublinha (P.16/17 do manual)
        else:
            self.device.write(0x01, b"\x1b\x2d\x00")

    def center(self, toggle=False):
        if toggle:
            self.device.write(0x01, b"\x1b\x61\x01") #Centraliza (p.25 do manual)
        else:
            self.device.write(0x01, b"\x1b\x61\x00")

    def fonte(self, toggle=False):
        if toggle:
            self.device.write(0x01, b"\x1b\x21\x01") #Fonte B (p.8/9 do manual)
            self.maxchars = 42
        else:
            self.device.write(0x01, b"\x1b\x21\x00") #Fonte A
            self.maxchars = 32

    def cut(self):
        self.print_text("\n\n\n\n\n") #Poe quebra de linha no final pra poder rasgar o papel
  
    def __del__(self): #Quando a classe for fechada, libera a impressora
        try:
            if self.device is not None:
                usb.util.dispose_resources(self.device)
        except:
            pass
