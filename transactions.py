import main
from database import *
from GoodChain.pools import Pools
from datetime import datetime
from DbHashCheck import *
from tools import sign



class Transactions:

    def __init__(self):
        self.Id = None
        self.amount = None

        self.sendToId = None
        self.transactionFee = None

    def validTransaction(self, id, sendername):
        sqlStatement = 'SELECT id from USERS WHERE username=:sender'
        try:
            cur.execute(sqlStatement, {"sender": sendername})
            self.sendToId = cur.fetchone()[0]
        except Error as e:
            print(e)
            return False
        self.Id = id

        return True

    def newTransaction(self):
        count = 0
        while count != 3:
            transferValue = input('Plz state the amount you would like to transfer, it must be a decimal number: ')
            if isinstance(float(transferValue), float):
                self.amount = transferValue
                self.createTransAction(float(transferValue))
                count = 3
            else:
                count += 1
                print(f'The amount is not a decimal number you have {3 - count} try remaining')
        return

    def createTransAction(self, value):
        self.transactionFee = value * 0.05
        poolId = Pools().getavailablePool()[0]
        try:
            signedTransaction = self.signtransaction(poolId)
            sqlstatement = '''insert into TRANSACTIONS (sender, reciever, txvalue, txfee, poolid, created, transactionsig) VALUES (?,?,?,?,?,?,?)'''
            values_to_insert = (self.Id, self.sendToId, self.amount, self.transactionFee, poolId, datetime.now(), signedTransaction)
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
            HashCheck().writeHashtransaction()
        except Error as e:
            print(e)

    def newUserInsert(self, userName):
        try:
            userId = cur.execute("SELECT ID FROM USERS WHERE username = (?)", [userName]).fetchone()[0]
        except Error as e:
            print(e)

        try:
            sqlstatement = '''select id from POOL where realpool = False'''
            poolId = cur.execute(sqlstatement).fetchone()[0]
        except Error as e:
            print(e)

        try:
            sqlstatement = '''select id from users where username = "fake"'''
            fakeSenderId = cur.execute(sqlstatement).fetchone()[0]
        except Error as e:
            print(e)

        try:
            sqlstatement = '''insert into TRANSACTIONS (sender, reciever, txvalue, txfee, poolid, created) VALUES (?,?,?,?,?,?)'''
            values_to_insert = (fakeSenderId, userId, 50, 0, poolId, datetime.now())
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()

            HashCheck().writeHashtransaction()


        except Error as e:
            print(e)

    def signtransaction(self,poolid):
        try:
            privatesig = cur.execute("SELECT private_key FROM USERS WHERE id = (?)", [self.Id]).fetchone()[0]
            signdata = [self.sendToId, self.amount, self.transactionFee, poolid]
            return sign(signdata,privatesig)



        except Error as e:
            print(e)