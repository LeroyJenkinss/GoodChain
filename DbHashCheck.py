from database import *
from tools import sha256
import pickle
from cryptography.hazmat.primitives import hashes


class HashCheck:
    transactionColumn = None
    usersColumn = None
    hashedUserColumn = None
    hashedUserColumn = None

    def __init__(self):
        transactionColumn = ''
        usersColumn = ''
        hashedUserColumn = ''
        hashedUserColumn = ''

    def writeHashtransaction(self):
        try:
            transactionColumnQuery = cur.execute(f'select * from TRANSACTIONS')
            self.transactionColumn = transactionColumnQuery.fetchone()[0]
        except Error as e:
            print(e)

        hashedTransColumn = sha256(str(self.transactionColumn))
        savefile = open('transactionHashes.txt', "wb")
        pickle.dump(hashedTransColumn, savefile)
        savefile.close()
        return

    def writeHashUser(self):
        try:
            usersColumnQuery = cur.execute(f'select * from USERS')
            self.usersColumn = usersColumnQuery.fetchone()[0]
        except Error as e:
            print(e)

        hashedUserColumn = sha256(str(self.usersColumn))
        savefile = open('userHash.txt', "wb")
        pickle.dump(hashedUserColumn, savefile)
        savefile.close()
        return

    def CompareHashes(self, file):

        with open(str(file)) as f:
            lines = f.readlines()

        if str(file) == 'transactionHashes.txt':
            try:
                transactionColumnQuery = cur.execute(f'select * from TRANSACTIONS')
                self.transactionColumn = transactionColumnQuery.fetchone()[0]
                hashedTransColumn = sha256(str(self.transactionColumn))
                return lines == hashedTransColumn

            except Error as e:
                print(e)

        if str(file) == 'userHash.txt':
            try:
                usersColumnQuery = cur.execute(f'select * from USERS')
                self.usersColumn = usersColumnQuery.fetchone()[0]
                hashedUserColumn = sha256(str(self.usersColumn))
                return lines == hashedUserColumn

            except Error as e:
                print(e)



        else:
            return "something went wrong"
