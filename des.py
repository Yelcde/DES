from tables import ip_table

class DES:
    def text_to_bin(self, text):
        # Converte cada caractere da string em seu valor binário (8 bits para cada caractere)
        return ''.join(format(ord(char), '08b') for char in text)

    def text_to_binary_64bits(self, text):
        message_bin = self.text_to_bin(text)
        
        # Divide a mensagem em blocos de 64 bits
        blocks = [message_bin[i:i+64] for i in range(0, len(message_bin), 64)]

        # Verifica se o último bloco tem menos de 64 bits e adiciona padding se necessário
        last_block = blocks[-1]
        last_block_size = len(last_block)

        if len(last_block_size) < 64:
            blocks[-1] = last_block.ljust(64 - last_block_size, '0')
        
        return blocks

    def permute(self, block, table):
        # Função de permutação de bits baseado em uma tabela
        return [block[x - 1] for x in table]

    def xor(self, bits1, bits2):
        # XOR entre duas listas de bits
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

    def split_bits(self, bits):
        # Divide o bloco em duas metades
        n = len(bits) // 2
        return bits[:n], bits[n:]

    def function_f(self, right, subkey):
        # Função Feistel F simplificada (expansão, substituição e permutação)
        # Expansão do lado direito (simplificado aqui)
        expanded = permute(right, expansion_table)
        # XOR com a subchave
        xor_output = xor(expanded, subkey)
        # Substituição (S-Boxes) omitida aqui por simplicidade
        return permute(xor_output, permutation_table)

    def generate_subkeys(self, key):
        # Geração de subchaves (simplificado)
        subkeys = []
        for i in range(16): # 16 rodadas
            subkeys.append(permute(key, key_schedule_table[i])) # Gerar subchaves a partir da chave principal
        return subkeys

    def encrypt(self, text, key=''):
        # Converte texto para blocos binários de 64 bits
        blocks = self.text_to_binary_64bits(text)
        print(blocks)

        # Permutação inicial
        text = self.permute(blocks, ip_table)
        
        # Dividir o bloco em metades
        left, right = self.split_bits(text)
        
        # Gerar subchaves
        subkeys = self;generate_subkeys(key)
        
        # 16 rodadas de Feistel
        for i in range(16):
            new_right = self;xor(left, self.function_f(right, subkeys[i]))
            left = right
            right = new_right
        
        # Combinar as metades (esquerda e direita)
        combined_block = right + left # Swap final das metades
        
        # Permutação final
        encrypted_block = self.permute(combined_block, final_permutation)
        
        return encrypted_block