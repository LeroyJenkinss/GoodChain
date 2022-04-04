from database import *

class Signup:
    succesfullLogIn = True
    userName = ''
    password = None



    def registerNewUser(self):
        username = input('Plz write your username: ')
        print(f'this is the username: {username}')
        cur = Getcur()
        sql_statement = 'SELECT * from USERS'
        cur.execute(sql_statement)
        print(cur.fetchone())
        return
