import socket
import commons
import random
from CFB_mode import *
from ECB_mode import *
from AES_pack import *
from Cryptodome.Util.Padding import pad, unpad

available_modes = [commons.CFB, commons.ECB]
MODE_OF_OPERATION_str = input('Choose operation mode (ECB or CFB): ')
if MODE_OF_OPERATION_str == "CFB":
    MODE_OF_OPERATION = commons.CFB
else: 
    MODE_OF_OPERATION = commons.ECB
key, encrypted_key = b'', b''


def send_mode_of_operation_to(sock):
    sock.sendall(bytes(MODE_OF_OPERATION, "utf-8"))
    sock.sendall(encrypted_key)


def get_key_and_decrypt(sock):
    global key, encrypted_key
    encrypted_key = sock.recv(16)
    print(f'Key received from node_KM: {encrypted_key}')
    key = AES_decrypt(encrypted_key, commons.K_prime)
    print(f'Decrypted key: {key}')


def get_start_signal(sock):
    data = sock.recv(5)
    print(f'Signal received from B: {data.decode("utf-8")}')


def encrypt_message_on_chosen_mode(message):
    if MODE_OF_OPERATION == commons.CFB:
        cfb = CFB_mode(commons.initialization_vector, key)
        encrypted_data = cfb.encrypt(message)
    else:
        ecb = ECB_mode(key)
        encrypted_data = ecb.encrypt(message)
    return encrypted_data


def send_encrypted_message(sock, message):
    print(f'Sending encrypted message: {message}')
    sock.sendall(message)


def connect_to_KM(KM_port):
    global key, encrypted_key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as kms:
        kms.connect((commons.HOST, KM_port))

        send_mode_of_operation_to(kms)

        get_key_and_decrypt(kms)


def connect_to_B(B_port):
    global key, encrypted_key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((commons.HOST, B_port))

        send_mode_of_operation_to(s)
        get_start_signal(s)

        try:
            with open("plaintext.txt", "rb") as f:
                file_text = f.read()
                encrypted_message = encrypt_message_on_chosen_mode(file_text)
                send_encrypted_message(s, encrypted_message)

        except FileNotFoundError:
            print("Did not find the requested file")


if __name__ == "__main__":
    connect_to_KM(commons.A_KM_PORT)
    connect_to_B(commons.A_B_PORT)