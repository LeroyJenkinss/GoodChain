from database import *
import main
from GoodChain.transactions import Transactions


class Submenu:

    def __init__(self, id):
        self.id = id

    def transferCoins(self, id):
        print(f'this is the id: {id}')
        count = 0
        validRecipient = False
        transaction = Transactions()
        while count != 3 and validRecipient == False:
            senderName = input('Pls give the name of the person you would like to send coins: ')
            if not transaction.validTransaction(self.id, senderName):
                count += 1
            else:
                validRecipient = True

        transaction.newTransaction()


    def checkTheBalance(self):
        pass

    def exploreTheChain(self):
        pass

    def checkThePool(self):
        pass

    def cancelTransaction(self):
        pass

    def mineBlock(self):
        pass
