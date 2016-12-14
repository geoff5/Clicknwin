"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from ClickNWin import app

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
def loginHome():
    return render_template('loginHome.html', title='ClickNWin', year = datetime.now().year)

@app.route('/myCards', methods=['POST', 'GET'])
def myCards():
    return render_template('myCards.html',title='ClickNWin', year = datetime.now().year)  