from _thread import *
from player_base import PlayerBase


class RemotePlayer(PlayerBase):

    def print(self):
        pass

    def get_input(self, prompt):
        msg = prompt + '\\input?'
        conn.send(msg.encode)
        return conn.recv(2048).decode()

    def __init__(self, conn):
        self._conn = conn