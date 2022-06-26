import socket, pickle
import time


class ClientService:

    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.BUFFER_SIZE = 1024

    def sendTransactions(self, transactionData):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, 1233))
            s.send(pickle.dumps(transactionData))
            data = s.recv(self.BUFFER_SIZE)
            if data == b'1':
                print('Transaction was send')
                s.close()
                return True
            else:
                return False
        except:
            print('Transaction failed and wil be removed')
            return False

    def sendUser(self, userData):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, 1234))
            s.send(pickle.dumps(userData))
            data = s.recv(self.BUFFER_SIZE)
            if data == b'1':
                print('User was send')
                s.close()
                return True
            else:
                return False
        except:
            print('User failed and wil be removed')
            return False

    def sendBlock(self, blockData):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, 1235))
            s.send(pickle.dumps(blockData))
            data = s.recv(self.BUFFER_SIZE)
            if data == b'1':
                print('Block was send')
                s.close()
                return True
            else:
                return False
        except:
            print('Block failed and wil be removed')
            return False

    def sendVerification(self, verifyData):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, 1236))
            s.send(pickle.dumps(verifyData))
            data = s.recv(self.BUFFER_SIZE)
            if data == b'1':
                print('Verification was send')
                s.close()
                return True
            else:
                return False
        except:
            print('verification failed and will be removed')
            return False


    def sendPool(self, poolData):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.TCP_IP, 1237))
            s.send(pickle.dumps(poolData))
            data = s.recv(self.BUFFER_SIZE)
            if data == b'1':
                print('Pool was send')
                s.close()
                return True
            else:
                return False
        except:
            print('Pool failed and wil be removed')
            return False
