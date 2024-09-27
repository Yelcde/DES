from des import DES

des = DES()

key = 'senha'
plaintext = "Hello World!!"

ciphertext = des.encrypt(plaintext, key)
print(f'Texto Criptografado: {ciphertext}')

text = des.decrypt(ciphertext, key)
print(f'Texto Descriptografado: {text}')
