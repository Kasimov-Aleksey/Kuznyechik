from Kuznyechik_Block_Cipher import kuznyechik_encrypt, kuznyechik_decrypt

def pad_message(message, block_size):
    # Добавление отступов к сообщению до размера блока
    padding_length = block_size - (len(message) % block_size)
    padding = bytes([padding_length]) * padding_length
    return message + padding

def unpad_message(padded_message):
    # Удаление добавленных отступов из сообщения
    padding_length = padded_message[-1]
    return padded_message[:-padding_length]

def encrypt_ecb(input_file, output_file, key):
    # Шифрование текста из файла в режиме ECB
    block_size = len(key)
    with open(input_file, 'rb') as file:
        plaintext = file.read()
    plaintext = pad_message(plaintext, block_size)
    ciphertext = b''
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        encrypted_block = int.to_bytes(kuznyechik_encrypt(int.from_bytes(block, byteorder='big'), int.from_bytes(key, byteorder='big')), 16, byteorder='big')
        ciphertext += encrypted_block
    with open(output_file, 'wb') as file:
        file.write(ciphertext)

def decrypt_ecb(input_file, output_file, key):
    # Расшифрование текста из файла, зашифрованного в режиме ECB
    block_size = len(key)
    with open(input_file, 'rb') as file:
        ciphertext = file.read()
    plaintext = b''
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        decrypted_block = int.to_bytes(kuznyechik_decrypt(int.from_bytes(block, byteorder='big'), int.from_bytes(key, byteorder='big')), 16, byteorder='big')
        plaintext += decrypted_block
    plaintext = unpad_message(plaintext)
    with open(output_file, 'wb') as file:
        file.write(plaintext)

# Пример использования
key_ecb = b'0123456789abcdef'  # 16-байтовый ключ

# Зашифровать текст из input_data.txt и записать результат в encrypted.txt
encrypt_ecb('input.txt', 'encrypted_ECB.txt', key_ecb)

# Расшифровать текст из encrypted.txt и записать результат в decrypted.txt
decrypt_ecb('encrypted_ECB.txt', 'decrypted_ECB.txt', key_ecb)
