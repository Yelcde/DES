from tables import *


class DES:
    def __decimal_to_binary(self, decimal):
        if decimal == 0:
            return '0000'  # Retorna '0' se o número for zero
        
        binary = ''
        
        while decimal > 0:
            bit = decimal % 2  # Obtém o bit menos significativo
            binary = str(bit) + binary  # Adiciona o bit à frente da string
            decimal //= 2  # Divide o decimal por 2 (desloca para a direita)
        
        if len(str(binary)) < 4:
            binary = binary.rjust(4, '0')

        return str(binary)


    def __binary_to_decimal(self, binario):
        decimal = 0
        length = len(binario)
        
        for i in range(length):
            # Converte cada dígito binário em decimal
            bit = int(binario[length - 1 - i])  # Acessa os bits de trás para frente
            decimal += bit * (2 ** i)  # Contribui para o total decimal
        
        return decimal

    def __text_to_bin(self, text, bits='08b'):
        # Converte cada caractere em seu valor binário (8 bits para cada caractere)
        return ''.join(format(ord(char), bits) for char in text)

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
        print(len(block))
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

    def __xor(self, expanded_right, subkey, len_range=48):
        xored = ''

        for bit in range(len_range):
            if expanded_right[bit] == subkey[bit]:
                xored += '0'
            else: 
                xored += '1'

        return xored

    def __sbox_substitution(self, sBox_entrance):
        sBox_chosen = 0
        replacement = ''
        for entrance in sBox_entrance:
            linha = entrance[0] + entrance[-1]
            linha = self.__binary_to_decimal(linha)
            coluna = self.__binary_to_decimal(''.join(entrance[1:5]))

            sBox_number = s_boxes[sBox_chosen][linha][coluna]

            replacement += self.__decimal_to_binary(sBox_number)

            sBox_chosen += 1

        return replacement

    def __function_f(self, right_side, subkey):
        # Expansão do lado direito
        expanded_right_side = self.__permute(right_side, e_box_table, 48)

        # XOR com a subchave
        xor = self.__xor(expanded_right_side, subkey)

        # Substituição (S-Boxes)
        sBox_entrance = []

        for i in range(0, len(xor), 6): # Separando XOR em grupos de 6
            entrance = list(xor[i:i+6])
            sBox_entrance.append(entrance)
        
        # Fazendo substituição com s_boxes
        replacement = self.__sbox_substitution(sBox_entrance)

        # Permutando depois de fazer a substituição
        replacement_permuted = self.__permute(replacement, p_box_table, 32)

        return replacement_permuted

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

            for key in subkeys:
                expanded_right_side = self.__function_f(right_side, key)

                xor = self.__xor(left_side, expanded_right_side, 32)
                
                right_side = left_side
                left_side = xor

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
