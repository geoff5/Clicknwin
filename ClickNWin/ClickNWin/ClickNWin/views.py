"""
Routes and views for the flask application.
"""

from datetime import datetime
from functools import wraps
from flask import render_template, session, request, redirect
from ClickNWin import app, database

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
        print(isFail)
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
