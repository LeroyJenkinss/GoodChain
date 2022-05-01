from database import *
from tools import sha256
import pickle
from cryptography.hazmat.primitives import hashes
import filecmp


class HashCheck:
    transactionColumn = None
    usersColumn = None
    hashedUserColumn = None

    def __init__(self):
        transactionColumn = ''
        usersColumn = ''
        hashedUserColumn = ''
        hashedUserColumn = ''

    def writeHashtransaction(self):
        try:
            transactionColumnQuery = cur.execute(f'select * from TRANSACTIONS')
            self.transactionColumn = transactionColumnQuery.fetchall()
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
            self.usersColumn = usersColumnQuery.fetchall()
        except Error as e:
            print(e)

        hashedUserColumn = sha256(str(self.usersColumn))
        savefile = open('userHash.txt', "wb")
        pickle.dump(hashedUserColumn, savefile)

        savefile.close()
        return

    def CompareHashes(self, file):

        if str(file) == 'transactionHashes.txt':
            try:
                transactionColumnQuery = cur.execute(f'select * from TRANSACTIONS')
                self.transactionColumn = transactionColumnQuery.fetchall()
                hashedTransColumn = sha256(str(self.transactionColumn))

                savefile = open('transactionHashes1.txt', "wb")
                pickle.dump(hashedTransColumn, savefile)
                savefile.close()

                f1 = str(file)
                f2 = 'transactionHashes1.txt'
                result = filecmp.cmp(f1, f2)
                return result
            except Error as e:
                print(e)

        if str(file) == 'userHash.txt':
            try:
                usersColumnQuery = cur.execute(f'select * from USERS')
                self.usersColumn = usersColumnQuery.fetchall()
                hashedUserColumn = sha256(str(self.usersColumn))

                savefile = open('userHash1.txt', "wb")
                pickle.dump(hashedUserColumn, savefile)
                savefile.close()

                f1 = str(file)
                f2 = 'userhash1.txt'
                result = filecmp.cmp(f1, f2)
                return result
            except Error as e:
                print(e)

        else:
            return "something went wrong"
