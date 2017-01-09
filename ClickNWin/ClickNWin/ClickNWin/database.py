import DBcm

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'srtb19',
    'database': 'clicknwin',
}

def checkUsername(username):
    _SQL = """SELECT username FROM users WHERE username = '{username}';""".format(username = username)
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL)
        user = database.fetchall()
    print(len(user))
    if len(user):
        return False
    return True     


def add_user(user):
    duplicate = checkUsername(user['username'])
    if not duplicate:
        return False
    
    _SQL = """INSERT INTO users
            (username, password, firstname, lastname, email, phone, birthdate, balance)
            values
            (%s, %s, %s, %s, %s, %s, %s, 0.00)"""
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (user['username'], user['password'], user['firstname'], user['lastname'], user['email'],
                        user['phone'], user['dob']))
    return True

def login(username, password):
    _SQL = """SELECT username,password FROM users WHERE username = '{username}';""".format(username = username)
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL)
        user = database.fetchall()
   
    if not len(user):
        return False
    elif user[0][1] != password:
        return False

    return True

def getBalance(username):
    _SQL = """SELECT balance FROM users WHERE username = '{username}';""".format(username = username)
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL)
        balance = database.fetchall()

    return balance[0][0]