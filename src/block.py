from database import *
from datetime import datetime
from pools import Pools
from tools import sha256
from transactions import Transactions
from blockmining import Blockmining


class Block:

    def verifyBlocks(self, userId):
        outputString = ""
        try:
            availableBlockId = cur.execute(
                "select DISTINCT B.id  from Block B left outer join BLOCKVERIFY BV on B.id = BV.blockid where b.mineruserid != (?) and b.verifiedblock == false and b.mineruserid != (?) and (bv.validateUserId != (?) or bv.validateUserId is null);",
                [userId, userId, userId]).fetchall()
            txsList = self.getTxFeeBlock(availableBlockId)
            for a in availableBlockId:
                if outputString == '':
                    outputString += str(a[0])
                else:
                    outputString += ', ' + str(a[0])
            if len(outputString) != 0:
                print(f'The following id numbers are from a block that can be verified by you: {outputString}')
                choice = input(f'Would you like to verify any of these blocks? (Y = yes N = no)')
                if choice == 'Y':
                    choiceloop = True
                    while choiceloop:
                        idchoice = input(f'Which block id would you like to verify? ')
                        if outputString.__contains__(idchoice):
                            choiceloop = False
                            self.verifyBlock(idchoice, userId)
                else:
                    return



        except Error as e:
            print(e)

        return

    def getTxFeeBlock(self, blockIdList):
        txList = []
        for a in blockIdList:
            try:
                txValue = cur.execute(
                    "SELECT sum(txfee) FROM TRANSACTIONS WHERE poolid IS (SELECT poolid FROM BLOCK WHERE id == (?))",
                    [a[0]]).fetchall()
                txList.append(txValue)
            except Error as e:
                print(e)
        return txList

    def getLatestBlock(self):
        sql_statement = '''SELECT * FROM Block where verifiedblock != 0 order by 1 desc limit 1'''
        try:
            cur.execute(sql_statement)
            return cur.fetchone()
        except Error as e:
            print(e)
            return False

    def CreateBlock(self, hash, nonce, minerId, poolId):
        sql_statement = '''INSERT INTO Block (blockHash, nonce ,mineruserid, poolid, created, pending) VALUES(?,?,?,?,?,?)'''
        values_to_insert = (hash, nonce, minerId, poolId, str(datetime.now()), 1)
        try:
            cur.execute(sql_statement, values_to_insert)
            conn.commit()
            print('Block has been added.')
            return
        except Error as e:
            print(e)

    def verifyBlock(self, block, userId):
        block = self.getALlFromBlock(block)
        checkTransactions = Blockmining().fetchTransactions2(block[2])
        previousBlock = self.getLatestVerifiedBlock()
        previousBlockHash = None
        if previousBlock is not None:
            print(f'previousblock {previousBlock}')
            previousBlockHash = previousBlock[1]
        data = Pools().GetPoolTransactions(block[2])

        digest = str(data) + str(block[5])
        print(f'this is the block1 {digest}')
        if previousBlockHash is not None:
            digest += str(previousBlockHash)
        digest = sha256(digest)
        print(f'this is digest {digest } and this is block[1] {block[1]}')
        if digest == block[1] and checkTransactions != False:
            self.createNewBlockVerify(block[0], userId, 1)
            amountBlockVerified = int(self.getAmountBlockVerified(block[0])[0])
            if amountBlockVerified == 3:
                Transactions().createTransAction2(1, userId, int(Transactions().GetPoolTransactionFees(block[2])[0]) + 50, 0, 1,
                                              'miningreward')




        else:
            print('block is not correct')
            self.createNewBlockVerify(block[0], userId, 0)

    def getLatestVerifiedBlock(self):
        try:
            cur.execute("SELECT * FROM BLOCK where verifiedblock = 1 ORDER BY 1 DESC LIMIT 1")
        except Error as e:
            print(e)
            return False
        return cur.fetchone()

    def createNewBlockVerify(self, blockId, userId, blockCorrect):
        sql_statement = '''INSERT INTO BLOCKVERIFY (BlockId, validateUserId ,Created, BlockCorrect) VALUES(?,?,?,?)'''
        values_to_insert = (blockId, userId, str(datetime.now()), blockCorrect)
        try:
            cur.execute(sql_statement, values_to_insert)
            conn.commit()
            print('Block has been verified.')

            if blockCorrect == 1:
                self.checkIfBlockVerified3Times(blockId)
        except Error as e:
            print(e)

    def getALlFromBlock(self, blockId):
        try:
            block = cur.execute("SELECT * FROM BLOCK where id = (?)", [blockId]).fetchone()

            return block
        except Error as e:
            print(e)
            print('wtf')



    def checkIfBlockVerified3Times(self, blockId):
        try:
            timesVerified = cur.execute(
                "select count(validateUserId) from BLOCKVERIFY as BV left join BLOCK B on B.id = BV.blockid where blockid = (?)",
                [blockId]).fetchall()
            if len(timesVerified) >= 2:
                cur.execute('''UPDATE BLOCK set pending=:pending WHERE id=:id , {"pending": 0, "id": blockId}''')
                conn.commit()
        except Error as e:
            print(e)

        return

    def exploreTheChain(self):
        blockString = ''
        idstr = []
        try:
            blockList = cur.execute("select * from BLOCK").fetchall()
        except Error as e:
            print(e)
            return

        if len(blockList) > 0:
            for a in range(0, len(blockList)):
                idstr.append(blockList[a][2])
                blockString += f'\nThe block Id = {str(blockList[a][0])}, '
                blockString += f'\nThe block Hash = {str(blockList[a][1])}, '
                blockString += f'\nThe block poolid = {str(blockList[a][2])}, '
                blockString += f'\nThe block mineruserid = {str(blockList[a][3])}, '
                blockString += f'\nThe block verifiedblock = {str(blockList[a][4])}, '
                blockString += f'\nThe block nonce = {str(blockList[a][5])}, '
                blockString += f'\nThe block was created at = {str(blockList[a][6])}, '
                blockString += f'\nThe block pending state = {str(blockList[a][7])}\n'
        print(f'{blockString}')
        if len(blockList) > 0:
            PoolIdChoice = int(input(f'Which of the above mentioned pool\'s (poolId) would you look into? : '))
        else:
            print(f'There are no available blocks for you to Explore')
            return

        if PoolIdChoice in idstr:
            try:
                requestedPooltransactions = cur.execute("SELECT * FROM TRANSACTIONS WHERE poolid = (?)",
                                                        [PoolIdChoice]).fetchall()
                if len(requestedPooltransactions) == 0:
                    print(f'The pool with id {PoolIdChoice} is empty')
                Pools().showTransactionsOfPool(requestedPooltransactions)
                return
            except Error as e:
                print(e)

    def getAmountBlockVerified(self, blockId):
        sql_statement = 'SELECT count(*) from blockverify where BlockId = :blockId and BlockCorrect = 1'
        try:
            cur.execute(sql_statement, {"blockId": blockId})
            return cur.fetchone()
        except Error as e:
            print(e)
            return False