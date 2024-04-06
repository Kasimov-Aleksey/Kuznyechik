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

def encrypt_cfb(input_file, output_file, key, iv):
    # Шифрование текста из файла в режиме CFB
    block_size = len(key)
    with open(input_file, 'rb') as file:
        plaintext = file.read()
    plaintext = pad_message(plaintext, block_size)
    ciphertext = b''
    previous_block = iv
    for i in range(0, len(plaintext), block_size):
        encrypted_block = kuznyechik_encrypt(int.from_bytes(previous_block, byteorder='big'), int.from_bytes(key, byteorder='big'))  # Шифрование предыдущего блока
        block = plaintext[i:i+block_size]
        encrypted_block = xor_bytes(block, int.to_bytes(encrypted_block, block_size, byteorder='big'))  # XOR с зашифрованным предыдущим блоком
        ciphertext += encrypted_block
        previous_block = encrypted_block[-block_size:]  # Последние block_size байтов зашифрованного блока
    with open(output_file, 'wb') as file:
        file.write(ciphertext)

def decrypt_cfb(input_file, output_file, key, iv):
    # Расшифрование текста из файла, зашифрованного в режиме CFB
    block_size = len(key)
    with open(input_file, 'rb') as file:
        ciphertext = file.read()
    plaintext = b''
    previous_block = iv
    for i in range(0, len(ciphertext), block_size):
        encrypted_block = kuznyechik_encrypt(int.from_bytes(previous_block, byteorder='big'), int.from_bytes(key, byteorder='big'))  # Шифрование предыдущего блока
        block = ciphertext[i:i+block_size]
        decrypted_block = xor_bytes(block, int.to_bytes(encrypted_block, block_size, byteorder='big'))  # XOR с зашифрованным предыдущим блоком
        plaintext += decrypted_block
        previous_block = block  # Зашифрованный текст становится предыдущим блоком для следующей итерации
    plaintext = unpad_message(plaintext)
    with open(output_file, 'wb') as file:
        file.write(plaintext)

# Пример использования
key_cfb = b'0123456789abcdef'  # 16-байтовый ключ
iv_cfb = b'1234567890abcdef'    # Вектор инициализации

# Зашифровать текст из input.txt и записать результат в encrypted_CFB.txt
encrypt_cfb('input.txt', 'encrypted_CFB.txt', key_cfb, iv_cfb)

# Расшифровать текст из encrypted_CFB.txt и записать результат в decrypted_CFB.txt
decrypt_cfb('encrypted_CFB.txt', 'decrypted_CFB.txt', key_cfb, iv_cfb)
