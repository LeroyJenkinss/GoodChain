from database import *
from tools import sha256


class Login:

    def __init__(self):
        # getcurConn()
        # self.conn, self.cur = getcurConn()
        self.userName = None
        self.password = None

    def tryLogIn(self):
        self.userName = input('Pls insert your username: ')
        correctUsername = self.validateUsername()
        self.password = input('Pls insert your password: ')
        correctPassword = self.validatePassword()

        if correctUsername and correctPassword:
            return True
        return False

    def validateUsername(self):
        correctUsername = False
        namePresent = cur.execute(f'select USERNAME from USERS WHERE USERNAME = \'{self.userName}\'')

        if len(namePresent.fetchall()) != 0:
            correctUsername = True
            return correctUsername
        return correctUsername

    def validatePassword(self):
        correctPassword = False
        hashedPassword = sha256(self.password)
        passwordPresent = cur.execute(f'select PASSWORD from USERS WHERE PASSWORD = \'{hashedPassword}\'')
        if len(passwordPresent.fetchall()) != 0:
            correctPassword = True
            return correctPassword
        return correctPassword
