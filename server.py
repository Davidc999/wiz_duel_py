# Python program to implement server side of chat room.
import socket
import sys
from _thread import *
import time
from wizard import Wizard
from game_state import GameState
from remote_player import RemotePlayer

game_state = GameState()
def main():
    """The first argument AF_INET is the address domain of the
    socket. This is used when we have an Internet Domain with
    any two hosts The second argument is the type of socket.
    SOCK_STREAM means that data or characters are read in
    a continuous flow."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()

    # takes the first argument from command prompt as IP address
    IP_address = str(sys.argv[1])

    # takes second argument from command prompt as port number
    Port = int(sys.argv[2])

    """ 
    binds the server to an entered IP address and at the 
    specified port number. 
    The client must be aware of these parameters 
    """
    server.bind((IP_address, Port))

    """ 
    listens for 100 active connections. This number can be 
    increased as per convenience. 
    """
    server.listen(100)

    while True:
        conn, addr = server.accept()
        init_new_player(conn)
        start_ans = input("Shall we start the game? <y/n>\n")
        if(start_ans == 'y'):
            break

    run_demo()


        #start_new_thread(clientthread, (conn, addr))

    conn.close()
    server.close()

def init_new_player(conn):
    new_wiz = Wizard(RemotePlayer(conn))
    game_state.wizards.append(new_wiz)
    game_state.entities.append(new_wiz)
    print("{} Has joined the game!".format(new_wiz.name))


def run_demo():
    while True:
        for wiz in game_state.wizards:
            print(wiz.play_turn(game_state.entities))




def clientthread(conn, addr):
    # sends a message to the client whose user object is conn
    conn.send("Welcome to this chatroom!".encode())

    while True:
        try:
            message = conn.recv(2048)
            if message:

                """prints the message and address of the 
                user who just sent the message on the server 
                terminal"""
                print("<" + addr[0] + "> " + message.decode())

                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message.decode()
                broadcast(message_to_send, conn)
            else:
                """message may have no content if the connection 
                is broken, in this case we remove the connection"""
                print("Removing connection {}".format(addr[0]))
                remove(conn)

        except:
            print("Exception for some reason!")
            raise
            #continue


"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()

                # if the link is broken, we remove the client
                remove(clients)


"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


if __name__ == '__main__':
    main()