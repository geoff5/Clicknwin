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
    decCards = []
    temp = []
    _SQL = """SELECT name, price FROM cardtypes"""
    
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL)
        cards = database.fetchall()
    for i in cards:
        temp = []
        for d in i:
            temp.append(encrypt.decrypt(d))      
        decCards.append(temp)            
        
    return decCards

def getPrizes(name):
    name = encrypt.encrypt(name)
    decPrizes = []
    temp = []
    _SQL = """SELECT * FROM cardtypes WHERE name = %s;"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (name, ))
        prizes = database.fetchall()
    for i in prizes:
        temp = []
        for d in i[1:]:
            temp.append(encrypt.decrypt(d))
        decPrizes.append(temp)

    return decPrizes

def getPrice(name):
    decPrice = [] 
    name = encrypt.encrypt(name)
    _SQL = """SELECT price FROM cardtypes WHERE name = %s;"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (name, ))
        price = database.fetchall()
    decPrice.append(encrypt.decrypt(price[0][0]))
    return decPrice

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
    _SQL = """SELECT type, prize FROM scratchcards WHERE id = %s AND redeemed = 0"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL,(id, ))
        card = database.fetchone()  
    if not card:
        return card
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

def getCardPrizes(name):
    temp = []
    decPrizes = []
    name = encrypt.encrypt(name)

    _SQL = """SELECT prize1, prize2, prize3, prize4 FROM cardtypes WHERE name = %s"""
    
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (name, ))
        prizes = database.fetchall()
    for i in prizes:
        temp = []
        for d in i:
            temp.append(encrypt.decrypt(d))
        decPrizes.append(temp)
    return decPrizes    


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
    
def adminLogin(admin):
    decUser = []
    admin['user'] = encrypt.encrypt(admin['user'])
    
    _SQL = """SELECT adminUsername, adminPassword FROM admin WHERE adminUsername = %s"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (admin['user'], ))
        user = database.fetchone()
        print(user)
    if not len(user):
        return False
    
    for i in range(0,2):
        decUser.append(encrypt.decrypt(user[i]))

    if admin['password'] != decUser[1]:
        return False
    return True

def addAdmin(admin):
    for i in admin:
        admin[i] = encrypt.encrypt(admin[i])
    _SQL = """INSERT INTO admin
             (adminUsername, adminPassword)
             values
             (%s, %s)"""
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (admin['username'], admin['password']))

def checkAdmin(user):
    print(user)
    user = encrypt.encrypt(user)
    _SQL = """SELECT adminUsername FROM admin WHERE adminUsername = %s"""
    
    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (user, ))
        row = database.fetchone()
    print(row)
    if row:
        return True 
    return False
    
def addCardType(newGame):
    for k in newGame:
        newGame[k] = encrypt.encrypt(newGame[k])
    
    _SQL = """INSERT INTO cardtypes 
            (name, price, prize1, prize1chance, prize2, prize2chance, prize3, prize3chance, prize4, prize4chance)
            values
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (newGame['gameName'], newGame['gamePrice'], newGame['prize1'], newGame['prize1Chance'], newGame['prize2'], newGame['prize2Chance'], newGame['prize3'], newGame['prize3Chance'], newGame['prize4'], newGame['prize4Chance']))      

def modifyGame(changeGame):
    for k in changeGame:
        changeGame[k] = encrypt.encrypt(changeGame[k])

    _SQL = """UPDATE cardtypes SET price=%s, prize1=%s, prize1chance=%s, prize2=%s, prize2chance=%s, prize3=%s, prize3chance=%s, prize4=%s, prize4chance=%s WHERE name = %s"""

    with DBcm.UseDatabase(config) as database:
        database.execute(_SQL, (changeGame['gamePrice'], changeGame['prize1'], changeGame['prize1Chance'], changeGame['prize2'], changeGame['prize2Chance'], changeGame['prize3'], changeGame['prize3Chance'], changeGame['prize4'], changeGame['prize4Chance'], changeGame['gameName']))