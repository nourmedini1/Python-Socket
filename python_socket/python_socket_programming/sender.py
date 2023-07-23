import os
import socket
from cryptography.fernet import Fernet
from datetime import datetime

PORT = 5054
SERVER = "192.168.1.16"
THIS_ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT!"
END = "!END!"
ACK_MESSAGE = "message received !"
ACK_FILE = "file received !"
SYN_FILE = "!SENDING FILE!"
SS = 227
NICKNAME = "!NICKNAME!"
DILIMITER = "!!321àà@@ù*!!"

sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.connect(THIS_ADDR)


def encrypt_message(msg):
    key_f = open("file.key", "rb")
    key = key_f.read()
    key_f.close()
    f = Fernet(key)
    return f.encrypt(msg.encode(FORMAT))


def decrypt_message(msg):
    key_f = open("file.key", "rb")
    key = key_f.read()
    key_f.close()
    f = Fernet(key)
    return f.decrypt(msg).decode(FORMAT)


def encrypt_message_bytes(msg):
    key_f = open("file.key", "rb")
    key = key_f.read()
    key_f.close()
    f = Fernet(key)
    return f.encrypt(msg)


def decrypt_message_bytes(msg):
    key_f = open("file.key", "rb")
    key = key_f.read()
    key_f.close()
    f = Fernet(key)
    return f.decrypt(msg)


LEN_ACK_MESSAGE = len(encrypt_message(ACK_MESSAGE))
LEN_ACK_FILE = len(encrypt_message(ACK_FILE))


def send_message(msg):
    msg += DILIMITER+str(datetime.now())
    message = msg.encode(FORMAT)
    enc_msg = encrypt_message_bytes(message)
    len_enc_msg = str(len(enc_msg)).encode(FORMAT)
    len_enc_msg += b' ' * (HEADER - len(len_enc_msg))
    sender.send(len_enc_msg)
    sender.send(enc_msg)
    enc_ack_message = sender.recv(1024)
    dec_ack_message = decrypt_message(enc_ack_message)
    message_ack = dec_ack_message.split(DILIMITER)[0]
    timestamp = dec_ack_message.split(DILIMITER)[1]
    print(f"[ACK MESSAGE] {message_ack} ; {timestamp}")


def send_file(file_path):
    to_send = SYN_FILE + DILIMITER + str(datetime.now())
    message = to_send.encode(FORMAT)
    enc_msg = encrypt_message_bytes(message)
    len_enc_msg = str(len(enc_msg)).encode(FORMAT)
    len_enc_msg += b' ' * (HEADER - len(len_enc_msg))
    sender.send(len_enc_msg)
    sender.send(enc_msg)
    file_name = file_path.split("\\")[-1]
    to_send = file_name + DILIMITER + str(datetime.now())
    message = to_send.encode(FORMAT)
    enc_msg = encrypt_message_bytes(message)
    len_enc_msg = str(len(enc_msg)).encode(FORMAT)
    len_enc_msg += b' ' * (HEADER - len(len_enc_msg))
    sender.send(len_enc_msg)
    sender.send(enc_msg)
    file = open(file_path, "rb")
    data = file.read()
    file.close()
    data = bytearray(data)
    for index, values in enumerate(data):
        data[index] = values ^ SS
    data += b'!END!'
    sender.sendall(data)
    print(f"[ACK FILE] {ACK_FILE} ; {datetime.now()}")
    


message = NICKNAME+DILIMITER+str(datetime.now())
enc_msg = encrypt_message(message)
len_enc_msg = str(len(enc_msg)).encode(FORMAT)
len_enc_msg += b' ' * (HEADER - len(len_enc_msg))
sender.send(len_enc_msg)
sender.send(enc_msg)
nickname = "Nour"
message = nickname+DILIMITER+str(datetime.now())
message = message.encode(FORMAT)
enc_msg = encrypt_message_bytes(message)
len_enc_msg = str(len(enc_msg)).encode(FORMAT)
len_enc_msg += b' ' * (HEADER - len(len_enc_msg))
sender.send(len_enc_msg)
sender.send(enc_msg)
send_message("salem")
send_message("bou salem champions d'afrique")
send_message("hit me baby one more time")
send_file("arthur.png")
