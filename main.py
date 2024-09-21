from des2 import DES

des = DES()

# # Exemplo de uso
text = input("Escreva um caracter para criptografar: ")

# Criptografar
ciphertext = des.encrypt(text)
# print("Texto criptografado:", ciphertext)