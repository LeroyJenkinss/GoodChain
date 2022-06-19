import socket, pickle
import time

class ClientService:

    def __init__(self):
        self.TCP_IP = '127.0.0.1'
        self.BUFFER_SIZE = 1024

    def sendTransactions(self, transactionData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, 1233))
        s.send(pickle.dumps(transactionData))
        data = s.recv(self.BUFFER_SIZE)
        print(data)
        s.close()

    def sendBlock(self, blockData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, 1235))
        s.send(pickle.dumps(blockData))
        data = s.recv(self.BUFFER_SIZE)
        print(data)
        s.close()

    def sendUser(self, userData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, 1234))
        s.send(pickle.dumps(userData))
        data = s.recv(self.BUFFER_SIZE)
        print(data)
        s.close()

    def sendVerification(self, verifyData):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, 1236))
        s.send(pickle.dumps(verifyData))
        data = s.recv(self.BUFFER_SIZE)
        print(data)
        s.close()