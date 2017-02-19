"""
Routes and views for the flask application.
"""

from datetime import datetime
from functools import wraps
from flask import render_template, session, request, redirect, json, jsonify
from ClickNWin import app, database, cards

def isLoggedIn(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'isLoggedIn' in session:
            return func(*args, **kwargs)
        return redirect('/home')
    return wrapped_function


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('index.html', title='ClickNWin', year=datetime.now().year)

@app.route('/register')
def register():
    return render_template('register.html', title='ClickNWin', year = datetime.now().year)

@app.route('/login')
def login():
    isFail = False
    if 'failLogin' in session:
        isFail = session['failLogin']
    return render_template('login.html', title='ClickNWin', year = datetime.now().year, fail = isFail)

@app.route('/loginHome', methods=['POST', 'GET'])
@isLoggedIn
def loginHome():
    return render_template('loginHome.html', title='ClickNWin', year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/myCards', methods=['POST', 'GET'])
@isLoggedIn
def myCards():
    return render_template('myCards.html',title='ClickNWin', year = datetime.now().year, balance=database.getBalance(session['user']))  

@app.route('/registered', methods=['POST', 'GET'])
def registered():
    user = {'username':'', 'password':'', 'firstname':'', 'lastname':'', 'email':'', 'phone':'', 'dob':''}
    for k,v in request.form.items():
        user[k] = request.form[k]    
    
    success = database.addUser(user)
    if not success:
        return render_template('register.html',title='ClickNWin', year = datetime.now().year)
    return render_template('registered.html',title='ClickNWin', year = datetime.now().year)

@app.route('/loggedIn', methods=['POST', 'GET'])
def loggedIn():
    username = request.form['username']
    password = request.form['password'] 
    success = database.login(username, password)
    
    if success:
        session['isLoggedIn'] = True
        session['user'] = request.form['username']
        session['failLogin'] = "false"
        return redirect('/loginHome')
    session['failLogin'] =  "true"
    return render_template('login.html',  year = datetime.now().year, fail=session['failLogin'])

@app.route('/addPaymentCard', methods=['POST', 'GET'])
@isLoggedIn
def addPaymentCard():
    return render_template('addPaymentCard.html', year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('isLoggedIn')
    session.pop('user')
    session.pop('failLogin')
    return redirect('/home')

@app.route('/cardAdded', methods=['GET', 'POST'])
@isLoggedIn
def cardAdded():
    card = {'cardType':'', 'cardNumber':'', 'expiryMonths':0, 'expiryYears':0, 'cardName':'', 'user': session['user']}    
    for k,v in request.form.items():
        card[k] = request.form[k]
        print(card[k])

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

@isLoggedIn
@app.route('/cardsBought', methods=['POST', 'GET'])
def cardsBought():
    if 'selectedUser' not in request.form.items():
        user = session['user']
    else:
        user = request.form['selectedUser']
    print(user)
    type = request.form['types']
    print(type)
    #quantity = request.form['quantity']
    #print("username = " + user + " type = " + type + " quantity = " + quantity)
    #cards.newCards
    return render_template("loginHome.html", year = datetime.now().year, balance=database.getBalance(session['user']))

@app.route('/checkUser', methods=['POST', 'GET'])
@isLoggedIn
def checkUser():
    user = request.form['user']
    exists = database.checkUsername(user)
    return jsonify(exists=exists)

@app.route('/getCardPrice', methods=['POST'])
@isLoggedIn
def getCardPrice():
    type = request.form['type']
    price = database.getPrice(type)
    return jsonify(price=price)
    
