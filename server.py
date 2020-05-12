#!/usr/bin/env python3
'''
Server for a multithreded (asynchronous) chat application
'''
#AF_INET : It is a family of addresses for the IPv4 adresses. Socket can only communicate with addresses in this family
#SOCK_STREAM : Enables us to use TCP Connection
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
adresses = {}

'''
HOST : Server address. '' Represents INADDR_ANY, which binds to any address
PORT : The socket on the server side which accepts requests and transmits data
BUFSIZE : Amount of data downloaded at a given time
'''
HOST = ''
PORT = 33000
BUFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)

#Binds the server socket to the address
SERVER.bind(ADDR)

def accept_incoming_connections():
    '''Sets up handling for incoming connections'''
    while True:
        '''accept() : Accept a connection. The socket must be bound to an address and listening for connections. The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection.'''
        client, client_address = SERVER.accept()
        print("%s:%s has connected" %client_address)

        '''The bytes() method returns a immutable bytes object initialized with the given size and data.
        socket.send() : Send data to the socket. The socket must be connected to a remote socket.'''
        client.send(bytes("Greetings Earthling! Type your name and press Enter!"))

    '''Stores the client’s address in the addresses dictionary '''
    addresses[client] = client_address
    '''handle_client is a function'''
    Thread(target = handle_client, args=(client,)).start()


'''Handles a single client connection'''
def handle_client(client):
    '''Receives BUFSIZE amount of data in byte format. Must decode to string'''
    name = client.recv(BUFSIZE).decode('utf8')
    msg = name + " has joined the chat"

    '''bytes(string, encoding)'''
    broadcast(bytes(msg, 'utf8'))
    '''Stores client's name in the clients dictionary'''
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZE)
        if msg != bytes('{quit}', 'utf8'):
            '''broadcast takes and message and a prefix'''
            broadcast(msg, name + ': ')
        else:       
            '''Client wants to leave chat'''
            '''Send client the quit message. Close their connection. Delete from clients dictionary. Notify chat of clients departure'''
            client.send(bytes('{quit}', 'utf8'))
            client.close()
            del clients[client]
            broadcast(bytes(name + 'has left the chat.', 'utf8'))
            break


'''Display the message prefixed with the optional prefix. Display to all clients
Parameters: msg : A bytes object in utf8 encoding
            prefix: string
'''
def broadcast(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix, 'utf8') + msg)


if __name__ == '__main__':
    '''socket.listen([baclog]) : Enable a server to accept connections. If backlog is specified, it must be at least 0 (if it is lower, it is set to 0); it specifies the number of unaccepted connections that the system will allow before refusing new connections. If not specified, a default reasonable value is chosen.'''
    SERVER.listen(5)
    print('Waiting for connection...')

    '''Target is the callable object to be invoked by the run() method.
     We join() ACCEPT_THREAD so that the main script waits for it to complete and doesn’t jump to the next line, which closes the server.'''
    ACCEPT_THREAD = Thread(target = accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()