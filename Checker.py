def check_texts(input_txt):
    data_crypto = {"1": "decrypted_CBС.txt", "2": "decrypted_CFB.txt", "3": "decrypted_ECB.txt",
                   "4": "decrypted_OFB.txt", "5": "decrypted_STR.txt"}
    print("Файлы по режимам шифрования: ")
    [print(f"{num[0]}):  {num[1]}") for num in data_crypto.items()]
    decrypted_text = data_crypto[input('Выберите номер нужного файла:  ')]
    with open(input_txt, "rb") as text_input, open(decrypted_text, "rb") as text_decrypted:
        text_input, text_decrypted = text_input.read(), text_decrypted.read()
        print(f"Исходный текст:", text_input[:100], sep="\n")
        print("_" * 50)
        print(f"Tекст расшифрования:",  text_decrypted[:100], sep="\n")
        print("_" * 50)
        print([ "Тексты НЕ совпадают", "Тексты совпадают"][bool(text_input==text_decrypted)])

check_texts("input.txt")