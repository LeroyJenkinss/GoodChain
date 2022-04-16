from database import *
import main
from GoodChain.transactions import Transactions



class Submenu:

    def __init__(self, id):
        selection = None
        self.id = id


    def transferCoins(self):
        # we moeten hier een user id meegeven
        count = 0
        transfered = False
        transaction = Transactions()
        while count != 3 and transfered == False:
            senderName = input('Pls give the name of the person you would like to send coins: ')
            if transaction.newTransaction(self.id, senderName) == False:
                count += 1
            else:
                transfered = True





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
