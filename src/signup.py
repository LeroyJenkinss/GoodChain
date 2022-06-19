from database import *
from tools import sha256, generate_keys
from sqlite3 import Error
from DbHashCheck import *
import transactions


class Signup:

    def __init__(self):
        self.userName = ''
        self.password = ''
        self.publicKey = ''
        self.privateKey = ''

    def registerNewUser(self):
        username = input('Pls write your username: ')
        userNameCorrect = self.validate_username(username)
        if userNameCorrect:
            self.userName = username

        password = input('Pls write your password: ')
        passwordCorrect = self.validate_password(password)

        if passwordCorrect:
            self.password = sha256(password)

        if userNameCorrect and passwordCorrect:
            self.privateKey, self.publicKey = self.call_generatekeys()
            insertStatement = '''INSERT INTO USERS(USERNAME,PASSWORD,PUBLIC_KEY,PRIVATE_KEY)VALUES(?,?,?,?)'''
            valuesToInsert = (self.userName, self.password, self.publicKey, self.privateKey)
            try:
                cur.execute(insertStatement, valuesToInsert)
                conn.commit()
                transactions.Transactions.newUserInsert(self,self.userName)
                HashCheck().writeHashUser()

            except Error as e:
                print(e)


            return True

        return False

    def validate_username(self, username):
        correctUsername = True
        namePresent = cur.execute(f'select USERNAME from USERS WHERE USERNAME = \'{username}\'')

        if len(namePresent.fetchall()) > 0:

            correctUsername = False
            return correctUsername
        return correctUsername

    def validate_password(self, password):
        correctPassword = True
        hashedPassword = sha256(password)
        passwordPresent = cur.execute(f'select PASSWORD from USERS WHERE PASSWORD = \'{hashedPassword}\'')
        if len(passwordPresent.fetchall()) > 0:
            correctPassword = False
            return correctPassword
        return correctPassword

    def call_generatekeys(self):
        return generate_keys()

    def newFakeUser(self):
        sqlstatement = '''select * from USERS where username = 'fake' '''
        nullcheck = cur.execute(sqlstatement).fetchone()
        if nullcheck is None:
            sqlstatement = '''insert into USERS (username, password) VALUES (?,?)'''
            values_to_insert = ('fake', 'fake')
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()

    def insertNewUser(self, userData):
        insertStatement = '''INSERT INTO USERS(USERNAME,PASSWORD,PUBLIC_KEY,PRIVATE_KEY)VALUES(?,?,?,?)'''
        valuesToInsert = (userData[0], userData[1], userData[2], userData[3])
        try:
            cur.execute(insertStatement, valuesToInsert)
            conn.commit()

        except Error as e:
            print(e)



