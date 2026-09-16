from datetime import datetime
import math
import os


# ==========================
# CLASSE
# ==========================

class Aluno:
    def __init__(self, nome, idade, notas):
        self.nome = nome
        self.idade = idade
        self.notas = notas

    def media(self):
        return sum(self.notas) / len(self.notas)

    def situacao(self):
        media = self.media()

        if media >= 7:
            return "APROVADO"
        elif media >= 5:
            return "RECUPERAÇÃO"
        else:
            return "REPROVADO"


# ==========================
# FUNÇÕES
# ==========================

def calcular_fatorial(numero):
    if numero < 0:
        raise ValueError("O número não pode ser negativo.")

    resultado = 1

    for i in range(1, numero + 1):
        resultado *= i

    return resultado


def verificar_primo(numero):
    if numero < 2:
        return False

    for i in range(2, int(math.sqrt(numero)) + 1):
        if numero % i == 0:
            return False

    return True


def maior_numero(lista):
    return max(lista)


# ==========================
# PROGRAMA PRINCIPAL
# ==========================

print("=" * 50)
print("        TESTE COMPLETO DE PYTHON")
print("=" * 50)

print("\n[1] Testando operações matemáticas...")

a = 15
b = 4

print(f"Soma: {a + b}")
print(f"Subtração: {a - b}")
print(f"Multiplicação: {a * b}")
print(f"Divisão: {a / b:.2f}")
print(f"Potência: {a ** 2}")


# ==========================
# LISTAS
# ==========================

print("\n[2] Testando listas...")

numeros = [10, 25, 7, 42, 18, 31]

print("Lista:", numeros)
print("Maior número:", maior_numero(numeros))
print("Menor número:", min(numeros))
print("Soma:", sum(numeros))
print("Média:", sum(numeros) / len(numeros))


# ==========================
# DICIONÁRIO
# ==========================

print("\n[3] Testando dicionários...")

produto = {
    "nome": "Computador Gamer",
    "preco": 2500,
    "estoque": 15,
    "categoria": "Informática"
}

print("Produto:", produto["nome"])
print("Preço: R$", produto["preco"])
print("Estoque:", produto["estoque"])
print("Categoria:", produto["categoria"])


# ==========================
# FUNÇÃO
# ==========================

print("\n[4] Testando funções...")

numero = 5

print(f"Fatorial de {numero}:", calcular_fatorial(numero))

for n in [2, 3, 4, 7, 11, 15]:
    resultado = verificar_primo(n)
    print(f"{n} é primo? {resultado}")


# ==========================
# CLASSE E OBJETO
# ==========================

print("\n[5] Testando classes e objetos...")

aluno = Aluno(
    "Carlos",
    20,
    [8.5, 7.0, 9.0, 6.5]
)

print("Nome:", aluno.nome)
print("Idade:", aluno.idade)
print("Notas:", aluno.notas)
print(f"Média: {aluno.media():.2f}")
print("Situação:", aluno.situacao())


# ==========================
# LOOP
# ==========================

print("\n[6] Testando loops...")

print("Contagem:")

for i in range(1, 11):
    print(i, end=" ")

print()


# ==========================
# LIST COMPREHENSION
# ==========================

print("\n[7] Testando List Comprehension...")

pares = [n for n in range(1, 21) if n % 2 == 0]

print("Números pares de 1 a 20:")
print(pares)


# ==========================
# TRATAMENTO DE ERROS
# ==========================

print("\n[8] Testando tratamento de erros...")

try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Erro capturado: não é possível dividir por zero!")


try:
    numero = int("abc")
except ValueError:
    print("Erro capturado: valor inválido!")


# ==========================
# ARQUIVOS
# ==========================

print("\n[9] Testando criação de arquivo...")

nome_arquivo = "teste_python.txt"

with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
    arquivo.write("Python está funcionando corretamente!\n")
    arquivo.write("Arquivo criado pelo teste do VS Code.\n")

print(f"Arquivo '{nome_arquivo}' criado com sucesso.")


with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()

print("Conteúdo do arquivo:")
print(conteudo)


# ==========================
# SISTEMA
# ==========================

print("[10] Informações do sistema...")

print("Sistema operacional:", os.name)
print("Diretório atual:", os.getcwd())
print("Data e hora:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


# ==========================
# FINAL
# ==========================

print("\n" + "=" * 50)
print("       TODOS OS TESTES FORAM EXECUTADOS!")
print("=" * 50)
print("Seu Python está funcionando no VS Code.")