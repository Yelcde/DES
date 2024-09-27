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

    def __to_64_bits(self, text):
        # Divide a mensagem em blocos de 64 bits
        blocks = [list(text[i:i+64]) for i in range(0, len(text), 64)]

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

    def __xor(self, a, b, len_range=48):
        xored = ''

        for bit in range(len_range):
            if a[bit] == b[bit]:
                xored += '0'
            else: 
                xored += '1'

        return xored

    def __s_box_substitution(self, s_box_entrance):
        s_box_chosen = 0
        replacement = ''
        for entrance in s_box_entrance:
            row = entrance[0] + entrance[-1]
            row = self.__binary_to_decimal(row)
            column = self.__binary_to_decimal(''.join(entrance[1:5]))

            sBox_number = s_boxes[s_box_chosen][row][column]

            replacement += self.__decimal_to_binary(sBox_number)

            s_box_chosen += 1

        return replacement

    def __feistel_round(self, left_side, right_side, subkey):
        # Expansão do lado direito
        expanded_right_side = self.__permute(right_side, e_box_table, 48)

        # XOR com a subchave
        xor = self.__xor(expanded_right_side, subkey)

        # Substituição (S-Boxes)
        s_box_entrance = []

        for i in range(0, len(xor), 6): # Separando XOR em grupos de 6
            entrance = list(xor[i:i+6])
            s_box_entrance.append(entrance)
        
        # Fazendo substituição com s_boxes
        replacement = self.__s_box_substitution(s_box_entrance)

        # Permutando depois de fazer a substituição
        replacement_permuted = self.__permute(replacement, p_box_table, 32)

        # Retornando lado esquerdo (antigo direito) e novo lado direito modificado com XOR
        return ''.join(right_side), self.__xor(replacement_permuted, left_side, 32)

    def __bin_to_ascii(self, binary):
        ascii_str = ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])
        return ascii_str

    def __bin_to_hex(self, binary):
        decimal = int(binary, 2)

        # Convertendo para hexadecimal e remove prefixo '0x'
        hex_value = hex(decimal)[2:]

        # 4 bits = 1 hexadecimal
        return hex_value.zfill(len(binary) // 4)
    
    def __hex_to_bin(self, hex_value):
        hex_len = len(hex_value)
        decimal = int(hex_value, 16)

        # Converte para binário e remove prefixo '0b'
        binary = bin(decimal)[2:]

        # 1 hexadecimal = 4 bits
        return binary.zfill(hex_len * 4)

    def encrypt(self, text, key=''):
        encrypted_block = ''

        # Converte texto para blocos binários de 64 bits
        blocks = self.__text_to_bin(text)

        # Divisão em blocos de 64
        blocks = self.__to_64_bits(blocks)

        # Converte chave de criptografia para binário
        key_bin = self.__proccess_key(key)

        for block_id in range(len(blocks)):
            # Permutação inicial
            permuted_block = self.__permute(blocks[block_id], ip_table)

            # Divide bloco em esquerda e direita
            left_side, right_side = self.__split_block(permuted_block)

            # Gerar subchaves
            subkeys = self.__generate_subkeys(''.join(key_bin))

            for key in subkeys:
                left_side, right_side = self.__feistel_round(left_side, right_side, key)
            
            # Combinando right_side e left_side
            blocks[block_id] = right_side + left_side

            # Permutação Inversa
            encrypted_block += ''.join(self.__permute(blocks[block_id], ip_inverse_table))

        cipherhex = self.__bin_to_hex(encrypted_block)
        return cipherhex

    # Descriptografia
    def decrypt(self, text, key=''):
        decrypted_block = ''

        # Transforma hexadecimal para binário
        blocks = self.__hex_to_bin(text)

        # Divisão em blocos de 64
        blocks = self.__to_64_bits(blocks)

        # Converte chave de criptografia para binário
        key_bin = self.__proccess_key(key)

        for block_id in range(len(blocks)):
            # Permutação Inicial
            permuted_inverse = self.__permute(blocks[block_id], ip_table)

            # Divide bloco em esquerda e direita
            left_side, right_side = self.__split_block(permuted_inverse)

            # Gerar subchaves
            subkeys = self.__generate_subkeys(''.join(key_bin))

            # Executa as 16 rodadas feistel, com 16 subchaves
            for key in reversed(subkeys):
                left_side, right_side = self.__feistel_round(left_side, right_side, key)

            # Combinando right_side e left_side
            blocks[block_id] = right_side + left_side

            # Permutação Inversa
            decrypted_block += ''.join(self.__permute(blocks[block_id], ip_inverse_table))

        decrypted_text = self.__bin_to_ascii(decrypted_block)  
        return decrypted_text
