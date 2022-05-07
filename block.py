from database import *
from datetime import datetime
from pools import Pools
from tools import sha256
from transactions import Transactions


class Block:

    def verifyBlocks(self, userId):
        outputString = ""
        try:
            availableBlockId = cur.execute(
                "select B.id  from Block B left outer join BLOCKVERIFY BV on B.id = BV.blockid where b.mineruserid != (?) and b.verifiedblock == false and b.mineruserid != (?) and (bv.validateUserId != (?) or bv.validateUserId is null);",
                [userId, userId, userId]).fetchall()
            txsList = self.getTxFeeBlock(availableBlockId)
            for a in availableBlockId:
                if outputString == '':
                    outputString += str(a[0])
                else:
                    outputString += ', ' + str(a[0])
            if len(outputString) != 0:
                print(f'The following id numbers are from block that can be verified by you: {outputString}')
                choice = input(f'Would you like to verify any of these blocks? (Y = yes N = no)')
                if choice == 'Y':
                    choiceloop = True
                    while choiceloop:
                        idchoice = input(f'Which block id would you like to verify?')
                        if outputString.__contains__(idchoice):
                            choiceloop = False
                            self.verifyBlock(idchoice, userId)



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
        try:
            latestBlock = cur.execute("SELECT * FROM BLOCK where verified != 0 ORDER BY 1 DESC LIMIT 1").fetchone()
            print(f'this is the latest {latestBlock}')
        except Error as e:
            print(e)
            return False
        print('going back')
        return latestBlock

    def CreateBlock(self, hash, nonce, minerId, poolId):
        sql_statement = '''INSERT INTO Block (blockHash, nonce ,mineruserid, poolid, created) VALUES(?,?,?,?,?)'''
        values_to_insert = (hash, nonce, minerId, poolId, str(datetime.now()))
        try:
            cur.execute(sql_statement, values_to_insert)
            conn.commit()
            print('Block has been added.')
        except Error as e:
            print(e)

    def verifyBlock(self, block, userId):
        previousBlock = self.getLatestVerifiedBlock()
        previousBlockHash = None
        if previousBlock is not None:
            print(f'previousblock {previousBlock}')
            previousBlockHash = previousBlock[1]
        data = Pools().GetPoolTransactions(block[2])
        digest = str(data) + str(block[2])
        if previousBlockHash is not None:
            digest += str(previousBlockHash)
        digest = sha256(digest)
        if digest == block[1]:
            self.createNewBlockVerify(block[0], userId, 1)
            Transactions().createTransAction2(1, userId, int(Pools().GetPoolTransactions(block[3])[0]) + 50, 0, 1,
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
        sql_statement = '''INSERT INTO BlockCheck (BlockId, validatedUserId ,Created, BlockCorrect) VALUES(?,?,?,?)'''
        values_to_insert = (blockId, userId, str(datetime.now()), blockCorrect)
        try:
            cur.execute(sql_statement, values_to_insert)
            conn.commit()
            print('Block has been verified.')
        except Error as e:
            print(e)
