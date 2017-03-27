import DBcm
import decimal
import base64

from ClickNWin import encrypt

"""Contains functions for inserting, updating and retrieving data from the MySQL database"""

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'srtb19',
    'database': 'clicknwin',
}

def checkUsername(username):
    _SQL = """SELECT username FROM users WHERE username = %s;"""
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (username, ))
        user = database.fetchall()
    if len(user):
        return True
    return False    


def addUser(user):
    duplicate = checkUsername(user['username'])
    if duplicate:
        return False
    
    for k in user:
        if k != 'username':
            user[k] = encrypt.encrypt(user[k])
    
    print(user)
    _SQL = """INSERT INTO users
            (username, password, firstname, lastname, email, phone, birthdate, balance)
            values
            (%s, %s, %s, %s, %s, %s, %s, %s)"""
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (user['username'], user['password'], user['firstname'], user['lastname'], user['email'],
                        user['phone'], user['dob'], user['balance']))
    return True

def login(username, password):
    _SQL = """SELECT username,password FROM users WHERE username = %s;"""
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (username, ))
        user = database.fetchall()

    if not len(user):
        return False
    
    decUser = []
    decUser.append(user[0][0])
    decUser.append(encrypt.decrypt(user[0][1]))
    if decUser[1] != password:
        return False

    return True

def getBalance(username):
    _SQL = """SELECT balance FROM users WHERE username = %s;"""
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (username, ))
        balance = database.fetchall()
    decBalance = encrypt.decrypt(balance[0][0])
    numBal = '{:.2f}'.format(float(decBalance))
    return numBal

def addPaymentCard(card):
    for k in card:
        if k != 'user':
            card[k] = encrypt.encrypt(card[k])

    _SQL = """INSERT INTO paymentcards
            (cardNumber, expiryMonth, expiryYear, cardType, holderFirstName, holderSurname, user)
            values
            (%s, %s, %s, %s, %s, %s, %s)"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (card['cardNumber'],card['expiryMonths'],card['expiryYears'], card['cardType'],card['cardFirstName'],card['cardSurname'], card['user']))

def getCardTypes():
    _SQL = """SELECT name, price FROM cardtypes"""
    
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL)
        cards = database.fetchall()
    return cards

def getPrizes(type):
    _SQL = """SELECT * FROM cardtypes WHERE name = %s;"""
    
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (type, ))
        prizes = database.fetchall()
    return prizes

def getPrice(name):
    _SQL = """SELECT price FROM cardtypes WHERE name = %s;"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (name, ))
        price = database.fetchall()
    return price

def addScratchCard(card):
    for k in card:
        if k != 'user':
            card[k] = encrypt.encrypt(card[k])

    _SQL = """INSERT INTO scratchcards
            (user, prize, type, boughtBy, boughtOn)
            values
            (%s, %s, %s, %s, %s)"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (card['user'], card['prize'], card['type'], card['boughtBy'], card['boughtOn']))

def reduceBalance(user, amount):
    balance = float(getBalance(user))
    if amount[0] == '€':
        newBal = balance - float(amount[1:])
    else:
        newBal = balance - float(amount)

    newBal = encrypt.encrypt(str(newBal))
    
    _SQL = """UPDATE users SET balance = %s WHERE username = %s;"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL,(newBal, user))

def getCards(user):
    cards = []
    temp = []
    
    _SQL = """SELECT id, boughtOn, type, boughtBy FROM scratchcards WHERE user = %s
     AND redeemed = 0"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL,(user,))
        userCards = database.fetchall()
    
    for i in userCards:
        temp.append(i[0])
        for d in i[1:]:
            temp.append(encrypt.decrypt(d))
        cards.append(temp)
        temp = []
    return cards

def getCard(id):
    decCard = []
    _SQL = """SELECT type, prize FROM scratchcards WHERE id = %s"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL,(id, ))
        card = database.fetchone()  
    for i in card:
        decCard.append(encrypt.decrypt(i))
    return decCard

def redeemCard(id):
    _SQL = """UPDATE scratchcards SET redeemed = 1 WHERE id = %s"""
    
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (int(id),))

def addFunds(user,prize):
    balance = float(getBalance(user))
    newBal = balance + float(prize)
    newBal = str(newBal)
    newBal = encrypt.encrypt(newBal)

    _SQL = """UPDATE users SET balance = %s WHERE username = %s"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (newBal, user))

def getCardPrizes(type):
    _SQL = """SELECT prize1, prize2, prize3, prize4 FROM cardtypes WHERE name = %s"""
    
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (type, ))
        cards = database.fetchall()
    return cards

def getPaymentCards(user):
    decCards = []
    temp = []
    _SQL = """SELECT id, cardNumber, cardType FROM paymentcards WHERE user = %s"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL,(user,))
        paymentCards = database.fetchall()

    for i in paymentCards:
        temp.append(i[0])
        for d in i[1:]:
            temp.append(encrypt.decrypt(d))
        decCards.append(temp)
        temp = []
    
    return decCards

def getPaymentCard(id):
    decCard = []
    temp = []
    _SQL = """SELECT id, cardNumber, expiryMonth, expiryYear, holderFirstName, cardType, holderSurname from paymentcards WHERE id = %s""".format(id = id)

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL,(id,))
        paymentCard = database.fetchall()

    for i in paymentCard:
        temp.append(i[0])
        for d in i[1:]:
            temp.append(encrypt.decrypt(d))
        decCard.append(temp)
        temp = []
    return decCard
    


    