"""
Routes and views for the flask application.
"""

from datetime import datetime
from functools import wraps
from flask import render_template, session, request, redirect, flash
from ClickNWin import app, database

def isLoggedIn(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'isloggedIn' in session:
            return func(*args, **kwargs)
        return render_template('index.html', title='ClickNWin', year=datetime.now().year)
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
    return render_template('login.html', title='ClickNWin', year = datetime.now().year)

@app.route('/loginHome', methods=['POST', 'GET'])
@isLoggedIn
def loginHome():
    return render_template('loginHome.html', title='ClickNWin', year = datetime.now().year)

@app.route('/myCards', methods=['POST', 'GET'])
@isLoggedIn
def myCards():
    return render_template('myCards.html',title='ClickNWin', year = datetime.now().year)  

@app.route('/registered', methods=['POST', 'GET'])
def registered():
    user = {'username':'', 'password':'', 'firstname':'', 'lastname':'', 'email':'', 'phone':'', 'dob':''}
    for k,v in request.form.items():
        user[k] = request.form[k]    
    
    success = database.add_user(user)
    if not success:
        return render_template('register.html',title='ClickNWin', year = datetime.now().year)
    return render_template('registered.html',title='ClickNWin', year = datetime.now().year)

@app.route('/loggedIn', methods=['POST', 'GET'])
def loggedIn():
    username = request.form['username']
    password = request.form['password'] 
    success = database.login(username, password)
    
    if success:
        session['isloggedIn'] = True
        return render_template('loggedIn.html',title='ClickNWin', year = datetime.now().year)
    return render_template('login.html', title='ClickNWin', year = datetime.now().year)
    