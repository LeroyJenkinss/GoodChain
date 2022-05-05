from database import *


class Block:

    def verifyBlocks(self, userId):
        outputString = ""
        try:
            availableBlockId = cur.execute(
                "SELECT id FROM BLOCK WHERE mineruserid != (?) and (validateduserid1 != (?) or validateduserid2 IS NULL) and (validateduserid2 != (?) or validateduserid2 IS NULL) and (validateduserid3 != (?) or validateduserid3 IS NULL)",
                [userId, userId, userId, userId]).fetchall()
            txsList = self.getTxFeeBlock(availableBlockId)
            for a in availableBlockId:
                if outputString == '':
                    outputString += str(a[0])
                else:
                    outputString += ', ' + str(a[0])

            print(f'The following id numbers are from block that can be verified by you: {outputString}')

        except Error as e:
            print(e)

        return

    def getTxFeeBlock(self, blockIdList):
        txList = []
        for a in blockIdList:
            try:
                txValue = cur.execute("SELECT sum(txfee) FROM TRANSACTIONS WHERE poolid IS (SELECT poolid FROM BLOCK WHERE id == (?))", [a[0]]).fetchall()
                txList.append(txValue)
            except Error as e:
                print(e)
        return txList



