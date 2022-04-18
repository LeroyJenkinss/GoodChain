import main
from database import *
from GoodChain.pools import Pools



class Transactions:

    def __init__(self):
        self.Id = None
        self.sendTo = None
        self.transactionFee = None

    def validTransaction(self, id, sendername):

        sqlStatement = 'SELECT username from USERS WHERE username=:sender'
        try:
            cur.execute(sqlStatement, {"sender": sendername})
            self.sendTo = sendername
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
                self.createTransAction(float(transferValue))
                count = 3
            else:
                print(f'this is the number: {transferValue}')
                count += 1
                print(f'The amount is not a decimal number you have {3 - count} try remaining')
        return


    def createTransAction(self,value):
        self.transactionFee = value * 0.05
        pool = Pools().getavailablePool()
        print(pool)



