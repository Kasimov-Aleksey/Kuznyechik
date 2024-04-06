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

def encrypt_ctr(input_file, output_file, key, nonce):
    # Шифрование текста из файла в режиме CTR
    block_size = len(key)
    with open(input_file, 'rb') as file:
        plaintext = file.read()
    plaintext = pad_message(plaintext, block_size)
    ciphertext = b''
    counter = 0
    for i in range(0, len(plaintext), block_size):
        counter_block = nonce + counter.to_bytes(block_size // 2, byteorder='big')  # Генерация счетчика
        encrypted_counter = kuznyechik_encrypt(int.from_bytes(counter_block, byteorder='big'), int.from_bytes(key, byteorder='big'))  # Шифрование счетчика
        block = plaintext[i:i+block_size]
        encrypted_block = xor_bytes(block, int.to_bytes(encrypted_counter, block_size, byteorder='big'))  # XOR с результатом шифрования счетчика
        ciphertext += encrypted_block
        counter += 1
    with open(output_file, 'wb') as file:
        file.write(ciphertext)

def decrypt_ctr(input_file, output_file, key, nonce):
    # Расшифрование текста из файла, зашифрованного в режиме CTR
    block_size = len(key)
    with open(input_file, 'rb') as file:
        ciphertext = file.read()
    plaintext = b''
    counter = 0
    for i in range(0, len(ciphertext), block_size):
        counter_block = nonce + counter.to_bytes(block_size // 2, byteorder='big')  # Генерация счетчика
        encrypted_counter = kuznyechik_encrypt(int.from_bytes(counter_block, byteorder='big'), int.from_bytes(key, byteorder='big'))  # Шифрование счетчика
        block = ciphertext[i:i+block_size]
        decrypted_block = xor_bytes(block, int.to_bytes(encrypted_counter, block_size, byteorder='big'))  # XOR с результатом шифрования счетчика
        plaintext += decrypted_block
        counter += 1
    plaintext = unpad_message(plaintext)
    with open(output_file, 'wb') as file:
        file.write(plaintext)

# Пример использования
key_ctr = b'0123456789abcdef'  # 16-байтовый ключ
nonce_ctr = b'\x00\x00\x00\x00\x00\x00\x00\x00'  # Nonce, также 8 байт

# Зашифровать текст из input_data.txt и записать результат в encrypted_CTR.txt
encrypt_ctr('input.txt', 'encrypted_CTR.txt', key_ctr, nonce_ctr)

# Расшифровать текст из encrypted_CTR.txt и записать результат в decrypted_CTR.txt
decrypt_ctr('encrypted_CTR.txt', 'decrypted_CTR.txt', key_ctr, nonce_ctr)
