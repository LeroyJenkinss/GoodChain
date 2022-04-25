from database import *
from tools import sha256


class Login:

    def __init__(self):

        self.id = None
        self.userName = None
        self.password = None

    def tryLogIn(self):
        self.userName = input('Pls insert your username: ')
        correctUsername = self.validateUsername()
        self.password = input('Pls insert your password: ')
        correctPassword = self.validatePassword()

        if correctUsername and correctPassword:
            print(f'this is username: {self.userName}')
            print(f'this is id: {self.id}')
            return True, self.id
        return False

    def validateUsername(self):
        correctUsername = False
        namePresent = cur.execute(f'select USERNAME from USERS WHERE USERNAME = \'{self.userName}\'')
        name = namePresent.fetchone()

        if not name:
            return correctUsername
        correctUsername = True
        idPresent = cur.execute(f'select id from USERS WHERE USERNAME = \'{self.userName}\'')
        rawid = str(idPresent.fetchone())
        self.id = rawid[1:2]
        return correctUsername

    def validatePassword(self):
        correctPassword = False
        hashedPassword = sha256(self.password)
        passwordPresent = cur.execute(f'select PASSWORD from USERS WHERE PASSWORD = \'{hashedPassword}\' and USERNAME = \'{self.userName}\'')
        password = passwordPresent.fetchone()
        if not password:
            return correctPassword
        correctPassword = True
        return correctPassword


    def getUserName(self):
        return self.userName

