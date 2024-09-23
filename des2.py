from tables import ip_table


class DES:
    def __text_to_bin(self, text):
        # Converte cada caractere em seu valor binário (8 bits para cada caractere)
        return ''.join(format(ord(char), '08b') for char in text)

    def __text_to_binary_blocks_64bits(self, text):
        message_bin = self.__text_to_bin(text)

        # Divide a mensagem em blocos de 64 bits
        blocks = [list(message_bin[i:i+64]) for i in range(0, len(message_bin), 64)]

        # Verifica se o último bloco tem menos de 64 bits e adiciona padding se necessário
        last_block = ''.join(blocks[-1])
        last_block_size = len(last_block)

        if last_block_size < 64:
            last_block = last_block.ljust(64, '0')
            blocks[-1] = list(last_block)

        return blocks

    def __permute(self, block, table, block_size = 64):
        # Função de permutação de bits baseado em uma tabela
        permutation = [None] * block_size
        for table_index in range(len(table)):
            dest_index = table[table_index] - 1
            permutation[table_index] = block[dest_index]

        return permutation

    def __split_block(self, block):
        # Divide o bloco em duas metades
        return block[:32], block[32:]

    def __proccess_key(self, key):
        key_bin = self.__text_to_bin(key)
        key_bin_size = len(key_bin)

        if key_bin_size < 64:
            key_bin = key_bin.ljust(64, '0')

        return list(key_bin)

    def encrypt(self, text, key=''):
        # Converte texto para blocos binários de 64 bits
        blocks = self.__text_to_binary_blocks_64bits(text)

        # Converte chave de criptografia para binário
        key_bin = self.__proccess_key(key)

        for block in blocks:
            # Permutação inicial
            permuted_block = self.__permute(block, ip_table)

            # Divide bloco em esquerda e direita
            left_side, right_side = self.__split_block(permuted_block)

        # Gerar subchaves
        # subkeys = self;generate_subkeys(key)

        # 16 rodadas de Feistel
        # for i in range(16):
        #     new_right = self;xor(left, self.function_f(right, subkeys[i]))
        #     left = right
        #     right = new_right

        # Combinar as metades (esquerda e direita)
        # combined_block = right + left # Swap final das metades

        # Permutação final
        # encrypted_block = self.permute(combined_block, final_permutation)

        # return encrypted_block
