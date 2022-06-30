from copyreg import pickle
import socket
from copyreg import pickle
import time
import pickle
import select
from transactions import Transactions
from signup import Signup
from block import Block
from pools import Pools


class ServerService:

    def __init__(self):
        self.socket = socket

    def recTransaction(self):

        port = 1233
        HEADERSIZE = 10
        BUFFER_SIZE = 1024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket

        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)

            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(f'Dit is de data {pickle.loads(data)}')
                    result = Transactions().addTransAction(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)
                    # waar is remove

    def recUser(self):
        port = 1234
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = Signup().insertNewUser(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recBlockchain(self):
        port = 1235
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print(' zit er in a mattie')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = Block().CreateNewBlock(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recBlockVerification(self):
        port = 1236
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print('zit er in a mattie ')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = Block().AddblockVerified(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recPool(self):
        port = 1237
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print('zit er in a mattie ')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = Pools().CreateNewPool(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recNewBlockVerify(self):
        port = 1238
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print('zit er in a mattie ')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = Block().AddNewblockVerify(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recUpdatePool(self):
        port = 1239
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print('zit er in a mattie ')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = Pools().UpdatefullPool(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

    def recDeleteTrans(self):
        port = 1240
        HEADERSIZE = 10
        BUFFER_SIZE = 10024
        server_socket = self.socket.socket(self.socket.AF_INET, self.socket.SOCK_STREAM)
        server_socket.bind(('', port))
        server_socket.setsockopt(self.socket.SOL_SOCKET, self.socket.SO_REUSEADDR, 1)
        server_socket.listen(5)
        socket = server_socket
        while True:
            ready_to_read, ready_to_write, in_error = select.select([socket], [],
                                                                    [socket], 15)
            for s in ready_to_read:
                clientsocket, addr = s.accept()
                print('zit er in a mattie ')
                data = clientsocket.recv(BUFFER_SIZE)
                if data:
                    print(pickle.loads(data))
                    result = Transactions().deleteTransAction(pickle.loads(data))
                    if result:
                        clientsocket.sendall(bytes('1', 'utf-8'))
                    else:
                        clientsocket.sendall(bytes('0', 'utf-8'))
                else:
                    s.close()
                    ready_to_read.remove(s)

