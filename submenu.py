from database import *
import main
from GoodChain.transactions import Transactions
from GoodChain.balance import Balance
from GoodChain.pools import Pools
from mining import Mining
from block import Block


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
                print(f'Username does not exist')
                if count == 3:
                    return
            else:
                validRecipient = True

        transaction.newTransaction()

    def checkTheBalance(self, id):

        print(f'Your balance is currently: {Balance().returnBalance(id)}')

    def exploreTheChain(self):
        Block().exploreTheChain()

    def checkThePool(self):
        Pools().checkPool()

    def cancelTransaction(self, userId):
        Transactions().cancelTransaction(userId)

    def mineBlock(self, minerId):
        Mining().mine(minerId)

    def showPublicKey(self, userId):
        try:
            pkey = cur.execute(f'select public_key from USERS where id = (?)', [userId]).fetchone()
            print(f'this is your public key: {pkey[0]}')

        except Error as e:
            print(e)
        return

    def showPrivateKey(self, userId):
        try:
            pkey = cur.execute(f'select private_key from USERS where id = (?)', [userId]).fetchone()
            print(f'this is your private key: {pkey[0]}')
        except Error as e:
            print(e)
        return

