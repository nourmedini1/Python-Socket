from fernet import Fernet

message = "hello world"


def create_key():
    with open("file.key", "wb") as file:
        key = Fernet.generate_key()
        file.write(key)


def encrypt_message(msg):
    with open("file.key", "rb") as key_f:
        key = key_f.read()
        f = Fernet(key)
        msg_length = str(len(msg)).encode("utf-8")
        msg_length += b' ' * (64 - len(msg_length))
        print(f.encrypt(msg_length))
        return f.encrypt(msg)


def decrypt_message(msg):
    with open("file.key", "rb") as key_f:
        key = key_f.read()
        f = Fernet(key)
        return f.decrypt(msg).decode("utf-8")



print(len(b'5                                                               '))
print(decrypt_message(b'gAAAAABkb4dbKZMkeJB6cxMSC9xmlXIF2zqcYPMi4YzGbKImoSzxDqQSoEm2VBTilzzLszB780Y3A_VeKpqM0kCYgZFNvI2VBQ=='))
