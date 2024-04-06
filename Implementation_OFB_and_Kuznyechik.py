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

def encrypt_ofb(input_file, output_file, key, iv):
    # Шифрование текста из файла в режиме OFB
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
        previous_block = encrypted_block  # Предыдущий блок для следующей итерации
    with open(output_file, 'wb') as file:
        file.write(ciphertext)

def decrypt_ofb(input_file, output_file, key, iv):
    # Расшифрование текста из файла, зашифрованного в режиме OFB
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
        previous_block = block  # Предыдущий блок для следующей итерации
    plaintext = unpad_message(plaintext)
    with open(output_file, 'wb') as file:
        file.write(plaintext)

# Пример использования
key_ofb = b'0123456789abcdef'  # 16-байтовый ключ
iv_ofb = b'1234567890abcdef'    # Вектор инициализации

# Зашифровать текст из input.txt и записать результат в encrypted_OFB.txt
encrypt_ofb('input.txt', 'encrypted_OFB.txt', key_ofb, iv_ofb)

# Расшифровать текст из encrypted_OFB.txt и записать результат в decrypted_OFB.txt
decrypt_ofb('encrypted_OFB.txt', 'decrypted_OFB.txt', key_ofb, iv_ofb)
