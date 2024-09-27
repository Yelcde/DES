from des import DES
from diffie_hellman import DiffieHellman

dh = DiffieHellman()

des_alice = DES()
des_bob = DES()

text = 'Olá, Bob! Como vai?'

n, g = dh.choose_numbers()
a = dh.calculate_a(n, g)
b, key_bob = dh.receive_from_a(n, g, a)
key_alice = dh.receive_from_b(b)

cripted = des_alice.encrypt(text=text, key=key_alice)
print('Alice encripta a mensagem e gera:', cripted)

decrypted = des_bob.decrypt(text=cripted, key=key_bob)
print('Bob decripta a mensagem e visualiza:', decrypted)