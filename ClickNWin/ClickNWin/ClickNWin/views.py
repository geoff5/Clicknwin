"""Routes and views for the flask application"""

from datetime import datetime
from functools import wraps
from flask import render_template, session, request, redirect, flash
from ClickNWin import app, database, utils


def isLoggedIn(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'isLoggedIn' in session:
            return func(*args, **kwargs)
        return redirect('/home')
    return wrapped_function

def keepToLogin(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'isLoggedIn' in session:
            return redirect('/loginHome')
        return func(*args, **kwargs)
    return wrapped_function


@app.route('/')
@app.route('/home', methods=['GET'])
@keepToLogin
def home():
    return render_template('index.html', title='ClickNWin', year=datetime.now().year)

@app.route('/register')
@keepToLogin
def register():
    return render_template('register.html', title='ClickNWin', year = datetime.now().year)

@app.route('/login')
@keepToLogin
def login():
    return render_template('login.html', title='ClickNWin', year = datetime.now().year)

@app.route('/loginHome', methods=['POST', 'GET'])
@isLoggedIn
def loginHome():
    return render_template('loginHome.html', title='ClickNWin', year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/myCards', methods=['GET'])
@isLoggedIn
def myCards():
    userCards = database.getCards(session['user'])
    for i in userCards:
        i[1] = i[1][0:i[1].find('.')]
        i[1] = datetime.strptime(i[1], "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%y %H:%M")
        
    return render_template('myCards.html',title='ClickNWin', year = datetime.now().year, balance=database.getBalance(session['user']), cards = userCards)  

@app.route('/registered', methods=['POST', 'GET'])
@keepToLogin
def registered():
    user = {'username':'', 'password':'', 'firstname':'', 'lastname':'', 'email':'', 'phone':'', 'dob':''}
    for k,v in request.form.items():
        user[k] = request.form[k]        
    user['balance'] = '0.00'
    database.addUser(user)
    return render_template('registered.html',title='ClickNWin', year = datetime.now().year)

@app.route('/loggedIn', methods=['POST'])
@keepToLogin
def loggedIn():
    username = request.form['username']
    password = request.form['password'] 
    success = database.login(username, password)
    
    if success:
        session['isLoggedIn'] = True
        session['user'] = request.form['username']
        return redirect('/loginHome')
    flash("Your username or password was incorrect.  Please try again","error")
    return redirect('/login')

@app.route('/addPaymentCard', methods=['POST', 'GET'])
@isLoggedIn
def addPaymentCard():
    return render_template('addPaymentCard.html', year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('isLoggedIn')
    session.pop('user')
    return redirect('/home')

@app.route('/cardAdded', methods=['GET', 'POST'])
@isLoggedIn
def cardAdded():
    card = {'cardType':'', 'cardNumber':'', 'expiryMonths':0, 'expiryYears':0, 'cardFirstName':'', 'cardSurname':'', 'user': session['user']}    
    for k,v in request.form.items():
        card[k] = request.form[k]

    database.addPaymentCard(card)
    return redirect('/loginHome')

@app.route('/buyCards', methods=['GET'])
@isLoggedIn
def buyCards():
    cards = database.getCardTypes()  
    cardTypes = []
    for i in cards:
        cardTypes.append(i[0])
    return render_template('buyCard.html', year = datetime.now().year, cards = cardTypes, balance=database.getBalance(session['user']))

@app.route('/cardsBought', methods=['POST', 'GET'])
@isLoggedIn
def cardsBought():
    sCards = {}
    
    if request.form['selectedUser'] == "":
        sCards['user'] = session['user']
    else:
        sCards['user'] = request.form['selectedUser']
    sCards['type'] = request.form['types']
    sCards['quantity'] = request.form['quantity']
    sCards['boughtBy'] = session['user']
    sCards['boughtOn'] = str(datetime.now())
    utils.newCards(sCards)
    price = request.form['price']
    database.reduceBalance(session['user'], price)
    return redirect("/myCards")

@app.route('/redeemCard', methods=['POST', 'GET'])
@isLoggedIn
def redeemCard():
    for i in request.form.items():
        id = i[0]
    card = database.getCard(id)
    if not card:
        return redirect('/myCards')
    return render_template('redeemCard.html', card=id, year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/topUp', methods=['GET'])
@isLoggedIn
def topUp():
    paymentCards = database.getPaymentCards(session['user'])
    formatCards = []
    index = 0
    for i in paymentCards:
        temp = ''
        formatCards.append({'id': i[0]})
        temp = i[1][12:]
        formatCards[index]['endNo'] = temp
        formatCards[index]['cardType'] = i[2]
        index = index + 1
    return render_template('topUp.html',payCards = formatCards, year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/addFunds', methods=['POST'])
@isLoggedIn
def addFunds():
    amount = request.form['amount']
    if request.form['payBy'] == "cardPay":
        cardID = request.form['card']
        cvv = request.form['cvv']  
        data = utils.processCardPayment(session['user'], cardID, amount, cvv)
        if data:
            return render_template('fundsAdded.html',data = data, year = datetime.now().year, balance=database.getBalance(session['user']))
    elif request.form['payBy'] == "paypal":
       data = utils.processPaypalPayment(session['user'], amount)
       if data:
            session['transactionID'] = data[1]
            session['amount'] = amount 
            return redirect(data[0]) 
    flash("Payment Error.  Please check your details and try again", "error")   
    return redirect('/topUp')


@app.route('/redeemBalance', methods=['GET'])
@isLoggedIn
def redeemBalance():
    return render_template('redeemBalance.html', year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/balanceRedeemed', methods=['POST'])
@isLoggedIn
def balanceRedeemed():
    amount = request.form['amount']
    email = request.form['email']
    password = request.form['password']
    success = database.login(session['user'], password)
    if not success:
        flash("Incorrect password.  Try again", "error")
        return redirect('/redeemBalance')
    amount = utils.formatCurrency(amount)
    if float(amount) > float(database.getBalance(session['user'])):
        flash("you do not have enough funds in your balance.", "error")
        return redirect('/redeemBalance')
    payoutSuccess = paypalAPI.balanceRedeem(email,amount)
    if payoutSuccess:
        database.reduceBalance(session['user'], amount)
        flash("Your payout was successful.  The requested funds will be available in your account shortly.")
        return render_template('loginHome.html', year = datetime.now().year, balance=database.getBalance(session['user']))
    else:
        flash("Payout Error.  Please check your details and try again", "error")
        return redirect('/redeemBalance')

@app.route('/paypalStoreReturn')
@isLoggedIn
def paypalStoreReturn():
    data = {}
    data['transactionID'] = session['transactionID']
    session['transactionID'] = ""
    data['user'] = session['user']
    data['amount'] = session['amount']
    session['amount'] = ""
    database.addFunds(data['user'], data['amount'])
    return render_template('paypalStoreReturn.html',data = data, year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html', title='ClickNWin')   