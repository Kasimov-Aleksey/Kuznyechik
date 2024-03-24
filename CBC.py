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

def encrypt_block(block, key):
    # Шифрование одного блока данных с использованием ключа
    result = b''
    for i in range(min(len(block), len(key))):
        result += bytes([block[i] ^ key[i]])
    return result

def decrypt_block(block, key):
    # Дешифрование одного блока данных с использованием ключа
    return encrypt_block(block, key)

def encrypt_cbc(plaintext, key, iv):
    # Шифрование текста в режиме input_file
    block_size = len(key)
    plaintext = pad_message(plaintext.encode(), block_size)
    ciphertext = b''
    previous_block = iv
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        block = xor_bytes(block, previous_block)
        encrypted_block = encrypt_block(block, key)
        ciphertext += encrypted_block
        previous_block = encrypted_block
    return ciphertext

def decrypt_cbc(ciphertext, key, iv):
    # Расшифрование текста, зашифрованного в режиме input_file
    block_size = len(key)
    plaintext = b''
    previous_block = iv
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i+block_size]
        decrypted_block = decrypt_block(block, key)
        decrypted_block = xor_bytes(decrypted_block, previous_block)
        plaintext += decrypted_block
        previous_block = block
    return unpad_message(plaintext).decode()

# Пример использования
key_cbc = b'0123456789abcdef'  # 16-байтовый ключ
iv_cbc = b'1234567890abcdef'    # Вектор инициализации
plaintext_cbc = "Hello, input_file mode!"

encrypted_cbc = encrypt_cbc(plaintext_cbc, key_cbc, iv_cbc)
print("Зашифрованный текст методом input_file:", encrypted_cbc)

decrypted_cbc = decrypt_cbc(encrypted_cbc, key_cbc, iv_cbc)
print("Расшифрованный текст методом input_file:", decrypted_cbc)
