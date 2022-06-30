from database import *
from datetime import datetime
from pools import Pools
from tools import sha256
from transactions import Transactions
from blockmining import Blockmining
from clientService import ClientService


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

            # Here I will broadcast the new block to the server
            latestblock = self.getLatestBlock4broadcast()
            result = ClientService().sendBlock(latestblock)
            if not result:
                self.removeLatestBlock(latestblock[7])

        except Error as e:
            print(e)

    def getLatestBlock4broadcast(self):
        try:
            latestBlockInserted = cur.execute(
                "select blockhash, poolid, mineruserid, verifiedblock,nonce, pending, created, id from  BLOCK where ID = (select max(ID) from BLOCK)").fetchone()
            latestInsertModified = (
            latestBlockInserted[0], latestBlockInserted[1], latestBlockInserted[2], latestBlockInserted[3],
            latestBlockInserted[4], latestBlockInserted[5], latestBlockInserted[6], latestBlockInserted[7])
            return latestInsertModified
        except Error as e:
            print(f'This is an error when getting lastest block: {e}')

    def removeLatestBlock(self, blockId):
        try:
            cur.execute("delete from  BLOCK where ID = (?)", [blockId])
            conn.commit()

        except Error as e:
            print(f'removeLatestBlock didnt work : {e}')

    def CreateNewBlock(self, blockData):
        sql_statement = '''INSERT INTO Block (blockHash, poolid, mineruserid, verifiedblock,nonce, pending, created ) VALUES(?,?,?,?,?,?,?)'''
        values_to_insert = (
        blockData[0], blockData[1], blockData[2], blockData[3], blockData[4], blockData[5], blockData[6])
        try:
            cur.execute(sql_statement, values_to_insert)
            conn.commit()
            print('Block has been added.')
            return True

        except Error as e:
            print(e)
            return False

    def getLatestBlock(self):
        try:
            cur.execute("SELECT * FROM BLOCK ORDER BY 1 DESC LIMIT 1")
        except Error as e:
            print(e)
            return False
        return cur.fetchone()

    def verifyBlock(self, block, userId):
        block = self.getALlFromBlock(block)
        checkTransactions = Blockmining().fetchTransactions2(block[2])
        previousBlock = self.getLatestVerifiedBlock()
        previousBlockHash = None
        if previousBlock is not None:
            previousBlockHash = previousBlock[1]
        data = Pools().GetPoolTransactions(block[2])

        digest = str(data) + str(block[5])
        if previousBlockHash is not None:
            digest += str(previousBlockHash)
        newDigest = sha256(digest)
        if newDigest == block[1] and checkTransactions != False:
            self.createNewBlockVerify(block[0], userId, 1)
            amountBlockVerified = int(self.getAmountBlockVerified(block[0])[0])
            if amountBlockVerified >= 1:
                Transactions().createTransAction2(1, block[3],
                                                  int(Transactions().GetPoolTransactionFees(block[2])) + 50, 0, 1,
                                                  'miningreward')
                self.blockVerified(block)

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

            # Here I will extract the latest insert for the serverbroadcast
            latestBlockverify = self.getLatestBlockVerify(blockId)
            result = ClientService().sendNewBlockVerify(latestBlockverify)
            if not result:
                self.removeLatestBlockVerify(latestBlockverify[4])

            if blockCorrect == 1:
                self.checkIfBlockVerified3Times(blockId)

        except Error as e:
            print(e)

    def removeLatestBlockVerify(self, blockid):
        try:
            cur.execute("delete from  BLOCKVERIFY where ID = (?)", [blockid])
            conn.commit()

        except Error as e:
            print(f'removeLatestTransaction didnt work : {e}')

    def getLatestBlockVerify(self, blockidd):
        try:
            latestInsert = cur.execute("select blockid, validateUserId, blockcorrect, created, id from  Blockverify where ID = (?)", [blockidd]).fetchone()
            latestInsertModified = (latestInsert[0], latestInsert[1], latestInsert[2], latestInsert[3], latestInsert[4])

            return latestInsertModified
        except Error as e:
            print(f'This is an error when getting lastest insert: {e}')

    def getALlFromBlock(self, blockId):
        try:
            block = cur.execute("SELECT * FROM BLOCK where id = (?)", [blockId]).fetchone()

            return block
        except Error as e:
            print(e)

    def checkIfBlockVerified3Times(self, blockId):
        try:
            # timesVerified = cur.execute(
            #     "select count(validateUserId) from BLOCKVERIFY as BV left join BLOCK B on B.id = BV.blockid where blockid = (?)",
            #     [blockId]).fetchall()
            # if len(timesVerified) >= 2:
            cur.execute("UPDATE BLOCK set pending = 0, verifiedblock = 1 WHERE id = (?)", [blockId])
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

    def getAmountBlockVerified(self, blockId):
        sql_statement = 'SELECT count(distinct validateUserId) from blockverify where BlockId = :blockId and BlockCorrect = 1'
        try:
            cur.execute(sql_statement, {"blockId": blockId})
            return cur.fetchone()
        except Error as e:
            print(e)
            return False

    def blockVerified(self, block):
        try:
            blockId = block[0]
            cur.execute("UPDATE BLOCK set verifiedblock = 1, pending = 0 WHERE id = (?) ", [blockId])
            conn.commit()

            # Here I will extract the latest insert for the serverbroadcast
            result = ClientService().sendVerification(blockId)
            if not result:
                self.removeLatestVerify(blockId)
        except Error as e:
            print(e)
        return

    def removeLatestVerify(self, blockId):
        try:
            cur.execute("UPDATE BLOCK set verifiedblock = 0 WHERE id = (?) ", [blockId])
            conn.commit()
        except Error as e:
            print(f'The removeLatestVerify failed: {e}')

    def AddblockVerified(self, verifyData):
        try:
            cur.execute("UPDATE BLOCK set verifiedblock = 1, pending = 1 WHERE id = (?) ", [verifyData])
            conn.commit()
        except Error as e:
            print(e)
        return

    def AddNewblockVerify(self, blockverifydata):
        try:
            sqlstatement = '''INSERT INTO BLOCKVERIFY (BlockId, validateUserId ,blockcorrect, Created) VALUES(?,?,?,?)'''
            values_to_insert = (
                blockverifydata[0], blockverifydata[1], blockverifydata[2], blockverifydata[3])
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
            return True

        except Error as e:
            print(e)
            return False
