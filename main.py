from des2 import DES

des = DES()

# Exemplo de uso
# text = input("Escreva um caracter para criptografar: ")
text = "A"

# Criptografar
ciphertext = des.encrypt(text)
# print("Texto criptografado:", ciphertext)

# Tabela de posições
# ip_table = [
#     57, 49, 41, 33, 25, 17, 9, 1,
#     59, 51, 43, 35, 27, 19, 11, 3,
#     61, 53, 45, 37, 29, 21, 13, 5,
#     63, 55, 47, 39, 31, 23, 15, 7,
#     56, 48, 40, 32, 24, 16, 8, 0,
#     58, 50, 42, 34, 26, 18, 10, 2,
#     60, 52, 44, 36, 28, 20, 12, 4,
#     62, 54, 46, 38, 30, 22, 14, 6
# ]

# # Primeira lista
# primeira_lista = ['0', '1', '1', '1', '0', '0', '1', '0', '0', '1', '1', '0', '1', '1',
# '0', '0', '0', '1', '1', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0',
# '1', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0',
# '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

# # Segunda lista
# segunda_lista = ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0',
# '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '0',
# '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '1', '0', '1', '0', '1', '0', '1',
# '0', '1', '0', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

# for i in range(len(primeira_lista)):
#     if primeira_lista[i] == segunda_lista[ip_table[i]]:
#         print(f'posição[{i}] da segunda lista esta correto')
#     else:
#         print(f'Está incorreta a posição[{i}] da segunda lista')
