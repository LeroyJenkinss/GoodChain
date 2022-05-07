from GoodChain.balance import calculateBalanceUntilTransaction
from database import *
from transactions import Transactions


class Mining:

    def __init__(self):
        self.MinerId = None
        self.poolsString = ''

    pass

    # alle transaction uit een pool in een list

    def mine(self, minerId):
        self.MinerId = minerId
        self.checkAvailablePools()

    def checkAvailablePools(self):
        choicepool = True
        try:
            pools = cur.execute('''SELECT P.id from block as B LEFT JOIN Pool P on P.id = B.poolid WHERE poolfull = 1 and realpool = 1''').fetchall()
            for a in range(0, len(pools)):
                if len(self.poolsString) == 0:
                    self.poolsString += str(pools[a][0])
                else:
                    self.poolsString += f', {str(pools[a][0])}'

            while choicepool:
                if len(self.poolsString) == 0:
                    print('There are no pools avialable to mine')
                    return
                mineChoice = input(f'Which of the following pools would you like to mine? {self.poolsString}: ')
                if len(mineChoice) <= 2 and self.poolsString.__contains__(mineChoice):
                    choicepool = False
                    self.fetchTransactions(mineChoice)
                else:
                    print('The given choice of pool was incorrect')
        except Error as e:
            print(e)

    def fetchTransactions(self, poolId):
        falseTransaction = []
        try:
            transactionList = cur.execute("SELECT * FROM TRANSACTIONS WHERE poolid = (?)", [poolId]).fetchall()
            for a in range(0, len(transactionList)):
                balance = self.checkTransactions(transactionList[a][0], transactionList[a][1], transactionList[a][3],
                                                 transactionList[a][9])
                if not balance:
                    Transactions().setFalseTransaction(transactionList[a][0])
                    falseTransaction.append(transactionList[a])
                # Hier moet gekeken worden naar de threshold voor aantal valse transacties

        except Error as e:
            print(e)

        print(f'these are the false transactions: {falseTransaction}')

    def checkTransactions(self, transactionId, senderId, txValue, transSig):
        balance = calculateBalanceUntilTransaction(transactionId, self.MinerId)
        return balance



# mine functie aanroepen met poolid
# van die pool alle transactions checken
# loop door transactions en elke transactie naar verifyu classmethod
#
#
# falseTransactions = []
