from database import *
from tools import sha256, generate_keys
from sqlite3 import Error


class Signup:

    def __init__(self):
        getcurConn()
        self.conn, self.cur = getcurConn()
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
            print(f'returning {userNameCorrect and passwordCorrect}')
            self.privateKey, self.publicKey = self.call_generatekeys()
            insertStatement = '''INSERT INTO USERS(USERNAME,PASSWORD,PUBLIC_KEY,PRIVATE_KEY)VALUES(?,?,?,?)'''
            valuesToInsert = (self.userName, self.password, self.publicKey, self.privateKey)
            try:
                self.cur.execute(insertStatement, valuesToInsert)
                self.conn.commit()

            except Error as e:
                print(e)

            return True
        print(f'returning {userNameCorrect and passwordCorrect}')
        return False

    def validate_username(self, username):
        correctUsername = True
        namePresent = self.cur.execute(f'select USERNAME from USERS WHERE USERNAME = \'{username}\'')

        if len(namePresent.fetchall()) > 0:
            print('false')
            correctUsername = False
            return correctUsername
        return correctUsername

    def validate_password(self, password):
        correctPassword = True
        hashedPassword = sha256(password)
        passwordPresent = self.cur.execute(f'select PASSWORD from USERS WHERE PASSWORD = \'{hashedPassword}\'')
        if len(passwordPresent.fetchall()) > 0:
            print('false')
            correctPassword = False
            return correctPassword
        return correctPassword

    def call_generatekeys(self):
        return generate_keys()
