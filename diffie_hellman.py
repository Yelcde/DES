from random import randint

class DiffieHellman:
    def choose_numbers(self):
        self.__n = 47
        self.__g = 3

        return self.__n, self.__g

    def calculate_a(self, n, g):
        self.__x = randint(0, 100)
        self.__a = (g ** self.__x) % n

        return self.__a
    
    def receive_from_a(self, n, g, a):
        self.__y = randint(0, 100)
        self.__b = (g ** self.__y) % n
        self.__sb = (a ** self.__y) % n

        return self.__b, str(self.__sb)
    
    def receive_from_b(self, b):
        self.__sa = (b ** self.__x) % self.__n
        
        return str(self.__sa)