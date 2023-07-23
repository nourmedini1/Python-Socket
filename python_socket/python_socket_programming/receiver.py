import socket
import threading
from cryptography.fernet import Fernet 
from datetime import datetime


PORT = 5054
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = "utf-8"
DISCONNECT = "!DISCONNECT!"
END = b"!END!"
PATH_SAVE = "C:\\Users\\medin\\Downloads"
SS = 227
ACK_MESSAGE = "message received !"
ACK_FILE = "file received !"
SYN_FILE = "!SENDING FILE!"
CONNECTIONS = {}
NICKNAME = "!NICKNAME!"
DILIMITER = "!!321àà@@ù*!!"

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.bind(ADDR)


def encrypt_message(msg):
    with open("file.key", "rb") as key_f:
        key = key_f.read()
        f = Fernet(key)
        return f.encrypt(msg.encode("utf-8"))


def decrypt_message(msg):
    with open("file.key", "rb") as key_f:
        key = key_f.read()
        f = Fernet(key)
        return f.decrypt(msg).decode("utf-8")

def encrypt_message_bytes(msg) :
    key_f = open("file.key","rb")
    key = key_f.read()
    key_f.close()
    f = Fernet(key)
    return f.encrypt(msg)

def decrypt_message_bytes(msg) :
    key_f = open("file.key","rb")
    key = key_f.read()
    key_f.close()
    f = Fernet(key)
    return f.decrypt(msg)

def client_handler(conn, addr):
    ip_addr_client, port_client = addr
    print(f"[NEW CLIENT CONNECTED] client with address {ip_addr_client} is connected on port {port_client}")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER)
        if msg_length:
            msg_length = int(msg_length)
            enc_msg = conn.recv(msg_length)
            msg_tmp = str(decrypt_message(enc_msg))
            msg = msg_tmp.split(DILIMITER)[0]
            timestamp =msg_tmp.split(DILIMITER)[1]
            if msg == DISCONNECT:
                print(f"[DISCONNECTED] client with address {ip_addr_client} is disconnected from port {port_client} on {timestamp} ")
                connected = False
            elif msg == NICKNAME:
                len_nickname = conn.recv(HEADER).decode(FORMAT)
                if len_nickname:
                    len_nickname = int(len_nickname)
                    enc_nickname = conn.recv(len_nickname)
                    nickname_tmp = decrypt_message(enc_nickname)
                    nickname = nickname_tmp.split(DILIMITER)[0]
                    timestamp_nickname =nickname_tmp.split(DILIMITER)[1]
                    CONNECTIONS[addr] = nickname
                    print(f"[CLIENT NICKNAME] client with address {ip_addr_client} on port {port_client} is {nickname}  {timestamp_nickname}")
            elif msg == SYN_FILE:
                len_file_name = conn.recv(HEADER).decode(FORMAT)
                if len_file_name:
                    len_file_name = int(len_file_name)
                    enc_file_name = conn.recv(len_file_name)
                    file_name_tmp = str(decrypt_message(enc_file_name))
                    file_name = file_name_tmp.split(DILIMITER)[0]
                    path = PATH_SAVE + f"\\{file_name}"
                    file = open(path, "wb")
                    bytes_stream = b""
                    done = False
                    while not done:
                        if bytes_stream[-5:] == END:
                            done = True
                        else:
                            enc_data = conn.recv(1024)
                            bytes_stream += enc_data
                    bytes_stream = bytes_stream[:-5]
                    bytes_stream = bytearray(bytes_stream)
                    for index,values in enumerate(bytes_stream) :
                        bytes_stream[index] = values ^ SS
                    file.write(bytes_stream)
                    file.close()
                    print(f"[FILE RECEIVED] {CONNECTIONS[addr]} sent a file on port {port_client} ; file name : {file_name}  {datetime.now()}")
                    print(f"[SAVED] file saved to : {path}  ")
            else:
                print(f"[MESSAGE] {CONNECTIONS[addr]} : {msg}  {timestamp}")
                to_send = ACK_MESSAGE+DILIMITER+str(datetime.now())
                enc_ack_message = encrypt_message(to_send)
                conn.send(enc_ack_message)
    conn.close()


def start_server():
    receiver.listen()
    print(f"[LISTENING] the server is listening on {SERVER} ")
    while True:
        conn, addr = receiver.accept()
        thread = threading.Thread(target=client_handler, args=(conn, addr))
        thread.start()
        print(f"[CURRENT ACTIVE CONNETIONS] {threading.active_count() - 1}")


print("[STARTING] the server is starting ...")
start_server()
