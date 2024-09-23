from des2 import DES

des = DES()

# Exemplo de uso
# text = input("Escreva um caracter para criptografar: ")
key = 'Bsdfd'
plaintext = "A"

# Criptografar
ciphertext = des.encrypt(plaintext, key)
# print("Texto criptografado:", ciphertext)
