from tables import ip_table, pc1_table, shift_schedule, pc2_table, e_box_table


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

    def __remove_parity_bits(self, key):
        key_56_bits = ''
    
        for i in range(0, len(key), 8):
            # Pega os primeiros 7 bits de cada bloco de 8 bits e os adiciona à chave de 56 bits
            key_56_bits += key[i:i+7]  # Pega os 7 primeiros bits (descarta o 8º bit)
        
        return list(key_56_bits)

    def __left_shift(self, bits, n_shifts):
        # Executa uma rotação circular a esquerda
        return bits[n_shifts:] + bits[:n_shifts]

    def __generate_subkeys(self, key):
        # Gera as 16 subchaves de 48 bits a partir da chave de 64 bits
        
        # 1. Remove os bits de paridade para obter a chave de 56 bits
        key_56_bits = self.__remove_parity_bits(key)

        # 2. Aplica PC-1 à chave de 56 bits
        key_56_bits = self.__permute(key, pc1_table, 56)


        # Divide a chave de 56 bits em dois blocos de 28 bits
        C = key_56_bits[:28]
        D = key_56_bits[28:]

        subkeys = []

        # 3. Para cada rodada (16 no total), execute as operações:
        for round_num in range(16):
            # 4. Rotaciona os blocos C e D à esquerda com base na tabela de shifts
            n_shifts = shift_schedule[round_num]
            C = self.__left_shift(C, n_shifts)
            D = self.__left_shift(D, n_shifts)

            # 5. Junta C e D para formar 56 bits e aplica PC-2 para obter 48 bits
            combined = C + D
            subkey = self.__permute(combined, pc2_table, 48)

            # Armazena a subchave
            subkeys.append(subkey)

        return subkeys

    def __xor(self, expanded_right, subkey):
        xored = ''.join('1' if expanded_right[i] != subkey[i] else '0' for i in range(48))
        return xored

    def __sbox_substitution(self, block):
        # Aplica as S-Boxes nos blocos de 6 bits

        # Divide o bloco em 8 blocos de 6 bits
        for i in range(8):
            six_bits = block[i*6:(i+1)*6]

            row = int(six_bits[0] + six_bits[5], 2)  # Combina o primeiro e o último bit para a linha
            col = int(six_bits[1:5], 2)  # Combina os bits do meio para a coluna
            sbox_value = S_BOXES[i][row][col]  # Procura o valor na S-Box

            output += self.__text_to_bin(sbox_value)  # Converte o valor de 4 bits para string binária

        return output

    def __function_f(self, right, subkey):
        # Expansão do lado direito
        expanded = self.__permute(right, e_box_table, 48)

        # XOR com a subchave
        xor_output = self.__xor(expanded, subkey)

        # Substituição (S-Boxes)


        # return permute(xor_output, permutation_table)

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
            subkeys = self.__generate_subkeys(''.join(key_bin))

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
