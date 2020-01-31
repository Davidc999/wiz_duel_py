from _thread import *
from player_base import PlayerBase


class RemotePlayer(PlayerBase):

    def print(self, prompt):
        msg = prompt + '\n'
        self._conn.send(msg.encode())

    def get_input(self, prompt):
        msg = prompt + '\\input?'
        self._conn.send(msg.encode())
        return self._conn.recv(2048).decode()

    def __init__(self, conn):
        self._conn = conn