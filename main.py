from des2 import DES

des = DES()

# Exemplo de uso
# text = input("Escreva um caracter para criptografar: ")
key = 'senha'
plaintext = "Hello World!!"

# Criptografar
ciphertext = des.encrypt(plaintext, key)
print(f'Texto Criptografado: {des.binary_to_text(ciphertext)}')

text = des.decrypt(ciphertext, key)
print(f'Texto Descriptografado: {des.binary_to_text(text)}')
# print("Texto criptografado:", ciphertext)
