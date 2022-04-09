from database import *
from tools import sha256


class Signup:
    successfulLogIn = True
    userName = ''
    password = None
    cur = None

    def __init__(self):
        self.cur = Getcur()

    def registerNewUser(self):
        username = input('Pls write your username: ')
        userNameCorrect = self.validate_username(username)

        password = input('Pls write your password: ')
        passwordCorrect = self.validate_password(password)

        if userNameCorrect and passwordCorrect:
            print(f'returning {userNameCorrect and passwordCorrect}')
            # opslaan naam plus password en generatekeys
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



