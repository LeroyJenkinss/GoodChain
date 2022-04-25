import main
from database import *
from GoodChain.pools import Pools
from datetime import datetime


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
            sqlstatement = '''insert into TRANSACTIONS (sender, reciever, txvalue, txfee, poolid, created) VALUES (?,?,?,?,?,?)'''
            values_to_insert = (self.Id, self.sendToId, self.amount, self.transactionFee, poolId, datetime.now())
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
        except Error as e:
            print(e)

