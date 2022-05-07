from database import *
import main
from GoodChain.transactions import Transactions
from GoodChain.balance import Balance
from GoodChain.pools import Pools
from mining import Mining


class Submenu:

    def __init__(self, id):
        self.id = id

    def transferCoins(self, id):
        count = 0
        validRecipient = False
        transaction = Transactions()
        while count != 3 and validRecipient == False:
            senderName = input('Pls give the name of the person you would like to send coins: ')
            if not transaction.validTransaction(self.id, senderName):
                count += 1
                if count == 3:
                    return
            else:
                validRecipient = True

        transaction.newTransaction()

    def checkTheBalance(self, id):

        print(f'Your balance is currently: {Balance().returnBalance(id)}')

    def exploreTheChain(self):
        pass

    def checkThePool(self):
        Pools().checkPool()

    def cancelTransaction(self):
        pass

    def mineBlock(self, minerId):
        Mining().mine(minerId)
        # call mining file

