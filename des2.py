from tables import ip_table

class DES:
    def text_to_bin(self, text):
        # Converte cada caractere da string em seu valor binário (8 bits para cada caractere)
        return ''.join(format(ord(char), '08b') for char in text)


    def text_to_binary_64bits(self, text):
        message_bin = self.text_to_bin(text)
        
        # Divide a mensagem em blocos de 64 bits
        blocks = [list(message_bin[i:i+64]) for i in range(0, len(message_bin), 64)]

        # Verifica se o último bloco tem menos de 64 bits e adiciona padding se necessário
        last_block = ''.join(blocks[-1])
        last_block_size = len(last_block)

        if last_block_size < 64:
            last_block = last_block.ljust(64, '0')
            print(last_block)
            blocks[-1] = list(last_block)
        
        return blocks
    

    def permute(self, blocks, table):
        # Função de permutação de bits baseado em uma tabela
        blocks_size = len(blocks)
        for i in range(blocks_size):
            permutation = [None]*64
            for j in range(len(table)):
                permutation[table[j]-1] = blocks[i][j]
            blocks[i] = permutation
        return blocks


    def encrypt(self, text, key=''):
        # Converte texto para blocos binários de 64 bits
        blocks = self.text_to_binary_64bits(text)

        # Permutação inicial
        text = self.permute(blocks, ip_table)
        
        # # Dividir o bloco em metades
        # left, right = self.split_bits(text)
        
        # # Gerar subchaves
        # subkeys = self;generate_subkeys(key)
        
        # # 16 rodadas de Feistel
        # for i in range(16):
        #     new_right = self;xor(left, self.function_f(right, subkeys[i]))
        #     left = right
        #     right = new_right
        
        # # Combinar as metades (esquerda e direita)
        # combined_block = right + left # Swap final das metades
        
        # # Permutação final
        # encrypted_block = self.permute(combined_block, final_permutation)
        
        # return encrypted_block