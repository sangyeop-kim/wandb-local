import re

import bcrypt

if __name__ == '__main__':
    password = '1'
    passwordSalt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), passwordSalt).decode('utf-8')
    print(password)
    print(str(password))
    print('%s:%s' % ('asd', str(password)))
