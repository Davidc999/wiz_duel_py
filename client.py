# Python program to implement client side of chat room.
import socket
import select
import sys
from _thread import *
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def main():
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    server.connect((IP_address, Port))

    while True:
        incoming = server.recv(2048).decode()
        for message in incoming.split("\\"):
            handle_incoming(message)


    server.close()

def handle_incoming(msg):
    if not msg:
        return
    if msg == 'input?':
        usr_input = input()
        server.send(usr_input.encode())
    else:
        print(msg)

def listen_thread(conn):
    while True:
        message = server.recv(2048)
        print(message.decode())

def send_thread(conn):
    while True:
        message = input()
        conn.send(message.encode())
        print("<You> {}".format(message))


if __name__ == '__main__':
    main()