from des import DES
from diffie_hellman import DiffieHellman

dh = DiffieHellman()

des_alice = DES()
des_bob = DES()

text = 'Olá, Bob! Como vai?'

# Escolhe os números N e G
n, g = dh.choose_numbers()

# Calcula o valor de *a* e o segredo de Alice
a = dh.calculate_a(n, g)

# Calcula o valor de *b* e o segredo de Bob
# Após os cálculos gera a chave de Bob
b, key_bob = dh.receive_from_a(n, g, a) 

# Recebe o valor de B e gera a chave de Alice
key_alice = dh.receive_from_b(b)

# Alice envia uma mensagem criptografada para Bob
cripted = des_alice.encrypt(text=text, key=key_alice)
print('Alice encripta a mensagem e gera:', cripted)

# Bob decripta a mensagem criptografada de Alice
decrypted = des_bob.decrypt(text=cripted, key=key_bob)
print('Bob decripta a mensagem e visualiza:', decrypted)