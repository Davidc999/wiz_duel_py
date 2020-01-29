from _thread import *
from player_base import PlayerBase


class RemotePlayer(PlayerBase):

    def get_move(self):
        pass

    def print(self):
        pass

    def _set_name(self):
        self._conn.send("What is your name?".encode())
        self.name = conn.recv(2048).decode()

    def __init__(self, conn):
        self._conn = conn
        self.name = _set_name()