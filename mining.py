import hashlib
import time
from datetime import datetime, timedelta

from database import *
from transactions import Transactions
from balance import Balance
from tools import verify, sha256
from block import Block
from pools import Pools


class Mining:

    def __init__(self):
        self.MinerId = None
        self.poolsString = ''

    # alle transaction uit een pool in een list

    def mine(self, minerId):
        MinerId = minerId
        poolId = self.checkAvailablePools()
        if poolId is not None:
            previousBlock = Block().getLatestBlock()
            print(f'this is previousblock {previousBlock}')
            previousBlockHash = None
            if previousBlock is not None:
                if previousBlock[3] is None:
                    print(f'A block is already avialable for verifing')
                    return
                blockDate = datetime.strptime(previousBlock[6], '%Y-%m-%d %H:%M:%S.%f')

                if blockDate > (datetime.now() - timedelta(minutes=3)):
                    print(
                        f'The last block has been mined less than 3 minutes before, please wait till you can mine again.')
                    return
                previousBlockHash = previousBlock[1]
            data = Pools().GetPoolTransactions(poolId)
            prefix = '0' * 2
            start = time.time()

            for i in range(1000000):
                Nonce = i
                digest = str(data) + str(i)
                if previousBlockHash is not None:
                    digest += str(previousBlockHash)
                digest = sha256(digest)
                if digest.startswith(prefix):
                    currentHash = digest
                    end = time.time()
                    timeCount = end - start
                    if timeCount < 20:
                        time.sleep(20 - timeCount)
                    Block().CreateBlock(currentHash, Nonce, minerId, poolId)
                    return

    def checkAvailablePools(self):
        choicepool = True
        try:
            # pools = cur.execute('''SELECT P.id from block as B LEFT JOIN Pool P on P.id = B.poolid WHERE  P.realpool = 1 and B.nonce IS null''').fetchall()
            pools = cur.execute('''SELECT P.Id from Pool as P LEFT JOIN Block B on P.Id = B.PoolId where PoolFull = 1
                                    EXCEPT
                                    SELECT P.Id from Block as B LEFT JOIN Pool P on P.Id = B.PoolId where PoolFull = 1''').fetchall()

            for a in range(0, len(pools)):
                if len(self.poolsString) == 0:
                    self.poolsString += str(pools[a][0])
                else:
                    self.poolsString += f', {str(pools[a][0])}'
            while choicepool:
                if len(self.poolsString) == 0:
                    print('There are insufficient transactions in pools to start mining')
                    return
                mineChoice = input(f'Which of the following pools would you like to mine? {self.poolsString}: ')
                if len(mineChoice) <= 2 and self.poolsString.__contains__(mineChoice):
                    choicepool = False

                    return self.fetchTransactions(mineChoice)
                else:
                    print('The given choice of pool was incorrect')
        except Error as e:
            print(e)

    def fetchTransactions(self, poolId):
        falseTransaction = []
        try:
            transactionList = cur.execute("SELECT * FROM TRANSACTIONS WHERE poolid = (?) and falsetransaction == true || falsetransaction is NULL", [poolId]).fetchall()
            for a in range(0, len(transactionList)):
                balance = self.checkTransactions(transactionList[a][0], transactionList[a][1], transactionList[a][3],
                                                 transactionList[a][9])
                if not balance:
                    Transactions().setFalseTransaction(transactionList[a][0])
                    falseTransaction.append(transactionList[a])
            if len(falseTransaction) < 5:
                return poolId
            else:
                print(f'This pool has more then 5 false transaction, which is too much')
                return

        except Error as e:
            print(e)
        if len(falseTransaction) != 0:
            print(f'these are the false transactions: {falseTransaction}')
            return

    def checkTransactions(self, transactionId, senderId, txValue, transSig):
        valuesTransaction = False
        if Balance().calculateBalanceUntilTransaction(transactionId, senderId):
            valuesTransaction = True
        if not Transactions().verifyTransAction(transactionId, senderId, txValue, transSig):
            valuesTransaction = False
        return valuesTransaction



