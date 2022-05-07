import main
from database import *
from GoodChain.pools import Pools
from datetime import datetime
from DbHashCheck import *
from tools import sign, verify


class Transactions:

    def __init__(self):
        self.Id = None
        self.amount = None

        self.sendToId = None
        self.transactionFee = None

    def validTransaction(self, id, sendername):
        name = True
        while name:
            sqlStatement = 'SELECT id from USERS WHERE username=:sender'
            try:
                name = cur.execute(sqlStatement, {"sender": sendername}).fetchone()
                if name is not None:
                    self.sendToId = name[0]
                    name = False
                else:
                    return False
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
            values_to_insert = (
                self.Id, self.sendToId, self.amount, self.transactionFee, poolId, datetime.now(), signedTransaction)
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

    def signtransaction(self, poolid):
        try:
            privatesig = cur.execute("SELECT private_key FROM USERS WHERE id = (?)", [self.Id]).fetchone()[0]
            if str(self.amount)[len(str(self.amount))-2:] == '.0':
                self.amount = int(str(self.amount)[0:len(str(self.amount))-2])
            if str(self.transactionFee)[len(str(self.transactionFee))-2:] == '.0':
                self.transactionFee = int(str(self.transactionFee)[0:len(str(self.transactionFee))-2])
            signdata = [self.sendToId, self.amount, self.transactionFee, poolid]
            print(f'this are the values in sign {self.sendToId}---{self.amount}--{self.transactionFee}--{poolid}')
            return sign(signdata, privatesig)

        except Error as e:
            print(e)

    def setFalseTransaction(self, transId):
        sql_statement = f'UPDATE transactions Set falsetransaction = 1 WHERE Id = {transId}'
        try:
            cur.execute(sql_statement)
            conn.commit()
            print(f'Transaction has been flagged as not correct')
        except Error as e:
            print(e)

    def setFalseTransactionToZero(self, userId):
        try:
            falseparlist = cur.execute(f'select id from transactions where sender = (?) and falsetransaction = 1 and txvalue != 0', [userId]).fetchall()
            cur.execute(f'UPDATE transactions set txvalue = 0, txfee = 0 where falsetransaction = 1 and sender = (?)', [userId])
            conn.commit()
            if len(falseparlist) > 0:
                print(f'The following transactions have been set to zero, due to not being valid {falseparlist}')
            return

        except Error as e:
            print(e)

    def verifyTransAction(self,transactionId,senderId,txvalue,signature):

        try:
            recieverId =  cur.execute(f'select reciever from transactions where id = (?)', [transactionId]).fetchone()[0]
            poolid = cur.execute(f'select poolid from transactions where id = (?)', [transactionId]).fetchone()[0]
            transactionFee = cur.execute(f'select txfee from transactions where id = (?)', [transactionId]).fetchone()[0]
            pubkeySender = cur.execute(f'select public_key from USERS where id = (?)', [senderId]).fetchone()[0]
            signedData = [recieverId, txvalue, transactionFee, poolid]
            return verify(signedData, signature, pubkeySender)
        except Error as e:
            print(e)

    def createTransAction2(self, fakeuser, recieverId, txValue, txFee, poolId, signature):
        poolId = Pools().getavailablePool()[0]
        try:
            signedTransaction = self.signtransaction(poolId)
            sqlstatement = '''insert into TRANSACTIONS (sender, reciever, txvalue, txfee, poolid, created, transactionsig) VALUES (?,?,?,?,?,?,?)'''
            values_to_insert = (
                self.Id, self.sendToId, self.amount, self.transactionFee, poolId, datetime.now(), signedTransaction)
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
            HashCheck().writeHashtransaction()
        except Error as e:
            print(e)







