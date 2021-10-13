# Python program to implement client side of chat room.
import socket
import select
import sys
from _thread import *
import time
import argparse

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def parse_args():
    parser = argparse.ArgumentParser(description="Start wizduel client and connect to server.")
    parser.add_argument("-ip", type=str, required=True,
                        help="The server\'s IP Address")
    parser.add_argument("-port", type=int, required=True,
                        help="The server\'s listen port")
    return parser.parse_args()


def main():

    args = parse_args()
    server.connect((args.ip, args.port))

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
        print(msg.strip())


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