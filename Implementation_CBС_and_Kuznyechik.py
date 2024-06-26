from Kuznyechik_Block_Cipher import kuznyechik_encrypt, kuznyechik_decrypt

def xor_bytes(a, b):
    # Функция для выполнения операции XOR над двумя байтовыми строками
    result = b''
    for i in range(min(len(a), len(b))):
        result += bytes([a[i] ^ b[i]])
    return result

def pad_message(message, block_size):
    # Добавление отступов к сообщению до размера блока
    padding_length = block_size - (len(message) % block_size)
    padding = bytes([padding_length]) * padding_length
    return message + padding

def unpad_message(padded_message):
    # Удаление добавленных отступов из сообщения
    padding_length = padded_message[-1]
    return padded_message[:-padding_length]

def encrypt_cbc(input_file, output_file, key, iv):
    # Шифрование текста из файла в режиме input_file
    block_size = len(key)
    with open(input_file, 'rb') as file:
        plaintext = file.read()
    plaintext = pad_message(plaintext, block_size)
    ciphertext = b''
    previous_block = iv
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        block = xor_bytes(block, previous_block)
        encrypted_block = int.to_bytes(kuznyechik_encrypt(int.from_bytes(block, byteorder='big'), int.from_bytes(key, byteorder='big')), 16, byteorder='big')
        ciphertext += encrypted_block
        previous_block = encrypted_block
    with open(output_file, 'wb') as file:
        file.write(ciphertext)

def decrypt_cbc(input_file, output_file, key, iv):
    # Расшифрование текста из файла, зашифрованного в режиме input_file
    block_size = len(key)
    with open(input_file, 'rb') as file:
        ciphertext = file.read()
    plaintext = b''
    previous_block = iv
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        decrypted_block = int.to_bytes(kuznyechik_decrypt(int.from_bytes(block, byteorder='big'), int.from_bytes(key, byteorder='big')), 16, byteorder='big')
        decrypted_block = xor_bytes(decrypted_block, previous_block)
        plaintext += decrypted_block
        previous_block = block
    plaintext = unpad_message(plaintext)
    with open(output_file, 'wb') as file:
        file.write(plaintext)

# Пример использования
key_cbc = b'0123456789abcdef'  # 16-байтовый ключ
iv_cbc = b'1234567890abcdef'    # Вектор инициализации

# Зашифровать текст из input_data.txt и записать результат в encrypted.txt
encrypt_cbc('input.txt', 'encrypted_CBС.txt', key_cbc, iv_cbc)

# Расшифровать текст из encrypted.txt и записать результат в decrypted.txt
decrypt_cbc('encrypted_CBС.txt', 'decrypted_CBС.txt', key_cbc, iv_cbc)
