from copyreg import pickle
import socket
import time
import pickle
import select

class ServerService:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def recObj(self):
        self.BUFFER_SIZE = 1024
        port = 1233
        self.HEADERSIZE = 10
        self.BUFFER_SIZE = 1024
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        # print (f"Connection from {} has been established!")
        socket = self.server_socket
        # ready_to_read, ready_to_write, in_error = select.select([socket], [],
        #                                                         [socket], 15)
        #
        # if socket in ready_to_read:
        # clientsocket, addr = socket.accept()
        while True:
            clientsocket, addr = socket.accept()
            all_data = b''
            # while True:
            print(' zit er in a mattie')
            data = clientsocket.recv(self.BUFFER_SIZE)
            print(pickle.loads(data))
            clientsocket.sendall(bytes('1', 'utf-8'))
