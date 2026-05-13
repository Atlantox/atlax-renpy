import os
import base64
import hashlib

key = ''

def main():
    try:
        print('Initializing script')
        with open('encryption.key', 'r') as f:
            my_key = f.read()
            f.close()
        global key    
        key = hashlib.sha256(my_key.encode()).digest()

        print('Key loaded correctly')
        print('Encrypting files from to_decrypt folder')
        for subdir, dirs, files in os.walk('./to_encrypt'):
            for file in files:
                filePath = os.path.join(subdir, file)

                finalPath = filePath.replace('./to_encrypt', './encrypted')

                folderPath = finalPath.replace('\\' + file, '')
                print('Encrypting:', filePath, ' => ', finalPath)

                if not os.path.isdir(folderPath):
                    os.makedirs(folderPath, exist_ok=True)

                encrypt_file(filePath ,finalPath)

        input('Encryption ready. Enter to exit')
    except Exception as e:
        print('ERROR', e)
        input('Press enter to exit')


def GetBytes(data):
    global key
    return bytes(
        data[i] ^ key[i % len(key)]
        for i in range(len(data))
    )

def encrypt_text(text):
    raw = text.encode("utf-8")
    encrypted = GetBytes(raw)
    return base64.b64encode(encrypted).decode("utf-8")


def encrypt_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
        f.close()

    encrypted = encrypt_text(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encrypted)
        f.close()


def decrypt_text(token):
    data = base64.b64decode(token)
    decrypted = GetBytes(data)
    return decrypted.decode("utf-8")


def decrypt_file(encrypted_path):
    with open(encrypted_path, "r", encoding="utf-8") as f:
        encrypted = f.read()

    return decrypt_text(encrypted)


'''
# ENCRYPTING THE FILES
for subdir, dirs, files in os.walk('./to_encrypt'):
    for file in files:
        filePath = os.path.join(subdir, file)

        encrypt_file(filePath, './encrypted' + '/' + file)
'''

'''
# DECRYPTIUNG THE FILES
for subdir, dirs, files in os.walk('./encrypted'):
    for file in files:
        filePath = os.path.join(subdir, file)

        result = decrypt_file(filePath)
        print(result)
'''

if __name__ == '__main__':
    main()