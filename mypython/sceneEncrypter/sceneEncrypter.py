import os
import base64
import hashlib

ENCRYPTION_TARGET = 'D:/Proyectos/Renpy/TheNextStepDemo/mypython/sceneEncrypter/to_encrypt'
ENCRYPTION_OUTPUT = 'D:/Proyectos/Renpy/TheNextStepDemo/mypython/sceneEncrypter/encrypted'
key = ''

def main():
    with open('encryption.key', 'r') as f:
        my_key = f.read()
        f.close()
    global key
    key = hashlib.sha256(my_key.encode()).digest()

    for subdir, dirs, files in os.walk(ENCRYPTION_TARGET):
        for file in files:
            filePath = os.path.join(subdir, file)

            encrypt_file(filePath, ENCRYPTION_OUTPUT + '/' + file)


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
for subdir, dirs, files in os.walk(ENCRYPTION_TARGET):
    for file in files:
        filePath = os.path.join(subdir, file)

        encrypt_file(filePath, ENCRYPTION_OUTPUT + '/' + file)
'''

'''
# DECRYPTIUNG THE FILES
for subdir, dirs, files in os.walk(ENCRYPTION_OUTPUT):
    for file in files:
        filePath = os.path.join(subdir, file)

        result = decrypt_file(filePath)
        print(result)
'''

if __name__ == '__main__':
    main()